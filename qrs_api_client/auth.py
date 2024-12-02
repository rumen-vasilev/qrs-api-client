from requests_ntlm import HttpNtlmAuth
import requests


class AuthManager:
    def __init__(self, cert_path=None, key_path=None, root_cert_path=None, user_id=None, password=None):
        """
        Initialisiert den AuthManager mit optionalen Parametern für verschiedene Authentifizierungsmethoden.

        :param cert_path: Pfad zur Zertifikatsdatei (.pem)
        :param key_path: Pfad zur Schlüsseldatei (.key)
        :param root_cert_path: Pfad zur Root-Zertifikatsdatei (root.pem)
        :param user_id: User ID
        :param password: password
        """
        self.cert_path = cert_path
        self.key_path = key_path
        self.root_cert_path = root_cert_path
        self.user_id = user_id
        self.password = password

    def get_certificate_auth(self):
        """
        Gibt das Zertifikats- und Schlüsselpfad-Tuple zurück.

        :return: Tuple (cert_path, key_path)
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("Please insert cert_path and key_path for certificate authentication.")
        return self.cert_path, self.key_path

    def get_ntlm_auth(self):
        """
        Creates a NTLM authentication.

        :return: requests_ntlm.HttpNtlmAuth-Objekt
        """
        if not self.user_id or not self.password:
            raise ValueError("Please insert user id and password for NTLM authentication")

        return HttpNtlmAuth(self.user_id, self.password)

    def get_auth(self, session: requests.Session, auth_method="certificate", verify_ssl=True):
        """
        Gibt die Authentifizierung basierend auf der angegebenen Methode zurück.

        :param session: Das zu konfigurierende Session-Objekt.
        :param auth_method: Authentifizierungsmethode ('certificate', 'ntlm').
        :param verify_ssl: Bool oder Pfad zur root.pem für SSL-Verifizierung
        :return: Authentifizierungsdaten (Tuple oder Auth-Objekt)
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
