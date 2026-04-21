from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager
import logging
import http.client

# For debugging purposes (Remove that, if not needed)
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)

# Inserts certificates into the authentication manager
auth_manager = AuthManager(
    cert_path="<path_to_certificates>/client.pem",
    key_path="<path_to_certificates>/client_key.pem",
    root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=4242, auth_manager=auth_manager,
                   auth_method="certificate", verify_ssl=True)

# Calls the API
result = client.get(endpoint="/qrs/about/api/description", params={"extended": "false", "method": "POST"})
if result:
    print(result)
else:
    print("API request error.")
