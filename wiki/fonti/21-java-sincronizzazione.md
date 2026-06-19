---
tipo: fonte
titolo: "Java — Sincronizzazione e meccanismi"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [java, synchronized, monitor, mutex, wait, notify, lock, semaphore, java15]
---

## Sommario

Slide sulla sincronizzazione in Java. Ogni oggetto Java ha un mutex associato accessibile tramite metodi/blocchi `synchronized`. Si trattano monitor, wait/notify, e i meccanismi avanzati di Java 1.5 (Lock, Condition, Semaphore).

## Punti chiave

1. Ogni oggetto Java ha associato un **mutex** (intrinsic lock)
2. Accesso al mutex tramite **metodi sincronizzati** o **blocchi sincronizzati** — mai direttamente
3. **Metodo sincronizzato**: `public synchronized void metodo() {...}` — acquisisce lock sull'istanza all'ingresso, rilascia all'uscita (anche per eccezione — automatico)
4. **Blocco sincronizzato**: `synchronized(obj) { ... }` — acquisisce il lock dell'oggetto `obj` specificato
5. **Metodi statici sincronizzati**: acquisiscono il mutex della **classe** (non dell'istanza) — lock di classe e lock di istanza sono **indipendenti**
6. Metodi non sincronizzati non richiedono il lock e possono eseguire senza garanzie di mutua esclusione
7. **Soluzione corretta** per sezione critica compound (check + write): usare blocco sincronizzato che avvolge l'intera operazione atomica
8. **Sincronizzazione implicita**: se la classe non ha metodi synchronized, si può usare `synchronized(obj)` dall'esterno per proteggere sequenze di chiamate
9. **Wait/Notify** (Monitor in Java):
   - `wait()` — rilascia il lock e sospende il thread in attesa di una notifica
   - `notify()` — sveglia un thread in attesa sul monitor corrente
   - `notifyAll()` — sveglia tutti i thread in attesa
   - Devono essere chiamati dentro un blocco `synchronized`
10. **Java 1.5 — java.util.concurrent**:
    - `Lock` / `ReentrantLock` — lock esplicito con `lock()` / `unlock()`
    - `Condition` — wait/notify avanzato su lock espliciti
    - `ReadWriteLock` — lock di lettura/scrittura separati
    - `Semaphore(n)` — limita accesso a N thread
    - `CountDownLatch` — barriera per attendere N eventi

## Concetti introdotti

- [[java-sincronizzazione]]
- [[threading]]

## Domande aperte

- Nessuna

## Domande da esame

- Come funziona `synchronized` in Java? Differenza metodo vs blocco
- Cosa succede al lock quando il metodo termina con eccezione?
- Quando usare blocchi sincronizzati invece di metodi sincronizzati?
- A cosa servono `wait()` e `notify()`? Dove devono essere chiamati?
- Lock di classe vs lock di istanza — quando entrano in conflitto?
