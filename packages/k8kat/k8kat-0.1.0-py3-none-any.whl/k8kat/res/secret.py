"""
Copyright 2022 nMachine.io
"""


from __future__ import annotations

import base64
from typing import Any, Dict, List, Optional

from kubernetes.client import models  # type: ignore

from k8kat.broker import Broker
from k8kat.utils import classproperty

from . import BaseResource


class Secret(BaseResource):
    """Secret resource.

    This class inherits from BaseResource and provide:

    1. static methods to list/find/delete secrets using K8s API
    2. object properties, methods to get stored data
    """

    def __init__(self, raw: models.V1ConfigMap, broker: Broker):
        BaseResource.__init__(self, raw, broker)

    def raw_ob(self) -> models.V1Secret:
        """Returns raw object V1Secret"""
        return self.raw

    def decoded_data(self) -> Dict:
        """Returns secrets in plain-text"""

        def dec(enc_str: str) -> str:
            message_bytes = base64.b64decode(enc_str.encode("ascii"))
            return message_bytes.decode("ascii")

        encoded_data: Dict = self.raw_ob().data or {}
        return {k: dec(v) for k, v in encoded_data.items()}

    @classmethod
    def list_excluding_sys(
        cls, ns: str, broker: Optional[Broker] = None, **query: Any
    ) -> List[Secret]:
        """Returns secrets without secrets assigned with service account"""
        not_fields = list(query.get("not_fields", []))
        not_fields.append(("type", "kubernetes.io/service-account-token"))
        query["not_fields"] = not_fields
        return cls.list(ns, broker=broker, **query)

    @classmethod
    def k8s_list_method(cls, broker: Broker, **kwargs: Any) -> models.V1SecretList:
        ns = kwargs["ns"]
        del kwargs["ns"]
        return broker.core_v1_api.list_namespaced_secret(namespace=ns, **kwargs)

    @classmethod
    def k8s_read_method(cls, broker: Broker, **kwargs: Any) -> models.V1Secret:
        ns = kwargs.get("ns")
        del kwargs["ns"]
        return broker.core_v1_api.read_namespaced_secret(namespace=ns, **kwargs)

    @classmethod
    def k8s_patch_method(cls, broker: Broker, **kwargs: Any) -> models.V1Secret:
        return broker.core_v1_api.patch_namespaced_secret(**kwargs)

    @classmethod
    def k8s_delete_method(cls, broker: Broker, **kwargs: Any) -> models.V1Status:
        return broker.core_v1_api.delete_namespaced_config_map(**kwargs)

    @classproperty
    def kind(self) -> str:
        return "Secret"
