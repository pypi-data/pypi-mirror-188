"""
Copyright 2022 nMachine.io
"""


import os
import tempfile
import unittest

from k8kat import Broker, ConfigException, Configuration, Pod


class TestBroker(unittest.TestCase):
    """E2E tests for Broker, Configuration"""

    def test_default_broker(self) -> None:
        """Tests creating default broker"""
        pods = Pod.list()
        self.assertTrue(len(pods) > 0)

    def test_configure_broker_with_invalid_kubeconfig(self) -> None:
        """Tests loading configuration from invalid config"""

        with self.assertRaises(ConfigException):
            configuration = Configuration(kubeconfig_path="/tmp/not/found/kubeconfig")
            Broker(configuration)

    def test_configure_broker_with_kubeconfig(self) -> None:
        """Tests loading configuration from kubeconfig"""

        path_kubeconfig = os.environ.get(
            "KUBECONFIG", os.path.expanduser("~/.kube/config")
        )
        temp_kubeconfig = None

        try:
            with tempfile.NamedTemporaryFile(delete=False) as ftemp:

                with open(path_kubeconfig, "br") as fcfg:
                    ftemp.write(fcfg.read())

                ftemp.close()
                temp_kubeconfig = ftemp.name

                configuration = Configuration(kubeconfig_path=temp_kubeconfig)
                broker = Broker(configuration)

                pods = Pod.list(broker=broker)
                self.assertTrue(len(pods) > 0)

        finally:
            if temp_kubeconfig:
                os.unlink(temp_kubeconfig)

    def test_configure_broker_with_bearer_token(self) -> None:
        """Tests passing token, api_server"""

        def readfile(env_name: str) -> str:
            with open(os.environ.get(env_name, env_name), "r", encoding="utf8") as fhn:
                return fhn.read().strip()

        token = readfile("E2E_TOKEN_FILE")
        api_server = readfile("E2E_API_SERVER_FILE")

        configuration = Configuration(token=token, api_server=api_server)
        broker = Broker(configuration)
        pods = Pod.list(broker=broker)
        self.assertTrue(len(pods) > 0)
