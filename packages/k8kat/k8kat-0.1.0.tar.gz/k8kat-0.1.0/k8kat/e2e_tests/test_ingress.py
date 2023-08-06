"""
Copyright 2022 nMachine.io

Requirements:
- e2e cluster, configuration from KUBECONFIG or ~/.kube/config
- applied configuration from k8kat/e2e_tests/cluster-e2e.yaml

"""

import unittest

from k8kat import Ingress


class TestIngress(unittest.TestCase):
    """Set of e2e tests for Ingress resource."""

    def test_list_ingress_from_e2e_namespace(self) -> None:
        """Tests listing Ingresses from 'e2e' namespace"""
        ingresses = Ingress.list(ns="e2e")
        self.assertEqual(len(ingresses), 1)
        self.assertEqual(ingresses[0].name, "example-ingress")

    def test_find_ingress_with_not_found_error(self) -> None:
        """Tests finding not-existing Ingress"""
        ingress = Ingress.find("ingress-does-not-exist", ns="e2e")
        self.assertIsNone(ingress)

    def test_find_ingress(self) -> None:
        """Tests finding ingress"""
        sec = Ingress.find("example-ingress", ns="e2e")
        assert sec

        self.assertEqual(sec.name, "example-ingress")
        self.assertEqual(sec.labels, {})
        self.assertEqual(
            sec.flat_rules(),
            [
                {
                    "host": "localhost",
                    "service": "foo-service",
                    "port": 5678,
                    "path": "/foo",
                },
                {
                    "host": "localhost",
                    "service": "bar-service",
                    "port": 5678,
                    "path": "/bar",
                },
            ],
        )
        self.assertEqual(
            sec.basic_rules(),
            {
                "localhost": [
                    {"path": "/foo", "port": 5678, "service": "foo-service"},
                    {"path": "/bar", "port": 5678, "service": "bar-service"},
                ]
            },
        )
