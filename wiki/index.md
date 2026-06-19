# Index — Advanced Computer Programming

## Overview
→ [[overview]]

---

## Concetti

### Python Base
- [[interprete-python]] — CPython, bytecode, PVM, modalità interattiva/script
- [[tipi-scalari]] — int, float, bool, NoneType, type casting, operatori
- [[stringhe]] — sequenza immutabile, slicing, metodi
- [[costrutti-controllo]] — if/elif/else, while, for, range, break
- [[funzioni]] — def, scope, return, first-class objects, lambda
- [[scope]] — LEGB, global, nonlocal, frame, esempio annidato
- [[passaggio-parametri]] — per assegnazione, mutabile vs immutabile, rebind
- [[moduli-package]] — import, pip, sys.path, __init__.py, import relativi
- [[strutture-dati]] — tuple, lista, dizionario, set, comprehension
- [[file-io]] — open(), context manager, read/write
- [[eccezioni]] — try/except/else/finally, raise, eccezioni custom

### OOP
- [[oop]] — classe, self, __init__, dunder, attributi istanza/classe
- [[ereditarieta]] — super(), polimorfismo, ABC, isinstance

### Concorrenza
- [[processo-thread]] — programma vs processo, PCB, context switch, ULT/KLT
- [[gil]] — Global Interpreter Lock, implicazioni, workaround
- [[threading]] — Thread, Lock, daemon, RLock, Event, Semaphore
- [[multiprocessing]] — Process, Pool, ProcessPoolExecutor, IPC
- [[asyncio]] — event loop, coroutine, async/await, alternativa single-thread per I/O-bound

### Networking
- [[socket]] — socket, TCP vs UDP, OSI, client/server TCP

### Middleware
- [[rpc]] — Remote Procedure Call, IDL, stub, skeleton, marshalling
- [[protocol-buffers]] — .proto, message, field tag, sintassi proto3
- [[grpc]] — HTTP/2, workflow 4 passi, _pb2.py, _pb2_grpc.py
- [[mom]] — Message Broker, store-and-forward, disaccoppiamento spaziale/temporale
- [[pub-sub]] — PTP vs Pub-Sub, Observer, Notification Service, AMQP/MQTT/STOMP
- [[sottoscrizioni-durabili]] — durable subscription, client-id + subscription name, STOMP/JMS, disaccoppiamento temporale sui topic
- [[middleware-trasparenza]] — specifica vs implementazione, IDL/Abstract Factory/STOMP, JMS vs gRPC vs ActiveMQ

### Web Services e NoSQL
- [[rest]] — risorsa, URI, interfaccia uniforme, safe/idempotente, stateless
- [[nosql]] — SQL vs NoSQL, ACID, tipologie (key-value, document, graph...)
- [[gestione-errori-api]] — eccezioni PyMongo↔status HTTP, abort/errorhandler Flask, gRPC context/StatusCode

### Container e Deployment
- [[virtualizzazione-container]] — container vs VM, no Guest OS, namespaces+cgroups, confronto prestazioni
- [[linux-namespaces]] — isolamento risorse per processo, tipi (mnt/pid/net/ipc/uts/user), syscall clone/unshare/setns
- [[cgroups]] — gestione risorse per gruppo di processi, moduli memory/cpuset/blkio, origine Google 2006

---

## Entità

- [[flask]] — micro-framework Python per REST API web
- [[mongodb]] — document-store NoSQL + PyMongo driver
- [[activemq]] — Apache ActiveMQ broker MOM + STOMP Python
- [[grpc-python]] — binding Python gRPC (grpcio, grpcio-tools)
- [[grpc-java]] — binding Java gRPC (io.grpc, protoc-gen-grpc-java, JAR deps)
- [[docker]] — Docker Engine (daemon/containerd/runc), immagini OverlayFS, Dockerfile, CLI
- [[docker-compose]] — deploy multi-container, compose.yaml, comandi up/down
- [[docker-swarm]] — orchestrazione cluster, Raft, manager/worker, servizi replicati/globali, task
- [[kubernetes]] — orchestratore avanzato, Control Plane, Pod, kubelet, CRI, OCI

---

## Snippets — boilerplate per tecnologia

Codice pronto da prova pratica, basato su slide e svolgimenti verificati.

| Tecnologia | Python | Java |
|---|---|---|
| Proxy-Skeleton (Socket TCP) | [[proxy-skeleton-python]] | [[proxy-skeleton-java]] |
| gRPC | [[grpc-python-boilerplate]] | [[grpc-java-boilerplate]] |
| MOM / ActiveMQ | [[stomp-python]] (STOMP) | [[jms-java]] (JMS) |
| REST | [[flask-boilerplate]] | — |
| NoSQL | [[mongodb-pymongo]] | — |
| Docker / Deploy | [[docker-dockerfile]] | — |

