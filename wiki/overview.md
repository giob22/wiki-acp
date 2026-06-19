# Overview — Advanced Computer Programming

**Corso:** Advanced Computer Programming (ACP)
**Docente:** Prof. Luigi De Simone — UniNA Federico II
**Esame:** Prova al computer + colloquio orale

**Temi principali:** Python avanzato, concorrenza (GIL, multiprocessing, threading), gRPC, Protocol Buffers, REST/Flask, MongoDB, MOM (ActiveMQ/STOMP), container e deployment (Docker, Docker Compose, Docker Swarm, Kubernetes).

---

## Argomenti coperti nel wiki

### Python Base
- Interprete CPython, bytecode, PVM → [[interprete-python]]
- Tipi scalari (int, float, bool, None) → [[tipi-scalari]]
- Stringhe (immutabili, slicing) → [[stringhe]]
- Costrutti di controllo (if, while, for, range) → [[costrutti-controllo]]
- Funzioni, docstring, funzioni come oggetti → [[funzioni]]
- Scope, regola LEGB, global, nonlocal → [[scope]]
- Passaggio parametri per assegnazione → [[passaggio-parametri]]
- Moduli e package, import, pip → [[moduli-package]]
- Tuple, Liste, Dizionari, Set, comprehension → [[strutture-dati]]
- File I/O, context manager → [[file-io]]
- Eccezioni, try/except/finally, custom → [[eccezioni]]

### OOP
- Classi, oggetti, self, `__init__`, dunder methods → [[oop]]
- Ereditarietà, polimorfismo, super(), ABC → [[ereditarieta]]

### Concorrenza
- Processo vs Thread, PCB, context switch, ULT/KLT → [[processo-thread]]
- GIL — Global Interpreter Lock → [[gil]]
- Modulo threading, Thread, Lock, daemon → [[threading]]
- Multiprocessing, Pool, ProcessPoolExecutor → [[multiprocessing]]

### Networking
- Socket, TCP vs UDP, OSI → [[socket]]

### Middleware e Sistemi Distribuiti
- RPC, IDL, stub/skeleton, marshalling → [[rpc]]
- Protocol Buffers, file `.proto`, field tag → [[protocol-buffers]]
- gRPC, HTTP/2, workflow, compilazione → [[grpc]]
- MOM, broker, store-and-forward, disaccoppiamento → [[mom]]
- Publish-Subscribe, PTP, Observer pattern → [[pub-sub]]

### Web Services
- REST, URI, HTTP methods, stateless → [[rest]]

### NoSQL
- NoSQL vs SQL, ACID, tipologie → [[nosql]]

### Container e Deployment
- Container vs VM, isolamento, footprint → [[virtualizzazione-container]]
- Linux Namespaces (mnt, pid, net, ipc, uts, user) + syscall clone/unshare/setns → [[linux-namespaces]]
- Cgroups — gestione risorse per gruppo di processi → [[cgroups]]

---

## Entità (tecnologie concrete)

- [[flask]] — micro-framework Python per REST API
- [[mongodb]] — database NoSQL document-store + PyMongo
- [[activemq]] — message broker MOM + STOMP
- [[grpc-python]] — binding Python per gRPC
- [[grpc-java]] — binding Java per gRPC (io.grpc, protoc-gen-grpc-java)
- [[docker]] — motore container, Docker Engine, immagini, Dockerfile
- [[docker-compose]] — deploy multi-container tramite compose.yaml
- [[docker-swarm]] — orchestrazione cluster nativa Docker (Raft, manager/worker)
- [[kubernetes]] — orchestratore container avanzato (Control Plane, Pod, CRI, OCI)

---

## Fonti ingestite

26 slide PDF ingestite (18 Python 2026-06-04, 5 Java 2026-06-04, 1 Java gRPC 2026-06-11, 1 Container/Docker 2026-06-12):
- 00 Introduzione, 01-17 Python (base, OOP, concorrenza, networking, middleware, gRPC, MOM, Flask, NoSQL), 20-25 Java (multithreading, sincronizzazione, networking, proxy-skeleton, JMS, gRPC), 03 Container-based Virtualization and Services Deployment

---

### Java
- Thread e Runnable, ciclo di vita → [[java-threading]]
- Synchronized, monitor, wait/notify, Java 1.5 Lock → [[java-sincronizzazione]]
- Pattern Proxy-Skeleton, oggetti remoti → [[proxy-pattern]]
- JMS, Abstract Factory, JNDI, administered objects → [[jms]]

---

## Argomenti mancanti / da approfondire

- asyncio (non coperto separatamente — TODO)
- Argomenti Java (multithreading, networking Java — non ancora ingestiti)
- Kubernetes (solo intro — nessun esercizio pratico nel corso)
- PyMongo avanzato (aggregation, indici)
- Flask avanzato (blueprint, template Jinja2, auth)

_Aggiornato: 2026-06-12 — ingest 03_Service_Deployment_Containers (container, Docker, Swarm, K8s)_
