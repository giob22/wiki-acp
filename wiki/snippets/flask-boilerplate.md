---
tipo: snippet
tecnologia: flask
linguaggio: python
---

#flashcards/acp

# Boilerplate — Flask (REST API)

Web service RESTful minimo + CRUD completo + gestione errori + client `requests`. → [[rest]] [[flask]]

## Setup

```bash
pip install flask requests
```

## App CRUD completa — `app.py`

```python
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# storage in memoria (nelle prove spesso sostituito da MongoDB → [[mongodb-pymongo]])
users = {}
next_id = 1


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(users.values()))


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        abort(404, description="utente non trovato")
    return jsonify(user)


@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.get_json()                # corpo JSON → dict
    if not data or "nome" not in data:
        abort(400, description="campo 'nome' obbligatorio")

    user = {"id": next_id, **data}
    users[next_id] = user
    next_id += 1
    return jsonify(user), 201           # 201 Created


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        abort(404)
    users[user_id].update(request.json)
    return jsonify(users[user_id])


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        abort(404)
    del users[user_id]
    return "", 204                      # 204 No Content


# handler errori uniformi in JSON
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e.description)}), 404


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": str(e.description)}), 400


if __name__ == "__main__":
    app.run(debug=True)                 # default: localhost:5000
```

## `abort` — uso corretto

`abort(code)` solleva una `HTTPException` e **interrompe subito** la view: nessun `return` dopo, il codice a valle non viene eseguito. → [[gestione-errori-api]]

```python
from flask import abort

abort(404)                                  # solo codice → messaggio default werkzeug
abort(400, description="campo 'nome' obbligatorio")   # codice + messaggio custom
```

**Regole d'oro:**
1. **Valida presto, esci subito** (guard clause): controlla input/risorsa all'inizio e `abort` prima di toccare lo storage.
2. **Usa solo codici HTTP standard** registrati in werkzeug (400, 401, 403, 404, 405, 409, 415, 500...). Un codice inventato (e.g. `abort(299)`) solleva `LookupError`.
3. **Accoppia sempre con `@app.errorhandler`** per restituire JSON uniforme invece dell'HTML di default.
4. **NON passare un dict a `abort`** (`abort({"error": "x"})` non funziona): per un body JSON personalizzato usa `make_response`.

```python
# guard clause: niente nesting, esce al primo errore
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if not request.is_json:
        abort(415, description="serve Content-Type: application/json")
    if user_id not in users:
        abort(404, description="utente non trovato")
    data = request.get_json()
    if "nome" not in data:
        abort(400, description="campo 'nome' obbligatorio")

    users[user_id].update(data)             # eseguito solo se tutto valido
    return jsonify(users[user_id])
```

```python
# body JSON custom (oltre description): abort con Response esplicita
from flask import make_response, jsonify

resp = make_response(jsonify(error="conflitto", id=user_id), 409)
abort(resp)
```

**Codici tipici nelle prove:**

| Situazione | Codice | abort |
|---|---|---|
| Payload mancante/malformato | 400 Bad Request | `abort(400, description=...)` |
| Risorsa inesistente | 404 Not Found | `abort(404)` |
| Content-Type sbagliato (non JSON) | 415 Unsupported Media Type | `abort(415)` |
| Risorsa già esistente / duplicato | 409 Conflict | `abort(409)` |

> 🎯 Esame: `abort` solleva `HTTPException` (sottoclasse) → catturabile da `@app.errorhandler(code)` **o** da `@app.errorhandler(HTTPException)` per un handler unico. `description` è accessibile via `e.description` nell'handler.

Cosa solleva abort() in Flask e chi lo cattura?
?
Solleva HTTPException (sottoclasse) → catturabile da @app.errorhandler(code) o @app.errorhandler(HTTPException). Il messaggio è in e.description nell'handler.


```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)             # un solo handler per tutti gli abort
def handle_http(e):
    return jsonify({"error": e.description}), e.code
```

## Request object — cheat sheet

```python
request.method      # 'GET', 'POST', ...
request.json        # corpo JSON (dict) — None se non JSON
request.args        # query string: /search?q=x → request.args.get("q")
request.form        # form data
request.headers     # header HTTP
```

## Response — cheat sheet

```python
return jsonify(data)                   # 200 OK
return jsonify(data), 201              # 201 Created
return "", 204                         # 204 No Content
abort(404, description="msg")          # solleva HTTPException
```

## Client — libreria `requests`

```python
import requests

BASE = "http://localhost:5000"

# GET
r = requests.get(f"{BASE}/users/1")
print(r.status_code)        # 200
print(r.json())             # dict dalla risposta JSON

# POST
r = requests.post(f"{BASE}/users", json={"nome": "Bob"})

try: 
	r.raise_for_status()
except requests.exceptions.HTTPError as e:
	print("Errore cazzo ",e)
	


# PUT / DELETE
requests.put(f"{BASE}/users/1", json={"nome": "Alice"})
requests.delete(f"{BASE}/users/1")
```

> 🎯 Esame: mapping CRUD ↔ metodi HTTP (POST=create 201, GET=read, PUT=update, DELETE=delete 204), route dinamiche `<int:id>`, safe/idempotente → [[rest]]. Status code corretti spesso valutati nelle prove.

Mapping CRUD ↔ metodi HTTP con status code tipici?
?
POST=create (201), GET=read, PUT=update, DELETE=delete (204). Route dinamiche con <int:id>. GET safe/idempotente, PUT/DELETE idempotenti, POST no.


## Collegamenti

- [[flask]] — pagina entità
- [[rest]] — risorse, URI, interfaccia uniforme
- [[gestione-errori-api]] — abort, errorhandler, mapping eccezioni→status
- [[mongodb-pymongo]] — backend tipico delle prove (Flask + MongoDB)

## Fonti

- [[16-python-flask]], svolgimenti sim-01 e sim-04

_Aggiornato: 2026-06-15 — aggiunta sezione "abort — uso corretto" (guard clause, codici standard, errorhandler unico, make_response)_
