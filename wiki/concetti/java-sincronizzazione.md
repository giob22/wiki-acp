---
tipo: concetto
importanza_esame: alta
prerequisiti: [java-threading, oop]
---

## Definizione

Java fornisce un meccanismo di sincronizzazione basato sui **mutex** per l'accesso alle sezioni critiche. **Ogni oggetto ha associato un mutex** (monitor intrinseco), che **non** è acceduto direttamente dall'applicazione ma tramite **metodi sincronizzati** o **blocchi sincronizzati** (`synchronized`). Il lock viene acquisito all'ingresso e rilasciato all'uscita — anche in caso di eccezione (automaticamente).

## Spiegazione

Quando un thread esegue un metodo/blocco `synchronized`: entra in possesso del mutex associato all'istanza; il thread che blocca il mutex (*mutex lock*) acquisisce **accesso esclusivo** alla sezione critica; eventuali altri thread che vogliano accedervi sono posti in **attesa**.

**Metodo sincronizzato** — acquisisce il lock sull'**istanza**:
```java
class SharedCounter {
    private int theData;
    public synchronized int read() {   // acquisisce il lock all'ingresso
        return theData;
    }                                   // rilascia il lock qui (automatico)
}
```

> ⚠️ **Nota**: i metodi **non** sincronizzati non richiedono il lock e possono eseguire **in ogni istante senza garanzie di mutua esclusione**. I metodi sincronizzati garantiscono mutua esclusione sui dati incapsulati **solo se si accede ai dati tramite metodi dichiarati `synchronized`**.

### Metodi statici sincronizzati

