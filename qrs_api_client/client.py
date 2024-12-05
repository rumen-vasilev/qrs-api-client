import requests
import random
import string
from qrs_api_client.auth import AuthManager
import qrs_api_client.models as models
import json


class QRSClient:
    """
    Instantiates the Qlik Repository Service Class
    """

    def __init__(self, server_name: str, server_port: int, auth_manager: AuthManager, auth_method: str, verify_ssl=True):
        """
        Establishes connectivity with Qlik Sense Repository Service

        :param server_name: servername.domain
        :param server_port: port of the server (e.g. 4242)
        :param auth_manager: server authentication
        :param auth_method: authentication method
        :param verify_ssl: Bool oder Pfad zur root.pem für SSL-Verifizierung
        """

        self.xrf = ''.join(random.sample(string.ascii_letters + string.digits, 16))

        self.server = server_name + ":" + str(server_port) + "/qrs"
        self.headers = {"X-Qlik-XrfKey": self.xrf, "Accept": "application/json",
                        "X-Qlik-User": "UserDirectory=INTERNAL;UserID=sa_repository",
                        "Content-Type": "application/json"}

        # Authentifizierungsmanager initialisieren
        self.session = requests.session()  # Initialisiere Session
        self.session = auth_manager.get_auth(self.session, auth_method, verify_ssl)

        if auth_method == "ntlm":
            self.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
            self.headers.pop("X-Qlik-User")
            # self.headers = {"X-Qlik-XrfKey": self.xrf, "User-Agent": "Windows"}

    def _request(self, method, endpoint, **kwargs):
        """
        Führt einen API-Request aus.

        :param method: HTTP-Methode (GET, POST, etc.)
        :param endpoint: API-Endpunkt
        :return: JSON-Antwort oder None bei Fehler
        """
        url = "https://" + f"{self.server}/{endpoint}?xrfkey={self.xrf}"
        print(f"Making request to: {url}")

        try:
            response = self.session.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self._request("POST", endpoint, data=data)

    def delete(self, endpoint):
        return self._request("DELETE", endpoint)

    def create_reload_task(self, app_id, task_name, custom_properties, tags, schema_events, composite_events):
        """Gibt den Endpunkt für eine benutzerdefinierte Eigenschaft nach Namen zurück."""
        # App, which gets the task
        app_condensed = models.app_condensed(_id=app_id)

        # Custom properties
        custom_property_list = []
        for custom_property_id, custom_property_values in custom_properties.items():
            custom_property_definition_condensed = models.custom_property_definition_condensed(_id=custom_property_id)
            for value in custom_property_values:
                custom_property_value = models.custom_property_value(value=value,
                                                                     definition=custom_property_definition_condensed)
                custom_property_list.append(custom_property_value)

        # Tags
        tag_list = []
        for tag in tags:
            tag_condensed = models.tag_condensed(_id=tag)
            tag_list.append(tag_condensed)

        # Reload task structure without scheduler
        reload_task = models.reload_task(custom_properties=custom_property_list, name=task_name, tags=tag_list,
                                         app=app_condensed)

        # Reload task structure with scheduler
        reload_task_bundle = models.reload_task_bundle(task=reload_task, composite_events=composite_events,
                                                       schema_events=schema_events)

        # Body of the HTTP method
        payload = json.dumps(reload_task_bundle)

        return self.post("reloadtask/create", data=payload)
