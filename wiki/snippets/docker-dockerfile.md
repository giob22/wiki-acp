# Docker — Dockerfile, CLI e Compose

Riferimento rapido per Dockerfile, comandi Docker CLI e Docker Compose usati nel corso.

---

## Dockerfile — struttura tipo

```dockerfile
# Immagine base di partenza (crea il primo layer)
FROM python:3.10-alpine

# Directory di lavoro nel container (creata automaticamente se non esiste)
WORKDIR /app

# Copia dipendenze prima del codice (sfrutta la cache dei layer)
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Copia il codice sorgente
COPY flask_app.py /app

# Porta su cui il container è in ascolto (documentativo, non pubblica la porta)
EXPOSE 5001

# ENTRYPOINT: programma fisso (non sovrascrivibile da argomenti docker run)
ENTRYPOINT ["python3"]

# CMD: argomenti di default (sovrascritto se si passa un arg a docker run)
CMD ["flask_app.py"]
```

### Direttive

| Direttiva | Funzione |
|---|---|
| `FROM img` | Immagine base; crea il primo layer |
| `WORKDIR /path` | Imposta la working directory (la crea se non esiste) |
| `COPY src dst` | Copia file dall'host al filesystem del container |
| `RUN cmd` | Esegue cmd durante il build; crea un nuovo layer |
| `EXPOSE port` | Documenta la porta (non la pubblica — serve `-p` al run) |
| `ENTRYPOINT ["exec"]` | Eseguibile fisso all'avvio del container |
| `CMD ["arg"]` | Argomenti di default; ignorato se si passa un arg a `docker run` |
| `ENV KEY=value` | Variabile d'ambiente nel container |

---

## CLI — comandi fondamentali

```bash
# Build
docker build -t nome_immagine .
docker build -t nome_immagine -f path/al/Dockerfile .

# Run
docker run nome_immagine
docker run -it --name nome_container nome_immagine         # interattivo (stdin + tty)
docker run -d  --name nome_container nome_immagine         # detached (background)
docker run -p 5001:5001 nome_immagine                      # porta host:container
docker run --rm nome_immagine                              # rimuovi container al termine

# Stato
docker ps                          # container in esecuzione
docker ps -a                       # tutti (anche fermi)
docker images                      # immagini locali disponibili
docker logs nome_container         # log stdout del container
docker logs -f nome_container      # segui log in tempo reale

# Gestione
docker stop nome_container
docker start nome_container
docker rm nome_container
docker rmi nome_immagine

# Interazione con container in esecuzione
docker exec -it nome_container bash         # shell interattiva
docker exec nome_container comando          # esegui comando singolo

# Registry
docker pull ubuntu:22.04
docker push repo/immagine:tag
docker tag immagine repo/immagine:tag
```

---

## Docker Compose — comandi

```bash
# Avvia tutto lo stack (build + run)
docker compose up
docker compose up -d                         # background
docker compose -f compose.yaml up -d         # file specifico

# Stop e pulizia
docker compose down                          # ferma e rimuove container
docker compose down -v                       # rimuove anche i volumi

# Stato e log
docker compose ps
docker compose logs
docker compose logs -f nome_servizio         # segui log di un servizio
```

---

## compose.yaml — struttura tipo (Flask + MongoDB)

```yaml
services:
  web:
    build:
      context: app                 # directory contenente il Dockerfile
    ports:
      - '5001:5001'

  db:
    image: mongo:latest
    hostname: mongodb
    environment:
      - MONGO_INITDB_DATABASE=mydb
      - MONGO_INITDB_ROOT_USERNAME=root
      - MONGO_INITDB_ROOT_PASSWORD=secret
    ports:
      - 27017:27017
    volumes:
      - ./init-db.js:/docker-entrypoint-initdb.d/init-db.js:ro
```

---

## Docker Swarm — comandi

```bash
# Inizializzazione cluster (sul nodo master)
docker swarm init --advertise-addr IP_MASTER

# Join worker al cluster (comando generato da swarm init)
docker swarm join --token TOKEN_GENERATO IP_MASTER:2377

# Servizio replicato
docker service create --replicas 3 --name svc --publish 5001:5001 immagine

# Deploy stack da compose file
docker stack deploy --compose-file=compose.yaml nome_stack
docker stack rm nome_stack

# Gestione nodi
docker node update --availability drain IP_HOST    # drain (simula guasto)
docker node update --availability active IP_HOST   # riattiva

# Uscire dallo swarm
docker swarm leave
```

---

## compose.yaml con sezione deploy (per Swarm)

```yaml
services:
  web:
    image: flask_image_hello_world
    ports:
      - '5001:5001'
    deploy:
      replicas: 5
      restart_policy:
        condition: on-failure
        max_attempts: 3
        window: 120s
```

```bash
# Deploy su swarm tramite stack
docker stack deploy --compose-file=compose_with_stack.yaml nome_stack
```
