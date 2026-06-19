---
tipo: fonte
titolo: "Container-based Virtualization and Services Deployment"
data_ingest: 2026-06-12
formato: slide-pdf
argomenti: [container, docker, docker-compose, docker-swarm, kubernetes, linux-namespaces, cgroups, virtualizzazione]
---

## Sommario

Le slide trattano la virtualizzazione basata su container come alternativa leggera alle Virtual Machine tradizionali. Il punto di partenza è la critica alle VM (overhead da hypervisor, consumo di memoria, avvio lento) per arrivare ai container come soluzione portabile e autosufficiente. I meccanismi kernel alla base dei container sono i Linux Namespaces (isolamento) e i Cgroups (gestione delle risorse). Docker è presentato come la principale tecnologia di container, con la sua architettura a tre livelli (daemon, containerd, runc), il modello a layer delle immagini basato su OverlayFS, il Dockerfile per la definizione delle immagini, e i comandi CLI fondamentali. Per applicazioni multi-container viene introdotto Docker Compose. Per il deployment su cluster vengono presentati Docker Swarm (orchestratore nativo) e una breve introduzione a Kubernetes.

## Punti chiave

1. Un container **non emula dispositivi fisici**: sfrutta le astrazioni del kernel host (namespaces + cgroups), non un hypervisor
2. **Namespaces**: isolamento delle risorse per processo — `mnt`, `pid`, `net`, `ipc`, `uts`, `user` — con syscall `clone()`, `unshare()`, `setns()`
3. **Cgroups**: gestione delle risorse per **gruppi** di processi (CPU, memoria, I/O, rete); origine da Google (2006 "process container" → 2007 "cgroup")
4. Un container condivide il kernel host: 10-100 VM vs **100-1000 container** sullo stesso server fisico; avvio in ~2 secondi
5. **Immagini Docker** = stack di layer read-only (Union File System / OverlayFS) + thin R/W layer in cima; più container condividono gli stessi layer dell'immagine base
6. Il **Dockerfile** definisce la build: `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENTRYPOINT`, `CMD`, `EXPOSE`
7. **Docker Engine** = daemon (API REST) → containerd (lifecycle) → runc (OCI runtime)
8. **Docker Compose** = deploy multi-container tramite `compose.yaml`; un singolo comando (`docker compose up`) avvia tutto lo stack
9. **Docker Swarm** = orchestratore cluster nativo; nodi manager (algoritmo Raft) + nodi worker; servizi replicati vs globali; task = unità atomica di scheduling
10. **Kubernetes** (intro): basato su Google Borg, incoraggia microservizi, Control Plane (etcd, kube-apiserver, scheduler, controller-manager) + Nodes (kubelet, CRI, Pods)

## Concetti introdotti

- [[virtualizzazione-container]]
- [[linux-namespaces]]
- [[cgroups]]

## Entità introdotte

- [[docker]]
- [[docker-compose]]
- [[docker-swarm]]
- [[kubernetes]]

## Domande aperte

- OverlayFS: come viene gestita la copia-su-scrittura (copy-on-write) quando un container modifica un file dell'immagine base?
- Docker Swarm vs Kubernetes: in quali scenari si sceglie l'uno sull'altro?
- Come si gestisce la persistenza dei dati in Swarm (volumi distribuiti)?

## Domande da esame

- Qual è la differenza fondamentale tra container e Virtual Machine?
- Cosa sono i Linux Namespaces e i Cgroups? Quali syscall li gestiscono?
- Descrivere l'architettura di Docker Engine (daemon, containerd, runc).
- Cosa contiene un Dockerfile? Differenza tra ENTRYPOINT e CMD.
- Cosa fa Docker Compose? Quali chiavi contiene un compose.yaml?
- Come funziona Docker Swarm? Differenza tra servizio replicato e globale.
- Cos'è un task in Docker Swarm?
- Qual è l'architettura di Kubernetes (Control Plane, Node, Pod, kubelet)?
