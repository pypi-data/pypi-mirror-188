"""This module provides classes required to communicate
with Kubernetes clusters.

There two classes:

    Configuration() which provides parameters (adresses,
        credentials etc.) required to connect to a cluster.

    Broker() is a class which exposes endpoints to connect
        to get/set data in K8s clusters.


Both classes are required by K8Kat's resources. The instance
of broker (singleton) will be created if you don't pass
your own instance of the broker.

Example:

    config = Configuration(kubeconfig_path='/my/kube/config')
    broker = Broker(config)
    ...
    pods = broker.core_v1_api.list_pod_for_all_namespaces()


Copyright 2022 nMachine.io
"""

from __future__ import annotations

from typing import Optional

from kubernetes import client, config  # type: ignore

# pylint: disable=unused-import
from kubernetes.config.config_exception import ConfigException  # type: ignore


class Configuration:  # pylint: disable=too-few-public-methods
    """Configuration for Broker."""

    def __init__(
        self,
        token: Optional[str] = None,
        api_server: Optional[str] = None,
        ca_cert: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        kubeconfig_path: Optional[str] = None,
    ) -> None:
        """Configuration for the class Broker. Use arguments: token,
        api_server, ca_cert, verify_ssl to authorize using the
        bearer token.

        Optionally it tries to load configuration from kubeconfig
        file from standard locations, defined in environment variable
        or passed by kubeconfig_path.

        It also handles the situation when it runs in "in-cluster" mode.

        Args:
            token(str): Bearer token
            api_server(str): address to API server
            ca_cert(str): cluster's certificate authority
            verify_ssl(bool): option to ignore server cert, ignored if ca_cert is passed

            kubeconfig_path(str): path to Kube Config file

        """
        self._kubernetes_config = client.Configuration()

        if api_server is not None:
            self._kubernetes_config.host = api_server
            self._kubernetes_config.api_key = {"authorization": f"Bearer {token}"}
            if ca_cert:
                self._kubernetes_config.verify_ssl = True
                self._kubernetes_config.ssl_ca_cert = ca_cert
            else:
                if verify_ssl is None:
                    verify_ssl = False
                self._kubernetes_config.verify_ssl = verify_ssl

        elif kubeconfig_path:
            config.load_kube_config(  # TODO: config.load_config()
                config_file=kubeconfig_path,
                client_configuration=self.kubernetes_config,
            )
        else:
            config.load_config(client_configuration=self.kubernetes_config)

    @property
    def kubernetes_config(self) -> client.Configuration:
        """Returns low-level client.Configuration from the kubernetes library."""
        return self._kubernetes_config


class Broker:  # pylint: disable=too-few-public-methods
    """Class privides endpoints, alrady configured to query K8s clusters.
    If you want to work with many clusters in the same application
    you will need to create Brokers manually. In simpler cases default
    Broker, automatically created should be enough.

    Class attributes:
        default_instance : singleton object if created

    Attributes:

        core_v1_api : raw K8s interface to get/set core resources
        custom_api : raw K8s interface to get/set custom resources

    """

    default_instance = None

    def __init__(self, configuration: Optional[Configuration] = None):
        """Broker constructor, the object can be created with custom configuration.
        If it's not provided it uses a default configuration.

        Args:
            configuration (Configuration): configuration for broker
        """

        if configuration is None:
            configuration = Configuration()
        self._configuration = configuration
        self._api_client = client.ApiClient(configuration.kubernetes_config)

        self.core_v1_api = client.CoreV1Api(self._api_client)
        self.custom_api = client.CustomObjectsApi(self._api_client)
        self.networking_v1_api = client.NetworkingV1Api(self._api_client)

    @classmethod
    def get_default_instance(cls) -> Broker:
        """Returns default instance of Broker if created automatically"""
        if cls.default_instance is None:
            cls.default_instance = Broker()
        return cls.default_instance
