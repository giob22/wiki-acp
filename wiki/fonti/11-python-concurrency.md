---
tipo: fonte
titolo: "Python — Concurrency"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, threading, multiprocessing, asyncio, gil, lock, daemon, thread-local]
---

## Sommario

Slide sulla concorrenza in Python con il modulo `threading`. Si descrivono le classi `Thread` e `Lock`, i thread daemon vs non-daemon, il thread-local storage, e i problemi di sincronizzazione. Si introduce il GIL e le sue implicazioni per il parallelismo reale.

## Punti chiave

1. Modulo `threading` — threading a livello kernel in Python
2. **Classe `Thread`**:
   ```python
   t = threading.Thread(target=funzione, args=(arg1,))
   t.start()   # avvia il thread
   t.join()    # aspetta la fine
   t.is_alive()  # controlla se ancora in esecuzione
   ```
3. Alternativa: sottoclassare `Thread` e sovrascrivere `run()`
4. **Thread daemon**: thread che muore automaticamente quando muore il thread principale
   - `t.daemon = True` (da impostare prima di `start()`)
   - Thread non-daemon: il processo aspetta la loro terminazione
5. **GIL (Global Interpreter Lock)**: in CPython un solo thread esegue bytecode alla volta
   - Threading utile per I/O-bound (il GIL viene rilasciato durante I/O)
   - Non utile per CPU-bound (usare `multiprocessing` o `concurrent.futures`)
6. **`Lock`** — primitiva di sincronizzazione per sezione critica:
   ```python
   lock = threading.Lock()
   with lock:
       # sezione critica
   ```
7. **`RLock`** (Reentrant Lock) — lo stesso thread può acquisirlo più volte
8. **Thread-local storage**: `threading.local()` — ogni thread ha la sua copia della variabile
9. **`Semaphore`** — limita accesso concorrente a N thread
10. **`Event`** — flag condiviso per notifica tra thread
11. **`Queue`** (da `queue`) — struttura thread-safe per producer-consumer

## Concetti introdotti

- [[threading]]
- [[gil]]
- [[multiprocessing]]

## Domande aperte

- asyncio e multiprocessing sono coperti in slide successive?

## Domande da esame

- Come si crea e avvia un thread in Python?
- Cos'è il GIL? Quali conseguenze ha sul parallelismo?
- Differenza tra thread daemon e non-daemon
- Come si usa un Lock? Perché è necessario?
- Quando conviene usare threading vs multiprocessing?
