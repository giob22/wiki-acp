# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 14/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito in **Python** per la prenotazione di biglietti eventi. Il sistema è caratterizzato dai seguenti componenti.

```
TicketClient (Python)
  6 thread → reserve() / check() via TCP [pattern Proxy-Skeleton]
        │
     (TCP raw)
        │
        ▼
TicketServer (Python TCP)          (HTTP POST)
  inventory: dict + Lock  ─────────────────────► SalesServer (Flask)
  un thread per client                             → sales.log
                                                   → GET /report
```

---

### TicketClient

È un client con **6 thread** concorrenti che interagiscono con il TicketServer tramite il **pattern Proxy**.

Ogni thread usa un oggetto `TicketProxy` per invocare i metodi remoti e, scelto casualmente, chiama **uno** dei due metodi:
- `reserve(event_id, qty)` — prenota `qty` biglietti per un evento
- `check(event_id)` — controlla i posti disponibili

La scelta è casuale: **70% `reserve`**, **30% `check`**.

Per `reserve`, i parametri sono:
1. **event_id** *(str)*: scelto casualmente tra `"EVT-A"`, `"EVT-B"`, `"EVT-C"`
2. **qty** *(int)*: intero casuale tra `1` e `3`

Per `check`, il parametro è:
1. **event_id** *(str)*: scelto casualmente tra `"EVT-A"`, `"EVT-B"`, `"EVT-C"`

Ogni thread effettua **3 invocazioni** (totale: 18 invocazioni), attendendo **0.5 secondi** tra una invocazione e la successiva.

Per ogni risposta il thread stampa:
- Se reserve OK: `[CLIENT-{id}] RESERVE {event_id} qty={qty} → RESERVED`
- Se reserve ERROR: `[CLIENT-{id}] RESERVE {event_id} qty={qty} → NOT ENOUGH SEATS`
- Se check: `[CLIENT-{id}] CHECK {event_id} → {seats} seats available`

---

### TicketServer

Implementa un server TCP in ascolto sulla porta **5100**. Ogni connessione client è gestita in un **thread separato** (un thread per client).

Gestisce internamente un **inventario** implementato come dizionario Python protetto da `threading.Lock`:

```python
inventory = {"EVT-A": 20, "EVT-B": 15, "EVT-C": 10}
lock = threading.Lock()
```

#### Protocollo di comunicazione (linea terminata da `\n`)

```
Client → Server:  "RESERVE|{event_id}|{qty}\n"
Server → Client:  "OK|RESERVED {qty} for {event_id}\n"   (se posti disponibili)
                  "ERROR|NOT ENOUGH SEATS\n"              (se posti insufficienti)

Client → Server:  "CHECK|{event_id}\n"
Server → Client:  "OK|{seats}\n"
```

#### Skeleton — gestione richiesta `RESERVE|event_id|qty`

1. Acquisisce il `lock`
2. Se `inventory[event_id] >= qty`: decrementa `inventory[event_id] -= qty`, registra `remaining = inventory[event_id]`, rilascia il lock
3. Altrimenti: rilascia il lock, risponde `ERROR|NOT ENOUGH SEATS\n`, termina
4. Risponde `OK|RESERVED {qty} for {event_id}\n`
5. **Fuori dal lock**: invia richiesta POST a SalesServer `/sale` con body JSON `{"event_id": ..., "qty": ...}`
6. Stampa: `[SERVER] RESERVE {event_id} qty={qty} → OK (remaining={remaining})`

#### Skeleton — gestione richiesta `CHECK|event_id`

1. Acquisisce il `lock`
2. Legge `seats = inventory[event_id]`
3. Rilascia il lock
4. Risponde `OK|{seats}\n`
5. Stampa: `[SERVER] CHECK {event_id} → {seats} seats`

> **Nota:** il POST a SalesServer avviene **dopo** aver rilasciato il lock, per non bloccare l'inventario durante la chiamata HTTP.

---

### SalesServer

Implementa un server **Flask** in ascolto sulla porta **5200** che gestisce lo storico delle vendite.

- **`POST /sale`** — riceve payload JSON `{"event_id": ..., "qty": ...}` e:
  1. Aggiorna un dizionario in memoria `sales = {"EVT-A": 0, "EVT-B": 0, "EVT-C": 0}` sommando `qty`
  2. Appende al file **`sales.log`** la riga: `{event_id}|{qty}` (es. `EVT-A|2`)
  3. Ritorna `200 OK`

