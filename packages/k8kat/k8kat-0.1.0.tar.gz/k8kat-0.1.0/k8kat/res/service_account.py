"""
Copyright 2022 nMachine.io
"""


from __future__ import annotations

from typing import Any, List, Optional

from kubernetes.client import models  # type: ignore

from k8kat.broker import Broker
from k8kat.utils import classproperty

from . import BaseResource
from .secret import Secret


class ServiceAccount(BaseResource):
    """Service Account resource.

    This class inherits from BaseResource and provide:

    1. static methods to list/find/delete service accounts using K8s API
    2. object properties, methods to get stored data
    """

    def __init__(self, raw: models.V1ConfigMap, broker: Broker):
        BaseResource.__init__(self, raw, broker)

    def body(self) -> models.V1ServiceAccount:
        """Returns raw object V1ServiceAccount"""
        return self.raw

    def secrets(self) -> List[Secret]:
        """Returns list of the secrets in the same namespace that
        pods running using this ServiceAccount are allowed to use."""
        secrets_raw = self.body().secrets or []
        secrets = []
        for secret_raw in secrets_raw:
            secret = Secret.find(
                secret_raw.name, ns=self.raw.metadata.namespace, broker=self.broker
            )
            if secret:
                secrets.append(secret)
        return secrets

    @classmethod
    def list_excluding_sys(
        cls, ns: str, broker: Optional[Broker] = None, **query: Any
    ) -> List[ServiceAccount]:
        """Returns service accounts without defaults."""
        not_fields = list(query.get("not_fields", []))
        not_fields.append(("metadata.name", "default"))
        query["not_fields"] = not_fields
        return cls.list(ns, broker=broker, **query)

    @classmethod
    def k8s_list_method(
        cls, broker: Broker, **kwargs: Any
    ) -> models.V1ServiceAccountList:
        ns = kwargs["ns"]
        del kwargs["ns"]
        return broker.core_v1_api.list_namespaced_service_account(
            namespace=ns, **kwargs
        )

    @classmethod
    def k8s_read_method(cls, broker: Broker, **kwargs: Any) -> models.V1ServiceAccount:
        ns = kwargs.get("ns")
        del kwargs["ns"]
        return broker.core_v1_api.read_namespaced_service_account(
            namespace=ns, **kwargs
        )

    @classmethod
    def k8s_patch_method(cls, broker: Broker, **kwargs: Any) -> models.V1ServiceAccount:
        return broker.core_v1_api.patch_namespaced_service_account(**kwargs)

    @classmethod
    def k8s_delete_method(cls, broker: Broker, **kwargs: Any) -> models.V1Status:
        return broker.core_v1_api.delete_namespaced_service_account(**kwargs)

    @classproperty
    def kind(self) -> str:
        return "ServiceAccount"
