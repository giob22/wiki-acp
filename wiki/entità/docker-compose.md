---
tipo: entità
categoria: strumento
---

## Cos'è

**Docker Compose** è uno strumento per il deploy di applicazioni **multi-container** tramite un file di specifica YAML. Risolve il problema di dover costruire, avviare e collegare manualmente ogni container di un'applicazione composta da più servizi.

## Problema che risolve

Senza Docker Compose, per deployare un'applicazione multi-container occorre:
1. Fare il build e il run di ogni container separatamente
2. Collegare manualmente i container per la comunicazione di rete
3. Gestire manualmente le dipendenze e l'ordine di avvio

Docker Compose centralizza tutto in un **file `compose.yaml`** e permette di avviare l'intero stack con un singolo comando.

## Struttura del compose.yaml

```yaml
services:
  app:
    build: .                        # usa Dockerfile nella directory corrente
    command: python -u app.py       # sovrascrive CMD del Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - .:/app                      # mount point host → container
    links:
      - db                          # collegamento di rete al servizio db

  db:
    image: mongo:latest             # usa immagine preesistente dal registry
    hostname: test_mongodb
    environment:
      - MONGO_INITDB_DATABASE=animal_db
      - MONGO_INITDB_ROOT_USERNAME=root
      - MONGO_INITDB_ROOT_PASSWORD=pass
    volumes:
      - ./init-db.js:/docker-entrypoint-initdb.d/init-db.js:ro
    ports:
      - 27017:27017
```

### Chiavi principali

| Chiave | Funzione |
|---|---|
| `build` | Configurazione di build (Dockerfile); può includere `context` per specificare percorso o URL git |
| `command` | Sovrascrive il CMD predefinito dell'immagine |
| `ports` | Espone le porte nel formato `host:container` |
| `volumes` | Mount points del filesystem host accessibili dal container |
| `links` | Collegamento di rete a un altro servizio |
| `image` | Immagine dal registry da cui avviare il container |
| `environment` | Variabili d'ambiente da impostare nel container |

## Comandi principali

```bash
# Installazione su Linux
sudo apt-get install docker-compose-plugin

# Avvia tutti i container (build + run)
docker compose up
docker compose up -d                    # modalità daemonized (background)
docker compose -f compose.yaml up -d    # specificando file non standard

# Ferma e distrugge tutti i container
docker compose down

# Lista container del progetto corrente
docker compose ps

# Log del progetto corrente
docker compose logs
docker compose logs -f nome_servizio    # segue i log di un servizio specifico
```

## Supporto a Docker Swarm

Docker Compose ha supporto nativo per [[docker-swarm]]: lo stesso `compose.yaml` può essere usato con `docker stack deploy` per il deploy su un cluster Swarm, aggiungendo una sezione `deploy` nel file YAML.

```yaml
services:
  web:
    image: flask_image_hello_world
    deploy:
      replicas: 5
      restart_policy:
        condition: on-failure
        max_attempts: 3
        window: 120s
```

## Come si usa nel corso

Utile per deployare stack completi come Flask + MongoDB in un unico comando, riproducibile su qualsiasi macchina con Docker installato.

## Connessioni

- [[docker]] — strumento base su cui si appoggia Compose
- [[docker-swarm]] — Compose file riutilizzabile per orchestrazione cluster con `docker stack deploy`
- [[flask]] — esempio di servizio deployato via Compose
- [[mongodb]] — esempio di servizio dipendente

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
