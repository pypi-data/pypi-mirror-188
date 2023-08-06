"""
Copyright 2022 nMachine.io

Requirements:
- e2e cluster, configuration from KUBECONFIG or ~/.kube/config
- applied configuration from k8kat/e2e_tests/cluster-e2e.yaml

"""

import unittest

from k8kat import ServiceAccount


class TestServiceAccount(unittest.TestCase):
    """Set of e2e tests for ServiceAccount resource."""

    def test_list_sa_from_e2e_namespace(self) -> None:
        """Tests listing Service Accounts from 'e2e' namespace"""
        ssa_list = ServiceAccount.list(ns="e2e")
        self.assertEqual(len(ssa_list), 2)
        self.assertEqual({ssa.name for ssa in ssa_list}, {"default", "example-sa"})

    def test_list_sa_from_e2e_namespace_excluding_sys(self) -> None:
        """Tests listing Service Accounts from 'e2e' namespace without default sa."""
        ssa_list = ServiceAccount.list_excluding_sys(ns="e2e")
        self.assertEqual(len(ssa_list), 1)
        self.assertEqual(ssa_list[0].name, "example-sa")

    def test_find_sa_with_not_found_error(self) -> None:
        """Tests finding not-existing service account"""
        sec = ServiceAccount.find("sa-does-not-exist", ns="e2e")
        self.assertIsNone(sec)

    def test_find_sa_with_secrets(self) -> None:
        """Tests finding service account"""
        sec = ServiceAccount.find("example-sa", ns="e2e")
        assert sec

        self.assertEqual(sec.name, "example-sa")
        self.assertEqual(sec.labels, {})
        secrets = sec.secrets()
        self.assertEqual(len(secrets), 1)
        self.assertEqual(secrets[0].name, "example-credentials")
