---
tipo: fonte
titolo: "Java — Multithreading"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [java, thread, runnable, lifecycle, sleep, join, interrupt, priority]
---

## Sommario

Slide sul multithreading in Java. Si descrivono i due modi per creare thread (estendere `Thread` o implementare `Runnable`), il ciclo di vita di un thread, e i metodi principali per il controllo dell'esecuzione.

## Punti chiave

1. Due approcci per creare thread in Java:
   - **Estendere `Thread`**: sovrascrivere `run()`, creare istanza, chiamare `start()`
   - **Implementare `Runnable`**: passare istanza al costruttore di `Thread`
2. `start()` avvia il thread; `run()` è il corpo del thread (NON chiamare `run()` direttamente)
3. **Ciclo di vita**: New → Runnable → Running → Blocked/Waiting → Terminated
4. `Thread.sleep(ms)` — sospende il thread corrente per ms millisecondi
5. `join()` — attende la terminazione del thread su cui è chiamato
6. `interrupt()` — invia segnale di interruzione al thread
7. `setPriority(int)` — imposta priorità (1=MIN, 5=NORM, 10=MAX)
8. `Thread.currentThread()` — riferimento al thread corrente
9. `isAlive()` — true se il thread è attivo
10. `yield()` — suggerisce allo scheduler di cedere la CPU

## Concetti introdotti

- [[java-threading]]
- [[processo-thread]]

## Domande aperte

- Nessuna

## Domande da esame

- Due modi per creare un thread in Java — differenze
- Differenza tra `start()` e `run()`
- Ciclo di vita di un thread Java
- A cosa serve `join()`?
