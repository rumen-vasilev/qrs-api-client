"""
qrs-api-client — Python client for the Qlik Sense Repository Service (QRS) API.
"""
from importlib.metadata import PackageNotFoundError, version

from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager

# The version is declared once, in pyproject.toml, and read here from the
# installed package metadata so the two can never drift apart.
try:
    __version__ = version("qrs-api-client")
except PackageNotFoundError:  # package is not installed (e.g. running from a source checkout)
    __version__ = "0.0.0+unknown"

__all__ = ["QRSClient", "AuthManager", "__version__"]
