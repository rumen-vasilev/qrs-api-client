import requests
import random
import string
from qrs_api_client.auth import AuthManager


# session = requests.session()


class QRSClient:
    """
    Instantiates the Qlik Repository Service Class
    """

    def __init__(self, server_name: str, server_port: int, auth_manager: AuthManager, auth_method: str, verify_ssl=True,
                 user_directory=False, user_id=False):
        """
        Establishes connectivity with Qlik Sense Repository Service

        :param server_name: servername.domain
        :param server_port: port of the server (e.g. 4242)
        :param auth_manager: server authentication
        :param auth_method: authentication method
        :param verify_ssl: Bool oder Pfad zur root.pem für SSL-Verifizierung
        :param user_directory: user_directory to use for queries
        :param user_id: user to use for queries
        """

        self.xrf = ''.join(random.sample(string.ascii_letters + string.digits, 16))

        self.server = server_name + ":" + str(server_port) + "/qrs"
        self.headers = {"X-Qlik-XrfKey": self.xrf, "Accept": "application/json",
                        "X-Qlik-User": "UserDirectory={0};UserID={1}".format(user_directory, user_id),
                        "Content-Type": "application/json"}

        # Authentifizierungsmanager initialisieren
        self.session = requests.session()  # Initialisiere Session
        self.auth_manager = auth_manager
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
            response = self.session.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei API-Anfrage: {e}")
            return None

    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self._request("POST", endpoint, json=data)

    def delete(self, endpoint):
        return self._request("DELETE", endpoint)
