---
tipo: concetto
importanza_esame: alta
prerequisiti: [strutture-dati, rest]
---

## Definizione

**NoSQL** (Not Only SQL) indica database non-relazionali che usano modelli di dati flessibili, senza schema fisso. Ottimizzati per grandi volumi di dati e scalabilità orizzontale, a scapito di alcune garanzie ACID.

## Spiegazione

**Database Relazionali (SQL)**:
- Schema fisso predefinito — ogni riga deve conformarsi al template
- Tabelle collegate da chiavi (relazioni)
- **ACID**: Atomicity, Consistency, Isolation, Durability
- Vantaggio: dati prevedibili, forte consistenza
- Svantaggio: difficile scalare orizzontalmente, schema rigido blocca big data e migrazione

**Database Non-Relazionali (NoSQL)**:
- Schema-free: documents possono variare liberamente
- Collections di documents (non tabelle di righe)
- Scalabilità orizzontale facile (distribuzione su nodi)
- Svantaggio: non si può assumere la presenza di un campo; aggiornamento dei dati più complesso

**Tipologie NoSQL**:

| Tipo | Struttura | Esempi | Uso |
|------|-----------|--------|-----|
| **Key-Value** | Coppie chiave→valore | Redis, DynamoDB | Cache, sessioni |
| **Document Store** | JSON documents annidati | MongoDB, Couchbase | Web app, cataloghi |
| **Column Store** | Colonne di dati | Cassandra, HBase | Analytics, time-series |
| **Graph** | Nodi e archi | Neo4j | Reti sociali, recommendation |
| **Search Engine** | Indice full-text | Elasticsearch, Solr | Ricerca testuale |

**SQL vs NoSQL — confronto sintetico**:

| | SQL (Relazionale) | NoSQL |
|---|---|---|
| Schema | Fisso | Flessibile |
| Scalabilità | Verticale (costosa) | Orizzontale (facile) |
| ACID | Garantito | BASE (Basically Available, Soft state, Eventual consistency) |
| Relazioni | Chiavi esterne | Documenti embedded / riferimenti |
| Query | SQL | API specifica (es. MongoDB Query Language) |

> 🎯 Esame: Differenza SQL/NoSQL in termini di schema, ACID, scalabilità; tipologie NoSQL con esempi.

## Perché importa

Le web application moderne usano frequentemente database NoSQL per scalabilità. Il corso usa MongoDB come esempio concreto.

## Connessioni

- [[rest]] — le API REST tipicamente accedono a database (spesso NoSQL) nel back-end
- [[strutture-dati]] — i documenti MongoDB sono rappresentati come dict Python

## Fonti

- [[17-nosql-databases]]

_Aggiornato: 2026-06-04 — ingest iniziale_
