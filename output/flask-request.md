# Flask `request` — come funziona

## Cos'è

`flask.request` è un **context-local proxy** — non è un oggetto normale passato come parametro, ma un proxy che punta all'oggetto request del thread/contesto corrente.

```python
from flask import request
```

---

## Context Locals

Flask usa **Werkzeug's Local** sotto (ora `ContextVar` in Python 3.7+). Ogni richiesta HTTP crea un **request context** isolato:

```
HTTP request in → push RequestContext → request proxy punta a QUESTO oggetto
                                       ↓
                                  view function gira
                                       ↓
                               pop RequestContext
```

Quindi `request` è "magicamente" diverso per ogni thread/greenlet/asyncio task concorrente — nessuna race condition.

---

## Attributi principali

| Attributo | Tipo | Contenuto |
|---|---|---|
| `request.method` | `str` | `"GET"`, `"POST"`, ecc. |
| `request.args` | `ImmutableMultiDict` | Query string `?foo=bar` |
| `request.form` | `ImmutableMultiDict` | Body form-urlencoded o multipart |
| `request.json` | `dict \| None` | Body JSON (parsed) |
| `request.data` | `bytes` | Body grezzo |
| `request.files` | `ImmutableMultiDict` | File upload (`FileStorage` objects) |
| `request.headers` | `Headers` | Header HTTP |
| `request.cookies` | `dict` | Cookie |
| `request.url` | `str` | URL completo |
| `request.path` | `str` | Solo path, es. `/users/42` |
| `request.host` | `str` | `localhost:5000` |
| `request.remote_addr` | `str` | IP client |
| `request.environ` | `dict` | WSGI environ grezzo |

---

## `ImmutableMultiDict` — perché MultiDict?

HTTP permette valori multipli per la stessa chiave: `?tag=python&tag=flask`

```python
request.args.get("tag")        # → "python" (primo)
request.args.getlist("tag")    # → ["python", "flask"]
request.args["tag"]            # → "python"
```

`Immutable` = non modificabile — protegge da bug accidentali nella view.

---

## Parsing JSON

```python
# Content-Type: application/json obbligatorio, altrimenti ritorna None
data = request.json          # auto-parse, None se fallisce
data = request.get_json()    # più controllo:
data = request.get_json(force=True, silent=True)
#  force=True  → ignora Content-Type
#  silent=True → None invece di 400 se JSON malformato
```

---

## File upload

```python
f = request.files["avatar"]   # FileStorage object
f.filename                     # nome originale (NON trusted — sanifica!)
f.content_type                 # "image/png"
f.save("/path/to/dest")        # salva su disco
f.read()                       # bytes
```

Sicurezza: usa `werkzeug.utils.secure_filename(f.filename)` prima di salvare.

---

## Cycle di vita del request context

```python
# Flask fa questo internamente ad ogni request:
with app.test_request_context("/foo", method="POST"):
    # request è disponibile qui
    print(request.path)   # /foo
# fuori: RuntimeError — "working outside of request context"
```

Puoi usare `test_request_context` nei test o per debug.

---

## Sotto il cofano (stack semplificato)

```
WSGI server chiama app(environ, start_response)
    → Flask.__call__()
        → push RequestContext (lega request a ContextVar)
            → dispatch to view
                → view legge `request` proxy
                    → proxy legge ContextVar → oggetto reale
            → pop RequestContext
```

---

## Errori comuni

```python
# SBAGLIATO — fuori contesto
with app.app_context():
    print(request.method)  # RuntimeError! app_context ≠ request_context

# GIUSTO
with app.test_request_context():
    print(request.method)
```

```python
# request.json → None se Content-Type non è application/json
# usa get_json(force=True) se client non manda header corretto
```
