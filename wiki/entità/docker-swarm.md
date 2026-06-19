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

I nodi manager implementano l'**algoritmo di consenso Raft** per gestire lo stato globale del cluster in modo distribuito. I dettagli su quorum, fallimenti tollerati e comportamento in caso di guasto sono nella sezione [[#Tolleranza ai guasti]].

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

## Tolleranza ai guasti

In uno swarm esistono **due tipi di guasto distinti**, gestiti da meccanismi diversi. Confonderli è l'errore tipico.

### Guasto dei manager → quorum Raft

I manager mantengono lo **stato del cluster** (leader corrente, servizi, repliche desiderate, placement). Essendo più di uno, devono restare d'accordo su quale sia lo stato: lo fanno con l'algoritmo di consenso **Raft**, che accetta una scrittura sullo stato solo se la **maggioranza** dei manager è d'accordo (**quorum**).

- Quorum richiesto = **(N/2)+1** manager vivi
- Fallimenti tollerati = **(N-1)/2**

| N manager | Quorum | Fallimenti tollerati |
|-----------|--------|----------------------|
| 1         | 1      | 0                    |
| 3         | 2      | 1                    |
| 5         | 3      | 2                    |
| 7         | 4      | 3                    |

La maggioranza serve a evitare lo **split-brain**: se il cluster si spezzasse in due gruppi, solo quello che possiede più della metà dei manager può agire; l'altro si blocca, impedendo decisioni contraddittorie.

**Se si perde il quorum** (es. 3 manager, ne muoiono 2):
- Il cluster **non può più orchestrare**: niente nuovi servizi, reschedule, scaling o join di nodi.
- I container **già in esecuzione continuano a funzionare**: si ferma il piano di controllo (il "cervello"), non il piano dati.
- Recupero: riportare online abbastanza manager da ricostituire il quorum.

Caso limite (swarm a singolo manager che si guasta): i servizi continuano a girare, ma il controllo è perso ed è necessario **creare un nuovo cluster** per ripristinarlo.

> 🎯 Esame: i manager si tengono sempre in numero **dispari** (3, 5, 7). Passare da 3 a 4 non aumenta la tolleranza (resta 1 fallimento), aggiunge solo un nodo da coordinare.

### Guasto dei worker → reschedule

Meccanismo **completamente diverso**: i worker non partecipano a Raft e non votano nulla. Ricevono ed eseguono i task assegnati dai manager.

Quando un worker si guasta, i manager rilevano che lo stato desiderato non è più rispettato (mancano repliche) e **ripianificano i task** sui nodi ancora disponibili. Poiché un task, una volta assegnato a un nodo, **non migra** (vedi [[#Task]]), non viene spostato ma ne viene **creato uno nuovo** altrove finché non si torna al numero di repliche richiesto.

> 💡 Connessione: quorum/Raft protegge la sopravvivenza del **controllo** del cluster (riguarda solo i manager); il reschedule protegge la sopravvivenza dei **servizi** (riguarda i worker). Un nodo che è insieme manager e worker è soggetto a entrambe le logiche.

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

Swarm supporta aggiornamenti **online** della configurazione (di rete, dei volumi, dell'immagine) legata a un servizio:
- Avvia nuovi container con la nuova configurazione
- Arresta automaticamente i container con la vecchia configurazione
- Gestisce **rollback** automatici in caso di fallimento

È il meccanismo del **rolling update**: aggiornando le repliche un po' alla volta, il servizio resta disponibile durante l'aggiornamento; in caso di problemi si torna alla configurazione precedente con rollback. Più in generale Swarm lavora per **reconciliation**: confronta di continuo lo stato reale con lo stato desiderato dichiarato e agisce per riallinearli (`verify: Service converged` è il lessico di questo stato — la realtà ha raggiunto la dichiarazione).

## Comandi principali

```bash
# Creazione dello swarm (sul nodo master)
docker swarm init --advertise-addr IP_NODO_MASTER

# Join allo swarm (sui nodi worker, con il comando generato da swarm init)
# la porta 2377 è quella di gestione del cluster
docker swarm join --token TOKEN_GENERATO IP_NODO_MASTER:2377

# Creazione di un servizio replicato
docker service create --replicas 3 --name mio_servizio \
  --publish 5001:5001 flask_image_hello_world

# Rimozione servizio
docker service rm mio_servizio

# Deploy stack da compose file (su Swarm)
docker stack deploy --compose-file=compose.yaml nome_stack
docker stack rm nome_stack

# Gestione disponibilità nodi (drain = anche procedura standard di manutenzione pianificata)
docker node update --availability drain IP_HOST    # svuota il nodo (simula guasto / manutenzione)
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

Le richieste GET verso il nodo manager vengono **bilanciate** automaticamente tra tutti i container in esecuzione. Ad ogni GET risponde uno dei 3 container, garantendo sia la distribuzione del carico (load balancing) sia l'**availability** del servizio in caso di guasto di uno dei nodi. Poiché ogni replica stampa il proprio `socket.gethostname()` (= ID del container), il round-robin diventa visibile come risposte da hostname diversi.

> 💡 Il meccanismo sottostante è l'**ingress routing mesh**: la porta pubblicata è aperta su **tutti** i nodi dello swarm, e qualunque nodo riceva la richiesta la inoltra (via **IPVS**, IP Virtual Server) a una replica qualsiasi, anche su un altro nodo. Per questo si può colpire un nodo qualsiasi e ottenere comunque il bilanciamento.

## Connessioni

- [[docker]] — base su cui si appoggia Swarm
- [[docker-compose]] — il compose.yaml è riutilizzabile con `docker stack deploy`
- [[kubernetes]] — alternativa più avanzata per orchestrazione a larga scala

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
_Aggiornato: 2026-06-19 — nuova sezione "Tolleranza ai guasti": consolidato quorum Raft (manager) vs reschedule (worker), su domanda dell'utente_
_Aggiornato: 2026-06-20 — MODULO 4 (appunti): ingress routing mesh + IPVS (meccanismo load balancing), rolling update + reconciliation/"Service converged", porta 2377, drain anche per manutenzione_
