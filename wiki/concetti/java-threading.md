---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, oop, ereditarieta]
---

## Definizione

In Java il multithreading è supportato **a livello di linguaggio** (non tramite libreria di sistema platform-dependent come `pthread` in C++): i programmi multithread sono quindi **standardizzati e indipendenti dalla piattaforma**. Java fornisce primitive per definire **attività indipendenti** e primitive per **comunicazione e sincronizzazione** tra di esse. I thread si creano estendendo la classe `Thread` o implementando l'interfaccia `Runnable`; usano **Kernel Level Thread** (KLT) senza GIL → parallelismo reale su multicore.

Perché sono supportati a livello di linguaggio? Poiché le **primitive per creare e gestire i thread fanno parte del linguaggio stesso**. I thread sono **tipicamente** **implementati a livello di sistema**, richiedono un'interfaccia di programmazione dipendente dalla piattaforma su cui girerà il programma; invece in Java sono, come detto, supportati a livello di linguaggio.

## Spiegazione

### Creare un thread — due tecniche

**Approccio 1 — estendere `Thread`** (la classe utente deriva da `Thread`, ridefinisce `run()`):
```java
public class MyThread extends Thread {
    public void run() {  // corpo del thread
        doWork();
    }
}
Thread t = new MyThread();
t.start();   // avvia il thread — NON chiamare run() direttamente!
```

**Approccio 2 — implementare `Runnable`** (preferibile: separa il *task* dal *thread*):
```java
public class MyRunnable implements Runnable {
    public void run() { doWork(); }
}
Runnable r = new MyRunnable();
Thread t = new Thread(r);
t.start();
```

> 🎯 Esame: **perché Java offre due tecniche?** Perché **Java non consente l'ereditarietà multipla**. Se la classe utente **non** è già coinvolta in un legame di derivazione → si può derivare da `Thread`. Se la classe utente **è già** in una gerarchia di derivazione (estende già un'altra classe) → si è costretti a implementare `Runnable`, ridefinendo `run()`. In entrambi i casi si fa l'**override di `run()`**.

**Costruttore principale** di `Thread`:
```java
Thread(ThreadGroup group, Runnable target, String name)
```
- `group`: il gruppo a cui appartiene il thread — `target`: oggetto `Runnable` — `name`: nome del thread.

### Thread e applicazioni — il modello di memoria della JVM

Thread diversi della **stessa applicazione** condividono la maggior parte dello stato. La distinzione è centrale per capire le race condition:

| Area | Condivisa tra thread? | Contenuto |
|---|---|---|
| **Method Area** (ambiente delle classi) | **Sì** | Runtime Constant Pool, codice dei metodi, attributi e valori dei campi |
| **Heap** | **Sì** | istanze degli oggetti e array |
| **Direct Memory** | Sì | oggetti allocati esplicitamente, deallocati dal GC della JVM |
| **PC Register** | **No** (uno per thread) | program counter |
| **JVM Stack** (stack delle attivazioni) | **No** (uno per thread) | stack frame = local variables + operand stack; **un frame per invocazione di metodo** |
| **Native Method Stack** | No (uno per thread) | info per eseguire metodi nativi (non-Java) |

