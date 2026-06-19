---
tipo: entità
categoria: framework
---

## Cos'è

**Flask** è un micro-framework Python per lo sviluppo di web application e API RESTful. "Micro" significa che è leggero e minimalista — non include ORM o form validation di default, ma è altamente estendibile tramite extension.

## Come si usa nel corso

Flask è usato per implementare **web service RESTful** che espongono risorse via HTTP.

**Installazione**:
```bash
pip install flask
```

**App base**:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    utente = {"id": id, "nome": "Alice"}
    return jsonify(utente)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json  # corpo della richiesta JSON
    # processa data...
    return jsonify({"id": 1, **data}), 201

if __name__ == '__main__':
    app.run(debug=True)
```

**Routing**:
- `@app.route('/path')` — associa URL a funzione handler
- Route dinamiche: `<int:id>`, `<string:nome>`, `<float:val>`
- Metodi HTTP: `methods=['GET', 'POST', 'PUT', 'DELETE']`

**Request object**:
```python
request.method      # 'GET', 'POST', ...
request.args        # query string params: ?key=val
request.json        # corpo JSON (dict)
request.form        # form data
request.headers     # header HTTP
```

**Response**:
```python
return jsonify(data)                   # → JSON con 200 OK
return jsonify(data), 201              # → JSON con 201 Created
return jsonify({"error": "msg"}), 404  # → errore 404
```

**Client HTTP** (libreria `requests`):
```python
import requests
r = requests.get("http://localhost:5000/users/1")
r.json()           # → dict dalla risposta JSON
r.status_code      # → 200

r = requests.post("http://localhost:5000/users", json={"nome": "Bob"})
```

## Link ai concetti correlati

- [[rest]] — Flask implementa l'architettura REST
- [[strutture-dati]] — il JSON è gestito come dict Python
- [[nosql]] — Flask tipicamente accede a MongoDB (o altro DB) nel backend
- [[gestione-errori-api]] — eccezioni PyMongo, abort(), @app.errorhandler in Flask

## Fonti

- [[16-python-flask]]

_Aggiornato: 2026-06-06 — aggiunto link a gestione-errori-api_
