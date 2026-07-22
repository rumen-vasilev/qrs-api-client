# stream_get_id Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `QRSClient.stream_get_id` method that resolves a stream name to a list of stream IDs as `uuid.UUID` objects — the sibling of `app_get_id`.

**Architecture:** A single new high-level convenience method on `QRSClient` that builds a server-side QRS filter and calls the existing `self.get("/qrs/stream/full", ...)`. Directly analogous to `app_get_id`. A companion example script demonstrates usage.

**Tech Stack:** Python (stdlib `uuid`, `logging`), `requests` (indirectly via `self.get`). No new dependencies.

## Global Constraints

- Return type is always `list[uuid.UUID]` — empty list on no match **and** on request error. Copy verbatim: `def stream_get_id(self, stream_name: str) -> list[uuid.UUID]:`
- No second parameter (unlike `app_get_id`).
- IDs are returned as `uuid.UUID` objects (convert the API's string `id`).
- No new third-party dependencies; no committed tests. Verification is a throwaway red/green script, not committed.
- Filter values are **not** escaped for single quotes — consistent with the rest of the codebase.
- Follow existing style: English docstrings, module-level `logger`, 4-space indent.
- Use the project venv interpreter for verification: `./.venv/Scripts/python.exe` (the global `python` on PATH lacks `requests`).

---

### Task 1: Implement `stream_get_id` on `QRSClient`

**Files:**
- Modify: `qrs_api_client/client.py` — add the method immediately after `app_get_id` and before `app_get_custom_properties`.

**Interfaces:**
- Consumes: `self.get(endpoint: str, params: dict = None, ...)` (existing) — returns a `list[dict]` of stream objects, or `None` on request error. Module-level `logger`, `uuid` (both already available in `client.py`).
- Produces: `stream_get_id(self, stream_name: str) -> list[uuid.UUID]`.

- [ ] **Step 1: Write the failing verification (red)**

```bash
cd "C:/Users/R.Vasilev/PycharmProjects/qrs-api-client" && ./.venv/Scripts/python.exe - <<'PY'
import uuid
from qrs_api_client.client import QRSClient

c = QRSClient.__new__(QRSClient)

captured = {}
def fake_get(endpoint, params=None, **kwargs):
    captured['endpoint'] = endpoint
    captured['params'] = params
    return [{'id': '12345678-1234-1234-1234-1234567890ab'}]
c.get = fake_get

res = c.stream_get_id('Everyone')
assert captured['endpoint'] == '/qrs/stream/full', captured['endpoint']
assert captured['params'] == {'filter': "name eq 'Everyone'"}, captured['params']
assert res == [uuid.UUID('12345678-1234-1234-1234-1234567890ab')]
assert all(isinstance(x, uuid.UUID) for x in res)

c.get = lambda endpoint, params=None, **kwargs: []
assert c.stream_get_id('nope') == []

c.get = lambda endpoint, params=None, **kwargs: None
assert c.stream_get_id('nope') == []

print('OK')
PY
```

- [ ] **Step 2: Run it to verify it fails**

Expected: FAIL with `AttributeError: 'QRSClient' object has no attribute 'stream_get_id'`.

- [ ] **Step 3: Write the implementation**

Insert into `qrs_api_client/client.py` immediately after the `app_get_id` method (after its `return [uuid.UUID(app["id"]) for app in apps]` line) and before `def app_get_custom_properties`:

```python
    def stream_get_id(self, stream_name: str) -> list[uuid.UUID]:
        """
        Resolves a stream name to the IDs of all streams with that name.

        The output format matches app_get_id: this method always returns a
        list of uuid.UUID. Stream names are normally unique in Qlik Sense,
        but a list is used for a consistent return type and to cover the
        theoretical case of duplicate names.

        The lookup uses the server-side QRS filter on /qrs/stream/full,
        mirroring app_get_id.

        Args:
            stream_name (str): The name of the stream(s) to look up.

        Returns:
            list[uuid.UUID]: The IDs of all matching streams. An empty list
                if no stream matches or the request fails.

        Examples:
            >>> client.stream_get_id("Everyone")
            [UUID('12345678-1234-1234-1234-1234567890ab')]

            >>> client.stream_get_id("Does not exist")
            []
        """
        _filter = f"name eq '{stream_name}'"

        streams = self.get(endpoint="/qrs/stream/full", params={"filter": _filter})

        # self.get returns None on a request error; treat it like "no matches"
        # so the return type stays a stable list.
        if not streams:
            logger.warning("No stream named \"%s\" found.", stream_name)
            return []

        return [uuid.UUID(stream["id"]) for stream in streams]
```

- [ ] **Step 4: Run the verification to confirm it passes (green)**

Run the exact same command from Step 1. Expected: prints `OK`, exit 0.

- [ ] **Step 5: Commit (method only)**

```bash
cd "C:/Users/R.Vasilev/PycharmProjects/qrs-api-client" && git add qrs_api_client/client.py && git commit -m "feat: add stream_get_id to resolve stream name to stream IDs

Adds QRSClient.stream_get_id(stream_name) -> list[uuid.UUID], the sibling
of app_get_id. Uses a server-side QRS filter on /qrs/stream/full. Always
returns a list (empty on no match or request error).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Add the example script

**Files:**
- Create: `examples/stream_get_id.py`

**Interfaces:**
- Consumes: `QRSClient.stream_get_id(stream_name)` from Task 1; `QRSClient`, `AuthManager` (existing).
- Produces: nothing consumed by later tasks (leaf).

- [ ] **Step 1: Create `examples/stream_get_id.py`**

```python
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

stream_name = "<stream_name>"

# Looks up the IDs of all streams with this name
result = client.stream_get_id(stream_name=stream_name)

if result:
    print(f"Found {len(result)} stream(s) named '{stream_name}':")
    for stream_id in result:
        print(" -", stream_id)
else:
    print(f"No stream named '{stream_name}' found.")
```

- [ ] **Step 2: Verify the example compiles**

```bash
cd "C:/Users/R.Vasilev/PycharmProjects/qrs-api-client" && ./.venv/Scripts/python.exe -m py_compile examples/stream_get_id.py && echo COMPILE_OK
```

Expected: prints `COMPILE_OK`, exit 0. The script is not executed (needs a live server and real certificates).

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/R.Vasilev/PycharmProjects/qrs-api-client" && git add examples/stream_get_id.py && git commit -m "docs: add example script for stream_get_id

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review

**1. Spec coverage:**
- New method resolving stream name -> stream ID(s): Task 1. ✅
- Output in same format as app IDs (`list[uuid.UUID]`, always a list): Task 1. ✅
- No second parameter: Task 1 signature. ✅
- Empty list on no match and on request error: Task 1 (`if not streams:` covers `[]` and `None`). ✅
- Example script only, no committed tests: Task 2; verification in Task 1 is throwaway. ✅
- Server-side `/qrs/stream/full` filter strategy: Task 1. ✅

**2. Placeholder scan:** No TBD/TODO/vague steps. The `<...>` tokens in the example are intentional user-supplied placeholders matching the other `examples/` files. ✅

**3. Type consistency:** Method name `stream_get_id` and signature `(self, stream_name: str) -> list[uuid.UUID]` are identical across header, Global Constraints, Task 1 interface/implementation, and Task 2 usage. Endpoint `/qrs/stream/full` and filter `name eq '<stream_name>'` match between verification and implementation. ✅