Tradotto in variabili:
- **condivise**: le **variabili statiche** (vivono nelle classi → Method Area) e le **variabili di istanza** (vivono nell'heap);
- **NON condivise**: le **variabili locali dei metodi** (vivono nello stack privato del thread).

> 🎯 Esame: "quando un thread viene creato ottiene un proprio **PC** e **stack**; *method area* e *heap* sono invece condivisi da tutti i thread della JVM". È il motivo per cui le variabili locali sono thread-safe per costruzione e quelle di istanza/statiche no.

### Context switch

Il cambio di contesto tra thread di un programma Java è effettuato **dalla JVM** e richiede tipicamente **meno di 100 istruzioni** — molto più leggero di un context switch tra processi (→ [[processo-thread]]).

### Metodi principali

```java
t.start()              // alloca il thread nella JVM e ne determina l'invocazione di run()
                       // run() definisce il comportamento del thread
Thread.sleep(ms)       // sospende (stato dormiente) il thread corrente per ms millisecondi
t.yield()              // cede la CPU allo scheduler a favore di un altro thread di pari priorità
t.join()               // attende la terminazione di t
t.isAlive()            // true se ancora in esecuzione
t.interrupt()          // invia segnale di interruzione
t.setPriority(int)     // 1=MIN, 5=NORM, 10=MAX
Thread.currentThread() // riferimento al thread corrente
```

> ⚠️ I thread Java **non hanno alcuna funzione di `exit`**: un thread viene deallocato **solo alla fine del metodo `run()`**.

### Stati di un thread

```
New → Runnable → Running → Blocked/Waiting → Terminated
```
Transizioni (dal diagramma del corso):
- `New` --`start()`--> `Runnable`
- `Runnable` ⟷ `Running`: lo scheduler sceglie un Runnable per metterlo in Running; da Running si torna a Runnable con `yield()` o quando lo scheduler fa lo *swap out*
- `Running` --`stop()`/fine `run()`--> `Terminated` (STOP)
- `Running` --thread si blocca (`sleep`, `wait`, `sync`, I/O)--> `Blocked` --si sblocca--> `Runnable`

| Stato | Blocked | Interruptible | Quando torna ready-to-run |
|---|---|---|---|
| Running | | | è in esecuzione sul processore |
| Runnable (ready-to-run) | | | in attesa del proprio turno di CPU |
| Sleeping | SÌ | SÌ | allo scadere del tempo di `sleep` o per interruzione |
| Waiting | SÌ | SÌ | allo scadere di un timeout, dopo una `notify`, o per interruzione |
| Blocked I/O | SÌ | | a seguito di una variazione della condizione di I/O attesa |
| Blocked synch | SÌ | | quando viene acquisito il lock su uno statement `synchronized` |

### Scheduling dei thread

- Su sistemi **monoprocessore** un solo thread alla volta può essere eseguito.
- I thread hanno una **priorità**: **10 livelli**, da `MIN_PRIORITY` (1) a `MAX_PRIORITY` (10), valore intermedio `NORM_PRIORITY` (5). Un thread **eredita la priorità del thread che lo crea**; si cambia con `setPriority(int)`.
- La specifica Java prevede l'algoritmo **"fixed priority scheduling"**: la JVM sceglie sempre il Runnable a **priorità più alta**; tra Runnable di **pari priorità** si opera **First Come-First Served**.
- Il thread scelto continua finché: arriva un thread a priorità maggiore; invoca `yield()` o `run()` finisce; in un OS **time-slicing** termina il suo quanto di CPU; passa da Running a Blocked (`sleep`, `sync`, `wait`, I/O).

> 🎯 Esame: la specifica Java sullo scheduling è molto **"lasca"**. La JVM usa una libreria nativa (POSIX/Win32) o una propria (**"green" threads**); le priorità sono solo un **suggerimento** per lo scheduler e **non garantiscono la correttezza** di un programma. **Good practice: scrivere programmi che funzionino bene a prescindere dal livello di priorità** (o non usarle affatto). La mappatura JVM-priority → Linux *nice* / Windows priority cambia da piattaforma a piattaforma.

### Il problema dei thread egoisti (*selfish thread*)

Un **selfish thread** è un thread **CPU-bound** che, una volta in esecuzione, **non cede volontariamente la CPU**: non fa I/O e non si blocca.
```java
public class SelfishRunner extends Thread {
    public int tick = 1;
    public void run() {
        while (tick < 4000000) { tick++; }   // mai cede la CPU
    }
}
```
Una volta in esecuzione, continua **fino alla fine del ciclo** (cioè fino alla fine di `run()`) o fino all'arrivo di un thread a priorità maggiore. I thread di pari priorità **potrebbero aspettare a lungo** (*starvation* → [[semaforo]]).

- Alcuni sistemi limitano i thread egoisti con il **time slicing**: i thread Runnable di pari priorità si alternano **solo per uno specifico quanto di tempo** (slice), con algoritmo round-robin.
- > ⚠️ **La specifica Java NON impone il time slicing!** Non ci si può fare affidamento: i risultati cambierebbero da architettura ad architettura.
- **Soluzione**: il programmatore forza la collaborazione con i metodi di `Thread`. `yield()` cede la CPU a un altro thread di pari priorità. **Good practice**: nel caso peggiore assumere che il sistema sia **NON time-slicing**; se l'elaborazione è fortemente CPU-intensive, cedere *occasionalmente* il controllo con `yield()` o una `sleep()`. La presenza di `yield()` tende a rendere l'esecuzione **deterministica** indipendentemente dall'OS.

> 💡 Connessione: è l'analogo Java del thread CPU-bound che in Python terrebbe il GIL; lì è CPython a forzare il rilascio periodico, qui è il time-slicing dell'OS (non garantito) o lo `yield()` esplicito → [[gil]], [[concorrenza-parallelismo]].

### Interruzione di un thread

Un'**interruzione** indica a un thread che deve interrompere ciò che sta facendo. Un thread la solleva su un altro invocando `interrupt()` sull'oggetto `Thread` da interrompere; è compito del programmatore indicare cosa fare alla notifica.
- Alcuni metodi sollevano `InterruptedException` quando `interrupt()` viene invocato durante la loro esecuzione → si gestisce con `try/catch`.
- Se il thread **non** invoca metodi che sollevano `InterruptedException`, può invocare periodicamente:
  - `Thread.interrupted()` (statico): ritorna `true` se è stato invocato `interrupt()`, e **resetta** il flag *interrupted status*;
  - `isInterrupted()`: verifica lo stato ma **non modifica** il flag.
- > ⚠️ I metodi `suspend()`, `resume()`, `stop()` sono **deprecati**: rischiosi (un thread può essere interrotto **prima di rilasciare una risorsa** → deadlock difficilmente risolvibile). Per questo si assume che un thread **si interrompa e muoia solo a conclusione di `run()`**.

### Sleep e Join

`sleep(long millisec)` pone il thread in attesa (stato dormiente) per i millisecondi specificati (richiede `try/catch` di `InterruptedException`). Quando un thread padre genera vari thread figli e deve **attenderne la conclusione** prima di procedere, usa `join()`:
```java
Thread[] threads = new Thread[numOfThreads];
for (int i = 0; i < threads.length; i++) {
    threads[i] = new MyThread();
    threads[i].start();
}
for (int i = 0; i < threads.length; i++) {
    try { threads[i].join(); }            // il padre attende la conclusione di threads[i]
    catch (InterruptedException ignore) {}
}
```

### ThreadGroup

All'atto della creazione i thread possono essere raggruppati in un **`ThreadGroup`**, per controllarli congiuntamente come **una singola entità** (struttura ad albero di gruppi e thread). Ogni thread appartiene **sempre** a un gruppo; se non specificato, appartiene al gruppo di default chiamato **`main`**.

> 🎯 Esame: differenza tra i due approcci di creazione e perché (no ereditarietà multipla); perché `start()` e non `run()`; ciclo di vita e stati; cos'è un selfish thread; cosa condividono i thread (heap/method area) e cosa no (stack/PC).

## Perché importa

Il threading Java è il modello di concorrenza del corso lato Java: server multithread (un worker thread per connessione socket), esempio Proxy-Skeleton (`CounterWorker extends Thread`), e termine di confronto con il threading Python vincolato dal GIL.

## Connessioni

- [[threading]] — threading Python a confronto (KLT vincolati dal GIL)
- [[gil]] — il selfish thread Java è l'analogo del thread CPU-bound che terrebbe il GIL
- [[java-sincronizzazione]] — sincronizzazione dei thread Java (`synchronized`, monitor, wait/notify)
- [[processo-thread]] — concetti condivisi processo/thread, context switch
- [[concorrenza-parallelismo]] — concorrenza vs parallelismo, time-slicing

## Fonti

- [[20-java-multithreading]]
- [[22-java-networking]]
- [[23-java-proxy-skeleton]]

_Aggiornato: 2026-06-04 — ingest iniziale_
_Aggiornato: 2026-06-20 — estensione da slide 02_JAVA_01: multithread a livello di linguaggio (vs pthread), perché due tecniche (no ereditarietà multipla), costruttore Thread, modello di memoria JVM (method area/heap condivisi vs PC/stack per thread; variabili statiche/istanza vs locali), context switch JVM <100 istruzioni, stati del thread (tabella completa), scheduling (priorità 1-10, fixed priority, FCFS, time-slicing, green threads, mapping piattaforma), selfish thread (yield/sleep), interruzione (interrupt/InterruptedException/interrupted vs isInterrupted/deprecati suspend-resume-stop), sleep/join, ThreadGroup_
