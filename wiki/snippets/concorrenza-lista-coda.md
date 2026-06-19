---
tipo: snippet
tecnologia: threading
linguaggio: python
---

# Boilerplate — Concorrenza su lista / coda condivisa (Python)

Modi per condividere una struttura dati tra thread (o processi) senza race condition. Caso tipico da prova: **produttore/consumatore con buffer limitato** (es. lista size 5). → [[threading]] [[gil]] [[strutture-dati]] [[processo-thread]]

> 🎯 Esame: il GIL **non** rende thread-safe le operazioni composte (`if len(buf) < N: buf.append(x)` sono due bytecode separati → race). Serve sempre sincronizzazione esplicita. → [[gil]]

---

## 1. `queue.Queue` — la via più semplice (già thread-safe)

Coda FIFO con lock interno. Da preferire quando basta passare item tra thread: niente lock manuali.

```python
from queue import Queue

q = Queue(maxsize=5)        # maxsize>0 → buffer limitato (bounded)

# Produttore
q.put(item)                 # blocca se piena finché si libera spazio
q.put(item, timeout=2)      # alza queue.Full dopo 2s
q.put_nowait(item)          # alza queue.Full subito se piena

# Consumatore
item = q.get()              # blocca se vuota finché arriva un item
q.task_done()               # segnala item processato (per q.join())

q.join()                    # blocca finché ogni put ha il suo task_done
```

Varianti: `LifoQueue` (stack), `PriorityQueue` (item = `(priorità, dato)`).

**Terminazione pulita** — sentinella (poison pill), una per consumatore:

```python
SENTINEL = None

def consumer():
    while True:
        item = q.get()
        if item is SENTINEL:
            q.task_done()
            break
        process(item)
        q.task_done()

# produttore a fine lavoro:
for _ in range(NUM_CONSUMERS):
    q.put(SENTINEL)
```

---

## 2. `list` + `threading.Lock` — mutua esclusione semplice

Quando serve una lista normale (indicizzazione, iterazione) e basta proteggere le sezioni critiche. **Non** gestisce l'attesa "piena/vuota": chi chiama su buffer pieno/vuoto deve fare polling (spreco CPU). Per produttore/consumatore preferire `Condition` (sotto).

```python
import threading

buf = []
lock = threading.Lock()

def append_safe(x):
    with lock:              # acquire + release automatici
        buf.append(x)

def pop_safe():
    with lock:
        if buf:             # controllo e pop nella STESSA sezione critica
            return buf.pop(0)
        return None
```

> ⚠️ Controllo e modifica devono stare nello stesso `with lock`. Separarli (`if buf:` fuori, `buf.pop()` dentro un altro lock) riapre la race.

`RLock` se la stessa funzione, già dentro il lock, ne richiama un'altra che riacquisisce → [[threading]].

---

## 3. `list` + `threading.Condition` — produttore/consumatore bounded buffer

**Pattern da prova** (sim-04, sim-11: lista size 5). La `Condition` unisce un lock + l'attesa su condizione: il thread rilascia il lock e dorme finché un altro lo `notify`. Niente busy-waiting.

```python
import threading

class BoundedBuffer:
    def __init__(self, size=5):
        self.buf = []
        self.size = size
        self.cond = threading.Condition()   # lock interno

    def produce(self, item):
        with self.cond:
            # while, NON if: al risveglio la condizione va riverificata
            while len(self.buf) >= self.size:
                self.cond.wait()             # rilascia il lock e dorme
            self.buf.append(item)
            self.cond.notify()               # sveglia un consumatore in attesa

    def consume(self):
        with self.cond:
            while len(self.buf) == 0:
                self.cond.wait()
            item = self.buf.pop(0)
            self.cond.notify()               # sveglia un produttore in attesa
            return item
```

> 🎯 Esame: tre punti chiave —
> 1. `while` e non `if` attorno a `wait()` (spurious wakeup + altri thread possono aver consumato la condizione prima di riacquisire il lock).
> 2. `wait()` rilascia il lock mentre dorme, lo riacquisisce al risveglio.
> 3. `notify()` sveglia 1 thread, `notify_all()` tutti. Con un solo tipo di attesa per lato basta `notify`; in dubbio `notify_all`.

Uso:

```python
b = BoundedBuffer(5)
threading.Thread(target=lambda: [b.produce(i) for i in range(20)]).start()
threading.Thread(target=lambda: [print(b.consume()) for _ in range(20)]).start()
```

---

## 4. `Semaphore` — conteggio slot pieni/vuoti

Alternativa alla `Condition` per il bounded buffer: due semafori contano slot liberi e item disponibili, un lock protegge la lista.

```python
import threading

buf = []
mutex = threading.Lock()
empty = threading.Semaphore(5)   # slot liberi (inizio: tutti)
full  = threading.Semaphore(0)   # item disponibili (inizio: nessuno)

def produce(x):
    empty.acquire()              # blocca se 0 slot liberi
    with mutex:
        buf.append(x)
    full.release()               # +1 item disponibile

def consume():
    full.acquire()               # blocca se 0 item
    with mutex:
        x = buf.pop(0)
    empty.release()              # +1 slot libero
    return x
```

> 💡 Connessione: `Semaphore(1)` ≈ `Lock`. La differenza: il semaforo non ha proprietario, può rilasciarlo un thread diverso da quello che l'ha acquisito — qui produttore e consumatore si rilasciano i semafori a vicenda.

---

## 5. Tra processi — `multiprocessing.Queue`

I thread condividono la memoria; i processi **no** (GIL aggirato ma niente stato condiviso). Serve una coda IPC. → [[multiprocessing]]

```python
from multiprocessing import Process, Queue

def worker(q):
    while True:
        item = q.get()
        if item is None:
            break
        process(item)

if __name__ == "__main__":
    q = Queue(maxsize=5)         # serializza via pickle dietro le quinte
    p = Process(target=worker, args=(q,))
    p.start()
    q.put("dato")
    q.put(None)                  # sentinella
    p.join()
```

Per una **lista** condivisa tra processi: `multiprocessing.Manager().list()` (proxy, più lento) oppure `multiprocessing.Array` (tipi C, dimensione fissa).

---

## Quale usare

| Scenario | Scelta |
|---|---|
| Passare item tra thread, nessun accesso casuale | `queue.Queue` |
| Buffer limitato produttore/consumatore (prova) | `list` + `Condition` |
| Lista con indicizzazione, sezioni critiche brevi | `list` + `Lock` |
| Bounded buffer con conteggio esplicito slot | `Semaphore` × 2 + `Lock` |
| Condivisione tra **processi** | `multiprocessing.Queue` / `Manager` |

> 🎯 Esame: se la traccia dice "lista condivisa di dimensione N tra produttori e consumatori" → `Condition` con `while`. Se dice solo "passa dati a un worker pool" → `queue.Queue`.

## Collegamenti

- [[threading]] — Lock, RLock, Semaphore, Event, Condition
- [[gil]] — perché le operazioni composte restano non atomiche
- [[multiprocessing]] — condivisione tra processi, IPC
- [[strutture-dati]] — liste, code in Python
- [[processo-thread]] — memoria condivisa thread vs isolamento processi
- [[java-sincronizzazione]] — controparte Java (`synchronized`, `wait`/`notify`)

## Fonti

- [[11-python-concurrency]], [[10-programmazione-concorrente-richiami]]
- svolgimenti sim-04 (lista + Condition), sim-11 (produttore/consumatore size 5)

_Aggiornato: 2026-06-18 — creazione snippet concorrenza lista/coda_
