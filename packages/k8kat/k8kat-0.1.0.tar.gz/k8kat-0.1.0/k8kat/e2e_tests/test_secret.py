"""
Copyright 2022 nMachine.io

Requirements:
- e2e cluster, configuration from KUBECONFIG or ~/.kube/config
- applied configuration from k8kat/e2e_tests/cluster-e2e.yaml

"""

import unittest

from k8kat import Secret


class TestSecret(unittest.TestCase):
    """Set of e2e tests for Secret resource."""

    def test_list_secret_from_e2e_namespace(self) -> None:
        """Tests listing pods from 'e2e' namespace"""
        secs = Secret.list(ns="e2e")
        self.assertEqual(len(secs), 1)

    def test_find_secret_with_not_found_error(self) -> None:
        """Tests finding not-existing secret"""
        sec = Secret.find("secret-does-not-exist", ns="e2e")
        self.assertIsNone(sec)

    def test_find_secret_with_data(self) -> None:
        """Tests finding secret and get decoded data"""
        sec = Secret.find("example-credentials", ns="e2e")
        assert sec
        self.assertEqual(
            sec.decoded_data(), {"PASSWORD": "1f2d1e2e67df", "USER_NAME": "admin"}
        )
