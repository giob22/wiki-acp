---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, oop, ereditarieta]
---

## Definizione

Java supporta la programmazione multithread **al livello di linguaggio**. Tipicamente i thread sono implementati a livello di sistema, e richiedono quindi un'interfaccia di programmazione **dipendente dalla piattaforma** su cui girerà il programma (es. in C++ la libreria `pthread`, POSIX Threads Programming, per programmi multithread su piattaforme UNIX). In Java invece le primitive per creare e gestire i thread fanno parte del linguaggio stesso: questo consente di realizzare programmi multithread in maniera **standardizzata e indipendente dalla specifica piattaforma**.

Java fornisce:
- primitive per definire **attività indipendenti**;
- primitive per la **comunicazione** e la **sincronizzazione** tra attività eseguite in modo concorrente (→ [[java-sincronizzazione]]).

I thread si creano estendendo la classe `Thread` o implementando l'interfaccia `Runnable` (entrambe in `java.lang`); usano **Kernel Level Thread** (KLT) senza GIL → parallelismo reale su multicore (→ [[gil]]).

## Spiegazione

### Creare un thread — due tecniche

Java offre **due** possibili tecniche per creare un thread: **derivazione** dalla classe `Thread` oppure **implementazione** dell'interfaccia `Runnable`. In entrambi i casi si fa l'**override del metodo `run()`**.

**Approccio 1 — estendere `Thread`** (la classe utente deriva da `Thread` e ridefinisce `run()`):
```java
public class MyThread extends Thread {
    public void run() {  // codice del thread
        doWork();
    }
}
Thread t = new MyThread();
t.start();   // avvia il thread — NON chiamare run() direttamente!
```

**Approccio 2 — implementare `Runnable`** (la classe utente implementa `Runnable` e ridefinisce `run()`):
```java
public class MyRunnable implements Runnable {
    public void run() { doWork(); }
}
Runnable r = new MyRunnable();
Thread t = new Thread(r);
t.start();
```

