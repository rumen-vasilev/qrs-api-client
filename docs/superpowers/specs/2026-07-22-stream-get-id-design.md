# Design: `stream_get_id` – Stream-Namen zu Stream-ID(s) auflösen

**Datum:** 2026-07-22
**Status:** Freigegeben (Design)
**Betroffene Dateien:** `qrs_api_client/client.py`, `examples/stream_get_id.py`
**Verwandt:** [[2026-07-20-app-get-id-design]] – direkte Schwester-Methode

## Ziel

Eine neue Methode auf `QRSClient`, die zu einem **Stream-Namen** die zugehörige(n)
**Stream-ID(s)** liefert. Die Ausgabe erfolgt im **selben Format wie bei
`app_get_id`**: immer eine Liste von `uuid.UUID`.

## Design-Entscheidungen

| Frage | Entscheidung |
|-------|--------------|
| Rückgabetyp | Immer eine Liste (`list[uuid.UUID]`), leere Liste wenn nichts gefunden |
| ID-Format | `uuid.UUID`-Objekte (identisch zu `app_get_id`) |
| Methodenname | `stream_get_id` |
| Zweiter Parameter | Keiner (kein natürliches Analog zum `stream_name`-Filter von `app_get_id`) |
| Tests | Nur Beispielskript (Repo-Konvention), keine committeten Unit-Tests |
| Query-Strategie | Serverseitiger QRS-Filter über `/qrs/stream/full` |

## API

```python
def stream_get_id(self, stream_name: str) -> list[uuid.UUID]:
```

- `stream_name` (str, Pflicht): Name des gesuchten Streams.
- **Rückgabe:** `list[uuid.UUID]` – die IDs aller passenden Streams. Leere Liste,
  wenn kein Stream passt oder der Request fehlschlägt.

## Verhalten / Datenfluss

1. Filterstring: `name eq '<stream_name>'`
2. Aufruf `self.get(endpoint="/qrs/stream/full", params={"filter": <filterstring>})`.
   Folgt exakt dem Muster von `app_get_id` (serverseitige Filterung). Der
   Stream-Endpoint `/qrs/stream` ist in Qlik Sense Standard (vgl. Alt-Client
   `qrs_bak.py`).
3. Aus jedem Treffer das Feld `id` lesen und in `uuid.UUID` umwandeln.
4. Liste der `uuid.UUID` zurückgeben.

## Fehler- und Randfälle

- **Kein Treffer:** leere Liste `[]` + `logger.warning`, dass kein Stream mit dem
  Namen gefunden wurde.
- **Request-Fehler** (`self.get` liefert `None`): ebenfalls `[]`. Der HTTP-Fehler
  wird bereits in `_request` geloggt. Rückgabetyp bleibt stabil eine Liste.
- **Matching:** über den serverseitigen `eq`-Filter (QRS-Standardverhalten).
- **Namen mit einfachem Anführungszeichen (`'`):** werden – konsistent mit dem
  restlichen Code – nicht escaped. Bekannte, akzeptierte Einschränkung.

## Beispielskript

`examples/stream_get_id.py`, analog zu `examples/app_get_id.py`:
Cert-Auth aufsetzen, `client.stream_get_id(stream_name=...)` aufrufen und das
Ergebnis ausgeben.

## Out of Scope

- Unit-Tests / Test-Infrastruktur.
- Escaping von Sonderzeichen in Filterwerten.
- Suche über andere Felder als den Stream-Namen.
