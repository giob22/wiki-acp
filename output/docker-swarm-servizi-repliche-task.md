# Docker Swarm — Servizio, repliche, task e container

> Nota di lettura (treno/iPad). Chiarisce la relazione tra la *definizione di un
> servizio*, il *numero di repliche*, i *task* e i *container* in Docker Swarm.

---

## Il dubbio di partenza

> La definizione di un servizio in Docker Swarm consiste nella specifica dello
> *stato desiderato* oppure anche dei *task* da eseguire nel cluster?

Risposta breve: **la definizione di un servizio specifica lo stato desiderato.
I task NON li definisci tu** — sono ciò che lo swarm genera e mantiene per
realizzare quello stato desiderato.

Sono due livelli distinti:

- **Cosa definisci tu** (il servizio = stato desiderato): il *cosa* vuoi, non il
  *come*. Immagine, comando, numero di repliche, rete, porte, vincoli di placement.
- **Cosa fa lo swarm** (i task): a partire dalla tua definizione, i manager creano
  i **task** necessari. Il task è l'unità atomica di scheduling: incapsula un
  container e i comandi da eseguirvi, e viene assegnato a un nodo worker.

Catena: **servizio (stato desiderato) → i manager generano N task → ogni task
viene schedulato su un worker → il worker esegue il container.**

---

## Come si imposta il numero di repliche

**Da riga di comando, alla creazione del servizio:**
```bash
docker service create --replicas 3 --name mio_servizio \
  --publish 5001:5001 flask_image_hello_world
```

**Scalando un servizio già esistente:**
```bash
docker service scale mio_servizio=5
```

**Nel compose.yaml (deploy con `docker stack deploy`):**
```yaml
services:
  web:
    image: flask_image_hello_world
    ports:
      - "5001:5001"
    deploy:
      replicas: 3
```

---

## "Il numero di repliche riguarda il singolo task?" → Sì

**Una replica = un task = un'istanza di container in esecuzione.**
Sono la stessa cosa vista da tre angolazioni:

- **replica** — il termine che usi tu quando dichiari "quante ne voglio"
- **task** — il nome che lo swarm dà a ciascuna di quelle istanze quando le crea
  e le schedula su un nodo
- **container** — ciò che il task fa girare concretamente sul worker

Quindi `--replicas 3` significa esattamente: *"desidero che nel cluster ci siano
3 istanze (3 task) in esecuzione di questo servizio"*. Lo swarm crea 3 task, li
distribuisce sui nodi disponibili, e mantiene quel numero nel tempo (se un task
muore, ne ricrea uno per tornare a 3).

---

## "La configurazione del container è dentro la specifica?" → Sì

Qui sta il pezzo chiave: nella specifica del servizio **definisci la
configurazione del container una sola volta**, come una sorta di *template*.

La specifica contiene:
- l'**immagine** (es. `flask_image_hello_world`)
- il **comando** da eseguire nel container
- variabili d'ambiente, **porte** esposte, volumi/mount, vincoli di placement

Lo swarm prende quel singolo template e lo **"timbra" N volte**, creando N task
identici. Non definisci 3 configurazioni: ne definisci **una**, e dici quante
copie vuoi.

---

## Schema mentale completo

```
SERVIZIO (la tua dichiarazione)
├── template del container: immagine, comando, env, porte   ← config, una volta
└── stato desiderato: replicas = 3                          ← quante copie
        │
        ▼  lo swarm genera
   ┌────────┬────────┬────────┐
   │ Task 1 │ Task 2 │ Task 3 │   ← un task per replica
   └────────┴────────┴────────┘
       │        │        │
   container container container   ← ogni task = 1 container in esecuzione
   (node A)  (node B)  (node A)
```

Riformulando in modo preciso: con il parametro di scala dici *"voglio N istanze
(task/repliche) del container descritto nel template del servizio"*. Il **template
del container vive dentro la specifica del servizio**; il numero di repliche dice
quante volte istanziarlo.

---

## Nota sul vocabolario (importante per l'orale)

Il **task** è l'unità *atomica* di scheduling e **non migra**: una volta assegnato
a un nodo, o gira lì o fallisce. Se fallisce, lo swarm non sposta quel task, ma ne
**crea uno nuovo** (magari altrove) per ripristinare il conteggio di repliche
desiderato.

Per questo "replica" e "task" a volte sembrano sfumare l'uno nell'altro:
- la **replica** è il *posto logico* da riempire (lo stato desiderato dice
  "3 posti")
- il **task** è l'*istanza concreta* che riempie quel posto in un dato momento

È lo stesso meccanismo di *reconciliation loop* che ritrovi anche in Kubernetes:
dichiari lo stato desiderato, il sistema lavora di continuo per farlo combaciare
con lo stato reale.

---

## Tipi di servizio (per completezza)

- **Servizio replicato** — il manager distribuisce un numero specifico di repliche
  tra i nodi (è il caso di `--replicas N`).
- **Servizio globale** — un task del servizio su **ogni** nodo disponibile; quando
  si aggiunge un nuovo nodo, gli viene assegnato automaticamente un task. (Non usa
  `--replicas`; si imposta con `--mode global`.)

---

_Fonte: pagina wiki `wiki/entità/docker-swarm.md` (slide 03 — Service Deployment
& Containers). File di lettura creato il 2026-06-19._
