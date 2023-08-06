"""
Copyright 2022 nMachine.io
"""


from __future__ import annotations

from typing import Any, Dict, List

from kubernetes.client import models  # type: ignore

from k8kat.broker import Broker
from k8kat.utils import classproperty

from . import BaseResource


class Ingress(BaseResource):
    """Ingress resource.

    This class inherits from BaseResource and provide:

    1. static methods to list/find/delete ingresses using K8s API
    2. object properties, methods to get ingress' rules
    """

    def __init__(self, raw: models.V1ConfigMap, broker: Broker):
        BaseResource.__init__(self, raw, broker)

    def body(self) -> models.V1Ingress:
        """Returns raw object V1Ingress"""
        return self.raw

    def basic_rules(self) -> Dict[str, List[Dict]]:
        """Returns dict with mapping hosts to their rules."""
        result = {}
        rules: List[models.V1IngressRule] = self.body().spec.rules
        for rule in rules:
            if rule.host:
                bundles = []
                ingress_paths: List[models.V1HTTPIngressPath] = rule.http.paths
                for ingress_path in ingress_paths:
                    bundles.append(
                        dict(
                            service=ingress_path.backend.service.name,
                            port=ingress_path.backend.service.port.number,
                            path=ingress_path.path,
                        )
                    )
                result[rule.host] = bundles
        return result

    def flat_rules(self) -> List[Dict]:
        """Returns rules as flat list."""
        as_list = []
        for host, rules in list(self.basic_rules().items()):
            for rule in rules:
                as_list.append({"host": host, **rule})
        return as_list

    @classmethod
    def k8s_list_method(cls, broker: Broker, **kwargs: Any) -> models.V1SecretList:
        ns = kwargs["ns"]
        del kwargs["ns"]
        return broker.networking_v1_api.list_namespaced_ingress(namespace=ns, **kwargs)

    @classmethod
    def k8s_read_method(cls, broker: Broker, **kwargs: Any) -> models.V1Secret:
        ns = kwargs.get("ns")
        del kwargs["ns"]
        return broker.networking_v1_api.read_namespaced_ingress(namespace=ns, **kwargs)

    @classmethod
    def k8s_patch_method(cls, broker: Broker, **kwargs: Any) -> models.V1Secret:
        return broker.networking_v1_api.patch_namespaced_ingress(**kwargs)

    @classmethod
    def k8s_delete_method(cls, broker: Broker, **kwargs: Any) -> models.V1Status:
        return broker.networking_v1_api.delete_namespaced_ingress(**kwargs)

    @classproperty
    def kind(self) -> str:
        return "Ingress"

    @classproperty
    def res_name_plural(self) -> str:
        return "ingresses"
