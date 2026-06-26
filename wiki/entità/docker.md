---
tipo: entità
categoria: strumento
---

#flashcards/acp

## Cos'è

**Docker** è un motore di container scritto in **Go**, basato su Linux container, che permette di eseguire applicazioni in container isolati e portabili. Nasce come **dotCloud, Inc.** (2010, fondata da **Solomon Hykes**) → rinominata **Docker Inc.** nel 2013. Il motore open-source è sviluppato dalla comunità sotto il nome **Moby** (github.com/moby/moby). Il payload è incapsulato come container **leggero, portabile, self-sufficient**, manipolabile con operazioni standard ed eseguibile in modo consistente su qualsiasi piattaforma hardware.

> 💡 Docker **non ha inventato i container**: esistevano già `chroot`, FreeBSD jails, Solaris Zones e Linux **LXC** (che Docker inizialmente usava come backend). L'innovazione di Docker (2013) è stata l'**esperienza d'uso**: il formato di immagine a layer, il Dockerfile, il registry pubblico — ha reso i container *facili*.

> 💡 **Perché Go**: Docker passò al proprio componente `libcontainer` in Go (v0.9, 2014) sostituendo LXC. Le ragioni: **binario compilato statico** (singolo eseguibile autosufficiente, ideale per uno strumento di deployment, e "neutro" rispetto ai team frammentati tra Python/Ruby/Java); capacità di fare **syscall di basso livello** (`clone()`, `setns()`, namespace/cgroups) restando ergonomico e sicuro (niente gestione manuale della memoria come in C); **concorrenza nativa** (goroutine/channel) perfetta per un daemon che gestisce molti container.

## Architettura Docker Engine

Il Docker Engine è composto da tre componenti principali:

```
Client                         DOCKER_HOST                      Registry
docker build  ──────────────→  Docker daemon  ←──────────────  Images
docker pull                    │                                (Docker Hub)
docker run                     ├── Containers
                               └── Images
```

**daemon** — espone un'API REST, riceve istruzioni dal client e orchestra le operazioni.

**containerd** — gestisce il ciclo di vita dei container: avvio, arresto, pausa, disattivazione, cancellazione. Comunica col daemon via gRPC.

**runc** — CLI leggera, implementazione di riferimento dell'OCI (Open Container Initiative) runtime. Crea e avvia effettivamente i container invocando le system call (`clone()` coi flag di namespace, configurazione cgroups). Tra containerd e ogni runc c'è uno **shim**, che disaccoppia il container dal daemon: una volta avviato il container, runc termina e lo shim resta come genitore del processo → si può **riavviare/aggiornare il daemon senza uccidere i container in esecuzione**.

> Ruoli in una frase: **containerd è il *container manager*** (gestisce il ciclo di vita: crea, avvia, ferma, mette in pausa, cancella, supervisiona) — un runtime **di alto livello**; **runc è il *container runtime*** (esegue materialmente la creazione parlando col kernel, poi termina) — un runtime **di basso livello**. Stessa terminologia che ritorna in [[kubernetes]] (CRI/OCI).

**Perché gRPC tra daemon e containerd**: gRPC non è il *linguaggio* di Docker (quello è Go), ma il **protocollo di comunicazione interna** tra componenti separati. Le ragioni si collegano a [[grpc]]: contratto tipizzato via `.proto`, HTTP/2 con multiplexing (adatto a un daemon concorrente), protobuf compatto. 💡 Bella simmetria d'esame: **Docker usa gRPC internamente (daemon→containerd)** e **Kubernetes usa gRPC via la CRI** per parlare con containerd — stesso protocollo, agli stessi livelli dello stack (tutto nasce in ambito Google).

```
$ docker container run ...
     ↓ REST POST /vX.X/containers/create
  daemon
     ↓ gRPC client.NewContainer(...)
  containerd
     ↓
  shim → runc → container
```

## Immagini Docker

Un'immagine Docker **non è** un disco rigido virtuale né un filesystem tradizionale. È:

- Un **Union File System** (OverlayFS) a layer
- Ogni layer è **read-only** (identificato da hash SHA256)
- Il layer più in alto, aggiunto al momento del run, è il **thin R/W layer** del container
- L'immagine è fondamentalmente un **file compresso** con una gerarchia di profondità arbitraria
- Più container possono condividere gli stessi layer read-only dell'immagine base

```
┌──────────────────────────────┐
│  Thin R/W layer (container)  │  ← scrivibile, specifico per istanza
├──────────────────────────────┤
│  91e54dfb1179   0 B          │
│  d74508fb6632   1.895 KB     │  ← Image layers (read-only)
│  c22013c84729   194.5 KB     │
│  d3a1f33e8a5a   188.1 MB     │
│  ubuntu:15.04                │
└──────────────────────────────┘
```