Anche i metodi statici possono essere `synchronized`: poiché non sono legati ad alcuna istanza, viene acquisito il **mutex associato alla classe** (l'oggetto `Class`).

| Scenario (stessa classe, thread diversi) | Esito |
|---|---|
| due metodi **`static synchronized`** | eseguono **in sequenza** (stesso lock di classe) |
| un metodo **`static synchronized`** + un metodo **d'istanza `synchronized`** | eseguono **in concorrenza** (lock diversi: classe vs istanza) |

> 🎯 Esame: **"comportamento di un metodo `synchronized` e di uno `static synchronized` chiamati contemporaneamente?"** → non si bloccano a vicenda. Ottenere il lock della classe **non influenza** i lock di alcuna istanza della classe: sono due monitor distinti.

### Blocco sincronizzato

Java consente di definire sezioni critiche anche quando **non coincidono col corpo di un metodo**, tramite i **blocchi sincronizzati**. La parola chiave `synchronized` prende come parametro **il riferimento all'oggetto** del quale ottenere il lock:
```java
public int read() {
    synchronized(this) {        // lock sull'oggetto corrente
        return theData;
    }
}
// oppure su un oggetto dedicato:
private Object obj = new Object();
synchronized(obj) { ... }
```
**Vantaggio**: maggiore espressività nell'implementare i vincoli di sincronizzazione. **Avvertenza**: l'uso eccessivo rende il codice disordinato — i vincoli non sono più incapsulati in un solo posto (per capire i vincoli su un oggetto `O` bisogna guardare *tutti* gli oggetti che accedono a `O` in un blocco `synchronized`).

### Problema della sezione critica composta (check + write)

Esempio: più thread accedono in lettura/scrittura a una variabile. Un thread deve eseguire in mutua esclusione `check()` (controllo disponibilità) e `write()`/`read()`. **Vincolo**: se un thread ha invocato `check()`, deve avere la **certezza che nessun altro thread possa usare la risorsa** prima che esegua `read()`/`write()`.

```java
// SOLUZIONE NON CORRETTA: solo metodi synchronized
class Wrapper {
    private int buffer;
    synchronized void write() {...}
    synchronized void read()  {...}
    synchronized bool check() {...}
}
// Un thread può acquisire il monitor rilasciato da un altro all'USCITA di check(),
// violando l'atomicità della coppia check()+read()/write().
```

```java
// SOLUZIONE CORRETTA: Wrapper SENZA sincronizzazione interna,
// la coppia check+write è racchiusa in un blocco sincronizzato nel run() del thread
class Wrapper {
    private int buffer;
    void write() {...}  void read() {...}  bool check() {...}   // nessuna sincronizzazione qui
}
class MyWriter extends Thread {
    private Wrapper wrapper;
    public MyWriter(Wrapper _wrapper) { wrapper = _wrapper; }
    void run() {
        synchronized(wrapper) {          // monitor sull'istanza di Wrapper
            if (wrapper.check())
                wrapper.write();
        }
    }
}
// (analoga MyReader, sottoclasse di Thread, che nel run() invoca read())
class TestApp {
    public static void main() {
        Wrapper buf = new Wrapper();
        for (int i = 0; i < N; i++) {
            Thread th = is_reader ? new MyReader(buf) : new MyWriter(buf);
            th.start();   // STESSO oggetto buf a tutti → blocchi sincronizzati sullo stesso monitor
        }
    }
}
```
> 🎯 Esame: il punto è passare **lo stesso oggetto `Wrapper`** a tutti i thread, così che i loro blocchi `synchronized(wrapper)` insistano **sullo stesso monitor** e la coppia check+write sia atomica.

### Monitor in Java

Una classe con metodi `synchronized` **è un monitor in Java**. Caratteristica chiave:

> 🎯 Esame: **un monitor Java ha una sola (ed implicita) variabile condition**. Questo è il suo **limite principale**: non si possono distinguere più condizioni di attesa (a differenza dei monitor con più condition variable esplicite → [[monitor]]). Il thread attivo nel monitor può sospendersi con `wait()`, che **rilascia il monitor** e inserisce il thread nel **wait set**; vi rimane finché un altro thread attivo nel monitor non invoca `notify()`/`notifyAll()`.

**Semantica del monitor JVM: "signal and continue"**. Diversamente dalla soluzione di **Hoare** (signal-and-wait), un thread Java che invoca `notify()` **rimane in possesso del monitor e continua la propria esecuzione** nella monitor region. Il thread svegliato non riprende subito: torna a competere per il lock (→ [[monitor]] per le tre semantiche).

**Modello di sincronizzazione** (Entry Set / Owner / Wait Set):
- i thread che vogliono entrare attendono nell'**Entry Set**; uno diventa **owner** del monitor ed esegue la sezione critica;
- (caso 1) l'owner **completa** la sezione critica → esce; (caso 2) l'owner esegue `wait()` → passa nel **Wait Set** rilasciando il monitor, così un thread dell'Entry Set viene sbloccato;
- se l'owner **non** invoca `notify()` prima di terminare, solo i thread dell'Entry Set competono per la risorsa;
- se invoca `notify()`/`notifyAll()`, uno (o più) thread passano dal **Wait Set** all'**Entry Set**.

### Cooperazione: wait / notify

```java
// Thread in attesa                       // Thread che abilita la condizione
synchronized(obj) {                       synchronized(obj) {
    while (<not condition>) {                  ...
        obj.wait();                            <condition goes true>;
    }                                          obj.notify();
    do_something();                            ...
}                                         }
```
Regole fondamentali:
- le primitive `wait()`/`notify()`/`notifyAll()` sono **ereditate dalla classe `Object`** e possono essere invocate **solo all'interno di sezioni critiche** (`synchronized`);
- > ⚠️ **`wait()` e `notify()` sono primitive di COOPERAZIONE: NON risolvono la mutua esclusione!** (Quella è data da `synchronized`.)
- > ⚠️ Al risveglio un thread **non può assumere che la sua condizione sia vera** (altri thread potrebbero essere stati svegliati indipendentemente), e Java non garantisce che un thread svegliato dopo una `wait()` acquisisca **immediatamente** il lock. **È essenziale rivalutare la condizione appena risvegliato → usare `while`, non `if`!**

**Varianti di `wait()`**: `wait()` (sospende finché `notify`/`notifyAll`/`interrupt`), `wait(long millis)` (si risveglia comunque dopo `millis`), `wait(long millis, int nanos)` (risoluzione al nanosecondo).

### Java 1.5 — `java.util.concurrent`

Meccanismi espliciti, alternativi a `synchronized`:
```java
Lock lock = new ReentrantLock();
lock.lock();
try { ... } finally { lock.unlock(); }   // finally garantisce l'unlock

Semaphore sem = new Semaphore(N);
sem.acquire();   // decrementa (blocca se 0)
sem.release();   // incrementa
sem.tryAcquire();// tenta senza bloccare

CountDownLatch latch = new CountDownLatch(N);
latch.await();       // attende fino a count = 0
latch.countDown();   // decrementa count
```
> 🎯 Esame: **limiti di `synchronized` e come superarli** → con `Lock`/`ReentrantLock`/`Semaphore` (lock interrompibili, `tryAcquire`, fairness, più condition variable). **`Lock` vs `ReentrantLock`**: `Lock` è l'**interfaccia**, `ReentrantLock` è l'**implementazione** rientrante (lo stesso thread può riacquisire il lock che già possiede senza autobloccarsi, come per `synchronized`; → [[threading]] per l'analogo `RLock` Python).

## Perché importa

La sincronizzazione è il meccanismo base per evitare race condition in Java — concetto centrale del corso. Il monitor `synchronized` con la sua unica condition implicita, la semantica signal-and-continue e la regola del `while` (non `if`) sono domande ricorrenti d'orale.

## Connessioni

- [[java-threading]] — i thread da sincronizzare, stati Blocked synch / Waiting
- [[monitor]] — il monitor Java (una condition, signal-and-continue) come istanza del costrutto monitor; confronto con Hoare
- [[semaforo]] — `Semaphore` di Java 1.5; mutua esclusione vs cooperazione
- [[threading]] — confronto con Python (`Lock`, `RLock`, `Condition`, `Semaphore`)
- [[produttore-consumatore]] — l'esempio deposito/preleva con wait/notifyAll

## Fonti

- [[21-java-sincronizzazione]]

_Aggiornato: 2026-06-04 — ingest iniziale_
_Aggiornato: 2026-06-20 — estensione da slide 02_JAVA_02: mutex per oggetto, metodi vs blocchi synchronized, metodi static synchronized (lock di classe vs istanza), soluzione corretta/non corretta della coppia check+write (Wrapper non sincronizzato + blocco synchronized condiviso), monitor Java (unica condition implicita), semantica signal-and-continue vs Hoare, modello Entry Set/Owner/Wait Set, wait/notify primitive di cooperazione (while non if), varianti wait(), Java 1.5 Lock/ReentrantLock/Semaphore/CountDownLatch_
