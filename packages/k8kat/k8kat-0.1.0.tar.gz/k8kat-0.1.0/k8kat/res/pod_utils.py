"""
Helper methods for Pod.

Copyright 2022 nMachine.io
"""


from http.client import HTTPResponse
from io import BytesIO
from typing import IO, Any, Callable, List, Optional, Union
from urllib.parse import unquote_plus

from kubernetes.client import V1Container  # type: ignore

from k8kat.utils import units


def coerce_cmd_format(cmd: Union[str, List[str]]) -> List[str]:
    """Returns command as list (coverts from string if necessary)"""
    if isinstance(cmd, str):
        parts = cmd.split(" ")
        # parts = [part.replace("SPACE_CHAR", " ") for part in parts]
        parts = [unquote_plus(part) for part in parts]
        return parts
    return cmd


def container_req_or_lim(
    container: V1Container, metric: str, resource: str
) -> Optional[float]:
    """Gets container capacity and returns in cores (cpu) / bytes (memory)."""
    assert metric in ["requests", "limits"]
    assert resource in ["cpu", "memory", "ephemeral-storage"]
    metrics_dict = getattr(container.resources, metric, None)
    capacity_expr = (metrics_dict or {}).get(resource, None)
    return capacity_expr and units.parse_quant_expr(capacity_expr)


def build_curl_cmd(**params: Any) -> List[str]:
    """Builds curl command line"""
    raw_headers = params.get("headers", {})
    headers = [f"{0}: {1}".format(k, v) for k, v in raw_headers]
    body = params.get("body", None)

    cmd = [
        "curl" if params.get("with_command") else None,
        "-s",
        "-i",
        "-X",
        params.get("verb", "GET"),
        "-H" if headers else None,
        headers if headers else None,
        "-d" if body else None,
        body if body else None,
        "--connect-timeout",
        "1",
        f"{params['url']}{params.get('path', '/')}",
    ]
    return [part for part in cmd if part is not None]


def parse_response(response_str: str) -> Optional[HTTPResponse]:
    """Converts output from curl to HTTPResponse."""
    if response_str:

        class _FakeSocket:
            # pylint: disable=unused-argument
            # pylint: disable=missing-function-docstring
            def __init__(self, response_bytes: bytes):
                self._file = BytesIO(response_bytes)

            def makefile(self, *args: Any, **kwargs: Any) -> IO:
                return self._file

        source = _FakeSocket(response_str.encode("ascii"))
        # noinspection PyTypeChecker
        response = HTTPResponse(source)  # type: ignore
        response.begin()
        return response

    return None


def when_running_normally(func: Callable) -> Callable:
    """Note: needs to be defined at top of class."""

    def running_normally_func(*args: Any, **kwargs: Any) -> Any:
        if args[0].is_running_normally():
            return func(*args, **kwargs)
        return None

    return running_normally_func
