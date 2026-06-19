---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread]
---

## Definizione

I **Linux Namespaces** sono un meccanismo del kernel Linux che fornisce isolamento delle risorse a livello di processo: ogni processo vede una visione parziale e separata delle risorse di sistema, come se fosse l'unico processo in esecuzione per quella risorsa.

## Spiegazione

Un namespace è un **dominio di denominazione** per un certo tipo di risorsa. Processi all'interno dello stesso namespace condividono la stessa vista di quella risorsa; processi in namespace diversi ne hanno viste completamente isolate.

### Tipi di namespace

| Namespace | Flag kernel | Isola |
|---|---|---|
| `mnt` | `CLONE_NEWNS` | Mount points, filesystem |
| `pid` | `CLONE_NEWPID` | Spazio dei PID dei processi |
| `net` | `CLONE_NEWNET` | Stack di rete (interfacce, routing, porte) |
| `ipc` | `CLONE_NEWIPC` | System V IPC (semafori, code, shared memory) |
| `uts` | `CLONE_NEWUTS` | Hostname e domainname |
| `user` | `CLONE_NEWUSER` | UID/GID (permessi utente) |
| `cgroup` | `CLONE_NEWCGROUP` | Vista dei cgroup |

### Syscall di gestione

**`clone()`** — crea un nuovo processo **e** un nuovo namespace; il processo viene "attaccato" al nuovo namespace. `fork()` e `exit()` sono modificati per gestire i flag dei namespace (es. `CLONE_NEWxxx`).

**`unshare()`** — **non** crea un nuovo processo; crea un nuovo namespace e lo "attacca" al processo corrente. Aggiunta nel 2005 anche per ragioni di sicurezza.

**`setns()`** — permette a un processo di fare il **join** di un namespace esistente (già creato da un altro processo).

```
Linux namespaces ─── API ─── clone
                              ├── setns
                              └── unshare
        │
        └── Tipi: net | ipc | cgroup | mount | PID | users | UTS
```

### Esempio: PID namespace

Nel namespace PID radice il processo vede i PID reali. All'interno di un namespace PID figlio, il processo ha PID 1 (dal suo punto di vista), ma il kernel host lo conosce con un PID diverso.

```
root PID Namespace:
  pid 1 (pid 1)
    ├── pid 2 (pid 2)
    └── pid 3 → pid Namespace x
                  └── pid 3 visto come pid 1 nel ns
                      ├── pid 5 visto come pid 3 nel ns
                      └── pid 4 visto come pid 2 nel ns
```

All'interno del namespace x, getpid() restituisce 1 per il processo che sarebbe pid 3 nel root namespace.

### Esempio: Network namespace

Ogni container ottiene il proprio stack di rete (interfacce, tabelle di routing, porte). La comunicazione tra namespace avviene tramite coppie di interfacce virtuali `veth` collegate attraverso un **Linux bridge**.

```
Linux Host
└── Root network namespace
    ├── Network namespace 1 (eth0@YY → vethYYYY → Linux bridge)
    └── Network namespace 2 (eth0@XX → vethXXXX → Linux bridge → eth0 fisico)
```

### Esempio: Mount namespace

Ogni container ha il proprio albero di mount points. I filesystem `/proc`, `/dev`, `/sys` sono montati privatamente per ogni container, così che un container non veda i processi o i device degli altri.

```
Global mount namespace
└── child mount namespace 1 (→ Virtual Disk 1)
└── child mount namespace 2 (→ Virtual Disk 2)
```

## Perché importa

I namespace sono il **fondamento dell'isolamento** nei container. Senza di essi, tutti i processi condividerebbero lo stesso spazio di nomi PID, la stessa rete, lo stesso filesystem — rendendo impossibile l'isolamento senza un OS guest completo.

> 🎯 Esame: Saper elencare i 6 tipi di namespace e le 3 syscall (`clone`, `unshare`, `setns`) con la differenza tra loro.

> 💡 Connessione: I namespace isolano **per processo**; i [[cgroups]] limitano le risorse **per gruppo** di processi. Insieme costituiscono i due pilastri dei container.

## Connessioni

- [[cgroups]] — complementare: gestione risorse per gruppo di processi
- [[virtualizzazione-container]] — namespace come meccanismo base dell'isolamento
- [[docker]] — Docker usa namespaces per isolare ogni container dal resto del sistema

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
