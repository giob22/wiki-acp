---
tipo: concetto
importanza_esame: alta
prerequisiti: [proxy-pattern, multiprocessing, threading, socket, jms, mom, grpc, flask, mongodb]
---

#flashcards/acp

## Definizione

Insieme di pattern architetturali e implementativi che si ripetono sistematicamente nelle prove pratiche d'esame di ACP. Riconoscerli permette di abbozzare la soluzione nei primi 10 minuti.

## Spiegazione

### Pattern 1 — Architettura a layer (sempre)

Ogni prova ha sempre 3-4 componenti disposti in layer:

```
[Client/User]  →  [Server/Manager]  →  [Consumer(s)]
   (genera)         (smista)            (elabora + scrive file)
```

Esempi:
- User → Printer Server → BW Printer / Color Printer
- Service → Logging Server → Error Checker / Info Filter
- Voter → Vote Manager → DB Server

---

### Pattern 2 — Client N richieste con sleep (sempre)

Il client genera sempre **10 o 20 richieste** con **1-2 secondi** di attesa tra l'una e l'altra.

```python
for i in range(10):
    proxy.metodo(param1, param2)
    time.sleep(1)
```

I parametri sono **generati casualmente** (random.choice, random.randint).

---

### Pattern 3 — Produttore/consumatore (sempre)

È sempre presente. Due varianti:

**Process-safe** — usare quando il testo dice "processo produttore" e "processo consumatore":
```python
from multiprocessing import Queue, Process
q = Queue()

def producer(q): q.put(item)
def consumer(q):
    while True:
        item = q.get()  # blocca finché non c'è qualcosa
        # elabora
```

**Thread-safe con lista** — usare quando il testo specifica lista + maxsize:
```python
import threading
lock = threading.Condition()
queue = []
MAX = 5

def producer(item):
    with lock:
        while len(queue) >= MAX:
            lock.wait()
        queue.append(item)
        lock.notify_all()

def consumer():
    with lock:
        while len(queue) == 0:
            lock.wait()
        item = queue.pop(0)
        lock.notify_all()
    return item
```

> 🎯 Esame: Se il testo dice "lista" → usare lista+Condition. Se dice "queue process-safe" → `multiprocessing.Queue`.

Nelle prove, come scegliere tra lista+Condition e multiprocessing.Queue?
?
Testo dice 'lista (condivisa)' → lista + Condition (con while). Testo dice 'queue process-safe' → multiprocessing.Queue.


---

### Pattern 4 — Routing messaggi (quasi sempre)

I messaggi vengono smistati su canali/file diversi in base a un campo:

```python
if tipo == "color":
    conn.send("/queue/color", body)
else:
    conn.send("/queue/bw", body)
```

Il consumer legge solo dal suo canale e filtra ulteriormente in base a un parametro CLI:

```python
filtro = sys.argv[1]  # es. "bw" o "gs"
if filtro in body:
    # scrivi su file + stampa a video
```

---

### Pattern 5 — Proxy-Skeleton per ereditarietà (quando c'è Socket TCP)

Ogni volta che la comunicazione è Socket TCP → il testo chiede esplicitamente proxy-skeleton.

**Struttura Python:**
```python
# Interfaccia
class IService:
    def metodo(self, p1, p2): pass

# Proxy (lato client)
class ServiceProxy(IService):
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))
    def metodo(self, p1, p2):
        msg = f"{p1}#{p2}"
        self.sock.send(msg.encode())
        return self.sock.recv(1024).decode()

# Skeleton (lato server, classe base astratta)
class ServiceSkeleton(IService):
    def run(self):
        s = socket.socket()
        s.bind(('', PORT))
        s.listen()
        while True:
            conn, _ = s.accept()
            data = conn.recv(1024).decode()
            p1, p2 = data.split('#')
            result = self.metodo(p1, p2)  # upcall
            conn.send(str(result).encode())

# Implementazione concreta (eredita da Skeleton)
class ServiceImpl(ServiceSkeleton):
    def metodo(self, p1, p2):
        # logica reale
        return result
```

> 🎯 Esame: "skeleton per ereditarietà" = `ServiceImpl extends ServiceSkeleton`. ServiceImpl NON gestisce la rete — la eredita.

Cosa significa 'skeleton per ereditarietà' nel Proxy-Skeleton?
?
ServiceImpl extends ServiceSkeleton: ServiceImpl NON gestisce la rete (la eredita), implementa solo i metodi astratti con la logica.


---

### Pattern 6 — Scrittura su file (sempre)

Il consumatore finale scrive sempre su file (append):

```python
with open("output.txt", "a") as f:
    f.write(messaggio + "\n")
```

Il file viene scritto solo se il messaggio supera il filtro (contiene la stringa CLI).

---

### Pattern 7 — Mutua esclusione sul metodo server (quando richiesta esplicitamente)

Se il testo dice "il metodo deve essere eseguito in mutua esclusione":

```python
# Python
lock = threading.Lock()
def metodo(self, p1, p2):
    with lock:
        # corpo del metodo

// Java
public synchronized void metodo(String p, int t) {
    // corpo
}
```

---

### Tabella tecnologie per combinazione

| Tecnologie | Esempio reale | Pattern concorrenza |
|-----------|---------------|---------------------|
| Socket TCP + STOMP | 2023-11 (Python) | multiprocessing |
| JMS + STOMP | 2024-03 (Java+Python) | multiprocessing |
| gRPC + Flask | 2024-06 (Python) | threading + lista |
| STOMP + Flask + MongoDB | 2024-07 (Python) | threading |
| Socket TCP + JMS | 2024-10 (Java) | threading |

**Tecnologie non ancora combinate** (probabili in esami futuri):
- gRPC + STOMP
- gRPC + MongoDB
- Socket TCP + Flask + MongoDB (Python)

---

### Checklist per ogni prova

Prima di scrivere codice, identifica:
- [ ] Quanti componenti? Quale lingua?
- [ ] Quale protocollo di comunicazione tra ogni coppia?
- [ ] Produttore/consumatore: processo o thread? Lista o Queue?
- [ ] C'è Socket TCP? → serve proxy-skeleton per ereditarietà
- [ ] Routing: su quale campo? Verso quali canali?
- [ ] Filtro CLI: quale parametro? Cosa filtra?
- [ ] File di output: quali? Chi li scrive?
- [ ] Mutua esclusione esplicita richiesta?

## Perché importa

Questi pattern coprono ~90% del codice da scrivere. Riconoscerli riduce il tempo di progettazione da 30 a 10 minuti, lasciando più tempo all'implementazione.

## Connessioni

- [[proxy-pattern]] — Pattern 5 in dettaglio
- [[multiprocessing]] — Pattern 3 (variante process-safe)
- [[threading]] — Pattern 3 (variante thread-safe) e Pattern 7
- [[socket]] — Pattern 5 trigger
- [[mom]] — Pattern 4 (STOMP routing)
- [[jms]] — Pattern 4 (JMS routing)
- [[grpc]] — alternativa a Socket+proxy per RPC
- [[flask]] — consumer finale HTTP
- [[mongodb]] — persistenza nel consumer finale

## Fonti

- [[prove-esame-2023-2024]] — 5 prove analizzate

_Aggiornato: 2026-06-07 — creazione da analisi prove 2023-2024_
