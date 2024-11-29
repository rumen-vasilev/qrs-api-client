class Endpoints:
    """
    Diese Klasse enthält die Endpunkte für die Qlik Sense Repository Service API.
    Endpunkte können durch Anhängen von IDs oder Query-Parametern dynamisch ergänzt werden.
    """

    # Basis-Entitäten
    ABOUT = "about"
    APP = "app"  # Für Apps
    USER = "user"  # Für Benutzer
    STREAM = "stream"  # Für Streams
    TASK = "task"  # Für Aufgaben (z. B. Reloads)
    CUSTOM_PROPERTY = "customproperty"  # Für benutzerdefinierte Eigenschaften

    # Spezifische Aktionen
    APP_EXPORT = "app/{id}/export"  # Exportiert eine App mit einer spezifischen ID
    APP_IMPORT = "app/import"  # Importiert eine App
    TASK_START = "task/{id}/start"  # Startet eine Aufgabe mit einer spezifischen ID
    LICENSE_USAGE = "license/usage"  # Lizenzinformationen abrufen

    @staticmethod
    def app_export(app_id: str) -> str:
        """Gibt den Endpunkt für den Export einer spezifischen App zurück."""
        return f"app/{app_id}/export"

    @staticmethod
    def task_start(task_id: str) -> str:
        """Gibt den Endpunkt zum Starten einer spezifischen Aufgabe zurück."""
        return f"task/{task_id}/start"

    @staticmethod
    def custom_property_by_name(name: str) -> str:
        """Gibt den Endpunkt für eine benutzerdefinierte Eigenschaft nach Namen zurück."""
        return f"customproperty/name/{name}"
