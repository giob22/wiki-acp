---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, interprete-python]
---

#flashcards/acp

## Definizione

Il **GIL (Global Interpreter Lock)** è un mutex interno a CPython che garantisce che **un solo thread alla volta** esegua bytecode Python — anche su macchine multicore. È uno dei limiti più discussi di CPython.

## Spiegazione

**Perché esiste**:
CPython gestisce la memoria con reference counting. Senza un lock globale, due thread potrebbero modificare il contatore di riferimenti contemporaneamente → corruzione della memoria. Il GIL risolve questo con un'unica lock globale.

**Conseguenze**:
- Su macchine multicore, i thread Python **non** eseguono in parallelo (solo concorrentemente)
- Il GIL viene rilasciato durante operazioni I/O (file, rete, socket) — il thread si "blocca" e cede il controllo
- Il GIL viene rilasciato ogni N bytecode istruzioni (check interval) per permettere il context switch

**Implicazioni pratiche**:

| Tipo workload | Threading utile? | Alternativa |
|---|---|---|
| I/O-bound (rete, file, DB) | Sì — GIL rilasciato durante I/O | — |
| CPU-bound (calcolo) | No — GIL non rilasciato | `multiprocessing` |

**Workaround**:
- **`multiprocessing`**: ogni processo ha il suo interprete Python e il suo GIL — parallelismo reale
- **`concurrent.futures.ProcessPoolExecutor`**: astrazione su multiprocessing
- Estensioni C (NumPy, SciPy) rilasciano il GIL internamente → parallelismo per operazioni numeriche

**Vantaggi del GIL** (perché esiste ed è rimasto):
- Permette di rendere facilmente multi-threaded l'interprete CPython, **a scapito del parallelismo**
- Dovendo gestire un solo lock, **migliora le performance degli applicativi single-thread**
- Le **librerie C non thread-safe** possono essere integrate facilmente

**Svantaggi del GIL**:
- Riduce il livello di parallelismo ottenibile su macchine multiprocessore
- A parità di workload **CPU-bound, un'applicazione multithreaded sarà più lenta di una multiprocess**
- Impatta principalmente i task CPU-bound; viene rilasciato per i task I/O-bound

**Il GIL oggi** (slide aggiornate):
- In **CPython vanilla** non è possibile disabilitare il GIL a runtime
- In **Python 3.13** esiste una build *free-threaded* in cui il GIL è disabilitato
- Da **Python 3.14** questa build è supportata ufficialmente, **ma resta opzionale** (non default)
- Si ottiene compilando l'interprete con l'opzione `--disable-gil`
- I tentativi passati di rimuovere il GIL fallirono per: calo di performance single-thread, aumento di complessità dell'interprete, necessità di modificare tutte le estensioni C che sfruttano il GIL

> 🎯 Esame: "Cos'è il GIL? Per quali workload il threading Python è utile nonostante il GIL? Perché un'app CPU-bound multithread è più lenta della stessa multiprocess?"

Cos'è il GIL e perché un'app CPU-bound multithread è più lenta della multiprocess?
?
Mutex di CPython: un solo thread esegue bytecode alla volta. Threading utile per I/O-bound (GIL rilasciato durante I/O); per CPU-bound serve il multiprocessing (un interprete+GIL per processo → parallelismo reale).


## Perché importa

Il GIL è la ragione principale per cui il threading Python non scala su CPU-bound. Capirlo è essenziale per scegliere la giusta strategia di concorrenza.

## Connessioni

- [[threading]] — soggetto al GIL
- [[multiprocessing]] — aggiramento del GIL
- [[interprete-python]] — il GIL è specifico di CPython
- [[concorrenza-parallelismo]] — il GIL fa sì che il threading Python dia concorrenza ma non parallelismo

## Fonti

- [[10-programmazione-concorrente-richiami]]
- [[11-python-concurrency]]

_Aggiornato: 2026-06-04 — ingest iniziale_
_Aggiornato: 2026-06-19 — vantaggi/svantaggi GIL, "GIL oggi" (build free-threaded 3.13/3.14, --disable-gil), confronto multithread vs multiprocess CPU-bound, da slide 11_
