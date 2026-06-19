---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, gil, oop]
---

## Definizione

Il modulo `threading` di Python fornisce un'**interfaccia di alto livello** per il multi-threading, costruita sopra il modulo di basso livello `_thread` (il cui uso diretto è **deprecato**). Crea thread a livello kernel (KLT). Utile per workload **I/O-bound** (networking, file). Non adatto per CPU-bound a causa del [[gil]].

Classi principali offerte: `Thread`, `Thread-local Data` (`local`), `Lock`/`RLock`, `Condition`, `Semaphore`, `Event`.

## Spiegazione

**main thread**: esiste un oggetto *main thread* (istanza di `_MainThread`) che corrisponde al flusso di controllo dell'intero programma Python. Tutti i thread **condividono lo spazio di memoria del processo padre**.

**Costruttore `Thread`**:
```python
Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
```
- `group`: riservato per future implementazioni di `ThreadGroup`, deve essere `None`
- `target`: il *callable object* invocato dal metodo `run`
- `name`: nome del thread
- `args` / `kwargs`: argomenti posizionali (tupla) e keyword (dict) passati al target
- `daemon`: booleano, se il thread è demone o meno

**Creazione thread (approccio funzione)**:
```python
import threading

def worker(nome):
    print(f"Thread {nome} partito")

t = threading.Thread(target=worker, args=("T1",))
t.start()    # avvia il thread
t.join()     # aspetta la terminazione
t.is_alive() # → False dopo join
```

**Creazione thread (approccio classe)**:
```python
class MioThread(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome

    def run(self):  # override di run()
        print(f"Thread {self.nome} in esecuzione")

t = MioThread("T1")
t.start()
t.join()
```

**Metodi principali della classe `Thread`**:
- `start()` — avvia il thread, portando all'esecuzione del metodo `run` non appena viene schedulato
- `run()` — contiene il corpo del thread (nell'approccio a classe si fa l'override di questo metodo)
- `join(timeout=None)` — **bloccante**: attende la terminazione (naturale o con eccezioni) del thread; `timeout` è il tempo massimo di attesa in secondi (float)
- `is_alive()` — ritorna `True` se il thread è ancora vivo. Va usato in combinazione con `join` quando si specifica un timeout: in caso di timeout scaduto, `join` ritorna sempre `None`, quindi serve `is_alive()` per sapere se il thread è ancora attivo

> 🎯 Esame: `join()` **non distrugge** l'oggetto thread. Dopo `join()` l'oggetto esiste ancora: si possono invocare i suoi metodi e leggere i suoi attributi (es. `is_alive()` → `False`).

**Thread daemon**:
```python
t = threading.Thread(target=worker)
t.daemon = True   # deve essere impostato PRIMA di start()
t.start()
# processo termina anche se t è ancora in esecuzione
```
- Thread non-daemon: il processo aspetta la loro terminazione prima di uscire — **il programma non può terminare se c'è almeno un thread non-daemon ancora vivo**
- Thread daemon: il processo **termina quando rimangono solo thread daemon**; vengono interrotti bruscamente alla terminazione del processo

**Precisazioni sui daemon** (slide):
- In Linux *daemon* indica un processo in background; **in Python sia daemon che non-daemon girano in background** — la differenza è solo nella gestione della terminazione
- I thread daemon vengono **interrotti** alla fine del processo: le loro risorse (file aperti, transazioni DB...) potrebbero **non essere rilasciate correttamente**. Per un arresto graduale → renderli non-daemon + meccanismi di segnalazione (es. un `Event`)
- Il valore iniziale di `daemon` è **ereditato dal thread creatore**
- Casi d'uso daemon: logging, manutenzione (pulizia file temporanei), monitoraggio risorse in background. Casi non-daemon: scrittura file/backup, richieste di rete, elaborazione dati che deve completare
- ⚠️ Jupyter **ignora** il flag daemon

### Lock — mutex semplice