---

## Fonti

- [[00-introduzione]] — Introduzione al corso ACP
- [[01-python-introduzione]] — Python: interprete, bytecode, PVM
- [[02-tipi-scalari-stringhe]] — Tipi scalari, stringhe, operatori
- [[03-costrutti-controllo]] — if/while/for/range/break
- [[04-funzioni]] — Funzioni, scope, passaggio parametri (pag 24-27)
- [[05-moduli-package]] — Moduli, package, import, pip
- [[06-tuple-liste-dizionari]] — Tuple, liste, dizionari, set, comprehension
- [[07-passaggio-parametri]] — Passaggio per assegnazione (standalone)
- [[08-file-eccezioni]] — File I/O, eccezioni, try/except/finally
- [[09-oop]] — OOP: classi, self, dunder, ereditarietà, polimorfismo
- [[10-programmazione-concorrente-richiami]] — Processo/Thread, PCB, ULT/KLT
- [[11-python-concurrency]] — threading, Lock, GIL, multiprocessing
- [[12-python-networking]] — Socket, TCP/UDP, OSI, client/server
- [[13-sistemi-middleware]] — Middleware, RPC, stub/skeleton, marshalling
- [[14-python-rpc-grpc]] — gRPC, protobuf, HTTP/2, workflow, Hello World
- [[15-python-mom]] — MOM, ActiveMQ, STOMP, PTP, pub-sub, Observer
- [[16-python-flask]] — REST, HTTP methods, URI, Flask, requests
- [[17-nosql-databases]] — NoSQL, MongoDB, PyMongo, SQL vs NoSQL

---

### Java
- [[java-threading]] — Thread/Runnable, start/join/sleep, ciclo di vita, vs Python
- [[java-sincronizzazione]] — synchronized, monitor, wait/notify, Java 1.5 Lock/Semaphore
- [[proxy-pattern]] — Proxy-Skeleton, separazione logica applicativa/comunicazione, RPC manuale
- [[jms]] — JMS API, Abstract Factory, JNDI, administered objects, Session/Producer/Consumer

---

## Fonti — Java

- [[20-java-multithreading]] — Thread, Runnable, lifecycle, sleep, join, priority
- [[21-java-sincronizzazione]] — synchronized metodo/blocco, monitor, wait/notify, Java 1.5
- [[22-java-networking]] — Socket, ServerSocket, DatagramSocket, multithread server
- [[23-java-proxy-skeleton]] — pattern Proxy-Skeleton, ereditarietà/delega, esempio UDP
- [[24-java-jms]] — JMS, ActiveMQ, interfacce PTP/PubSub, Abstract Factory, JNDI
- [[25-java-grpc]] — gRPC Java: setup, API comparative Java/Python, Hello World
- [[03-service-deployment-containers]] — Container-based Virtualization: VM vs container, Namespaces, Cgroups, Docker, Compose, Swarm, Kubernetes

---

## Esame

- [[pattern-esame]] — pattern ricorrenti nelle prove pratiche ACP (architettura, produttore/consumatore, proxy-skeleton, routing)

_per generare domande/riepilogo/mappa: eseguire `esame`_

---

## Fonti — Prove d'esame

- [[prove-esame-2023-2024]] — analisi 5 prove pratiche (2023-11, 2024-03, 2024-06, 2024-07, 2024-10)

---

## Prove simulate — Svolgimenti

| Data | Tema | Svolgimento |
|------|------|-------------|
| 2026-06-08 | Monitoraggio sensori (Socket TCP + Flask + MongoDB) | [sim-01](../svolgimenti/2026-06-08-sim-01/prova.md) |
| 2026-06-09 | Telemetria industriale (gRPC + STOMP, Java JMS) | [sim-02](../svolgimenti/2026-06-09-sim-02/prova.md) |
| 2026-06-10 | Qualità produzione (Java proxy-skeleton + JMS Topic, Python STOMP) | [sim-03](../svolgimenti/2026-06-10-sim-03/prova.md) |
| 2026-06-10 | Ordini produzione Python puro (gRPC + lista+Condition + Flask) | [sim-04](../svolgimenti/2026-06-10-sim-04/prova.md) |
| 2026-06-14 | Prenotazione biglietti Python puro (Socket TCP proxy-skeleton + Lock + Flask) | [sim-05](../svolgimenti/2026-06-14-sim-05/prova.md) |
