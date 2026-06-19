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

**`concurrent.futures`** — astrazione unificata su thread e processi:
```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

with ProcessPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(worker, x) for x in range(8)]
    risultati = [f.result() for f in futures]
```

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
- [[threading]] — alternativa per I/O-bound
- [[processo-thread]] — ogni processo ha il suo PCB e spazio di indirizzamento

## Fonti

- [[11-python-concurrency]]
- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-04 — ingest iniziale_
