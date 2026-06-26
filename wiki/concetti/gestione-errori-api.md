---
tipo: concetto
importanza_esame: alta
prerequisiti: [eccezioni, flask, mongodb, grpc, rest]
---

#flashcards/acp

## Definizione

La **gestione degli errori in API distribuite** è il processo di tradurre eccezioni interne (driver DB, validazione, logica applicativa) in segnali d'errore **coerenti e standardizzati** verso il client — status HTTP nel caso REST/Flask, `grpc.StatusCode` nel caso gRPC. Una buona gestione mappa ogni categoria di eccezione a un codice ben preciso, invece di far trapelare stack trace o errori generici 500.

## Spiegazione

### A. Flask + MongoDB — eccezioni PyMongo e mapping status HTTP

Eccezioni del modulo `pymongo.errors` (tutte sottoclassi di `PyMongoError`) e status HTTP consigliato:

| Eccezione | Causa | Status HTTP |
|---|---|---|
| `ConnectionFailure` | connessione al DB persa | 503 |
| `ServerSelectionTimeoutError` | DB irraggiungibile, timeout selezione server | 503 |
| `DuplicateKeyError` | violazione unique index (es. `_id` duplicato) | 409 |
| `WriteError` / `WriteConcernError` | scrittura rifiutata (validazione schema, write concern) | 400 / 500 |
| `OperationFailure` | comando/query fallita lato server | 500 |
| `InvalidOperation` | operazione non valida su collection/cursor | 500 |
| `bson.errors.InvalidId` | `ObjectId(stringa)` con stringa malformata | 400 |
| `PyMongoError` | classe base — catch-all | 500 |

Più alcune eccezioni Python generiche tipiche su input malformato:

| Eccezione | Causa | Status |
|---|---|---|
| `KeyError` | campo mancante in `request.json` | 400 |
| `TypeError` / `ValueError` | tipo o valore non valido nei dati ricevuti | 400 |
| `find_one` → `None` | risorsa non esiste (non è un'eccezione, va controllata esplicitamente) | 404 |

**Pattern completo**:
```python
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError, PyMongoError

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        oid = ObjectId(id)
    except InvalidId:
        return jsonify({"error": "id malformato"}), 400

    utente = collection.find_one({"_id": oid})
    if utente is None:
        return jsonify({"error": "non trovato"}), 404
    utente["_id"] = str(utente["_id"])
    return jsonify(utente), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        nome = data["nome"]
    except (KeyError, TypeError):
        return jsonify({"error": "campo 'nome' obbligatorio"}), 400
    try:
        result = collection.insert_one({"nome": nome})
        return jsonify({"id": str(result.inserted_id)}), 201
    except DuplicateKeyError:
        return jsonify({"error": "duplicato"}), 409
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500
```

### B. Flask — `abort()` e `@app.errorhandler`: come funzionano davvero

Punto chiave: `@app.errorhandler` **non** scatta quando una view *ritorna* uno status code (`return jsonify(...), 404` è solo una risposta normale, nessuna eccezione coinvolta). Scatta solo quando viene **lanciata un'eccezione** che corrisponde a quanto registrato — sia lanciata esplicitamente con `abort()`, sia sollevata internamente da Flask (es. nessuna route corrisponde all'URL → Flask solleva `werkzeug.exceptions.NotFound`, code 404).

```python
from flask import abort

@app.route('/users/<id>')
def get_user(id):
    utente = collection.find_one({"_id": ObjectId(id)})
    if utente is None:
        abort(404)   # solleva werkzeug.exceptions.NotFound (HTTPException, code=404)
    return jsonify(utente)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "risorsa non trovata"}), 404
```

Flusso: `abort(404)` solleva `NotFound` → Flask intercetta l'eccezione mentre risale lo stack → cerca un handler registrato per quel code/classe → esegue `not_found(e)` e usa il suo *return value* come risposta finale.

Si può registrare anche su classi di eccezione arbitrarie, non solo su status code:
```python
@app.errorhandler(PyMongoError)
def mongo_error(e):
    return jsonify({"error": "errore database"}), 500
```
Qui ogni `PyMongoError` (o sottoclasse, es. `DuplicateKeyError`) sollevata in una view e **non catturata** viene intercettata da Flask prima di diventare una pagina 500 generica, e gestita da questo handler.

**Regole di lookup**:
- match esatto sulla classe dell'eccezione, poi risalita della MRO verso le superclassi → registrare su `Exception` cattura tutto il non gestito
- `@app.errorhandler(404)` fa match su `HTTPException` con quel `code` — scatta sia per `abort(404)` esplicito sia per i 404/405/ecc. generati internamente da Flask
- **non** scatta per eccezioni già gestite con try/except dentro la view (non propagano più)
- **non** scatta per `return ..., 404` (nessuna eccezione coinvolta)

> 🎯 Esame: distinguere "ritornare uno status" da "lanciare un'eccezione che produce quello status" — è la chiave per capire quando un errorhandler si attiva.

Quando scatta un @app.errorhandler in Flask?
?
Solo quando viene LANCIATA un'eccezione corrispondente (abort() o eccezione interna). NON scatta su `return jsonify(...), 404` (è una risposta normale, nessuna eccezione).


### C. gRPC — gestione errori via `context`

`context` (`grpc.ServicerContext`) è passato a ogni metodo servicer e sostituisce il meccanismo HTTP-status di REST:

