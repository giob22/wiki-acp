---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, oop, ereditarieta]
---

## Definizione

In Java i thread si creano estendendo `Thread` o implementando `Runnable`. Java usa **Kernel Level Thread** (KLT) senza GIL — il parallelismo reale su multicore è possibile. La sincronizzazione è gestita tramite `synchronized`.

## Spiegazione

**Approccio 1 — estendere Thread**:
```java
class MioThread extends Thread {
    public void run() {  // corpo del thread
        // lavoro
    }
}
MioThread t = new MioThread();
t.start();   // avvia il thread — NON chiamare run() direttamente!
t.join();    // attende terminazione
```

**Approccio 2 — implementare Runnable** (preferibile — separa task da thread):
```java
class MioTask implements Runnable {
    public void run() { ... }
}
Thread t = new Thread(new MioTask());
t.start();
```

**Ciclo di vita**:
```
New → Runnable → Running → Blocked/Waiting → Terminated
```

**Metodi principali**:
```java
t.start()              // avvia il thread
t.join()               // attende terminazione
t.isAlive()            // true se ancora in esecuzione
Thread.sleep(ms)       // sospende il thread corrente
t.interrupt()          // invia segnale di interruzione
t.setPriority(int)     // 1=MIN, 5=NORM, 10=MAX
Thread.currentThread() // riferimento al thread corrente
t.yield()              // cede CPU allo scheduler
```

**Differenza con Python**:
- Java non ha GIL → thread Java sfruttano davvero i core multipli per CPU-bound
- Java usa KLT; Python usa KLT ma li vincola con il GIL

> 🎯 Esame: Differenza tra i due approcci, perché `start()` e non `run()`, ciclo di vita.

## Perché importa

Il threading Java è usato per server multithread (socket worker thread), e compare nell'esempio Proxy-Skeleton (`CounterWorker extends Thread`).

## Connessioni

- [[threading]] — threading Python a confronto
- [[java-sincronizzazione]] — sincronizzazione dei thread Java
- [[processo-thread]] — concetti condivisi processo/thread

## Fonti

- [[20-java-multithreading]]
- [[22-java-networking]]
- [[23-java-proxy-skeleton]]

_Aggiornato: 2026-06-04 — ingest iniziale_
