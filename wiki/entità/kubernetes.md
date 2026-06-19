---
tipo: entità
categoria: strumento
---

## Cos'è

**Kubernetes** (K8s) è un sistema open source di orchestrazione di container, basato sul sistema interno di Google chiamato **Borg**. Avviato nel **2014**, è scritto in Go e progettato per deployare, scalare e gestire applicazioni containerizzate in ambienti cloud, bare-metal e ibridi.

## Filosofia: microservizi

Kubernetes incoraggia l'approccio ai **microservizi**: l'applicazione viene scomposta in servizi piccoli e indipendenti, ognuno deployabile su macchine diverse. Questo garantisce:
- **Scalabilità** superiore rispetto a un'applicazione monolitica su singola macchina
- **Affidabilità** migliore grazie alla distribuzione dei componenti
- Supporto a più tecnologie di container (non solo Docker), cloud provider e ambienti bare-metal
- Open source (scritta in Go), con ecosistema molto ampio

## Architettura

```
End Users → Load Balancer → Nodi del cluster
                              ↑
                    Cloud Provider Network Edge

Control Plane:
  ┌─────────────────────────────────────────────────┐
  │  etcd ←────────────→ kube-apiserver             │
  │  controller-manager ←─────────→ scheduler       │
  └─────────────────────────────────────────────────┘
              ↕ (comunica con i nodi)
  Node:
  ┌──────────────────────────────────────┐
  │  Pods                                │
  │  Container Runtime                   │
  │  kubelet (System Services)           │
  └──────────────────────────────────────┘
```

### Control Plane

Il Control Plane gestisce lo stato globale del cluster:

| Componente | Funzione |
|---|---|
| **etcd** | Store distribuito chiave-valore per lo stato del cluster (configurazioni, stato corrente) |
| **kube-apiserver** | API server centrale; tutti gli altri componenti comunicano attraverso di esso |
| **controller-manager** | Esegue i controller che mantengono lo stato desiderato (es. garantisce il numero di repliche corretto) |
| **scheduler** | Decide su quale nodo fisico schedulare i nuovi Pod |

### Node

Ogni nodo del cluster esegue:

| Componente | Funzione |
|---|---|
| **Pod** | Unità di deployment minima; uno o più container che condividono rete e storage locali |
| **kubelet** | Agente su ogni nodo; comunica col Control Plane via gRPC; gestisce il ciclo di vita dei Pod |
| **Container Runtime** | Motore che esegue effettivamente i container (Docker, containerd, CRI-O) |

## Container Runtime Interface (CRI) e OCI

Kubernetes non dipende direttamente da un singolo runtime di container: usa la **Container Runtime Interface (CRI)**, un'interfaccia gRPC standardizzata che consente di usare qualsiasi runtime compatibile.

```
kubelet
  ↓ gRPC
CRI (Container Runtime Interface)
  ├── CRI-O          (CRI daemon + OCI generate)
  ├── containerd     (CRI Plugin v1.1)
  └── Docker         (tramite cri-dockerd → Docker engine)
           ↓
OCI (Open Container Initiative)
  ├── runc           (runtime standard)
  ├── gVisor (runsc) (sandbox sicura)
  ├── Kata (kata-runtime) (VM leggera per isolamento forte)
  └── crun
           ↓
Containers
  [Linux Namespaces | cgroups | Seccomp | SELinux]
```

**OCI (Open Container Initiative)** definisce gli standard aperti per:
- **Image spec** — formato delle immagini container
- **Runtime spec** — come avviare un container da un'immagine

Questo disaccoppiamento permette di sostituire il runtime (da Docker a containerd o CRI-O) senza modificare Kubernetes.

## Differenza con Docker Swarm

| Aspetto | Docker Swarm | Kubernetes |
|---|---|---|
| Complessità setup | Semplice, integrato in Docker | Più complesso, richiede setup dedicato |
| Scalabilità | Buona per cluster medi | Eccellente, progettato per scala enorme |
| Funzionalità | Essenziali | Molto più ricco (RBAC, ConfigMap, Secrets, Ingress, Helm...) |
| Adozione industry | Limitata | Standard de facto per la produzione |

## Come si usa nel corso

Le slide presentano Kubernetes a livello introduttivo. Il corso non prevede esercizi pratici su K8s — il focus pratico è su [[docker]] e [[docker-swarm]].

> 🎯 Esame: Conoscere l'architettura a livello alto (Control Plane vs Node, componenti principali) e il concetto di Pod. Il dettaglio di CRI/OCI può essere richiesto come domanda di approfondimento.

TODO: da espandere con esempi pratici se vengono trattati in futuro.

## Connessioni

- [[docker]] — runtime sottostante più comune in K8s
- [[docker-swarm]] — alternativa più semplice per orchestrazione cluster
- [[virtualizzazione-container]] — Kubernetes orchestra container
- [[linux-namespaces]] — usati dai container orchestrati da K8s
- [[cgroups]] — usati dai container orchestrati da K8s

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