> 🎯 Esame: **perché Java offre due tecniche?** Perché **Java non consente la derivazione (ereditarietà) multipla**. Se la classe utente **non** è già coinvolta in un legame di derivazione → si può usare la soluzione di derivare dalla classe `Thread`. Se la classe utente **è già** coinvolta in un legame di derivazione (estende già un'altra classe, es. `ParentClass`) → si usa la soluzione di implementare l'interfaccia `Runnable`, ridefinendo `run()`.

**Costruttore principale** di `Thread`:
```java
Thread(ThreadGroup group, Runnable target, String name)
```
- `group`: il gruppo a cui appartiene il thread — `target`: un oggetto di tipo `Runnable` — `name`: il nome del thread.

Per le altre versioni del costruttore si rimanda alla javadoc.

### Thread e applicazioni — il modello di memoria della JVM

Thread diversi all'interno della **stessa applicazione (programma)** condividono la maggior parte dello stato. La distinzione è centrale per capire le race condition:

| Area | Condivisa tra thread? | Contenuto |
|---|---|---|
| **Method Area** (ambiente delle classi) | **Sì** | Runtime Constant Pool, codice dei metodi, attributi e valori dei campi |
| **Heap** | **Sì** | istanze degli oggetti e array |
| **Direct Memory** | Sì | oggetti allocati esplicitamente nella *direct memory area*, deallocati automaticamente dal *garbage collector* della JVM |
| **PC Register** | **No** (uno per thread) | program counter |
| **JVM Stack** (stack delle attivazioni) | **No** (uno per thread) | è composto da *stack frame* = local variables + operand stack; **ogni frame coincide con una invocazione di un metodo** |
| **Native Method Stack** | No (uno per thread) | area dati che memorizza informazioni per eseguire metodi nativi (non-Java) |

Tradotto in variabili:
- **condivise**: le **variabili statiche** (vivono nelle classi → Method Area) e le **variabili di istanza** (vivono nell'heap);
- **NON condivise**: le **variabili locali dei metodi** (vivono nello stack privato del thread).

> 🎯 Esame: "*method area* e *heap* sono condivisi da tutti i thread in esecuzione nella JVM; invece, quando un thread viene creato ottiene un proprio **PC** e **stack**". È il motivo per cui le variabili locali sono thread-safe per costruzione, mentre quelle di istanza e statiche no.

### Metodi principali

```java
t.start()              // alloca il thread nella JVM e ne determina l'invocazione di run()
                       // run() definisce il comportamento del thread
Thread.sleep(ms)       // sospende (stato dormiente) il thread corrente per ms millisecondi
t.yield()              // causa la sospensione del thread a favore di un altro thread
t.join()               // attende la terminazione di t
t.isAlive()            // true se ancora in esecuzione
t.interrupt()          // invia segnale di interruzione
t.setPriority(int)     // 1=MIN, 5=NORM, 10=MAX
Thread.currentThread() // riferimento al thread corrente
```

> ⚠️ I thread Java **non hanno alcuna funzione di `exit`**: un thread viene deallocato **solo alla fine del metodo `run()`**.

### Stati di un thread

Dal diagramma del corso (slide 18):
```
New --start()--> Runnable ⟷ Running --stop()/fine run()--> STOP
                    ↑              ↓ (thread blocks: sleep, wait, sync, I/O)
                    └── unblocks ── blocked
```
- `New` --`start()`--> `Runnable`;
- da `Runnable` a `Running`: il thread viene *chosen by the scheduler to run*;
- da `Running` a `Runnable`: il thread invoca `yield()`, oppure lo scheduler lo fa *swap out*;
- da `Running` a `STOP`: `stop()` oppure `run()` finisce (*run exit*);
- da `Running` a `blocked`: il thread si blocca (`sleep`, `wait`, `sync`, I/O); da `blocked` torna a `Runnable` quando *unblocks*.

| Stato | Blocked | Interruptible | Quando diventa ready-to-run |
|---|---|---|---|
| Running | | | è in esecuzione (*running*) sul processore |
| Runnable (ready-to-run) | | | in attesa del proprio *turno* per il processore |
| Sleeping | SÌ | SÌ | allo scadere del tempo di `sleep` o a seguito di una interruzione |
| Waiting | SÌ | SÌ | allo scadere di un timeout, dopo una `notify`, o a seguito di una interruzione |
| Blocked I/O | SÌ | | a seguito di una variazione della condizione di I/O attesa |
| Blocked synch | SÌ | | quando è acquisito il lock su uno statement `synchronized` |

### Scheduling dei thread — il modello della specifica Java

- Su sistemi **monoprocessore** un solo thread alla volta può essere eseguito.
- I thread Java hanno una **priorità**: esistono **10 livelli**, compresi fra `MIN_PRIORITY` (1) e `MAX_PRIORITY` (10); il valore intermedio è `NORM_PRIORITY` (5). Un thread **eredita la priorità del thread che lo crea**; la si può cambiare con `setPriority(int)`.
- La specifica Java prevede l'algoritmo **"fixed priority scheduling"**, basato sulle priorità dei thread: in generale, i thread a priorità più alta ottengono più tempo di processore rispetto a quelli a priorità più bassa. In dettaglio:
  - in ogni momento, se c'è più di un thread `Runnable` in attesa, si sceglie quello a **priorità più alta**;
  - se ci sono più thread `Runnable` con la **stessa priorità**, se ne sceglie uno operando in modalità **First Come-First Served**.
- Il thread scelto può continuare l'esecuzione finché: un thread a priorità maggiore diviene `Runnable`; invoca `yield()` o `run()` finisce; in un **OS "time-slicing"** il suo periodo (quanto) di CPU termina; passa da `Running` a `Blocked` (`sleep`, `sync`, `wait`, condizione di I/O).

### Chi schedula davvero i thread? JVM vs sistema operativo

> 💡 Disambiguazione (punto critico d'esame). Il PDF dice in due punti cose apparentemente in contrasto: alla slide "Context switch" che *"il cambio contesto tra thread di un programma Java viene effettuato dalla JVM"*, e alla slide "JVM e threads" che *"la maggior parte delle implementazioni JVM utilizza i thread del sistema operativo sottostante"* (con priorità che valgono solo come suggerimento). Non c'è contraddizione se si separano due livelli:

1. **Modello / specifica** — definito dalla **JVM**. È la JVM a fissare l'astrazione di thread, i 10 livelli di priorità e il "fixed priority scheduling" come comportamento *nominale*. A questo livello logico è la JVM l'entità responsabile dei thread e del loro avvicendamento.

2. **Esecuzione concreta** — dipende da **come la JVM è implementata**. La JVM utilizza una libreria nativa (come POSIX o Win32) **oppure** una propria libreria (i **"green" threads**) per fornire l'infrastruttura su cui girano i thread. Si hanno due casi:
   - **Green threads**: la JVM schedula i thread *internamente*, in spazio utente, multiplexandoli su un singolo thread di sistema. Qui il context switch è eseguito **letteralmente dalla JVM** — ed è il senso preciso dell'affermazione della slide "Context switch".
   - **Thread nativi (1:1)**: ogni thread Java è mappato su un thread dell'OS. È quello che fa la **maggior parte** delle implementazioni moderne (es. HotSpot). In questo caso lo scheduling e il context switch *concreti* sono eseguiti dallo **scheduler del sistema operativo**, non dalla JVM.

> 🎯 Esame: **è proprio la delega all'OS la ragione per cui non ci si può fidare delle priorità.** Nelle implementazioni a thread nativi le priorità JVM sono solo un *suggerimento* per lo scheduler dell'OS e **non servono a garantire la correttezza di un programma**. La mappatura JVM-priority → priorità dell'OS è **dipendente dalla piattaforma** e per giunta **non iniettiva** (più priorità Java collassano sullo stesso livello OS), come mostra la tabella del corso:

| JVM Priority | Linux (nice value) | Windows Thread Priority |
|---|---|---|
| 1 (MIN) | 19 (very low) | THREAD_PRIORITY_IDLE |
| 2 | 15 | THREAD_PRIORITY_LOWEST |
| 3 | 10 | THREAD_PRIORITY_BELOW_NORMAL |
| 4 | 5 | THREAD_PRIORITY_BELOW_NORMAL |
| 5 (NORM) | 0 (default) | THREAD_PRIORITY_NORMAL |
| 6 | -5 | THREAD_PRIORITY_ABOVE_NORMAL |
| 7 | -10 | THREAD_PRIORITY_ABOVE_NORMAL |
| 8 | -15 | THREAD_PRIORITY_HIGHEST |
| 9 | -18 | THREAD_PRIORITY_HIGHEST |
| 10 (MAX) | -20 (very high) | THREAD_PRIORITY_TIME_CRITICAL |

> La specifica Java per lo scheduling è quindi molto **"lasca"**: al fine di ottenere codice **portabile** non si dovrebbero mai fare troppe assunzioni sul sistema di scheduling sottostante. 
> **Good practice: scrivere programmi che funzionino bene a prescindere dal livello di priorità (o non utilizzarle affatto).**

### Il problema dei thread egoisti (*selfish thread*)

Un **selfish thread** è un thread **CPU-bound** che, una volta in esecuzione, **non cede volontariamente la CPU**: non fa I/O e non si blocca. Esempio di metodo `run`:
```java
public class SelfishRunner extends Thread {
    public int tick = 1;
    public void run() {
        while (tick < 4000000) {
            tick++;            // non cede mai la CPU
        }
    }
}
```
Una volta in esecuzione, tale thread continua **fino alla terminazione del ciclo** (cioè fino alla fine del suo metodo `run()`) o fino all'arrivo di un altro thread a priorità maggiore. I thread con la **stessa priorità** di `SelfishRunner` **potrebbero aspettare a lungo** (*starvation* → [[semaforo]]).

Confronto del comportamento osservabile (slide 25):
- **Sistema NON time-slicing**: il primo thread che assume il controllo della CPU arriva fino in fondo al conteggio (fino alla fine del suo `run()`); solo allora parte il successivo (`Thread #0` completa tutto, poi `Thread #1`, …).
- **Sistema time-slicing**: i thread si alternano; la frequenza dei cambi dipende dalla larghezza dei singoli slot temporali in relazione alla potenza elaborativa del PC.

Come alcuni sistemi limitano i thread egoisti:
- col **time slicing**: l'esecuzione di più thread, eseguiti in alternanza **solo per uno specifico quanto di tempo** (slice). Si applica quando più thread con **identica priorità** hanno diritto ad essere eseguiti e non ci sono altri thread a priorità più elevata.
- > ⚠️ **La specifica Java NON impone il time slicing!** Non ci si può fare affidamento, dato che i risultati sarebbero differenti da architettura ad architettura.

**Una soluzione** — il programmatore ha a disposizione i metodi della classe `Thread` per forzare i thread alla collaborazione. Il metodo `yield()`, ad esempio, permette al sistema di **cedere la CPU ad un altro thread** eseguibile con la stessa priorità.
- > **Good practice**: nel caso peggiore conviene assumere che il sistema sia **NON time-slicing**; se l'elaborazione è fortemente CPU-intensive si potrebbe *occasionalmente* lasciare il controllo con `yield()` o effettuare una `sleep`.
- Con `yield()` esplicito il sistema alterna i thread `Runnable` con un algoritmo **round-robin** (output regolare: `Thread #0, #1, #2, #0, #1, #2, …`). La presenza dell'istruzione `yield()` tende a rendere l'esecuzione del programma **deterministica**, indipendentemente dal sistema operativo (time-slicing o meno) e dalle risorse di calcolo disponibili.

> 💡 Connessione: è l'analogo Java del thread CPU-bound che in Python terrebbe il GIL; lì è CPython a forzare il rilascio periodico, qui è il time-slicing dell'OS (non garantito) oppure lo `yield()` esplicito → [[gil]], [[concorrenza-parallelismo]].

### Interruzione di un thread

Un'**interruzione** indica che un thread deve **interrompere ciò che sta facendo** e fare qualcos'altro. È compito del programmatore indicare cosa deve fare un thread a seguito della notifica di interruzione. Un thread solleva un'interruzione su un altro thread invocando il metodo `interrupt()` sull'oggetto `Thread` da interrompere.

- Alcuni metodi che un thread può invocare durante la sua esecuzione **sollevano `InterruptedException`** quando `interrupt()` viene invocato durante la loro esecuzione → basta gestire l'eccezione con `try/catch`:
  ```java
  try {
      // ... metodo che può sollevare InterruptedException ...
  } catch (InterruptedException ex) {
      // codice gestione eccezione
  }
  ```
- Se invece il thread **non** invoca metodi che sollevano `InterruptedException`, può periodicamente invocare:
  - `Thread.interrupted()` (statico): ritorna `true` se sul thread è stato invocato `interrupt()`, e **resetta** il flag *interrupted status* del thread corrente;
  - `isInterrupted()`: verifica se il thread è stato interrotto ma **non modifica** il flag.
  ```java
  for (int i = 0; i < inputs.length; i++) {
      heavyCrunch(inputs[i]);
      if (Thread.interrupted()) {   // thread interrotto…
          return;
      }
  }
  ```
  In alcune circostanze ha senso, invece, **sollevare** un'eccezione se `interrupted()` restituisce `true`:
  ```java
  if (Thread.interrupted()) {
      throw new InterruptedException();
  }
  ```

Oltre a `interrupt()`, la classe `Thread` presenta **tre ulteriori metodi** per l'interruzione di un thread:
- `suspend()` — sospende un thread;
- `resume()` — riattiva un thread precedentemente interrotto da `suspend()`;
- `stop()` — ferma un thread e lo uccide.

> ⚠️ Questi tre metodi sono **deprecati**: il loro uso è **rischioso** e comporta notevoli complicazioni. Es.: un thread può essere interrotto **prima di poter rilasciare una risorsa**, impedendo così agli altri di potervi accedere e generando un **deadlock** difficilmente risolvibile. Per questa ragione si assume che un thread **si interrompa e muoia solo a conclusione del suo metodo `run()`**.

### Sleep e Join

`sleep(long millisec)` è un metodo comunemente adoperato che pone in attesa (stato dormiente) un thread per il numero di millisecondi specificato (richiede `try/catch` di `InterruptedException`):
```java
try {
    Thread.sleep(4000);
} catch (InterruptedException ex) {
    System.out.println(ex);
}
```
Quando un thread padre genera vari thread figli e deve **attenderne la conclusione prima di procedere**, usa `join()`:
```java
Thread[] threads = new Thread[numOfThreads];
for (int i = 0; i < threads.length; i++) {
    threads[i] = new MyThread();
    threads[i].start();
}
for (int i = 0; i < threads.length; i++) {
    try {
        threads[i].join();         // il padre attende la conclusione di threads[i]
    } catch (InterruptedException ignore) {}
}
```

### ThreadGroup

All'atto della loro creazione, i thread possono essere raggruppati per mezzo di un **`ThreadGroup`**, così da poterli controllare congiuntamente come se fossero **una singola entità** (struttura ad albero in cui i nodi sono gruppi e thread). Ogni thread appartiene **sempre** a un gruppo; se non specificato, un thread appartiene a un gruppo di default chiamato **`main`**.

> 🎯 Esame: differenza tra i due approcci di creazione e perché (no derivazione multipla); perché `start()` e non `run()`; ciclo di vita e stati; cos'è un selfish thread; cosa condividono i thread (heap/method area) e cosa no (stack/PC); chi schedula davvero (JVM nel modello / OS nell'esecuzione nativa) e perché le priorità non sono affidabili.

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
_Aggiornato: 2026-06-20 — estensione da slide 02_JAVA_01_
_Aggiornato: 2026-06-23 — riscrittura integrale aderente al PDF 02_JAVA_01 (slide 1-38). Disambiguata la coerenza JVM↔OS sullo scheduling/context switch: separati il livello "modello/specifica" (JVM: fixed-priority, 10 livelli) dal livello "esecuzione concreta" (green threads = switch fatto dalla JVM; thread nativi 1:1 = switch e scheduling fatti dall'OS, caso della maggior parte delle JVM). Chiarito che la delega all'OS è la causa per cui le priorità sono solo un suggerimento; aggiunta tabella mapping JVM-priority→Linux nice/Windows priority (non iniettiva). Aggiunto confronto NON time-slicing vs time-slicing del selfish thread, esempio round-robin/yield deterministico, blocco interruzione completo (interrupt/InterruptedException/interrupted vs isInterrupted/suspend-resume-stop deprecati), sleep/join con esempi del PDF, ThreadGroup_
