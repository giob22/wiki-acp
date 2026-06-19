---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, interprete-python]
---

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

> 🎯 Esame: "Cos'è il GIL? Per quali workload il threading Python è utile nonostante il GIL?"

## Perché importa

Il GIL è la ragione principale per cui il threading Python non scala su CPU-bound. Capirlo è essenziale per scegliere la giusta strategia di concorrenza.

## Connessioni

- [[threading]] — soggetto al GIL
- [[multiprocessing]] — aggiramento del GIL
- [[interprete-python]] — il GIL è specifico di CPython

## Fonti

- [[10-programmazione-concorrente-richiami]]
- [[11-python-concurrency]]

_Aggiornato: 2026-06-04 — ingest iniziale_
