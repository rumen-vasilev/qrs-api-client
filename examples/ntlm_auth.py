from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager
import logging
import http.client

# For debugging purposes (Remove that, if not needed)
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.DEBUG)

# Inserts credentials into the authentication manager
auth_manager = AuthManager(user_id="<DOMAIN>\\<user_id>", password="<password>",
                           root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=443, auth_manager=auth_manager,
                   auth_method="ntlm", verify_ssl=False)

# Calls the API
api_desc_post = client.get("about/api/description", "extended=false&method=POST")
if api_desc_post:
    print(api_desc_post)
else:
    print("API request error.")
