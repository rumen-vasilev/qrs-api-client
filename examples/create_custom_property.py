from qrs_api_client.client import QRSClient
from qrs_api_client.auth import AuthManager


# Inserts certificates into the authentication manager
auth_manager = AuthManager(
    cert_path="<path_to_certificates>/client.pem",
    key_path="<path_to_certificates>/client_key.pem",
    root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=4242, auth_manager=auth_manager,
                   auth_method="certificate", verify_ssl=True)

cp_name = "Department"
cp_choice_values = ["Finance", "Sales", "HR"]
cp_object_types = ["App", "Stream"]
cp_description = "Department the app belongs to"

# Calls the API
result = client.create_custom_property(name=cp_name, choice_values=cp_choice_values, object_types=cp_object_types,
                                       description=cp_description)

if result:
    print("Custom property created:", result)
else:
    print("API request error.")