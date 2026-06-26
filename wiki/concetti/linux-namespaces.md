---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread]
---

#flashcards/acp

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

> 🎯 Esame — i namespace si **ereditano, non si "hanno"**: un normale processo lanciato da terminale **non** ha un namespace proprio. Con una `fork()` ordinaria il figlio **eredita** i namespace del padre. Risalendo la catena (shell → ... → init, PID 1), tutti i processi normali vivono negli stessi **namespace "root"**, esistenti dall'avvio e contenenti tutte le risorse globali. Un namespace **nuovo** nasce **solo** passando i flag `CLONE_NEWxxx` a `clone()`/`unshare()` — ed è esattamente ciò che fa Docker all'avvio di un container. Formulazione efficace: *«i namespace non sono una proprietà intrinseca del processo, ma un contesto che si eredita»*. (Verificabile: ogni processo espone i propri namespace in `/proc/<pid>/ns/` come link simbolici.)

I namespace si 'hanno' o si ereditano?
?
Si ereditano: una fork() ordinaria fa ereditare al figlio i namespace del padre; i processi normali vivono nei namespace 'root'. Uno nuovo nasce solo con i flag CLONE_NEWxxx a clone()/unshare() (ciò che fa Docker).


**`ioctl()`** è una system call generica del kernel (input/output control): serve a inviare comandi di controllo a oggetti del kernel che non rientrano nelle normali `read`/`write`. Nel contesto dei namespace è usata per **interrogarli** (tipo, relazioni padre/figlio), operazioni non coperte da `clone`/`setns`/`unshare`.

**`nsenter` e `docker exec`** — `nsenter` (*namespace enter*) è un comando Linux che permette di **entrare nei namespace di un processo già in esecuzione**: dato il PID, esegue un comando nel contesto dei suoi namespace (stessa rete, stesso filesystem, stessi processi). Si appoggia internamente a `setns()`. È il meccanismo che sta **sotto a `docker exec`**: `docker exec -it <container> sh` fa sostanzialmente un `nsenter` nei namespace del container e avvia lì una shell.

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

All'interno del namespace x, getpid() restituisce 1 per il processo che sarebbe pid 3 nel root namespace. Due conseguenze:
1. dentro il container il processo principale è **PID 1**, e in Unix il PID 1 (*init*) ha responsabilità speciali: **raccoglie i processi zombie** e riceve i segnali con semantica particolare (se non installa un handler, molti segnali vengono **ignorati** invece di terminare il processo);
2. l'host **vede** tutti i processi dei container (coi loro PID reali), mentre un container **non vede** i processi dell'host: l'isolamento è **unidirezionale**, dall'interno verso l'esterno.

> 💡 Il "PID 1 nel container" è un problema pratico noto: se l'`ENTRYPOINT` è l'applicazione stessa, questa diventa init e potrebbe non gestire `SIGTERM` (quindi `docker stop` aspetta il timeout e poi manda `SIGKILL`) né raccogliere gli zombie. Per questo esiste l'opzione `docker run --init`, che inserisce un piccolo init (`tini`) come PID 1.

### Esempio: Network namespace

Ogni container ottiene il proprio stack di rete (interfacce, tabelle di routing, porte). Più precisamente, nel container è presente una **propria istanza dello stack TCP/IP**: non viene duplicato il *codice* dello stack (che è uno solo, nel kernel condiviso), ma vengono replicate **per namespace** tutte le strutture dati — interfacce, tabelle di routing, tabella ARP, regole iptables/firewall e, soprattutto, lo **spazio delle porte**. Conseguenza pratica: **due container possono entrambi fare bind sulla porta 5001 senza conflitto**, perché ciascuno la apre nel proprio stack; il conflitto nasce solo quando si vogliono pubblicare entrambe sulla **stessa porta dell'host** (che vive nel root namespace ed è unica).

La comunicazione tra namespace avviene tramite **coppie veth** (*virtual ethernet pair*, come un cavo virtuale: ciò che entra da un capo esce dall'altro): un capo è la `eth0` interna al container, l'altro sta nel **root network namespace** collegato a un **Linux bridge** (uno switch software). In Docker questo bridge si chiama di default **`docker0`**, e il traffico verso l'esterno passa per **NAT** attraverso l'interfaccia fisica dell'host. È anche il motivo per cui serve la **pubblicazione delle porte** (`-p 5001:5001`): le porte aperte dentro il container vivono nel suo network namespace e non sono raggiungibili dall'esterno finché non si crea un inoltro esplicito dall'host.

```
Linux Host
└── Root network namespace
    ├── Network namespace 1 (eth0@YY → vethYYYY → docker0 bridge)
    └── Network namespace 2 (eth0@XX → vethXXXX → docker0 bridge → eth0 fisico → NAT)
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

Tipi di namespace e syscall di gestione?
?
Tipi: mnt, pid, net, ipc, uts, user (+ cgroup). Syscall: clone() (nuovo processo+namespace), unshare() (nuovo namespace al processo corrente), setns() (join a un namespace esistente).


> 💡 Connessione: I namespace isolano **per processo**; i [[cgroups]] limitano le risorse **per gruppo** di processi. Insieme costituiscono i due pilastri dei container.

## Connessioni

- [[cgroups]] — complementare: gestione risorse per gruppo di processi
- [[virtualizzazione-container]] — namespace come meccanismo base dell'isolamento
- [[docker]] — Docker usa namespaces per isolare ogni container dal resto del sistema

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
_Aggiornato: 2026-06-20 — MODULO 4 (appunti): namespace si ereditano non si "hanno" (fork eredita, nuovo solo con CLONE_NEWxxx), ioctl, nsenter↔docker exec (via setns), istanza stack TCP/IP per network namespace (bind stessa porta senza conflitto), veth/docker0/NAT, PID 1=init (zombie reaping, SIGTERM, docker run --init/tini)_
