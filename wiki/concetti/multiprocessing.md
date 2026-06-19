---
tipo: concetto
importanza_esame: media
prerequisiti: [processo-thread, gil]
---

## Definizione

Il modulo `multiprocessing` di Python crea processi separati — ognuno con il suo interprete Python e il suo GIL — consentendo **vero parallelismo** su macchine multicore. È la soluzione per workload CPU-bound.

## Spiegazione

**Perché multiprocessing invece di threading per CPU-bound**:
- Ogni processo ha il proprio GIL → parallelismo reale su N core
- Overhead maggiore rispetto ai thread (fork del processo, IPC per comunicazione)

**API base**:
```python
from multiprocessing import Process, Queue, Pool

def worker(x):
    return x ** 2

# Processo singolo
p = Process(target=worker, args=(4,))
p.start()
p.join()

# Pool di processi
with Pool(processes=4) as pool:
    risultati = pool.map(worker, [1, 2, 3, 4])
```

**Comunicazione tra processi** (IPC):
```python
from multiprocessing import Queue
q = Queue()
q.put(42)     # processo produttore
val = q.get() # processo consumatore
```

La classe `Process` ha **metodi equivalenti** a `threading.Thread`: costruttore con stessa firma, `start()`, `run()`, `join(timeout=None)`, `is_alive()`. Si può creare un processo passando un *callable* o estendendo la classe `Process`.

**`concurrent.futures`** — astrazione unificata su thread e processi:
```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

with ProcessPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(worker, x) for x in range(8)]
    risultati = [f.result() for f in futures]
```

### Start method — come viene avviato un processo

A seconda della piattaforma `multiprocessing` supporta **tre modi** per avviare un processo. Si imposta con `mp.set_start_method("spawn")` (chiamabile **una sola volta** per esecuzione, come prima istruzione) oppure ottenendo un contesto con `mp.get_context('spawn')`. Metodi: `spawn`, `fork`, `forkserver`.

**spawn** (default su Windows e macOS, disponibile ovunque, **il più lento**):
- Il processo padre avvia un **nuovo interprete Python** per ogni figlio e **re-importa il modulo principale**
- Il figlio eredita **solo le risorse necessarie** ed esegue `run()`
- Trasferisce al figlio solo ciò che è esplicitamente necessario tramite **pickling** (serializzazione): args/kwargs, l'oggetto funzione target, oggetti condivisi espliciti (Queue, Pipe...). **Non** trasferisce variabili globali, stato della memoria, file aperti
- ⚠️ Poiché re-importa il modulo, la creazione dei processi **deve stare dentro `if __name__ == "__main__":`** altrimenti `RuntimeError` (bootstrapping non terminato)

**fork** (solo Unix, default fino a Python 3.13):
- Usa la system call `os.fork()` per avviare il figlio **senza re-importare** il modulo principale
- Il figlio **eredita tutte le risorse del padre** (file descriptor, lock, socket...); l'immagine del processo è duplicata con **copy-on-write**
- Solo il **thread running** del padre è attivo nel figlio (fork crea un figlio single-thread)
- È considerata **unsafe**: i lock acquisiti da altri thread al momento della fork restano acquisiti → potenziali deadlock
- Non richiede l'idiom `if __name__ == "__main__":` (non re-importa); le variabili globali del padre **sono visibili** nel figlio

**forkserver** (Unix con passaggio di file descriptor, **default da Python 3.14**):
- Viene creato (tramite spawn) un **server process single-threaded**; quando serve un nuovo processo il padre chiede al server di fare la fork
- Le risorse non necessarie non vengono ereditate; essendo il server single-threaded, **la fork è safe**

### Scambio e condivisione di oggetti tra processi

I processi non condividono memoria: servono **canali di comunicazione**. `multiprocessing` offre due canali, entrambi **thread/process-safe**:

**Pipe** — `Pipe([duplex])` ritorna una coppia di oggetti `Connection (conn1, conn2)`, gli endpoint:
- `duplex=True` (default) → bidirezionale; `False` → `conn1` solo riceve, `conn2` solo invia
- `send(obj)` invia, `recv()` riceve (**bloccante** se non ci sono oggetti)
- ⚠️ i dati si corrompono se due processi usano lo **stesso** endpoint; nessun rischio con endpoint diversi

**Queue** — `Queue([maxsize])`, una *process shared queue* FIFO implementata tramite pipe + lock/semafori:
- `put(item, block=True, timeout=None)` / `put_nowait(item)`; al raggiungimento di `maxsize` il `put` blocca (o solleva `Full`)
- `get(block=True, timeout=None)` / `get_nowait()`; su coda vuota blocca (o solleva `Empty`)
- `qsize()`, `empty()`, `full()`
- Varianti: `SimpleQueue` (FIFO senza limiti), `LifoQueue` (pila), `JoinableQueue` (aggiunge `task_done()` e `join()`)

**Shared Memory** — per condividere dati semplici tra processi senza canali:
- Oggetti `Value(typecode_or_type, *args, lock=True)` e `Array(typecode_or_type, size_or_initializer, *, lock=True)`, **process- e thread-safe**
- Sfruttano il modulo **`ctypes`** (tipi compatibili col C); es. `'d'`=`c_double`, `'i'`=`c_int`
- `lock=True` (default) crea un `RLock` per sincronizzare gli accessi; con `lock=False` gli accessi non sono protetti

### Il modulo `multiprocess`

Fork del modulo `multiprocessing` (**supporta i notebook Jupyter**). Estende `multiprocessing` con una serializzazione migliorata basata su **`dill`** (invece di `pickle`), permettendo di serializzare più tipi di oggetti.

**Confronto threading vs multiprocessing**:

| | threading | multiprocessing |
|---|---|---|
| GIL | Soggetto | Aggiramento |
| Memoria condivisa | Sì | No (IPC) |
| Overhead | Basso | Alto |
| Utile per | I/O-bound | CPU-bound |
| Comunicazione | Variabili condivise | Queue, Pipe |

> 🎯 Esame: "Quando usare multiprocessing invece di threading? Perché?"

## Perché importa

Il multiprocessing è la risposta Python al GIL per calcolo parallelo. Comprendere la differenza con threading è fondamentale.

## Connessioni

- [[gil]] — motivo per cui multiprocessing esiste
- [[threading]] — alternativa per I/O-bound; stesse primitive di sincronizzazione (Lock, Condition...)
- [[processo-thread]] — ogni processo ha il suo PCB e spazio di indirizzamento
- [[produttore-consumatore]] — la `Queue` di multiprocessing implementa direttamente produttori/consumatori multipli
- [[concorrenza-parallelismo]] — multiprocessing dà parallelismo reale (limitato da [[legge di Amdahl|concorrenza-parallelismo]])

## Fonti

- [[11-python-concurrency]]
- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-04 — ingest iniziale_
_Aggiornato: 2026-06-19 — start method (spawn/fork/forkserver con pickling, __main__, copy-on-write, safe/unsafe), Process class, Pipe, Queue (+ varianti), Shared Memory (Value/Array/ctypes), modulo multiprocess (dill); da slide 11_
