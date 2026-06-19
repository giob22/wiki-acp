---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, gil, oop]
---

## Definizione

Il modulo `threading` di Python fornisce un'API per creare e gestire thread a livello kernel (KLT). Utile per workload **I/O-bound** (networking, file). Non adatto per CPU-bound a causa del [[gil]].

## Spiegazione

**Creazione thread (approccio funzione)**:
```python
import threading

def worker(nome):
    print(f"Thread {nome} partito")

t = threading.Thread(target=worker, args=("T1",))
t.start()    # avvia il thread
t.join()     # aspetta la terminazione
t.is_alive() # → False dopo join
```

**Creazione thread (approccio classe)**:
```python
class MioThread(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def run(self):  # override di run()
        print(f"Thread {self.nome} in esecuzione")

t = MioThread("T1")
t.start()
t.join()
```

**Thread daemon**:
```python
t = threading.Thread(target=worker)
t.daemon = True   # deve essere impostato PRIMA di start()
t.start()
# processo termina anche se t è ancora in esecuzione
```
- Thread non-daemon: il processo aspetta la loro terminazione prima di uscire
- Thread daemon: muore automaticamente con il processo principale

**Sincronizzazione — Lock**:
```python
lock = threading.Lock()

def sezione_critica():
    with lock:          # acquisisce e rilascia automaticamente
        risorsa_condivisa += 1
```

**Tipi di primitive di sincronizzazione**:
- `Lock` — mutex semplice
- `RLock` — reentrant lock (stesso thread può acquisirlo N volte)
- `Semaphore(n)` — permette accesso a massimo N thread contemporaneamente
- `Event` — flag condiviso per notifica (set/wait/clear)
- `Condition` — attesa su condizione (wait/notify)

**Thread-local storage**:
```python
local_data = threading.local()
local_data.valore = 42   # ogni thread ha la propria copia
```

**Queue thread-safe** (da modulo `queue`):
```python
from queue import Queue
q = Queue()
q.put(item)      # produttore
item = q.get()   # consumatore — blocca se vuota
```

> 🎯 Esame: Come creare un thread, differenza daemon/non-daemon, come usare Lock, perché il threading non scala su CPU-bound.

## Perché importa

Threading è usato nel corso per server gRPC concorrenti, server socket multi-client, consumer STOMP.

## Connessioni

- [[gil]] — limita il parallelismo su CPU-bound
- [[processo-thread]] — differenza thread/processo
- [[multiprocessing]] — alternativa per CPU-bound
- [[socket]] — server socket usano threading per gestire più client

## Fonti

- [[11-python-concurrency]]
- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-04 — ingest iniziale_