Più container basati sulla stessa immagine condividono i layer R/O e hanno solo il proprio thin R/W layer separato.

### Come funziona lo Union/Overlay File System

Tre concetti da non confondere: **union filesystem** è la *categoria* astratta (un FS che fonde più layer impilati in un'unica vista); **OverlayFS** è l'*implementazione concreta* usata oggi da Docker (storicamente esistevano AUFS, devicemapper, btrfs); **rootfs** è il *risultato*, il filesystem radice che il container effettivamente vede. In una frase: *OverlayFS (un union filesystem) produce il rootfs del container.*

I tre tipi di layer in OverlayFS:
- **lowerdir** — i layer **inferiori, read-only** (possono essere molti, impilati): nel caso Docker sono i **layer dell'immagine**;
- **upperdir** — l'unico layer **superiore, read/write**: è il **thin R/W layer** del container;
- **merged** — la **vista fusa** risultante, ciò che il processo vede come proprio filesystem (il rootfs).

Le tre **regole di risoluzione** (analogia: lucidi trasparenti sovrapposti guardati dall'alto):
1. **Lettura** — si cerca il file **dall'alto verso il basso** e si restituisce la prima occorrenza: se lo stesso file esiste in upperdir e in un lowerdir, **vince l'upperdir** (il layer superiore "copre" l'inferiore);
2. **Scrittura su un file di un lowerdir read-only** — interviene il **copy-on-write**: il file viene prima copiato nell'upperdir (*copy-up*) e la modifica avviene sulla copia; l'originale nel lowerdir resta intatto (per questo più container possono condividere lo stesso layer immagine senza interferenze);
3. **Cancellazione di un file in un lowerdir** — non potendolo rimuovere davvero (è read-only), si crea un **whiteout file** nell'upperdir, un marcatore che "maschera" il file sottostante facendolo risultare inesistente in lettura.

Da queste regole discendono tutte le proprietà viste: condivisione efficiente dei lowerdir, immagini immutabili/"senza stato" (lo stato sta nell'upperdir per-container), container effimero (distruggerlo butta solo l'upperdir), avvio quasi istantaneo (si monta un overlay sui lowerdir esistenti + un upperdir vuoto). Si chiude il cerchio col Dockerfile: ogni `RUN`/`COPY`/`ADD` produce un **lowerdir**; l'immagine è la pila ordinata di lowerdir, il container aggiunge l'upperdir, e il merged attivato con `pivot_root` diventa il rootfs.

## Docker under the hood

Mettendo insieme i pezzi ([[linux-namespaces]] + OverlayFS + volumi), ecco come Docker realizza un container:
- il container ottiene il **proprio root filesystem** (`rootfs`): i layer R/O dell'immagine vengono montati in overlay (`mount -t overlay`) e il kernel passa al nuovo root con **`pivot_root`** — il filesystem dell'host è completamente **isolato** da quello del container (grazie al **mount namespace**);
- viene aggiunto un **layer Copy-on-Write** al primo avvio del container, che preserva le modifiche al rootfs finché il container non viene rimosso;
- i **pseudo-filesystem del kernel** sono montati privatamente per il container: `/proc` (richiede un nuovo **PID namespace**), `/sys` (sysfs), `/dev` (tmpfs);
- i **file di configurazione specifici del container** (`hostname`, `hosts`, `resolv.conf`) non possono stare nell'immagine (le immagini sono generiche) → vengono **bind-mountati** come file regolari (`mount --bind`); richiedono un nuovo **network namespace**;
- i **volumi** sono cartelle regolari sull'host **bind-mountate** nel container: i dati **sopravvivono** al singolo container e possono essere **condivisi** tra più container.

> 🎯 Esame: collegare i meccanismi — overlay/pivot_root per il filesystem, PID namespace per `/proc`, network namespace per la rete, volumi bind-mount per la persistenza dei dati oltre il ciclo di vita del container.

Quali meccanismi del kernel realizzano un container Docker?
?
OverlayFS+pivot_root per il rootfs, mount namespace per il filesystem, PID namespace per /proc, network namespace per la rete, cgroups per le risorse, volumi bind-mount per la persistenza.


## Docker Registry

Un **registro** contiene immagini Docker:
- Registro locale sullo stesso host
- **Docker Hub** — registro pubblico ufficiale
- Registro privato condiviso su docker.com

Il registry controlla dove vengono archiviate le immagini e gestisce l'intera pipeline di distribuzione.

## Dockerfile — direttive principali

Il Dockerfile definisce come costruire un'immagine layer per layer:

| Direttiva | Funzione |
|---|---|
| `FROM` | Crea un nuovo layer partendo dall'immagine specificata |
| `WORKDIR` | Cambia la working directory di default (la crea se non esiste) |
| `COPY` | Copia file dall'host nel filesystem del container |
| `RUN` | Esegue comandi durante il build, creando un nuovo layer sopra il precedente |
| `ENTRYPOINT` | Specifica l'eseguibile fisso lanciato all'avvio del container |
| `CMD` | Specifica i comandi/argomenti di default (sovrascritto se si passa un arg a `docker run`) |
| `EXPOSE` | Definisce le porte su cui l'app nel container è in ascolto (documentativo) |

> **ENTRYPOINT vs CMD**: `ENTRYPOINT` è il programma fisso; `CMD` sono gli argomenti di default. Il comando effettivo è la concatenazione `ENTRYPOINT + CMD`. Se si passa un argomento a `docker run immagine args...`, questo **sostituisce CMD** ma non ENTRYPOINT (per sostituire l'ENTRYPOINT serve il flag esplicito `--entrypoint`). Nel Dockerfile `ENTRYPOINT ["python3"]` + `CMD ["flask_app.py"]` significa: esegui sempre python3, con flask_app.py come script di default. Nota: **`EXPOSE` è solo documentazione** — non apre nessuna porta verso l'host; la pubblicazione reale avviene con `-p host:container` al run.

> **Istruzioni e layer / cache di build**: ogni istruzione del Dockerfile crea (concettualmente) un layer; nelle versioni moderne solo le istruzioni che **modificano il filesystem** (`FROM`, `RUN`, `COPY`, `ADD`) producono layer con contenuto, le altre (`CMD`, `ENTRYPOINT`, `EXPOSE`, `ENV`, `WORKDIR`, `LABEL`) generano solo **metadati** (storicamente comparivano come layer da 0 B). Docker **riusa i layer in cache** se l'istruzione e i file coinvolti non sono cambiati: per questo nell'esempio Flask si copia **prima** `requirements.txt` e si fa `pip install`, e **solo dopo** si copia il codice — se modifichi solo `flask_app.py`, la cache dei layer delle dipendenze resta valida e il rebuild è quasi istantaneo. Best practice: concatenare comandi correlati in un singolo `RUN` (`RUN apt-get update && apt-get install -y ...`) per non moltiplicare i layer. L'ordine delle istruzioni non è estetico: è ottimizzazione.

## Comandi CLI fondamentali

```bash
docker build -t nome_immagine .                           # costruisce immagine dal Dockerfile
docker run -it --name nome -p host:cont immagine          # avvia container interattivo
docker run -d --name nome -p host:cont immagine           # avvia in background
docker ps                                                 # lista container in esecuzione
docker ps -a                                              # tutti i container (anche fermi)
docker stop nome                                          # ferma un container
docker rm nome                                            # rimuove un container
docker images                                             # lista immagini disponibili
docker pull immagine                                      # scarica immagine dal registry
docker exec -it container bash                            # shell nel container in esecuzione
docker logs nome                                          # log stdout del container
```

## Esempio: Flask containerizzata

```python
# flask_app.py
from flask import Flask, request
import socket

app = Flask(__name__)

@app.route("/")
def index():
    return "Served from {} to {}".format(socket.gethostname(), request.remote_addr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
```

```dockerfile
FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY flask_app.py /app
ENTRYPOINT ["python3"]
CMD ["flask_app.py"]
```

```bash
docker build -t flask_image_hello_world .
docker run -it --name flask_app_container -p 5001:5001 flask_image_hello_world
```

## Come si usa nel corso

Docker è lo strumento di deployment per le applicazioni sviluppate durante il corso (Flask, gRPC server, MongoDB). Containerizzare un servizio rende il deploy indipendente dall'ambiente host e facilmente riproducibile.

## Connessioni

- [[virtualizzazione-container]] — motivazione e confronto VM vs container
- [[linux-namespaces]] — meccanismo di isolamento usato da Docker internamente
- [[cgroups]] — meccanismo di gestione risorse usato da Docker internamente
- [[docker-compose]] — per applicazioni multi-container
- [[docker-swarm]] — orchestrazione cluster Docker
- [[flask]] — esempio di applicazione containerizzata
- [[mongodb]] — esempio di servizio deployato via Docker

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
_Aggiornato: 2026-06-19 — MODULO 4 (slide 03 rilettura): sezione "Docker under the hood" (rootfs/pivot_root, copy-on-write, pseudo-fs /proc-/sys-/dev, config bind-mount, volumi); dettagli storici (Solomon Hykes, Moby)_
_Aggiornato: 2026-06-20 — MODULO 4 (appunti): OverlayFS interno (lowerdir/upperdir/merged + 3 regole lettura-CoW-whiteout), containerd=manager/runc=runtime + shim, perché gRPC interno + simmetria K8s CRI, storia container (chroot/jails/LXC) + perché Go, ENTRYPOINT+CMD concatenazione/--entrypoint/EXPOSE solo doc, cache di build_