Un `Lock` può trovarsi in due stati: **locked** o **unlocked** (creato unlocked).
- Quando un thread acquisisce il lock → passa a *locked*; ulteriori `acquire()` da altri thread li **bloccano in attesa**
- Quando il lock viene rilasciato → torna *unlocked* e uno dei thread in attesa viene risvegliato (quale, dipende dall'implementazione)

```python
lock = threading.Lock()
lock.acquire()       # blocca se già locked
# sezione critica
lock.release()
```

Firma completa: `acquire(blocking=True, timeout=-1)` → ritorna `True` se acquisito, `False` altrimenti.
- `blocking=False` → la chiamata non è bloccante, ritorna subito `False` se il lock è già preso
- `timeout` (float positivo) → attende al massimo `timeout` secondi, poi ritorna `False`
- `release()` → rilascia (nessun valore di ritorno); `locked()` → ritorna `True` se lo stato è locked

**`with` e primitive di sincronizzazione** — lo statement `with` acquisisce il lock e lo **rilascia automaticamente** alla fine del blocco:
```python
with lock:          # equivale a lock.acquire() ... lock.release()
    risorsa_condivisa += 1
```

### RLock — reentrant lock

Lock che può essere acquisito **più volte dallo stesso thread**. Utile per **funzioni ricorsive**, **metodi che chiamano altri metodi che fanno locking** o **sezioni critiche innestate** (con un `Lock` normale si andrebbe in **deadlock**). Oltre allo stato locked/unlocked introduce due concetti:
- **owning thread** — il thread che ha acquisito il lock
- **recursion level** — il numero di acquisizioni fatte dallo stesso thread

Se `acquire()` è invocata dall'owning thread, **non blocca** e incrementa il recursion level; `release()` decrementa il livello e solo quando arriva a **zero** il lock passa a unlocked (e può essere preso da altri thread).

### Condition — variabile condition

Permette a uno o più thread di **rimanere in attesa che una condizione si verifichi**, finché non vengono notificati da un altro thread. È sempre associata a un **lock**: di default ne crea automaticamente uno (**un `RLock`**), oppure se ne passa uno esistente al costruttore `Condition(lock=None)`.
- `acquire()` / `release()` — agiscono sul lock associato
- `wait(timeout=None)` — **rilascia il lock** e blocca fino a `notify()`/`notify_all()` (o scadenza timeout); al risveglio **ri-acquisisce** il lock e ritorna `False` se timeout scaduto, `True` altrimenti
- `wait_for(predicate, timeout=None)` — attende finché `predicate` (callable che ritorna bool) diventa `True`
- `notify(n=1)` — risveglia `n` thread in attesa; `notify_all()` — risveglia tutti

```python
# pattern produttore/consumatore con Condition
with cv:
    while not item_disponibile(queue):  # il while è NECESSARIO (vedi monitor signal-and-continue)
        cv.wait()
    consuma(queue)
# produttore
with cv:
    produci(queue)
    cv.notify()
```

### Semaphore — semaforo

Gestisce un **contatore interno**: inizializzato alla creazione, **decrementato** ad ogni `acquire()`, **incrementato** ad ogni `release()`. Quando il contatore arriva a **zero**, un ulteriore `acquire()` **blocca** il thread finché un altro thread non fa `release()`.
- `Semaphore(value=1)` — costruttore (default 1)
- `acquire(blocking=True, timeout=None)` / `release(n=1)` — rilascia `n` permessi, risvegliando fino a `n` thread

Usato per limitare l'accesso concorrente a una risorsa a **massimo N thread**.

### Event — segnalazione tra thread

Meccanismo semplice di comunicazione basato su `Condition` ma con API più snella. Un thread segnala un evento per il quale altri thread sono in attesa. Caratterizzato da un **flag interno** booleano:
- `set()` — pone il flag a `True`; risveglia tutti i thread in attesa
- `clear()` — pone il flag a `False`; chi farà `wait()` resterà bloccato
- `is_set()` — ritorna lo stato del flag
- `wait(timeout=None)` — blocca finché il flag non diventa `True` (ritorna subito se già `True`; ritorna `False` se timeout scaduto)

**Thread-local storage** (classe `local`):
Poiché i thread condividono lo spazio di memoria del processo, può servire definire **dati unici per ogni thread** per evitare effetti collaterali. L'oggetto `threading.local()` crea un'istanza i cui attributi sono **differenti per ogni thread**.
```python
local_data = threading.local()
local_data.valore = 42   # ogni thread ha la propria copia
```
> 🎯 Esame: senza `threading.local`, una variabile globale condivisa (es. `data['user'] = value`) viene **sovrascritta** in base alla velocità relativa dei thread → **race condition**. Con `threading.local` ogni thread vede solo il proprio dato.

**Queue thread-safe** (da modulo `queue`):
```python
from queue import Queue
q = Queue()
q.put(item)      # produttore
item = q.get()   # consumatore — blocca se vuota
```

> 🎯 Esame: Come creare un thread, differenza daemon/non-daemon, come usare Lock, perché il threading non scala su CPU-bound.

## Perché importa

Threading è usato nel corso per server gRPC concorrenti, server socket multi-client, consumer STOMP.

## Connessioni

- [[gil]] — limita il parallelismo su CPU-bound
- [[processo-thread]] — differenza thread/processo
- [[multiprocessing]] — alternativa per CPU-bound; offre primitive di sincronizzazione **equivalenti** (Lock, RLock, Semaphore, Condition, Event)
- [[socket]] — server socket usano threading per gestire più client
- [[semaforo]] — il `Semaphore` Python implementa il semaforo classico; il `Lock` è il caso mutex
- [[monitor]] — `Condition` + lock realizzano un monitor; il pattern `while + wait()` è la semantica *signal-and-continue*
- [[produttore-consumatore]] — risolto con `Condition` o `queue.Queue`

## Fonti

- [[11-python-concurrency]]
- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-04 — ingest iniziale_
_Aggiornato: 2026-06-19 — costruttore Thread completo, metodi (run/start/join/is_alive), ciclo di vita, daemon (Linux vs Python, risorse, ereditarietà), Lock (stati/acquire/locked/with), RLock (owning thread/recursion/deadlock), Condition (wait/wait_for/notify), Semaphore (contatore), Event, thread-local + race condition; da slide 11_
