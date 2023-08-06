"""
Copyright 2022 nMachine.io
"""


from __future__ import annotations

import json
from typing import Any, Dict, Optional

import yaml  # type: ignore
from kubernetes.client import models  # type: ignore

from k8kat.broker import Broker
from k8kat.utils import classproperty

from . import BaseResource


class ConfigMap(BaseResource):
    """ConfigMap resource.

    This class inherits from BaseResource and provide:

    1. static methods to list/find/patch/delete configmaps using K8s API
    2. object properties, methods to get stored data
    """

    def __init__(self, raw: models.V1ConfigMap, broker: Broker):
        BaseResource.__init__(self, raw, broker)

    @property
    def data(self) -> Dict[str, str]:
        """Returns key-value pairs stored in object"""
        return self.raw.data or {}

    @property
    def binary_data(self) -> Dict[str, str]:
        """Returns key-binary-value pairs stored in object"""
        return self.raw.binary_data or {}

    def jget(
        self, key: Optional[str] = None, default: Optional[Any] = None
    ) -> Optional[Any]:
        """Gets a value from ConfigMap. Values stored in ConfigMap has to
        be json encoded.

        Args:
            key: name of key in ConfigMap, default master
            default: default value

        Returns:
            value stored on key"""

        key = key or "master"
        raw_value = self.data.get(key)
        obtained = raw_value and json.loads(raw_value)
        return obtained if obtained is not None else default

    def yget(
        self, key: Optional[str] = None, default: Optional[Any] = None
    ) -> Optional[Any]:
        """Gets a value from ConfigMap. Values stored in ConfigMap has to
        be yaml encoded.

        Args:
            key: name of key in ConfigMap, default master
            default: default value

        Returns:
            value stored on key"""

        key = key or "master"
        raw_value = self.data.get(key)
        obtained = raw_value and yaml.load(raw_value, Loader=yaml.FullLoader)
        return obtained if obtained is not None else default

    def jpatch(
        self, content: Any, key: Optional[str] = None, merge: Optional[bool] = False
    ) -> None:
        """Modifies a value from ConfigMap.

        Args:
            content: new value to store
            key: name of key in ConfigMap, default master
            merge: if true it tries to merge values with values from the configmap.
                   if values are not dict it raises ValueError"""
        key = key or "master"
        if merge:
            current_content = self.jget(key)
            if isinstance(current_content, dict) and isinstance(content, dict):
                content = {**current_content, **content}
            else:
                raise ValueError("Only dicts can be merged")
        self.raw.data = {key: json.dumps(content)}
        return self.patch()

    @classmethod
    def k8s_list_method(cls, broker: Broker, **kwargs: Any) -> models.V1PodList:
        ns = kwargs["ns"]
        del kwargs["ns"]
        return broker.core_v1_api.list_namespaced_config_map(namespace=ns, **kwargs)

    @classmethod
    def k8s_read_method(cls, broker: Broker, **kwargs: Any) -> models.V1ConfigMap:
        ns = kwargs.get("ns")
        del kwargs["ns"]
        return broker.core_v1_api.read_namespaced_config_map(namespace=ns, **kwargs)

    @classmethod
    def k8s_patch_method(cls, broker: Broker, **kwargs: Any) -> models.V1ConfigMap:
        return broker.core_v1_api.patch_namespaced_config_map(**kwargs)

    @classmethod
    def k8s_delete_method(cls, broker: Broker, **kwargs: Any) -> models.V1Status:
        return broker.core_v1_api.delete_namespaced_config_map(**kwargs)

    @classproperty
    def kind(self) -> str:
        return "ConfigMap"
