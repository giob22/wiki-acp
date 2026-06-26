---
tipo: concetto
importanza_esame: alta
prerequisiti: [semaforo, monitor]
---

#flashcards/acp

## Definizione

Il **problema produttore/consumatore** è il problema classico di **cooperazione** tra processi concorrenti. Due categorie di processi condividono una risorsa (buffer):
- **Produttori** — depositano un messaggio sulla risorsa condivisa
- **Consumatori** — prelevano il messaggio dalla risorsa condivisa

## Spiegazione

### Vincoli

- Il produttore **non può produrre** un nuovo messaggio prima che un consumatore abbia prelevato il precedente (buffer pieno)
- Il consumatore **non può prelevare** finché un produttore non ha depositato (buffer vuoto)

### Differenza con la mutua esclusione

Pur esistendo un (potenziale) problema di mutua esclusione nell'uso del buffer comune, la soluzione **impone un ordinamento** nelle operazioni dei due processi: produttori e consumatori devono **coordinarsi** per segnalare rispettivamente l'avvenuto **deposito** e **prelievo**. È quindi **cooperazione** (sincronizzazione diretta), non solo competizione.

> 🎯 Esame: è il prototipo della **condition synchronization**: un'operazione (prelievo) va differita finché la risorsa non è in stato appropriato (non vuota).

Di quale problema è prototipo il produttore-consumatore?
?
Della condition synchronization: un'operazione (prelievo) va differita finché la risorsa non è in stato appropriato (buffer non vuoto/non pieno).


### Soluzioni

- Con **semafori**: un mutex per la mutua esclusione sul buffer + due semafori contatori (`empty`, `full`) per coordinare deposito/prelievo
- Con **monitor** + variabili condition: il `while (!condizione) wait_cond()` differisce produttore/consumatore finché il buffer non è in stato appropriato → vedi [[monitor]]
- In **Python**: con `threading.Condition` (pattern `while + wait()` / `notify()`), oppure con `queue.Queue` (thread-safe), o `multiprocessing.Queue` tra processi
- In **Java**: con `synchronized` + `wait()`/`notify()`, oppure `BlockingQueue`

## Il problema dei Lettori/Scrittori

Variante correlata, due categorie di processi su una risorsa condivisa:
- **Lettori** — leggono la risorsa
- **Scrittori** — scrivono la risorsa

Vincoli:
1. I **lettori** possono accedere **contemporaneamente** alla risorsa
2. Gli **scrittori** hanno accesso **esclusivo**
3. Lettori e scrittori si **escludono mutuamente**

> 💡 Connessione: a differenza della pura mutua esclusione (un solo accesso), qui si ammette **concorrenza tra lettori** ma esclusività per gli scrittori — è il modello dietro i lock read-write.

## Perché importa

È lo schema ricorrente nelle prove pratiche del corso (vedi [[pattern-esame]]): un server riceve dati (produttore), li mette in una struttura condivisa, un altro thread/processo li consuma. Compare con buffer a dimensione fissa (es. lista size 5).

## Connessioni

- [[semaforo]] — soluzione con mutex + semafori contatori
- [[monitor]] — soluzione con condition variables e ordinamento di accesso
- [[threading]] — `Condition`, `queue.Queue`
- [[multiprocessing]] — `Queue` implementa direttamente produttori/consumatori multipli
- [[pattern-esame]] — pattern produttore/consumatore nelle prove pratiche

## Fonti

- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-19 — pagina creata da slide 10 (produttore/consumatore: vincoli, differenza con mutua esclusione, soluzioni; problema lettori/scrittori)_