| Metodo | Effetto |
|---|---|
| `context.set_code(grpc.StatusCode.X)` | imposta il code — **non** termina l'handler |
| `context.set_details("msg")` | imposta il messaggio d'errore |
| `context.abort(code, details)` | imposta code+details **e lancia un'eccezione** → termina subito l'handler |
| `context.abort_with_status(status)` | come `abort`, con oggetto `grpc.Status` (per dettagli ricchi) |
| `context.set_trailing_metadata([...])` | metadata extra nella risposta |
| `context.is_active()` | controlla se l'RPC è ancora attiva |
| `context.add_callback(fn)` | callback a terminazione RPC |

`grpc.StatusCode` — i più usati e l'equivalente REST corrispondente:

| StatusCode | ~Equivalente HTTP | Uso tipico |
|---|---|---|
| `INVALID_ARGUMENT` | 400 | input malformato/mancante |
| `NOT_FOUND` | 404 | risorsa assente |
| `ALREADY_EXISTS` | 409 | duplicato |
| `UNAUTHENTICATED` | 401 | credenziali mancanti/invalide |
| `PERMISSION_DENIED` | 403 | autorizzazione negata |
| `FAILED_PRECONDITION` | 400/412 | stato del sistema non valido per l'operazione |
| `RESOURCE_EXHAUSTED` | 429 | quota / rate-limit |
| `DEADLINE_EXCEEDED` | 504 | timeout |
| `UNAVAILABLE` | 503 | servizio/DB irraggiungibile |
| `UNIMPLEMENTED` | 501 | metodo non implementato |
| `INTERNAL` | 500 | errore interno generico |
| `OK` | 200 | successo (default implicito) |

**Pattern server**, stesso scenario MongoDB:
```python
import grpc
from pymongo.errors import DuplicateKeyError, PyMongoError
from bson.errors import InvalidId
from bson import ObjectId

class UtentiServicer(utenti_pb2_grpc.UtentiServicer):
    def GetUser(self, request, context):
        try:
            oid = ObjectId(request.id)
        except InvalidId:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id malformato")
            # riga sotto MAI eseguita: abort lancia un'eccezione interna

        utente = collection.find_one({"_id": oid})
        if utente is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"utente {request.id} non trovato")

        return utenti_pb2.UserResponse(id=str(utente["_id"]), nome=utente["nome"])

    def CreateUser(self, request, context):
        if not request.nome:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("campo 'nome' obbligatorio")
            return utenti_pb2.UserResponse()   # set_code non interrompe: serve return esplicito

        try:
            result = collection.insert_one({"nome": request.nome})
        except DuplicateKeyError:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "utente già esistente")
        except PyMongoError as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

        return utenti_pb2.UserResponse(id=str(result.inserted_id), nome=request.nome)
```

**Lato client**:
```python
try:
    risposta = stub.GetUser(utenti_pb2.UserRequest(id="abc"))
except grpc.RpcError as e:
    print(e.code())      # → grpc.StatusCode.NOT_FOUND
    print(e.details())   # → "utente abc non trovato"
```

**Differenza chiave** `abort()` vs `set_code`+`set_details`:
- `abort()` → lancia un'eccezione interna, **interrompe subito** l'esecuzione (analogo a `raise`)
- `set_code` + `set_details` → **non interrompe**: serve un `return` esplicito dopo (una response vuota va bene, gRPC la scarta perché il code non è `OK`)

> 🎯 Esame: i metodi di `context` per segnalare errori, il significato dei principali `StatusCode`, e come un client gRPC li intercetta (`grpc.RpcError`, `.code()`, `.details()`).

Come segnala un errore un servicer gRPC e come lo intercetta il client?
?
Server: context.set_code/set_details (non interrompe) o context.abort(code, details) (lancia e interrompe). Client: cattura grpc.RpcError e legge e.code() / e.details().


## Perché importa

Ogni servizio del corso (Flask+MongoDB e gRPC) prevede scenari d'errore — input invalido, risorsa assente, conflitti, DB irraggiungibile. Una gestione coerente è ciò che distingue un prototipo da un servizio production-ready, ed è materia tipica di domande pratiche/esercizi all'esame.

## Connessioni

- [[eccezioni]] — meccanismo try/except/raise alla base di tutta la gestione errori
- [[flask]] — `abort()`, `@app.errorhandler`, `jsonify(..., status)`
- [[mongodb]] — eccezioni `pymongo.errors` da intercettare e tradurre
- [[grpc]] — `context`, `StatusCode`, differenza dal modello REST basato su status HTTP
- [[rest]] — semantica safe/idempotente guida quale status aspettarsi su quale verbo (es. POST non idempotente → 409 su duplicato)
- [[nosql]] — MongoDB rinuncia a parte delle garanzie ACID: gli errori di scrittura (`WriteError`, `DuplicateKeyError`) sono conseguenza diretta di questo trade-off

> 💡 Connessione: la tabella `StatusCode ↔ HTTP` è utile per chi progetta sistemi ibridi REST+gRPC che devono restituire semantiche d'errore equivalenti su entrambe le interfacce.

## Fonti

- [[16-python-flask]]
- [[17-nosql-databases]]
- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-06 — pagina creata da sintesi di una sessione di query su gestione errori Flask/MongoDB/gRPC_
