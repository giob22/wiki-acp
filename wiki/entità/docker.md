---
tipo: entità
categoria: strumento
---

## Cos'è

**Docker** è un motore di container scritto in Go, basato su Linux container, che permette di eseguire applicazioni in container isolati e portabili. Fondato come progetto di Docker Inc. (ex dotCloud, 2010 → rinominata Docker Inc. nel 2013).

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

**runc** — CLI leggera, implementazione di riferimento dell'OCI (Open Container Initiative) runtime. Crea e avvia effettivamente i container.

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

> **ENTRYPOINT vs CMD**: `ENTRYPOINT` è il programma fisso; `CMD` sono gli argomenti di default. Se si passa un argomento a `docker run`, `CMD` viene ignorato ma `ENTRYPOINT` no. Nel Dockerfile `ENTRYPOINT ["python3"]` + `CMD ["flask_app.py"]` significa: esegui sempre python3, con flask_app.py come script di default.

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
