---
tipo: fonte
titolo: "NoSQL Database for Web Applications"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [nosql, mongodb, pymongo, database, dbms, sql, document-store, json, crud]
---

## Sommario

Slide su database NoSQL per web application (20+ pagine). Si introduce il concetto di database e DBMS, si confrontano database relazionali (SQL) e non-relazionali (NoSQL), si descrivono le tipologie NoSQL (key-value, document stores, search engines), e si tratta MongoDB come esempio di document-store con PyMongo come driver Python.

## Punti chiave

1. I database sono tipicamente usati nel **back-end** delle web application per persistenza dei dati
2. **Database**: collection di dati organizzati per accesso, gestione e aggiornamento facile
3. **DBMS**: software per creazione, definizione e manipolazione di database; fornisce protezione, sicurezza e consistenza
4. **Due categorie principali**:
   - **Relazionali (SQL)**: tabelle collegate, schema fisso, ACID-compliance
   - **Non-relazionali (NoSQL)**: flessibili, schema-free, scalabili orizzontalmente
5. **Database Relazionali**:
   - Usano **schema** fisso come template
   - Tabelle (Entità) in relazione tra loro tramite chiavi
   - **ACID**: Atomicity, Consistency, Isolation, Durability
   - Vantaggio: dati prevedibili, pochi errori
   - Svantaggio: difficile scalare orizzontalmente, schema rigido (problemi big data, migrazione)
6. **Database Non-Relazionali (NoSQL)**:
   - Schema-free: **collections** di **documents** senza schema predefinito
   - Facile gestione di grandi volumi; scalabilità orizzontale
   - Svantaggio: non si può fare affidamento sulla presenza di un campo; aggiornamento complesso
7. **Tipologie NoSQL**:
   - **Key-Value**: coppie chiave-valore (Amazon DynamoDB, Redis)
   - **Document Stores**: dizionari JSON innestati (Couchbase, **MongoDB**)
   - **Search Engines**: text-based search (Solr, Elasticsearch)
   - **Graph**: relazioni tra nodi (Neo4j)
8. **MongoDB** — document-oriented DBMS:
   - Documenti **JSON-like** (BSON internamente)
   - Gerarchia: **Database** → **Collection** → **Document** → **Field**
   - **Collection** ≈ tabella relazionale (ma senza schema fisso)
   - **Document** = record con campi nome-valore; ogni doc può essere diverso
   - **`_id`**: campo obbligatorio, chiave primaria, autogenerato se non specificato
   - **Cursor**: puntatore al risultato di una query; iterabile
   - **Embedded document**: un field ha come value un altro documento
9. Confronto Relazionale vs MongoDB: dati correlati in 4 tabelle separate → un singolo documento nidificato in MongoDB

## Concetti introdotti

- [[nosql]]
- [[mongodb]]

## Domande aperte

- Come si effettuano query complesse in MongoDB?
- Cos'è PyMongo esattamente? (probabilmente slide successive)

## Domande da esame

- Differenza tra database relazionale e NoSQL
- Cosa sono ACID? Perché i relazionali li garantiscono e i NoSQL no?
- Cos'è MongoDB? Descrivere la struttura Document/Collection/Database
- Cos'è `_id` in MongoDB?
- Tipologie di database NoSQL — esempi per ognuna
- Vantaggi e svantaggi dei database non-relazionali
