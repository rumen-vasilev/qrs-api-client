from qrs_api_client.client import QRSClient
import qrs_api_client.models as models
from qrs_api_client.auth import AuthManager


# Inserts certificates into the authentication manager
auth_manager = AuthManager(
    cert_path="<path_to_certificates>/client.pem",
    key_path="<path_to_certificates>/client_key.pem",
    root_cert_path="<path_to_certificates>/root.pem")

# Authenticates on the enterprise server
client = QRSClient(server_name="<server_name>", server_port=4242, auth_manager=auth_manager,
                   auth_method="certificate", verify_ssl=True)

cp1 = models.custom_property_definition(name="Department", choice_values=["Finance", "Sales"], object_types=["App"])
cp2 = models.custom_property_definition(name="Region", choice_values=["EMEA", "APAC", "AMER"], object_types=["App", "Stream"])

# Calls the API
result = client.create_custom_properties([cp1, cp2])

if result:
    print("Custom properties created:", result)
else:
    print("API request error.")