# Design: `app_get_id` – App-Namen zu App-ID(s) auflösen

**Datum:** 2026-07-20
**Status:** Freigegeben (Design)
**Betroffene Dateien:** `qrs_api_client/client.py`, `examples/app_get_id.py`

## Ziel

Eine neue Methode auf `QRSClient`, die zu einem **App-Namen** die zugehörige(n)
**App-ID(s)** liefert. Da in Qlik Sense mehrere Apps denselben Namen tragen
können, gibt die Methode immer eine **Liste** zurück. Optional kann zusätzlich
über den **Stream-Namen** eingegrenzt werden, um gezielt zu suchen.

## Design-Entscheidungen

| Frage | Entscheidung |
|-------|--------------|
| Rückgabetyp | Immer eine Liste (`list[uuid.UUID]`), leere Liste wenn nichts gefunden |
| Stream-Parameter | Filtert über den **Stream-Namen** (nicht die ID) |
| ID-Format | `uuid.UUID`-Objekte |
| Methodenname | `app_get_id` |
| Tests | Vorerst nur Beispielskript (Repo-Konvention), keine Unit-Tests |
| Query-Strategie | Serverseitiger QRS-Filter über `/qrs/app/full` |

## API

```python
def app_get_id(self, app_name: str, stream_name: str = None) -> list[uuid.UUID]:
```

- `app_name` (str, Pflicht): Name der gesuchten App.
- `stream_name` (str, optional): Wenn gesetzt, wird zusätzlich auf den
  Stream-Namen eingegrenzt. Standard `None` (keine Stream-Einschränkung).
- **Rückgabe:** `list[uuid.UUID]` – die IDs aller passenden Apps. Leere Liste,
  wenn keine App passt oder der Request fehlschlägt.

## Verhalten / Datenfluss

1. Filterstring aufbauen:
   - ohne Stream: `name eq '<app_name>'`
   - mit Stream: `name eq '<app_name>' and stream.name eq '<stream_name>'`
2. Aufruf `self.get(endpoint="/qrs/app/full", params={"filter": <filterstring>})`.
   Der Ansatz folgt dem bestehenden Muster aus `app_reload` und
   `app_change_owner` (serverseitige Filterung statt Client-seitigem Durchsuchen
   aller Apps).
3. Aus jedem Treffer das Feld `id` lesen und in `uuid.UUID` umwandeln.
4. Liste der `uuid.UUID` zurückgeben.

## Fehler- und Randfälle

- **Kein Treffer:** leere Liste `[]`. Zusätzlich eine `logger.warning`-Meldung,
  dass keine App mit dem Namen (ggf. im Stream) gefunden wurde.
- **Request-Fehler** (`self.get` liefert `None`): ebenfalls `[]`. Der eigentliche
  HTTP-Fehler wird bereits in `_request` geloggt. Damit bleibt der Rückgabetyp
  stabil eine Liste.
- **Apps ohne Stream** (unveröffentlicht, „Work"): matchen bei gesetztem
  `stream_name` korrekt nicht.
- **Matching:** über den serverseitigen `eq`-Filter (QRS-Standardverhalten).
- **Namen mit einfachem Anführungszeichen (`'`):** werden – konsistent mit dem
  gesamten bestehenden Code (`app_set_tags`, `app_change_owner` etc.) – nicht
  escaped. Bekannte, akzeptierte Einschränkung.

## Beispielskript

`examples/app_get_id.py`, analog zu `examples/app_get_owner.py`:
Cert-Auth aufsetzen, `client.app_get_id(app_name=..., stream_name=...)` aufrufen
und das Ergebnis ausgeben. Zeigt beide Varianten (mit und ohne Stream).

## Out of Scope

- Unit-Tests / Test-Infrastruktur (Repo hat aktuell keine; bewusst nicht Teil
  dieses Features).
- Escaping von Sonderzeichen in Filterwerten (konsistent zum restlichen Code
  nicht umgesetzt).
- Suche über andere Felder als Name/Stream.
