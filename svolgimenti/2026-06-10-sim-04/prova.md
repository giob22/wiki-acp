# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 10/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito in **Python** per la gestione di ordini di produzione in una piccola fabbrica. Il sistema è caratterizzato dai seguenti componenti.

```
FactoryClient (Python)
  10 thread → book() / deliver() via gRPC
        │
      (gRPC)
        │
        ▼
OrderManager (Python gRPC)           (HTTP POST)
  order_queue: lista + Condition  ──────────────►  TrackServer (Flask)
  maxsize = 5                                       → history.txt
                                                    → GET /stats
```

---

### FactoryClient

È un client con **10 thread** concorrenti che interagiscono con l'OrderManager.

Ogni thread, scelto casualmente, invoca **uno** dei due metodi gRPC:
- `Book(BookRequest)` — prenota uno slot di produzione
- `Deliver(Empty)` — ritira un ordine dalla coda

La scelta è casuale: ogni thread chiama con probabilità **60% `Book`** e **40% `Deliver`**.

Per `Book`, i parametri sono:
1. **order_id** *(String)*: nel formato `ORD-{N}` con N intero casuale tra 1 e 999 (es. `ORD-247`)
2. **product** *(String)*: scelto casualmente tra `chair`, `table`, `lamp`

Ogni thread attende **1 secondo** dopo ogni invocazione. Ogni thread effettua **2 invocazioni** (totale: 20 invocazioni).

Per ogni risposta ricevuta il thread stampa:
- Se Book: `[BOOK] order_id=... product=... → BOOKED`
- Se Deliver: `[DELIVER] order_id=... product=... → DELIVERED` (oppure `→ QUEUE EMPTY` se la risposta è vuota)

---

### OrderManager

Implementa il servizio gRPC `OrderService` con i due metodi.

Gestisce internamente una **`order_queue`** implementata con una **lista Python** e un oggetto `threading.Condition` (maxsize=5). **Non è permesso usare `queue.Queue` o `multiprocessing.Queue`.**

#### Metodo `Book(BookRequest) → Ack`

1. Acquisisce il lock della `Condition`
2. **Blocca** (`condition.wait()`) finché `len(order_queue) >= 5`
3. Aggiunge l'ordine `{"order_id": ..., "product": ...}` in coda
4. Notifica i thread in attesa (`condition.notify_all()`)
5. Rilascia il lock
6. Invia una richiesta **POST** all'endpoint `/history` del TrackServer con body JSON `{"operation": "book", "order_id": ..., "product": ...}`
7. Stampa: `[MANAGER] BOOK order_id=... product=... queued (size=...)`
8. Ritorna `Ack(status="BOOKED")`

#### Metodo `Deliver(Empty) → OrderItem`

1. Acquisisce il lock della `Condition`
2. **Blocca** (`condition.wait()`) finché `len(order_queue) == 0`
3. Estrae il primo elemento dalla lista (`order_queue.pop(0)`)
4. Notifica i thread in attesa (`condition.notify_all()`)
5. Rilascia il lock
6. Invia una richiesta **POST** all'endpoint `/history` del TrackServer con body JSON `{"operation": "deliver", "order_id": ..., "product": ...}`
7. Stampa: `[MANAGER] DELIVER order_id=... product=... (remaining=...)`
8. Ritorna `OrderItem(order_id=..., product=...)`

> **Nota:** il POST al TrackServer avviene **dopo** aver rilasciato il lock della Condition, per evitare di tenerlo occupato durante la chiamata HTTP.

---

### TrackServer

Implementa un server **Flask** che gestisce lo storico degli ordini ed espone una REST API con due endpoint:

- **`POST /history`** — riceve un payload JSON `{"operation": ..., "order_id": ..., "product": ...}` e:
  1. Appende al file **`history.txt`** la riga nel formato `operation|order_id|product` (es. `book|ORD-247|chair`)
  2. Aggiorna un dizionario in memoria `{product: {"booked": N, "delivered": N}}`
  3. Ritorna `200 OK`

- **`GET /stats`** — ritorna un JSON con i conteggi per prodotto, nel formato:
  ```json
  {
    "chair":  {"booked": 7, "delivered": 4},
    "table":  {"booked": 5, "delivered": 3},
    "lamp":   {"booked": 6, "delivered": 5}
  }
  ```

Lo studente progetti la REST API scegliendo opportunamente i metodi HTTP da utilizzare.

---

## Schema `.proto` (fornito)

```protobuf
syntax = "proto3";

service OrderService {
  rpc Book    (BookRequest) returns (Ack);
  rpc Deliver (Empty)       returns (OrderItem);
}

message BookRequest {
  string order_id = 1;
  string product  = 2;
}

message Ack {
  string status = 1;
}

message OrderItem {
  string order_id = 1;
  string product  = 2;
}

message Empty {}
```

Il candidato **non deve modificare** questo schema. Eseguire:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. orders.proto
```

---

## Vincoli tecnici

- Usare **gRPC** per la comunicazione tra FactoryClient e OrderManager
- La `order_queue` deve essere implementata con **lista Python + `threading.Condition`** (maxsize=5)
- **Vietato** usare `queue.Queue`, `multiprocessing.Queue` o altre strutture pre-built
- Il POST al TrackServer deve avvenire **fuori dal lock** della Condition
- Il TrackServer deve usare **Flask**; non è richiesto MongoDB (dati in memoria + file)

---

## File da consegnare

```
orders.proto              ← definizione servizio gRPC
orders_pb2.py             ← generato da protoc (non modificare)
orders_pb2_grpc.py        ← generato da protoc (non modificare)
factory_client.py         ← FactoryClient (10 thread)
order_manager.py          ← OrderManager (gRPC server, lista + Condition)
track_server.py           ← TrackServer (Flask)
history.txt               ← generato a runtime
```

---

## Sequenza di avvio

1. Avviare **TrackServer** (`python track_server.py`)
2. Avviare **OrderManager** (`python order_manager.py`)
3. Avviare **FactoryClient** (`python factory_client.py`)

---

## Test attesi

Il sistema è testato con: **1 FactoryClient** (10 thread), **1 OrderManager**, **1 TrackServer**

Verifica finale:
- FactoryClient stampa 20 righe `[BOOK]` o `[DELIVER]`
- OrderManager stampa 20 righe `[MANAGER]`
- `history.txt` contiene 20 righe nel formato `operation|order_id|product`
- `GET /stats` ritorna conteggi coerenti (somma booked + delivered per prodotto uguale alle righe in `history.txt`)
- Nessun deadlock: il sistema termina in circa 20 secondi

---

## Suggerimento struttura OrderManager

```python
import threading

order_queue = []
condition = threading.Condition()

class OrderServicer(orders_pb2_grpc.OrderServiceServicer):

    def Book(self, request, context):
        with condition:
            while len(order_queue) >= 5:
                condition.wait()
            order_queue.append({"order_id": request.order_id, "product": request.product})
            condition.notify_all()
        # POST fuori dal lock
        # TODO: requests.post(...)
        return orders_pb2.Ack(status="BOOKED")

    def Deliver(self, request, context):
        with condition:
            while len(order_queue) == 0:
                condition.wait()
            item = order_queue.pop(0)
            condition.notify_all()
        # POST fuori dal lock
        # TODO: requests.post(...)
        return orders_pb2.OrderItem(order_id=item["order_id"], product=item["product"])
```

---

*Prova generata il 2026-06-10 — Python puro: gRPC multi-thread + lista + Condition + Flask*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-10-sim-04` dopo aver completato la soluzione*
