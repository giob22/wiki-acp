---
tipo: concetto
importanza_esame: alta
prerequisiti: [java-threading, oop]
---

## Definizione

In Java ogni oggetto ha un **mutex intrinsic** (monitor). L'accesso avviene tramite `synchronized` (metodo o blocco). Il lock viene acquisito all'entrata e rilasciato all'uscita — anche in caso di eccezione (automaticamente).

## Spiegazione

**Metodo sincronizzato** — acquisce lock sull'istanza:
```java
class SharedCounter {
    private int theData;
    public synchronized int read() {   // acquisisce lock all'ingresso
        return theData;
    }                                   // rilascia lock qui (automatico)
}
```

**Blocco sincronizzato** — più granulare, specifica quale oggetto lockare:
```java
public int read() {
    synchronized(this) {        // acquisisce lock su this
        return theData;
    }
}

// Con oggetto dedicato:
private Object obj = new Object();
synchronized(obj) { ... }
```

**Metodi statici sincronizzati** — acquisiscono lock sulla **classe** (non sull'istanza):
- Due metodi statici sync della stessa classe da thread diversi → eseguono **in sequenza**
- Un metodo statico sync e un metodo d'istanza sync → eseguono **in concorrenza** (lock diversi)

**Regola importante**: Metodi NON sincronizzati non richiedono lock e possono eseguire in ogni momento **senza garanzie di mutua esclusione**.

**Problema sezione critica compound** (check + write):
```java
// SBAGLIATO: un thread può intercalarsi tra check() e write()
synchronized void check() {...}
synchronized void write() {...}

// CORRETTO: racchiudere la coppia in un blocco sincronizzato
void run() {
    synchronized(wrapper) {
        if(wrapper.check())
            wrapper.write();
    }
}
```

**Wait / Notify** (Monitor):
```java
// Dentro synchronized:
obj.wait();         // rilascia lock e sospende; riprende su notify
obj.notify();       // sveglia UN thread in attesa su obj
obj.notifyAll();    // sveglia TUTTI i thread in attesa su obj
```

**Java 1.5 — `java.util.concurrent`**:
```java
Lock lock = new ReentrantLock();
lock.lock();
try { ... } finally { lock.unlock(); }  // finally garantisce unlock

Semaphore sem = new Semaphore(N);
sem.acquire();   // decrementa (blocca se 0)
sem.release();   // incrementa

CountDownLatch latch = new CountDownLatch(N);
latch.await();       // attende fino a count = 0
latch.countDown();   // decrementa count
```

> 🎯 Esame: Differenza metodo/blocco synchronized, problema della coppia check+write, quando usare wait/notify.

## Perché importa

La sincronizzazione è il meccanismo base per evitare race condition in Java — concetto centrale del corso per sistemi concorrenti.

## Connessioni

- [[java-threading]] — i thread che sincronizzare
- [[threading]] — confronto con Python Lock e sincronizzazione

## Fonti

- [[21-java-sincronizzazione]]

_Aggiornato: 2026-06-04 — ingest iniziale_
