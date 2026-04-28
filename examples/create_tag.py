from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager
import uuid


# Inserts certificates into the authentication manager
auth_manager = AuthManager(
    cert_path="C:/LocalUserData/Certificates/Sense TEST/client.pem",
    key_path="C:/LocalUserData/Certificates/Sense TEST/client_key.pem",
    root_cert_path="C:/LocalUserData/Certificates/Sense TEST/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="sv01aqst245c.lr-netz.local", server_port=4242, auth_manager=auth_manager,
                   auth_method="certificate", verify_ssl=False)

tags=["30.ApplicationDatalayer", "10.BasicDatalayer", "1.Application", "Test Rumen"]
# tag = "30.ApplicationDatalayer"

# Calls the API
# result = client.create_tag(name=tag)
result = client.create_tags(names=tags)

if result:
    print("Tags created:", result)
else:
    print("API request error.")
