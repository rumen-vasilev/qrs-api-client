"""
qrs-api-client — Python client for the Qlik Sense Repository Service (QRS) API.
"""
from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager

__version__ = "3.0.0"
__all__ = ["QRSClient", "AuthManager", "__version__"]
