---
tipo: entità
categoria: framework
---

## Cos'è

**MongoDB** è un DBMS document-oriented open-source. Memorizza i dati come **documenti JSON-like** (internamente BSON) in **collections**. Schema-free: ogni documento può avere campi diversi.

## Come si usa nel corso

MongoDB è usato come database NoSQL per le web application Flask del corso.

**Gerarchia dati**:
```
MongoDB Instance
└── Database
    └── Collection  (≈ tabella relazionale, ma senza schema)
        └── Document (≈ riga, ma JSON annidato)
            └── Field (coppia nome: valore)
```

**Concetti chiave**:
- **Document**: oggetto JSON-like, primary key = campo `_id` (autogenerato se assente)
- **Collection**: gruppo di documenti — equivalente a una tabella SQL ma senza schema fisso
- **Embedded document**: un campo il cui valore è un altro documento (vs JOIN in SQL)
- **Cursor**: puntatore al risultato di una query — iterabile

**Esempio documento MongoDB**:
```json
{
    "_id": "ObjectId(...)",
    "nome": "Alice",
    "età": 30,
    "indirizzo": {
        "via": "Via Roma 1",
        "città": "Napoli"
    },
    "interessi": ["Python", "MongoDB"]
}
```

## PyMongo — driver Python

```python
from pymongo import MongoClient

# Connessione
client = MongoClient("mongodb://localhost:27017/")
db = client["mio_database"]
collection = db["utenti"]

# INSERT
doc = {"nome": "Alice", "età": 30}
result = collection.insert_one(doc)
print(result.inserted_id)   # → ObjectId

collection.insert_many([doc1, doc2])

# FIND
utente = collection.find_one({"nome": "Alice"})  # → dict o None
cursore = collection.find({"età": {"$gt": 25}})  # → cursor
for u in cursore:
    print(u)

# UPDATE
collection.update_one(
    {"nome": "Alice"},             # filtro
    {"$set": {"età": 31}}          # aggiornamento
)

# DELETE
collection.delete_one({"nome": "Alice"})
collection.delete_many({"età": {"$lt": 18}})
```

## Schema query — operatori, modificatori, atomicità

Tre livelli da distinguere: operatori di **filtro** (selezionano documenti), operatori di **update** (modificano campi), ed **esecuzione atomica** (demandata al DBMS).

### Operatori di filtro/selezione (in `find`, `find_one`, filtro di update/delete)

| Categoria | Operatori | Esempio |
|---|---|---|
| Confronto | `$eq` `$ne` `$gt` `$gte` `$lt` `$lte` | `{"età": {"$gte": 18, "$lt": 65}}` |
| Appartenenza | `$in` `$nin` | `{"ruolo": {"$in": ["admin","mod"]}}` |
| Logici | `$and` `$or` `$not` `$nor` | `{"$or": [{"età": {"$lt": 18}}, {"vip": true}]}` |
| Elemento | `$exists` `$type` | `{"email": {"$exists": true}}` |
| Valutazione | `$regex` `$expr` `$mod` `$text` | `{"nome": {"$regex": "^A", "$options": "i"}}` |
| Array | `$all` `$elemMatch` `$size` | `{"tags": {"$all": ["py","db"]}}` |

Campi top-level uniti in AND implicito: `{"a": 1, "b": 2}` ≡ `{"$and": [{"a":1},{"b":2}]}`. `$elemMatch` serve quando un **singolo** elemento di un array deve soddisfare più condizioni insieme (senza, i criteri possono matchare elementi diversi dell'array).

### Operatori di update / "modificatori" (secondo argomento di `update_*` / `find_one_and_update`)

| Categoria | Operatori | Effetto |
|---|---|---|
| Campo | `$set` `$unset` `$rename` `$setOnInsert` | imposta/rimuove/rinomina (`$setOnInsert`: solo se upsert crea un nuovo doc) |
| Numerico | `$inc` `$mul` `$min` `$max` | incrementa/moltiplica/clampa — atomico lato server |
| Array | `$push` `$pop` `$pull` `$pullAll` `$addToSet` | aggiunge/rimuove elementi |
| Modificatori di `$push` | `$each` `$slice` `$sort` `$position` | push multiplo + troncamento + ordinamento |

```python
collection.update_one({"_id": uid}, {"$set": {"nome": "Bob"}, "$inc": {"login_count": 1}})
collection.update_one({"_id": uid}, {"$push": {"tags": {"$each": ["py","grpc"], "$slice": -10}}})
collection.update_one({"_id": uid}, {"$addToSet": {"tags": "mongodb"}})  # niente duplicati
```

> ⚠️ Stesso simbolo `$` in contesti diversi: `{"$gt": 5}` filtra (lettura), `{"$inc": 1}` modifica (scrittura) — non confonderli.

### Operazioni atomiche — `find_one_and_*`

`find_one()` seguito da `update_one()` separati introduce una **race condition** (TOCTOU, time-of-check-to-time-of-use): tra le due chiamate un altro client può modificare il documento, e la scrittura successiva sovrascrive perdendo quel cambiamento — stesso problema delle race condition multi-thread, → [[threading]] [[gil]].

`find_one_and_update` / `find_one_and_replace` / `find_one_and_delete` eseguono lettura+scrittura come **un'unica operazione atomica lato server** — il DBMS garantisce l'atomicità (lock a livello documento), nessuna sincronizzazione applicativa necessaria.

```python
from pymongo import ReturnDocument

# contatore atomico — pattern classico
doc = collection.find_one_and_update(
    {"_id": "contatore_visite"},
    {"$inc": {"valore": 1}},
    upsert=True,                          # crea se non esiste
    return_document=ReturnDocument.AFTER  # doc DOPO l'update (default: BEFORE)
)
print(doc["valore"])  # corretto anche con N client concorrenti
```

Parametri chiave: `filter`, `update`/`replacement`, `upsert`, `return_document` (`ReturnDocument.BEFORE` | `AFTER`), `sort` (su quale documento operare se il filtro ne matcha più d'uno), `projection`.

> 💡 Connessione: stesso principio di `Lock` in [[threading]] — invece di sincronizzare il client con lock applicativi, si **demanda l'atomicità al DBMS**, che la implementa nello storage engine.

### Schema decisionale — quale operazione usare

| Scenario | Operazione |
|---|---|
| Solo lettura | `find` / `find_one` |
| Scrittura, non serve il documento risultante | `update_one` / `update_many` / `delete_one` |
| Devi leggere E modificare come unità atomica (contatore, coda, lock distribuito) | `find_one_and_update` |
| Batch di operazioni eterogenee (insert+update+delete insieme) | `bulk_write` |
| Più documenti/collection devono cambiare insieme con garanzie ACID | sessioni + `start_transaction()` (MongoDB ≥4.0, replica set) |

> 🎯 Esame: perché `find_one`+`update_one` separati sono sbagliati sotto concorrenza, e come `find_one_and_update` risolve il problema delegando l'atomicità al DBMS.

## Link ai concetti correlati

- [[nosql]] — MongoDB è un database NoSQL document-store
- [[strutture-dati]] — i documenti MongoDB sono dict Python in PyMongo
- [[rest]] — MongoDB tipicamente esposto via API REST con Flask
- [[threading]] — race condition read-modify-write risolte da `find_one_and_update` (atomicità demandata al DBMS)
- [[gestione-errori-api]] — eccezioni `pymongo.errors` da intercettare e tradurre in status HTTP/gRPC

## Fonti

- [[17-nosql-databases]]

_Aggiornato: 2026-06-06 — espansa sezione query con operatori filtro/update completi, find_one_and_update e schema decisionale_
