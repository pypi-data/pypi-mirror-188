"""It provides BaseResource class.

Copyright 2022 nMachine.io
"""

import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from kubernetes.client import ApiException  # type: ignore

from k8kat.broker import Broker
from k8kat.res.selectors import convert_selectors
from k8kat.utils import classproperty

KR = TypeVar("KR", bound="BaseResource")


class BaseResource:
    """Base class for other resources like Pod, ConfigMap etc."""

    def __init__(self, raw: Any, broker: Broker):
        """Raw object and Broker are required to construct base resource.

        Args:
            raw: object returned from Kubernetes library
            broker: source Broker which return this object, will be used
                    to patch, reload or delete the object

        """

        self.raw = raw  # raw object from Kubernetes library.
        self.broker = broker  # Broker which returns this resource

    def as_dict(self) -> Dict:
        """Returns objects attributes as dict"""
        return self.raw.to_dict()

    @property
    def uid(self) -> str:
        """Returns UID from metadata"""
        return self.raw.metadata.uid

    @classproperty
    def res_name_plural(self) -> str:
        """Returns plural name of the resource"""
        kind_lower = str(self.kind).lower()
        return f"{kind_lower}s"

    @classproperty
    def kind_aliases(self) -> List[str]:
        """Returns aliases for this type of resource"""
        return [self.kind, str(self.kind).lower(), self.res_name_plural]

    @property
    def name(self) -> str:
        """Returns name of the object"""
        return self.raw.metadata.name

    @property
    def namespace(self) -> str:
        """Returns name of the namespace"""
        return self.raw.metadata.namespace

    @property
    def ns(self) -> str:
        """Returns name of the namespace"""
        return self.namespace

    def sig(self, with_ns: Optional[bool] = False) -> str:
        """Returns name in format namespace:kind:name

        Returns:
            string as extended name"""
        ns_less = f"{self.kind}:{self.name}"
        return f"{self.ns}:{ns_less}" if with_ns else ns_less

    @property
    def metrics_component(self) -> Optional[Dict]:
        """Returns object's run time metrics."""
        return None

    @property
    def labels(self) -> Dict[str, str]:
        """Returns dict of labels"""
        return self.raw.metadata.labels or {}

    @property
    def annotations(self) -> Dict[str, str]:
        """Returns dict of annotations"""
        return self.raw.metadata.annotations or {}

    def created_at(self) -> Optional[datetime]:
        """Returns timestamp when object has been created

        Returns:
            object creation datetime"""
        value: datetime = self.raw.metadata.creation_timestamp
        return value.replace(tzinfo=None) if value else None

    def seconds_existed(self) -> int:
        """Returns how long the object lives (in second)

        Returns:
            live time in secods"""
        created_ts = self.created_at()
        if created_ts:
            return (datetime.utcnow() - created_ts).seconds
        return 1_000_000_000

    def wait_until(
        self, predicate: Callable, max_time_sec: Optional[float] = None
    ) -> bool:
        """Waits until pedicated() return true, reloads the object
        periodically.

        Args:
            predicate : function to check
            max_time_sec : timeout

        Returns:
            True if condition met, False otherwise
        """
        start_time = time.time()
        condition_met = False
        for _ in range(0, 1_000):
            if predicate():
                condition_met = True
                break
            if max_time_sec and time.time() - start_time > max_time_sec:
                return False
            time.sleep(1)
            self.reload()
        return condition_met

    def reload(self) -> Any:
        """Reloads object state by querying Kubernetes API.

        Returns:
            self refreshed or None if object disappeared"""
        self.raw = self.find_raw(self.name, self.ns, self.broker)
        return self if self.raw else None

    def patch(self, modifier: Optional[Callable] = None) -> Optional[KR]:
        """Patches object using modifier or self.raw object

        Args:
            modifier : function which modifies the object

        Returns:
            reloaded object

        """

        if modifier is not None:
            self._enter_patch_loop(modifier)
        else:
            self.ns_agnostic_call(
                self.k8s_patch_method, body=self.raw, broker=self.broker
            )
        return self.reload()

    def _enter_patch_loop(self, modification_delegate: Callable) -> None:
        failed_attempts = 0
        while True:
            try:
                modification_delegate(self.raw)
                self.ns_agnostic_call(
                    self.k8s_patch_method, body=self.raw, broker=self.broker
                )
                return
            except ApiException:
                if failed_attempts >= 5:
                    raise
                failed_attempts += 1
                time.sleep(1)
                self.reload()

    def ns_agnostic_call(self, impl: Callable, **kwargs: Any) -> Any:
        """Calls method impl with name and with the namespace
        if the resource is namespaced.

        Args:
            impl: method to call

        Returns:
            values from impl
        """
        if self.is_namespaced():
            return impl(name=self.name, namespace=self.ns, **kwargs)
        return impl(name=self.name, **kwargs)

    def delete(self, wait_until_gone: Optional[bool] = False) -> None:
        """Deletes the object

        Args:
            wait_until_gone: True if you want to wait for
                             the object to disappear.

        """
        self.ns_agnostic_call(self.k8s_delete_method, broker=self.broker)

        if wait_until_gone:
            while self.reload():
                time.sleep(0.5)

    @classproperty
    def kind(self) -> str:
        """Name of the resource"""
        raise NotImplementedError

    @classmethod
    def k8s_list_method(cls, broker: Broker, **kwargs: Any) -> Any:
        """Returns list of raw objects using K8s API"""
        raise NotImplementedError

    @classmethod
    def k8s_read_method(cls, broker: Broker, **kwargs: Any) -> Any:
        """Returns only one raw object using K8s API"""
        raise NotImplementedError

    @classmethod
    def k8s_patch_method(cls, broker: Broker, **kwargs: Any) -> Any:
        """Patches the raw object using K8s API"""
        raise NotImplementedError

    @classmethod
    def k8s_delete_method(cls, broker: Broker, **kwargs: Any) -> None:
        """Deletes object using K8s API"""
        raise NotImplementedError

    @classmethod
    def is_namespaced(cls) -> bool:
        """True if resource is namespaced"""
        return True

    @classmethod
    def list(
        cls: Type[KR],
        ns: Optional[str] = None,
        broker: Optional[Broker] = None,
        **kwargs: Any,
    ) -> List[KR]:
        """Returns list of objects.

        Args:
            ns: namespace
            broker: Broker to query K8s API

            field_selector: str, K8s string with expression to include/exclude
                            resources
            fields: List[Tuple(str, str)], list of pair (field name, field value) which
                    have to match in returned resources
            not_fields: List[Tuple(str, str)], list of pair (field name, field value) which
                    have to be excluded from resources

            label_selector: str, K8s string with expression to include/exclude
                            resources
            labels: List[Tuple(str, str)], list of pair (label name, label value) which
                    have to match in returned resources
            not_labels: List[Tuple(str, str)], list of pair (label name, label value) which
                    have to be excluded from resources

            limit: int, limit returned resources

        Returns:
            list of objects
        """
        if broker is None:
            broker = Broker.get_default_instance()
        convert_selectors(kwargs)
        k8s_items = cls.k8s_list_method(broker, ns=ns, **kwargs)
        return [cls(raw, broker=broker) for raw in k8s_items.items]

    @classmethod
    def find_raw(
        cls, name: str, ns: Optional[str] = None, broker: Optional[Broker] = None
    ) -> Any:
        """Finds raw object by name.

        Args:
            name: name of the object
            ns: namespace
            broker: Broker to query K8s API

        Returns:
            return raw k8s object or None if not found
        """
        try:
            if broker is None:
                broker = Broker.get_default_instance()
            fun: Callable = cls.k8s_read_method
            is_ns: bool = cls.is_namespaced()
            return (
                fun(name=name, ns=ns, broker=broker)
                if is_ns
                else fun(name=name, broker=broker)
            )
        except ApiException as ex:
            if ex.status != 404:
                raise
        return None

    @classmethod
    def find(
        cls: Type[KR],
        name: str,
        ns: Optional[str] = None,
        broker: Optional[Broker] = None,
    ) -> Optional[KR]:
        """Finds object by name.

        Args:
            name: name of the object
            ns: namespace
            broker: Broker to query K8s API

        Returns:
            return object or None if not found
        """
        if broker is None:
            broker = Broker.get_default_instance()
        raw_res = cls.find_raw(name, ns, broker)
        return cls(raw_res, broker=broker) if raw_res else None

    @classmethod
    def delete_if_exists(
        cls,
        name: str,
        ns: str,
        wait_until_gone: Optional[bool] = False,
        broker: Optional[Broker] = None,
    ) -> None:
        """Deletes object by name.

        Args:
            name: name of the object
            ns: namespace
            wait_until_gone: True if you want to wait for
                             the object to disappear.
            broker: Broker to query K8s API

        Returns:
            return object or None if not found
        """
        instance = cls.find(name, ns, broker)
        if instance:
            instance.delete(wait_until_gone)

    @classmethod
    def wait_until_exists(
        cls,
        name: str,
        ns: Optional[str] = None,
    ) -> Any:
        """Waits for the object and returns it.

        Args:
            name: name of the object
            ns: namespace
            broker: Broker to query K8s API

        Returns:
            return object or None if not found
        """
        res = None
        for _ in range(0, 20):
            res = cls.find(name, ns)
            if res:
                break
            time.sleep(1)
        return res
