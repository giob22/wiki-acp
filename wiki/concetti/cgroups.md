---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, linux-namespaces]
---

## Definizione

I **Cgroups** (Control Groups) sono un sottosistema del kernel Linux che fornisce un framework generico per la **gestione, il limite e il monitoraggio delle risorse** (CPU, memoria, I/O, rete) assegnate a **gruppi** di processi.

## Spiegazione

### Origine

Progetto nato da Google:
- **2006**: introdotto con il nome *process container*
- **2007**: rinominato in *cgroup* per evitare ambiguità col termine "container"

### Differenza fondamentale con i Namespace

| Meccanismo | Scopo | Granularità |
|---|---|---|
| **Namespace** | Isolamento della visibilità delle risorse | Per singolo processo |
| **Cgroups** | Limite e monitoraggio del consumo delle risorse | Per **gruppo** di processi |

> 💡 Connessione: I namespace forniscono una **soluzione di isolamento delle risorse per processo**; i cgroups forniscono una **soluzione di gestione delle risorse per gruppi**. Entrambi necessari per realizzare un container.

### Moduli principali

I moduli di cgroup non si trovano in un'unica cartella: sono distribuiti nell'albero del kernel in base alla loro funzionalità.

| Modulo | File kernel | Funzione |
|---|---|---|
| `memory` | `mm/memcontrol.c` | Imposta limiti sull'uso della memoria; genera report automatici sulle risorse utilizzate |
| `cpuset` | `kernel/cpuset.c` | Assegna CPU specifiche (in sistemi multicore) e nodi NUMA ai task del cgroup |
| `net_prio` | `net/core/netprio_cgroup.c` | Imposta dinamicamente la priorità del traffico di rete per interfaccia |
| `devices` | `security/device_cgroup.c` | Consente o nega l'accesso ai dispositivi ai task del cgroup |
| `blkio` | — | Imposta limiti sull'I/O verso dispositivi a blocchi (dischi, SSD, USB) |
| `cpu` | — | Controllo dell'utilizzo della CPU per gruppo |
| `freezer` | — | Sospende e riprende tutti i task di un cgroup |

Il **controller della memoria** (`memcg`) è considerato il più complesso da implementare.

### Come vengono usati nei container

Docker crea un cgroup dedicato per ogni container e vi associa il processo principale. Questo permette di:
- Limitare la RAM usata da un container (`--memory 512m`)
- Limitare la CPU (`--cpus 0.5`)
- Limitare la banda I/O su disco
- Monitorare il consumo effettivo in tempo reale

### Gerarchia cgroup

I cgroup sono organizzati in una gerarchia ad albero. Un processo appartiene a esattamente un cgroup per ogni tipo di controller. I limiti si propagano dall'alto verso il basso: un cgroup figlio non può superare i limiti del cgroup padre.

## Perché importa

Senza cgroups, container diversi sullo stesso host potrebbero monopolizzare CPU o memoria, compromettendo l'isolamento prestazionale. I cgroups garantiscono che ogni container rispetti i limiti assegnati e che le risorse siano distribuite in modo controllato.

> 🎯 Esame: Saper spiegare la differenza concettuale tra namespace (isolamento) e cgroups (gestione risorse), e conoscere almeno 3-4 moduli cgroup con la loro funzione.

## Connessioni

- [[linux-namespaces]] — namespace isola la visibilità, cgroup limita il consumo; entrambi fondamentali per i container
- [[virtualizzazione-container]] — cgroups come secondo pilastro dei container Linux
- [[docker]] — Docker usa cgroups per imporre limiti di risorse ai container (`--memory`, `--cpus`)

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
