from requests_ntlm import HttpNtlmAuth
import requests


class AuthManager:
    def __init__(self, cert_path=None, key_path=None, root_cert_path=None, ntlm_credentials=None):
        """
        Initialisiert den AuthManager mit optionalen Parametern für verschiedene Authentifizierungsmethoden.

        :param cert_path: Pfad zur Zertifikatsdatei (.pem)
        :param key_path: Pfad zur Schlüsseldatei (.key)
        :param root_cert_path: Pfad zur Root-Zertifikatsdatei (root.pem)
        :param ntlm_credentials: Dictionary mit NTLM-Anmeldeinformationen ('username', 'password')
        """
        self.cert_path = cert_path
        self.key_path = key_path
        self.root_cert_path = root_cert_path
        self.ntlm_credentials = ntlm_credentials

    def get_certificate_auth(self):
        """
        Gibt das Zertifikats- und Schlüsselpfad-Tuple zurück.

        :return: Tuple (cert_path, key_path)
        """
        if not self.cert_path or not self.key_path:
            raise ValueError("Für die Zertifikatsauthentifizierung müssen cert_path und key_path angegeben werden.")
        return self.cert_path, self.key_path

    def get_ntlm_auth(self):
        """
        Erstellt eine NTLM-Authentifizierung.

        :return: requests_ntlm.HttpNtlmAuth-Objekt
        """
        if not self.ntlm_credentials:
            raise ValueError("Für NTLM-Authentifizierung müssen ntlm_credentials (username und password) angegeben werden.")

        username = self.ntlm_credentials.get("username")
        password = self.ntlm_credentials.get("password")

        if not username or not password:
            raise ValueError("NTLM-Anmeldedaten müssen username und password enthalten.")

        return HttpNtlmAuth(username, password)

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
            raise ValueError(f"Unbekannte Authentifizierungsmethode: {auth_method}")

        # SSL-Root-Zertifikatsüberprüfung hinzufügen, falls angegeben
        if self.root_cert_path:
            session.verify = self.root_cert_path
        else:
            session.verify = verify_ssl  # Standardmäßig SSL-Verifizierung aktivieren

        return session
