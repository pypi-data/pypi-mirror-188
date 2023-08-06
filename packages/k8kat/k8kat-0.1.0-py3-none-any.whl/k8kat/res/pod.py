"""
Copyright 2022 nMachine.io
"""


from __future__ import annotations

from enum import Enum
from http.client import HTTPResponse
from typing import Any, Dict, List, Optional, Set

from kubernetes.client import ApiException, models  # type: ignore
from kubernetes.stream import stream  # type: ignore

from k8kat.broker import Broker
from k8kat.types import IntelDict, PodMetricsDict
from k8kat.utils import classproperty

from . import BaseResource, pod_utils


class PodStatus(Enum):
    """Enum with pod statuses."""

    PENDING = 0
    POSITIVE = 1
    NEGATIVE = 2


class Pod(BaseResource):
    """Pod resource.

    This class inherits from BaseResource and provide:

    1. static methods to list/find/patch/reload pods using K8s API
    2. object properties, methods to get logs, execute commands etc.
    """

    def __init__(self, raw: models.V1Pod, broker: Broker):
        BaseResource.__init__(self, raw, broker)

    @classmethod
    def k8s_list_method(cls, broker: Broker, **kwargs: Any) -> models.V1PodList:
        ns = None
        if "ns" in kwargs:
            ns = kwargs.get("ns")
            del kwargs["ns"]
        if ns:
            return broker.core_v1_api.list_namespaced_pod(namespace=ns, **kwargs)
        return broker.core_v1_api.list_pod_for_all_namespaces(**kwargs)

    @classmethod
    def k8s_read_method(cls, broker: Broker, **kwargs: Any) -> models.V1Pod:
        ns = kwargs.get("ns")
        del kwargs["ns"]
        return broker.core_v1_api.read_namespaced_pod(namespace=ns, **kwargs)

    @classmethod
    def k8s_patch_method(cls, broker: Broker, **kwargs: Any) -> models.V1Pod:
        return broker.core_v1_api.patch_namespaced_pod(**kwargs)

    @classmethod
    def k8s_delete_method(cls, broker: Broker, **kwargs: Any) -> models.V1Status:
        return broker.core_v1_api.delete_namespaces_pod(**kwargs)

    @classproperty
    def kind(self) -> str:
        return "Pod"

    @property
    def labels(self) -> Dict[str, str]:
        base = super().labels
        bad_key = "pod-template-hash"
        return {k: base[k] for k in base.keys() if k != bad_key}

    @property
    def phase(self) -> str:
        """Phase of the pod"""
        return self.raw.status.phase

    @property
    def ip(self) -> Optional[str]:
        """IP of the pod"""
        try:
            return self.raw.status.pod_ip
        except Exception:  # pylint: disable=broad-except
            return None

    @property
    def has_parent(self) -> bool:
        """True if there is a parent object"""
        refs = self.raw.metadata.owner_references
        return refs is not None and len(refs) > 0

    def body(self) -> models.V1Pod:
        """Return raw K8s object

        Returns:
            raw pod (V1Pod)"""
        return self.raw

    def containers(self) -> List[models.V1Container]:
        """Return list of containers

        Returns:
            list of containers"""
        return self.raw.spec.containers

    def container(self, index: Optional[int] = 0) -> models.V1Container:
        """Return container details

        Args:
            index: container to return

        Returns:
            container details"""
        return self.raw.spec.containers[index]

    def image(self, index: Optional[int] = 0) -> str:
        """Return container docker image

        Args:
            index: container to return

        Returns:
            container details"""
        return self.container(index).image

    def rs(self) -> None:  # pylint: disable=invalid-name
        """NotImplementedError"""
        raise NotImplementedError

    def dep(self) -> None:
        """NotImplementedError"""
        raise NotImplementedError

    def ternary_status(self) -> PodStatus:
        """Returns pod status.

        Returns:
            PodStatus"""
        if self._is_old_enough_to_call():
            if self.is_working():
                return PodStatus.POSITIVE
            if self.is_broken():
                return PodStatus.NEGATIVE
        return PodStatus.PENDING

    def _is_old_enough_to_call(self) -> bool:
        # TODO: find better way to check if pod structers are already inited
        return self.seconds_existed() > 2

    def is_running_normally(self) -> bool:
        """Returns true if all containers are in running state"""
        if self.is_running():
            main_states = self.main_container_states()
            runners = self.filter_container_states(main_states, "running")
            return len(main_states) == len(runners)
        return False

    def is_pending_normally(self) -> bool:
        """Returns true if pod is pending"""
        return (
            self.is_pending()
            and not self.is_terminating()
            and not self.is_pending_morbidly()
        )

    def is_running_morbidly(self) -> bool:
        """Returns true if pod is running but some of its container not."""
        return (
            self.is_running()
            and not self.is_terminating()
            and not self.is_running_normally()
        )

    def is_working(self) -> bool:
        """Returns true if pod is working"""
        return self.is_running_normally() or self.has_succeeded()

    def is_broken(self) -> bool:
        """Returns True if pod is not running or failed"""
        return (
            self.is_pending_morbidly()
            or self.is_running_morbidly()
            or self.has_failed()
        )

    def is_terminating(self) -> bool:
        """Returns True if pod is in terminating state"""
        states = self.main_container_states()
        terminators = self.filter_container_states(states, "terminated")
        return len(terminators) > 0

    def has_settled(self) -> bool:
        """Returns True if pod is already settled"""
        return not self.is_pending_normally()

    def did_scheduling_fail(self) -> bool:
        """Returns True if sheduling fail"""
        lifecycle_conditions = self.raw.status.conditions
        return self.cond_has_scheduling_failed(lifecycle_conditions)

    def is_pending_morbidly(self) -> bool:
        """Whether this pod is pending because one or more container is failing to start."""
        if self.is_pending():

            if self.did_scheduling_fail():
                return True

            init_states = self.init_container_states()
            waiting_init = self.filter_container_states(init_states, "waiting")
            if len(self.morbid_pending_reasons(waiting_init)) > 0:
                return True

            main_states = self.main_container_states()
            waiting_main = self.filter_container_states(main_states, "waiting")
            if len(self.morbid_pending_reasons(waiting_main)):
                return True

            return False
        return False

    def is_running(self) -> bool:
        """Whether this pod is in the Running state"""
        return self.raw.status.phase == "Running"

    def is_pending(self) -> bool:
        """Whether this pod is in the Pending state"""
        return self.raw.status.phase == "Pending"

    def has_failed(self) -> bool:
        """Whether this pod is in the Failed state"""
        return self.raw.status.phase == "Failed"

    def has_succeeded(self) -> bool:
        """Whether this pod is in the Succeeded state"""
        return self.raw.status.phase == "Succeeded"

    def has_run(self) -> bool:
        """Whether this pod is in the Failed or Succeeded state"""
        return self.has_failed() or self.has_succeeded()

    def cpu_request(self) -> float:
        """Returns pod's total memory limits in bytes."""
        return self.read_resources_req_or_lim("requests", "cpu")

    def cpu_limit(self) -> float:
        """Returns pod's total memory limits in bytes."""
        return self.read_resources_req_or_lim("limits", "cpu")

    def mem_limit(self) -> float:
        """Returns pod's total memory limits in bytes."""
        return self.read_resources_req_or_lim("limits", "memory")

    def mem_request(self) -> float:
        """Returns pod's total memory requests in bytes."""
        return self.read_resources_req_or_lim("requests", "memory")

    def eph_storage_limit(self) -> float:
        """Returns pod's total ephemeral storage limits in bytes."""
        return self.read_resources_req_or_lim("limits", "ephemeral-storage")

    def eph_storage_request(self) -> float:
        """Returns pod's total ephemeral storage requests in bytes."""
        return self.read_resources_req_or_lim("requests", "ephemeral-storage")

    def read_resources_req_or_lim(self, metric: str, resource: str) -> float:
        """Fetches pod's total resource capacity (either limits or requests)
        for either CPU (cores) or memory (bytes)."""

        def container_level_value(container: models.V1Container) -> float:
            return pod_utils.container_req_or_lim(container, metric, resource) or 0

        containers = self.raw.spec.containers or []
        return sum(list(map(container_level_value, containers)))

    @pod_utils.when_running_normally
    # TODO: cache with TTL will be better here
    # @lru_cache(maxsize=128)
    def load_per_pod_metrics(self) -> Optional[List[PodMetricsDict]]:
        """Loads the appropriate metrics dict from k8s metrics API."""
        try:
            self_metrics = self.broker.custom_api.get_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=self.namespace,
                plural="pods",
                name=self.name,
            )
            return [self_metrics] if self_metrics else None
        except ApiException:
            return []

    def running_morbidly_intel(self) -> List[IntelDict]:
        """TODO"""
        return []

    def condition_status_intel(self) -> List[IntelDict]:
        """Return list of invalid conditions"""
        intel = []
        for cond in self.body().status.conditions or []:
            if cond.status == "False":
                intel.append(
                    IntelDict(
                        type="StatusCondition", status=cond.reason, message=cond.message
                    )
                )
        return intel

    def intel(self) -> List[IntelDict]:
        """Return list of IntelDict with errors related to the pod"""
        if self.is_broken():
            return [
                *self.bad_events_intel(),
                *self.running_morbidly_intel(),
                *self.bad_events_intel(),
            ]
        return []

    def main_container_status_summaries(self) -> List[Dict]:
        """Return list of containers with theirs names and statuses"""
        summaries = []

        def extract(cont_status: models.V1ContainerStatus) -> Optional[str]:
            try_states = ["running", "waiting", "terminated"]
            tup = next(
                filter(
                    lambda try_state: getattr(cont_status.state, try_state[1]),
                    enumerate(try_states),
                ),
                None,
            )
            return try_states[tup[0]] if tup else None

        for state in self.body().status.container_statuses:
            summaries.append({"name": state.name, "status": extract(state)})

        return summaries

    def container_status_intel(self) -> List[IntelDict]:
        """Return list of containers in status waiting"""
        bad_states: List[models.V1ContainerState] = self.filter_container_states(
            [*self.init_container_states(), *self.main_container_states()], "waiting"
        )

        intel = []
        for state in bad_states:
            intel.append(
                IntelDict(
                    type="ContainerStatus",
                    message=state.waiting.message,
                    status=state.waiting.reason,
                )
            )

        return intel

    def bad_events_intel(self) -> List[IntelDict]:
        """List of bad events connected with this pod."""
        # bad_events = list(filter(KatEvent.is_failure, self.events()))
        # return list(map(KatEvent.intel_bundle, bad_events))
        return []

    def main_container_states(self) -> List[models.V1ContainerState]:
        """Return list of containers' state"""
        statuses = self.body().status.container_statuses or []
        return [status.state for status in statuses]

    def init_container_states(self) -> List[models.V1ContainerState]:
        """Return list of init containers' state"""
        statuses = self.body().status.init_container_statuses or []
        return [{"state": status.state, "name": status.name} for status in statuses]

    @staticmethod
    def cond_has_scheduling_failed(conditions: List[models.V1PodCondition]) -> bool:
        """Checks conditions if there are invalid sheduling state"""

        def finder(name: str) -> Optional[models.V1PodCondition]:
            return next(filter(lambda c: c.type == name, conditions or []), None)  # type: ignore

        relevant_cond = finder("PodScheduled")
        return bool(relevant_cond and relevant_cond.status == "False")

    @staticmethod
    def morbid_pending_reasons(states: List[models.V1ContainerState]) -> Set[str]:
        """Checks containers states and returns list of reason other
        than ContainerCreating PullingImage, PodInitializing."""
        stated_reasons = {state.waiting.reason for state in states}
        good_reasons = {"ContainerCreating", "PullingImage", "PodInitializing"}
        return stated_reasons - good_reasons

    @staticmethod
    def filter_container_states(
        states: List, _type: str
    ) -> List[models.V1ContainerState]:
        """Filter out an attribute from containers states"""
        return [state for state in states if getattr(state, _type)]

    def raw_logs(self, seconds: Optional[int] = 60) -> Optional[str]:
        """Returns logs from pod as raw output from K8s.

        Args:
            seconds: a relative time in seconds before the current
            time from which to show logs.

        Returns:
            list of log lines
        """
        try:
            return self.broker.core_v1_api.read_namespaced_pod_log(
                namespace=self.namespace, name=self.name, since_seconds=seconds
            )
        except ApiException:
            return None

    def clean_logs(self, seconds: Optional[int] = 60) -> str:
        """Returns logs from pod as string.

        Args:
            seconds: a relative time in seconds before the current
            time from which to show logs.


        Returns:
            list of log lines
        """
        _raw_logs = self.raw_logs(seconds)
        return (_raw_logs or "").strip()

    def log_lines(self, seconds: Optional[int] = 60) -> List[str]:
        """Returns logs from pod as list of logs.

        Args:
            seconds: a relative time in seconds before the current
            time from which to show logs.

        Returns:
            list of log lines

        """
        raw_log_str = self.raw_logs(seconds)
        if raw_log_str:
            return raw_log_str.strip("\n").split("\n")
        return []

    @classmethod
    def consume_runner(
        cls, name: str, ns: str, wait_until_gone: Optional[bool] = False
    ) -> Optional[str]:
        """Returns logs from runner

        Args:
            name: name of pod
            ns: namespace
            wait_until_gone: wait for deleting pod

        Returns:
            logs from pod

        """
        pod = cls.wait_until_exists(name, ns)
        if pod:
            pod.wait_until(pod.has_run)
            logs = None
            if pod.has_succeeded():
                logs = pod.raw_logs()
            pod.delete(wait_until_gone)
            return logs
        return None

    @pod_utils.when_running_normally
    def shell_exec(self, command: str) -> Optional[str]:
        """Executes shell command in pod.

        Args:
            command: command to execute

        Returns:
            output from the command
        """
        fmt_command = pod_utils.coerce_cmd_format(command)
        result = stream(
            self.broker.core_v1_api.connect_get_namespaced_pod_exec,
            self.name,
            self.namespace,
            command=fmt_command,
            stderr=True,
            stdin=False,
            stdout=True,
            tty=False,
        )
        return result.strip() if result else None

    def replace_image(
        self, new_image_name: str, index: Optional[int] = 0
    ) -> models.V1Pod:
        """Replaces container's image.

        Args:
            new_image_name: new image
            index: points container to patch

        Returns:
            Patched object
        """
        self.body().spec.containers[index].image = new_image_name
        return self.patch()

    def wait_until_running(self) -> bool:
        """Waits until pod is in running state.

        Returns:
            True if pod is in running state.
        """
        return self.wait_until(self.is_running)

    def invoke_curl(self, **kwargs: Any) -> HTTPResponse:
        """Executes 'curl' command inside Pod.

        TODO: repace kwargs with named args

        Args:
            headers: optional, list of headers
            body: optional, body for post command
            verb: default GET, http method
            url: url
            path: default /

        Return
            HTTPResponse from the command"""
        fmt_command = pod_utils.build_curl_cmd(**kwargs, with_command=True)
        result = self.shell_exec(fmt_command)
        if result is not None:
            result = pod_utils.parse_response(result)
        return result
