---
tipo: entità
categoria: strumento
---

## Cos'è

**Docker Swarm** è il sistema di orchestrazione cluster nativo integrato nel Docker Engine. Permette di gestire un insieme di istanze Docker come un'unica unità, distribuendo automaticamente i container sui nodi disponibili e garantendo la disponibilità dei servizi.

## Architettura

Uno swarm è composto da **host Docker in modalità swarm** che assumono uno dei seguenti ruoli:

**Manager** — gestiscono il join di nuovi nodi, mantengono lo stato globale del cluster e orchestrano il deployment dei servizi. I manager eleggono un **singolo leader** per le operazioni di orchestrazione.

**Worker** — ricevono ed eseguono i **task** assegnati dai manager. Su ogni nodo worker è in esecuzione un agente che riferisce sullo stato dei task assegnati.

Un nodo può essere contemporaneamente manager e worker.

### Algoritmo di consenso Raft

I nodi manager implementano l'**algoritmo di consenso Raft** per gestire lo stato globale del cluster in modo distribuito:
- Tollera fino a **(N-1)/2 fallimenti** di manager
- Richiede un **quorum** di (N/2)+1 membri per accordarsi sui valori
- Se il manager di uno swarm a singolo nodo si guasta, i servizi **continuano a funzionare**, ma è necessario creare un nuovo cluster per ripristinare il controllo

```
Raft consensus group
┌──────────────────────────────────────────────┐
│  Internal distributed state store            │
│  Manager ←→ Manager ←→ Manager               │
└──────────────────────────────────────────────┘
       ↓           ↓           ↓
Worker  Worker  Worker  Worker  Worker  Worker  Worker
                (Gossip network)
```

## Servizi, Task e Placement

### Servizio

Un **servizio** è la definizione dei task da eseguire sui nodi. Per ogni servizio si definisce lo **stato desiderato**:
- Numero di repliche
- Risorse di rete e storage disponibili
- Porte esposte verso l'esterno
- Vincoli di risorse e preferenze di placement

Docker Swarm lavora costantemente per **mantenere lo stato desiderato**: se un nodo worker diventa indisponibile, i task di quel nodo vengono automaticamente ripianificati su altri nodi.

### Task

Un **task** è l'**unità atomica di scheduling** in Docker Swarm:
- Implementa un container Docker e i comandi da eseguire al suo interno
- I manager assegnano i task ai worker in base al numero di repliche
- Una volta assegnato a un nodo, il task **non può spostarsi su un altro nodo**: viene eseguito su quel nodo o fallisce

### Tipi di servizio

**Servizio replicato** — il manager distribuisce un numero specifico di repliche tra i nodi disponibili, in base alla scala impostata nello stato desiderato.

**Servizio globale** — lo swarm esegue un task del servizio su **ogni nodo disponibile** nel cluster. Quando si aggiunge un nuovo nodo, gli viene automaticamente assegnato un task.

### Controllo del placement

Swarm fornisce meccanismi per controllare **dove** vengono schedulati i task:
- Servizio replicato o globale
- Riserva di memoria o CPU per un servizio
- **Vincoli di placement**: il servizio viene eseguito solo su nodi con una specifica etichetta
- **Preferenze di placement**: distribuzione uniforme dei task tra nodi appropriati

## Service Update

Swarm supporta aggiornamenti **online** della configurazione di rete e dei volumi legati a un servizio:
- Avvia nuovi container con la nuova configurazione
- Arresta automaticamente i container con la vecchia configurazione
- Gestisce **rollback** automatici in caso di fallimento

## Comandi principali

```bash
# Creazione dello swarm (sul nodo master)
docker swarm init --advertise-addr IP_NODO_MASTER

# Join allo swarm (sui nodi worker, con il comando generato da swarm init)
docker swarm join --token TOKEN_GENERATO IP_NODO_MASTER:2377

# Creazione di un servizio replicato
docker service create --replicas 3 --name mio_servizio \
  --publish 5001:5001 flask_image_hello_world

# Rimozione servizio
docker service rm mio_servizio

# Deploy stack da compose file (su Swarm)
docker stack deploy --compose-file=compose.yaml nome_stack
docker stack rm nome_stack

# Gestione disponibilità nodi
docker node update --availability drain IP_HOST    # simula nodo non disponibile
docker node update --availability active IP_HOST   # riattiva il nodo

# Uscire dallo swarm
docker swarm leave
```

## Esempio: Flask replicata con load balancing

```bash
docker service create --replicas 3 \
  --name flask_helloworld_service \
  --publish 5001:5001 \
  flask_image_hello_world
```

Le richieste GET verso il nodo manager vengono **bilanciate** automaticamente tra tutti i container in esecuzione. Ad ogni GET risponde uno dei 3 container, garantendo sia la distribuzione del carico (load balancing) sia l'**availability** del servizio in caso di guasto di uno dei nodi.

## Connessioni

- [[docker]] — base su cui si appoggia Swarm
- [[docker-compose]] — il compose.yaml è riutilizzabile con `docker stack deploy`
- [[kubernetes]] — alternativa più avanzata per orchestrazione a larga scala

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
