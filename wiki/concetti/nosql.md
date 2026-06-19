---
tipo: concetto
importanza_esame: alta
prerequisiti: [strutture-dati, rest]
---

## Definizione

**NoSQL** (Not Only SQL) indica database non-relazionali che usano modelli di dati flessibili, senza schema fisso. Ottimizzati per grandi volumi di dati e scalabilità orizzontale, a scapito di alcune garanzie ACID.

## Spiegazione

### Database, DBMS e ruolo nel web

- **Database**: *collection* di dati organizzati per essere facilmente acceduti, gestiti e aggiornati.
- **DBMS (Database Management System)**: software che permette creazione, definizione e manipolazione di un database; offre interfaccia/tool per memorizzare, processare e analizzare i dati, oltre a **protezione/sicurezza** e **consistenza** con utenti multipli. Esempi: MySQL, Oracle, SQL Server, IBM DB2, PostgreSQL.

**Features tipiche di un DBMS**: dati in tabelle, riduzione ridondanza via **normalizzazione**, **data consistency**, supporto **multi-utente/accesso concorrente**, **query language**, **security**, **supporto alle transazioni**.

> 💡 Nelle web app i database stanno nel **back-end**, usati dai web server: forniscono **persistenza** (i dati sopravvivono al crash del server), **riducono il carico** sulla memoria centrale, e servono le richieste che leggono/scrivono dati → [[rest]] [[flask]].

I database si dividono in due categorie: **Relazionali** (SQL) e **Non-relazionali** (NoSQL); un'organizzazione può usarli singolarmente o in combinazione, in base alla natura del dato.

**Database Relazionali (SQL)**:
- Usano uno **schema**: template che definisce la struttura dei dati; ogni nuova entry deve conformarsi → dati **prevedibili e facilmente valutabili**.
- Dati in **tabelle** (chiamate anche **Entità**) collegate da **keys** (chiavi); le chiavi danno accesso rapido a riga/colonna e mettono le tabelle in relazione (es. `User` ← `Order` ← `LineItem` → `Product`). Una modifica si propaga in modo predicibile e sistematico.
- **ACID-compliance** è un *must* per gli RDBMS: Atomicity, Consistency, Isolation, Durability → poco spazio agli errori.
- **Svantaggi**: schema rigido + vincoli forti rendono quasi impossibile l'uso in scenari **big data**; scalare richiede distribuzione su server multipli ma **gestire le tabelle su server diversi è difficile**; i vincoli di schema **ostacolano la migrazione** tra RDBMS diversi (devono essere identici).

**Database Non-Relazionali (NoSQL)**:
- Più **indulgenti** nella struttura: invece di tabelle righe/colonne usano **collections** di categorie diverse, caratterizzate da **documents** (*semi-structured data*); collection diverse non devono avere relazioni.
- **Schema-free**: i documents possono variare liberamente, anche senza schema definito in anticipo; campi creati on-the-fly.
- **Pros**: facile gestione/memorizzazione di grandi volumi, **scalabilità orizzontale** facile (distribuzione su nodi → accessibilità).
- **Cons**: non si può assumere la presenza di un campo (potrebbe mancare); senza relazioni l'**aggiornamento dei dati è più complesso** (ogni dettaglio va aggiornato separatamente).

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
- [[flask]] — Archive/Query Server Flask che persiste su MongoDB
- [[mongodb]] — esempio concreto di document store usato nel corso (+ PyMongo)
- [[strutture-dati]] — i documenti MongoDB sono rappresentati come dict Python

## Fonti

- [[17-nosql-databases]]

_Aggiornato: 2026-06-20 — MODULO 4: aggiunti Database/DBMS, features DBMS, ruolo back-end, schema/keys/entità relazionali, pro/contro estesi_
