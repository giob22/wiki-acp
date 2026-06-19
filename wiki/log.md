# Log — Advanced Computer Programming

Formato entry: `## [YYYY-MM-DD] <operazione> | <dettaglio>`
Filtra ultimi 10: `grep "^## " wiki/log.md | tail -10`

---

## [2026-06-11] canvas | Mappa esame Flask/REST (wiki/canvas/flask-websrv-mappa-esame.canvas)
## [2026-06-11] canvas | Mappa esame NoSQL/MongoDB (wiki/canvas/nosql-mappa-esame.canvas)
## [2026-06-11] canvas | Mappa esame MOM (wiki/canvas/mom-mappa-esame.canvas)
## [2026-06-11] canvas | Mappa esame gRPC (wiki/canvas/grpc-mappa-esame.canvas)

## [2026-06-04] setup | Wiki acp inizializzato

## [2026-06-04] ingest | 00_INTRODUZIONE — Introduzione al corso ACP
## [2026-06-04] ingest | 01_PYTHON_01 — Python Introduzione (interprete, bytecode, PVM)
## [2026-06-04] ingest | 01_PYTHON_02 — Tipi scalari, non scalari, Stringhe
## [2026-06-04] ingest | 01_PYTHON_03 — Costrutti di controllo
## [2026-06-04] ingest | 01_PYTHON_04 — Funzioni (+ scope complesso, passaggio parametri pp.24-27)
## [2026-06-04] ingest | 01_PYTHON_05 — Moduli e Package (+ import relativi/assoluti pp.21-22)
## [2026-06-04] ingest | 01_PYTHON_06 — Tuple, Liste, Dizionari
## [2026-06-04] ingest | 01_PYTHON_07 — Passaggio parametri
## [2026-06-04] ingest | 01_PYTHON_08 — File ed Eccezioni
## [2026-06-04] ingest | 01_PYTHON_09 — Python OOP
## [2026-06-04] ingest | 01_PYTHON_10 — Programmazione Concorrente: Richiami
## [2026-06-04] ingest | 01_PYTHON_11 — Python Concurrency (threading, GIL, multiprocessing)
## [2026-06-04] ingest | 01_PYTHON_12 — Python Networking (socket, TCP/UDP)
## [2026-06-04] ingest | 01_PYTHON_13 — Sistemi Middleware (RPC, stub, skeleton)
## [2026-06-04] ingest | 01_PYTHON_14 — Python RPC / gRPC / Protocol Buffers
## [2026-06-04] ingest | 01_PYTHON_15 — Python MOM (ActiveMQ, STOMP, pub-sub)
## [2026-06-04] ingest | 01_PYTHON_16 — Flask / REST / Web Services
## [2026-06-04] ingest | 01_PYTHON_17 — NoSQL Databases (MongoDB, PyMongo)
## [2026-06-04] ingest | 02_JAVA_01 — Java Multithreading (Thread, Runnable, lifecycle)
## [2026-06-04] ingest | 02_JAVA_02 — Sincronizzazione Java (synchronized, monitor, wait/notify, Java 1.5)
## [2026-06-04] ingest | 02_JAVA_03 — Java Networking (Socket, ServerSocket, DatagramSocket, multithread)
## [2026-06-04] ingest | 02_JAVA_04 — Proxy-Skeleton Java (pattern, esempio Contatore Remoto UDP)
## [2026-06-04] ingest | 02_JAVA_05 — JMS (ActiveMQ, PTP/PubSub, Abstract Factory, JNDI)
## [2026-06-06] nuova-pagina | gestione-errori-api — sintesi da query su eccezioni PyMongo/status HTTP, abort/errorhandler Flask, gRPC context/StatusCode
## [2026-06-06] aggiornamento | mongodb — espansa sezione query: operatori filtro/update completi, find_one_and_update, schema decisionale (da query utente)
## [2026-06-06] lint | fix pagine orfane e link rotti: 4 fonti+entità, [[asyncio]] stub, [[middleware-trasparenza]] nuova pagina, backlink grpc/mom/flask/jms aggiornati
## [2026-06-07] setup | Cartelle prove-esame e svolgimenti create — workflow genera/valuta pronto
## [2026-06-07] ingest | prove-esame-2023-2024 — 5 prove pratiche analizzate (2023-11, 2024-03, 2024-06, 2024-07, 2024-10)
## [2026-06-07] nuova-pagina | pattern-esame — pattern ricorrenti estratti dalle 5 prove (architettura, prod/cons, proxy-skeleton, routing, checklist)
## [2026-06-07] prova-simulata | 2026-06-08-sim-01 — sistema monitoraggio sensori (Python, Socket TCP + Flask + MongoDB)
## [2026-06-09] prova-simulata | 2026-06-09-sim-02 — telemetria industriale (Python gRPC + STOMP, Java JMS)
## [2026-06-10] prova-simulata | 2026-06-10-sim-03 — qualità produzione (Java proxy-skeleton Socket + JMS Topic, Python STOMP subscriber)
## [2026-06-10] prova-simulata | 2026-06-10-sim-04 — ordini produzione Python puro (gRPC multi-thread + lista+Condition + Flask)
## [2026-06-11] ingest | 02_JAVA_06-GRPC — Remote Procedure Call in Java (setup, API comparative Java/Python, Hello World)
## [2026-06-12] snippets | Creata wiki/snippets/ — 8 pagine boilerplate (proxy-skeleton py/java, gRPC py/java, STOMP, JMS, Flask, PyMongo) da slide + svolgimenti

## [2026-06-12] update | snippet grpc-python: sezione liste `repeated`
## [2026-06-12] ingest | 03_Service_Deployment_Containers — Container-based Virtualization and Services Deployment (Docker, Swarm, K8s, Namespaces, Cgroups)
## [2026-06-14] prova-simulata | 2026-06-14-sim-05 — prenotazione biglietti (Python Socket TCP proxy-skeleton + threading.Lock + Flask)

## [2026-06-15] prova-simulata | 2026-06-15-sim-06 — telemetria gateway (Java proxy-skeleton Socket TCP + skeleton ereditarietà, MOM STOMP/ActiveMQ, Python Channel Router subscriber + Flask Archive Server) — testo senza soluzione

## [2026-06-15] update | snippet proxy-skeleton-java: marshalling con DataInputStream/DataOutputStream (writeUTF/readUTF) al posto di PrintWriter/BufferedReader, conforme slide 22-java-networking

## [2026-06-15] update | snippet flask-boilerplate: sezione "abort — uso corretto" (guard clause, codici standard, make_response, errorhandler unico HTTPException)

## [2026-06-15] prova-simulata | 2026-06-15-sim-08 — smistamento pacchi (Java proxy-skeleton Socket TCP + skeleton ereditarietà, REST/Flask Python + MongoDB) — testo senza soluzione, no JMS/gRPC Java

## [2026-06-15] nuova-pagina | sottoscrizioni-durabili — gap segnalato dall'utente (non in slide raw): durable subscription STOMP (client-id + activemq.subscriptionName) e JMS (setClientID + createDurableSubscriber); aggiornati snippet stomp-python/jms-java, entità activemq, concetto jms, index

## [2026-06-16] update | snippet proxy-skeleton (py+java) — aggiunta variante trasporto UDP

## [2026-06-16] prova | sim-09 — Java puro: gRPC client/server + JMS producer/consumer asincrono (no Python)

## [2026-06-18] prova-simulata | 2026-06-18-sim-11 — bike-sharing (Python proxy-skeleton Socket TCP + skeleton ereditarietà, produttore/consumatore lista size 5, Flask + MongoDB) — testo senza soluzione
