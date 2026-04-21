"""
Authentication management for the QRS API client.

Supports certificate-based and NTLM authentication. NTLM support requires
the optional `requests_ntlm` dependency (install via `pip install qrs-api-client[ntlm]`).
"""
import os
import requests


class AuthManager:
    """
    Manages authentication for connecting to Qlik Sense Enterprise,
    supporting certificate-based and NTLM authentication.
    """
    def __init__(self, cert_path=None, key_path=None, root_cert_path=None, user_id=None, password=None):
        """
        Initializes the AuthManager with optional parameters for authentication methods.

        Args:
            cert_path (str, optional): Path to the certificate file (.pem).
            key_path (str, optional): Path to the private key file (.key).
            root_cert_path (str, optional): Path to the root certificate file (root.pem).
            user_id (str, optional): User ID for NTLM authentication (e.g., "DOMAIN\\\\user").
            password (str, optional): Password for NTLM authentication.
        """
        self.cert_path = cert_path
        self.key_path = key_path
        self.root_cert_path = root_cert_path
        self.user_id = user_id
        self.password = password

    def get_certificate_auth(self) -> tuple:
        """
        Returns the (cert, key) tuple for certificate-based authentication.

        Raises:
            ValueError: If `cert_path` or `key_path` is not provided.
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("Please provide cert_path and key_path for certificate authentication.")
        return self.cert_path, self.key_path

    def get_ntlm_auth(self):
        """
        Creates an NTLM authentication object.

        Note: Requires the optional `requests_ntlm` package. Install via:
            pip install qrs-api-client[ntlm]

        Raises:
            ImportError: If `requests_ntlm` is not installed.
            ValueError: If `user_id` or `password` is not provided.
        """
        try:
            from requests_ntlm import HttpNtlmAuth
        except ImportError as e:
            raise ImportError(
                "NTLM authentication requires the 'requests_ntlm' package. "
                "Install it with: pip install qrs-api-client[ntlm]"
            ) from e

        if not self.user_id or not self.password:
            raise ValueError("Please provide user_id and password for NTLM authentication.")

        return HttpNtlmAuth(self.user_id, self.password)

    def get_auth(self, session: requests.Session, auth_method="certificate", verify_ssl=True) -> requests.Session:
        """
        Configures the given session with authentication and SSL settings.

        Args:
            session: The requests session to configure.
            auth_method: Either ``"certificate"`` or ``"ntlm"``.
            verify_ssl: ``True``/``False`` for SSL verification, or a path to
                a root CA bundle. If ``root_cert_path`` is set on this
                instance and ``verify_ssl`` is truthy, the root cert path
                is used instead.

        Raises:
            ValueError: If an unknown authentication method is specified.
        """
        if auth_method == "certificate":
            session.cert = self.get_certificate_auth()
        elif auth_method == "ntlm":
            session.auth = self.get_ntlm_auth()
        else:
            raise ValueError(f"Unknown authentication method: {auth_method!r}")

        # Prefer explicit root cert path if provided and SSL verification is enabled
        if self.root_cert_path and verify_ssl:
            session.verify = self.root_cert_path
        else:
            session.verify = verify_ssl

        return session
