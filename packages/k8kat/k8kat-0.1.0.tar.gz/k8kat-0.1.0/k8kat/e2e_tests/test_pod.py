"""
Copyright 2022 nMachine.io

Requirements:
- e2e cluster, configuration from KUBECONFIG or ~/.kube/config
- applied configuration from k8kat/e2e_tests/cluster-e2e.yaml

"""

import time
import unittest

from k8kat import Pod, PodStatus


class TestPod(unittest.TestCase):
    """Set of e2e tests for Pod resource."""

    def test_list_pod_from_all_namespaces(self) -> None:
        """Tests listing pods"""
        pods = Pod.list()
        self.assertTrue(len(pods) > 0)

    def test_list_pod_from_e2e_namespace(self) -> None:
        """Tests listing pods from 'e2e' namespace"""
        pods = Pod.list(ns="e2e")
        self.assertEqual(len(pods), 4)

    def test_find_pod_with_not_found_error(self) -> None:
        """Tests finding not-existing Pod"""
        pod = Pod.find("container-does-not-exist", ns="e2e")
        self.assertIsNone(pod)

    def test_find_pod(self) -> None:
        """Tests finding pod"""
        pod = Pod.find("busybox-with-init-containers", ns="e2e")
        assert pod  # mypy requires it (TODO: report/find an issue)
        self.assertEqual(pod.name, "busybox-with-init-containers")
        self.assertEqual(pod.kind, "Pod")
        self.assertEqual(pod.labels, {"name": "busybox-with-init-containers"})
        self.assertEqual(pod.phase, "Running")
        self.assertRegex(pod.ip, r"^\d+\.\d+\.\d+\.\d+$")  # type: ignore
        self.assertEqual(pod.image(), "busybox")
        self.assertEqual(pod.ternary_status(), PodStatus.POSITIVE)
        self.assertTrue(pod.is_running())
        self.assertTrue(pod.is_running_normally())
        self.assertTrue(pod.is_working())
        self.assertTrue(pod.has_settled())
        self.assertFalse(pod.has_parent)
        self.assertFalse(pod.is_pending_normally())
        self.assertFalse(pod.is_running_morbidly())
        self.assertFalse(pod.is_broken())
        self.assertFalse(pod.is_terminating())
        self.assertFalse(pod.did_scheduling_fail())
        self.assertFalse(pod.is_pending_morbidly())
        self.assertFalse(pod.is_pending())
        self.assertFalse(pod.has_failed())
        self.assertFalse(pod.has_succeeded())
        self.assertFalse(pod.has_run())
        self.assertEqual(pod.cpu_request(), 0.25)
        self.assertEqual(pod.cpu_limit(), 0.5)
        self.assertEqual(pod.mem_limit(), 134217728)
        self.assertEqual(pod.mem_request(), 67108864)
        self.assertEqual(pod.eph_storage_limit(), 3221225472.0)
        self.assertEqual(pod.eph_storage_request(), 2147483648.0)

    def test_get_logs(self) -> None:
        """Tests getting logs"""
        pod = Pod.find("busybox-with-init-containers", ns="e2e")
        assert pod
        logs = pod.log_lines()
        self.assertIn("The app is running!", logs)

    def test_shell_exec(self) -> None:
        """Tests executing command"""
        pod = Pod.find("busybox-with-init-containers", ns="e2e")
        assert pod
        result = pod.shell_exec("whoami")
        self.assertEqual(result, "root")

    def test_replace_image(self) -> None:
        """Tests replacing container image"""
        pod = Pod.find("busybox-to-patch", ns="e2e")
        assert pod
        new_image = "busybox:1.35" if pod.image() == "busybox:1.34" else "busybox:1.34"
        pod = pod.replace_image(new_image)
        assert pod
        self.assertEqual(pod.image(), new_image)

    def test_pod_metrics(self) -> None:
        """Tests querying run-time metrics"""
        pod = Pod.find("busybox-with-init-containers", ns="e2e")
        assert pod

        for _ in range(1, 10):
            metrics = pod.load_per_pod_metrics()
            if metrics is None or len(metrics) == 0:
                time.sleep(3)
                continue

        self.assertEqual(len(metrics), 1)
        metrics = metrics[0]["containers"][0]
        self.assertEqual(metrics["name"], "busybox")
        self.assertEqual(list(metrics["usage"].keys()), ["cpu", "memory"])
