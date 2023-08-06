"""Defines types use in the library.

Copyright 2022 nMachine.io
"""

from typing import List, Optional

from typing_extensions import TypedDict


class UsageDict(TypedDict):
    """Struct with cpu/memory usage"""

    cpu: Optional[str]
    memory: Optional[str]


class ContainerMetricsDict(TypedDict):
    """Struct with container usage"""

    usage: UsageDict


class PodMetricsDict(TypedDict):
    """Struct with containers usage"""

    containers: List[ContainerMetricsDict]


class NodeMetricsDict(TypedDict):
    """Struct with node metrics"""

    usage: UsageDict


class IntelDict(TypedDict):
    """Struct with intel messages"""

    type: str
    status: str
    message: str