- **`GET /report`** — ritorna JSON con il totale biglietti venduti per evento:
  ```json
  {
    "EVT-A": 12,
    "EVT-B": 7,
    "EVT-C": 5
  }
  ```

---

## Suggerimento struttura TicketProxy

```python
import socket

class TicketProxy:
    def __init__(self, host="localhost", port=5100):
        self.host = host
        self.port = port

    def _call(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall((message + "\n").encode())
            return s.recv(1024).decode().strip()

    def reserve(self, event_id, qty):
        return self._call(f"RESERVE|{event_id}|{qty}")

    def check(self, event_id):
        return self._call(f"CHECK|{event_id}")
```

Il candidato **non deve modificare** questa struttura.

---

## Suggerimento struttura TicketServer (Skeleton)

```python
import socket
import threading
import requests

inventory = {"EVT-A": 20, "EVT-B": 15, "EVT-C": 10}
lock = threading.Lock()

def handle_client(conn):
    with conn:
        data = conn.recv(1024).decode().strip()
        parts = data.split("|")
        method = parts[0]

        if method == "RESERVE":
            event_id, qty = parts[1], int(parts[2])
            with lock:
                if inventory[event_id] >= qty:
                    inventory[event_id] -= qty
                    remaining = inventory[event_id]
                else:
                    conn.sendall("ERROR|NOT ENOUGH SEATS\n".encode())
                    return
            conn.sendall(f"OK|RESERVED {qty} for {event_id}\n".encode())
            # POST fuori dal lock
            # TODO: requests.post(...)
            print(f"[SERVER] RESERVE {event_id} qty={qty} → OK (remaining={remaining})")

        elif method == "CHECK":
            event_id = parts[1]
            with lock:
                seats = inventory[event_id]
            conn.sendall(f"OK|{seats}\n".encode())
            print(f"[SERVER] CHECK {event_id} → {seats} seats")

def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("localhost", 5100))
        s.listen()
        print("[SERVER] In ascolto su porta 5100...")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    serve()
```

---

## Vincoli tecnici

- Usare **Socket TCP raw** per la comunicazione tra TicketClient e TicketServer (pattern Proxy-Skeleton)
- **Vietato** usare gRPC, xmlrpc, o altri framework RPC
- Ogni connessione TCP deve essere gestita in un **thread separato** sul server
- L'inventario deve essere protetto da `threading.Lock` (non usare `queue.Queue`)
- Il POST a SalesServer deve avvenire **fuori dal lock**
- Il SalesServer deve usare **Flask**; non è richiesto MongoDB

---

## File da consegnare

```
ticket_client.py    ← TicketClient (6 thread, usa TicketProxy)
ticket_server.py    ← TicketServer (TCP multi-thread, Skeleton, inventory + Lock)
sales_server.py     ← SalesServer (Flask, POST /sale, GET /report)
sales.log           ← generato a runtime
```

---

## Sequenza di avvio

1. Avviare **SalesServer** (`python sales_server.py`)
2. Avviare **TicketServer** (`python ticket_server.py`)
3. Avviare **TicketClient** (`python ticket_client.py`)

---

## Test attesi

Il sistema è testato con: **1 TicketClient** (6 thread), **1 TicketServer**, **1 SalesServer**

Verifica finale:
- TicketClient stampa 18 righe `[CLIENT-*]` (RESERVE OK / RESERVE NOT ENOUGH SEATS / CHECK)
- TicketServer stampa 18 righe `[SERVER]`
- `sales.log` contiene tante righe quante sono le `RESERVE` andate a buon fine
- `GET /report` ritorna conteggi coerenti con `sales.log`
- La somma dei biglietti venduti per ogni evento non supera la disponibilità iniziale (`EVT-A: 20, EVT-B: 15, EVT-C: 10`)
- Nessuna race condition: l'inventario non va mai sotto zero

---

## Domande da esame sul pattern implementato

1. Perché il POST al SalesServer viene eseguito **fuori dal lock**? Cosa succederebbe se fosse dentro?
2. Cos'è il **pattern Proxy-Skeleton**? Qual è il ruolo di ciascuna parte in questa implementazione?
3. Perché si usa `threading.Lock` e non `threading.Condition`? Quando sarebbe necessaria la `Condition`?
4. Cosa garantisce `s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` e perché è utile?
5. Ogni thread di TicketClient apre **una nuova connessione TCP** per ogni invocazione. Quali sono i pro e i contro rispetto al riuso della connessione?

---

*Prova generata il 2026-06-14 — Python puro: Socket TCP proxy-skeleton + threading.Lock + Flask*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-14-sim-05` dopo aver completato la soluzione*
