"""
Copyright 2022 nMachine.io

Requirements:
- e2e cluster, configuration from KUBECONFIG or ~/.kube/config
- applied configuration from k8kat/e2e_tests/cluster-e2e.yaml

"""

import unittest

from k8kat import ConfigMap


class TestConfigMap(unittest.TestCase):
    """Set of e2e tests for ConfigMap resource."""

    def test_list_configmap_from_e2e_namespace(self) -> None:
        """Tests listing pods from 'e2e' namespace"""
        cfms = ConfigMap.list(ns="e2e")
        cfms_filtered = [cfm for cfm in cfms if cfm.name.startswith("map-")]
        self.assertEqual(len(cfms_filtered), 2)

    def test_find_configmap_with_not_found_error(self) -> None:
        """Tests finding not-existing configmap"""
        cfm = ConfigMap.find("config-map-does-not-exist", ns="e2e")
        self.assertIsNone(cfm)

    def test_find_configmap_with_data(self) -> None:
        """Tests finding configmap and get data"""
        cfm = ConfigMap.find("map-raw-data", ns="e2e")
        assert cfm  # mypy requires it (TODO: report/find an issue)
        self.assertEqual(cfm.data, {"key": "value"})
        self.assertEqual(cfm.binary_data, {"bin": "dmFsdWUK"})

    def test_configmap_jdata(self) -> None:
        """Tests setting/getting data from configmap"""
        cfm = ConfigMap.find("map-data", ns="e2e")
        assert cfm
        cfm.jpatch({"k1": "v1"})
        self.assertEqual(cfm.jget(), {"k1": "v1"})

        cfm = ConfigMap.find("map-data", ns="e2e")
        assert cfm
        self.assertEqual(cfm.jget(), {"k1": "v1"})

        cfm.jpatch({"k1": "v2"})
        self.assertEqual(cfm.jget(), {"k1": "v2"})

        cfm.jpatch({"k2": "v3"}, merge=True)
        self.assertEqual(cfm.jget(), {"k1": "v2", "k2": "v3"})

        self.assertEqual(
            cfm.jget(key="non-existent-key", default="default-value"), "default-value"
        )

    def test_configmap_ydata(self) -> None:
        """Tests using yget"""
        cfm = ConfigMap.find("map-data", ns="e2e")
        assert cfm
        self.assertEqual(
            cfm.yget(key="non-existent-key", default="default-value"), "default-value"
        )
