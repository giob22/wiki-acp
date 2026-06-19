---
tipo: snippet
tecnologia: mongodb
linguaggio: python
---

# Boilerplate — MongoDB (PyMongo)

Driver Python per MongoDB: connessione, CRUD, operazioni atomiche, integrazione Flask. → [[nosql]] [[mongodb]]

## Setup

```bash
pip install pymongo
# server: mongod (default localhost:27017)
```

## Connessione + CRUD

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mio_database"]
collection = db["utenti"]

# INSERT
result = collection.insert_one({"nome": "Alice", "età": 30})
print(result.inserted_id)                  # ObjectId autogenerato
collection.insert_many([{"nome": "Bob"}, {"nome": "Carl"}])

# FIND
utente = collection.find_one({"nome": "Alice"})      # dict o None
for u in collection.find({"età": {"$gt": 25}}):      # cursor iterabile
    print(u)

# UPDATE
collection.update_one(
    {"nome": "Alice"},                     # filtro
    {"$set": {"età": 31}}                  # modificatore
)
collection.update_many({"attivo": False}, {"$set": {"archiviato": True}})

# DELETE
collection.delete_one({"nome": "Alice"})
collection.delete_many({"età": {"$lt": 18}})
```

## Operatori frequenti

```python
# filtro (lettura)
{"età": {"$gte": 18, "$lt": 65}}                  # range
{"ruolo": {"$in": ["admin", "mod"]}}              # appartenenza
{"$or": [{"età": {"$lt": 18}}, {"vip": True}]}    # logici
{"email": {"$exists": True}}                      # presenza campo

# update (scrittura)
{"$set": {"nome": "Bob"}, "$inc": {"login_count": 1}}
{"$push": {"tags": "python"}}
{"$addToSet": {"tags": "mongodb"}}                # no duplicati

{"$set": {"eta": {"$max": [432, "$eta"]}}
```

Tabella completa → [[mongodb]].

## Operazione atomica — `find_one_and_update`

`find_one()` + `update_one()` separati = race condition (TOCTOU). Versione atomica lato server:

```python
from pymongo import ReturnDocument

doc = collection.find_one_and_update(
    {"_id": "contatore_visite"},
    {"$inc": {"valore": 1}},
    upsert=True,                          # crea se non esiste
    return_document=ReturnDocument.AFTER  # doc DOPO l'update
)
print(doc["valore"])    # corretto anche con N client concorrenti
```

## Gestione errori

```python
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError

try:
    client = MongoClient("mongodb://localhost:27017/",
                         serverSelectionTimeoutMS=3000)
    client.admin.command("ping")          # forza verifica connessione
except ConnectionFailure:
    print("MongoDB non raggiungibile")

try:
    collection.insert_one(doc)
except DuplicateKeyError:
    ...   # _id già esistente → in Flask: abort(409)
except PyMongoError as e:
    ...   # errore generico → abort(500)
```

Mapping eccezioni → status HTTP → [[gestione-errori-api]].

## Pattern da prova: Flask + MongoDB

```python
from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
collection = MongoClient("mongodb://localhost:27017/")["acp"]["readings"]


@app.route("/readings", methods=["POST"])
def add_reading():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route("/readings/<location>", methods=["GET"])
def get_readings(location):
    # _id (ObjectId) non è serializzabile in JSON: escluderlo o convertirlo
    docs = list(collection.find({"location": location}, {"_id": 0}))
    if not docs:
        abort(404)
    return jsonify(docs)
```

> ⚠️ `ObjectId` non è JSON-serializzabile: `jsonify` fallisce se il documento contiene `_id`. Soluzioni: projection `{"_id": 0}` oppure `str(doc["_id"])`.

> 🎯 Esame: perché `find_one`+`update_one` separati sono sbagliati sotto concorrenza e come `find_one_and_update` delega l'atomicità al DBMS → [[mongodb]].

## Collegamenti

- [[mongodb]] — pagina entità: operatori completi, schema decisionale
- [[nosql]] — document-store, SQL vs NoSQL
- [[gestione-errori-api]] — eccezioni PyMongo → status HTTP
- [[flask-boilerplate]] — l'API REST davanti al DB

## Fonti

- [[17-nosql-databases]], svolgimento sim-01 (`svolgimenti/2026-06-08-sim-01/database.py`)

_Aggiornato: 2026-06-12 — creazione raccolta snippet_
