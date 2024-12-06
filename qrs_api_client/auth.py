from requests_ntlm import HttpNtlmAuth
import requests
from dotenv import load_dotenv
import os

# Loads environment variables from .env file.
load_dotenv()


class AuthManager:
    """
    Manages authentication for connecting to services, supporting certificate and NTLM authentication.
    """
    def __init__(self, cert_path=None, key_path=None, root_cert_path=None, user_id=None, password=None):
        """
        Initializes the AuthManager with optional parameters for authentication methods.

        Args:
            cert_path (str, optional): Path to the certificate file (.pem).
            key_path (str, optional): Path to the private key file (.key).
            root_cert_path (str, optional): Path to the root certificate file (root.pem).
            user_id (str, optional): User ID for NTLM authentication.
            password (str, optional): Password for NTLM authentication.
        """
        self.cert_path = cert_path if cert_path is not None else os.getenv("CERT_PATH")
        self.key_path = key_path if key_path is not None else os.getenv("KEY_PATH")
        self.root_cert_path = root_cert_path if root_cert_path is not None else os.getenv("ROOT_CERT_PATH")
        self.user_id = user_id if user_id is not None else os.getenv("USER_ID")
        self.password = password if password is not None else os.getenv("PASSWORD")

    def get_certificate_auth(self):
        """
        Returns the certificate and key paths as a tuple for certificate-based authentication.

        Returns:
            tuple: A tuple containing the certificate path and key path.

        Raises:
            ValueError: If `cert_path` or `key_path` is not provided.
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("Please insert cert_path and key_path for certificate authentication.")
        return self.cert_path, self.key_path

    def get_ntlm_auth(self):
        """
        Creates an NTLM authentication object.

        Returns:
            HttpNtlmAuth: An instance of `HttpNtlmAuth` for NTLM authentication.

        Raises:
            ValueError: If `user_id` or `password` is not provided.
        """
        if not self.user_id or not self.password:
            raise ValueError("Please insert user id and password for NTLM authentication")

        return HttpNtlmAuth(self.user_id, self.password)

    def get_auth(self, session: requests.Session, auth_method="certificate", verify_ssl=True):
        """
        Configures and returns the authentication for the specified method.

        Args:
            session (requests.Session): The session object to configure.
            auth_method (str, optional): The authentication method to use ('certificate' or 'ntlm').
            verify_ssl (bool or str, optional): Either a boolean for SSL verification or the path to a root.pem file.

        Returns:
            requests.Session: The configured session object.

        Raises:
            ValueError: If an unknown authentication method is specified.
        """
        if auth_method == "certificate":
            session.cert = self.get_certificate_auth()
        elif auth_method == "ntlm":
            session.auth = self.get_ntlm_auth()
        else:
            raise ValueError(f"Unknown authentication method: {auth_method}")

        # SSL-Root-Zertifikatsüberprüfung hinzufügen, falls angegeben
        if self.root_cert_path and verify_ssl:
            session.verify = self.root_cert_path
        else:
            session.verify = verify_ssl

        return session
