---
tipo: snippet
tecnologia: stomp
linguaggio: python
---

# Boilerplate — STOMP (Python, `stomp.py` + ActiveMQ)

Client Python per ActiveMQ via protocollo STOMP (porta **61613**). Code (`/queue/...`) per PTP, topic (`/topic/...`) per pub-sub. → [[mom]] [[pub-sub]] [[activemq]]

## Setup

```bash
pip install stomp.py
# broker: ./bin/activemq start  (console web: http://localhost:8161, admin/admin)
```

## Producer / Sender

```python
import stomp
import sys

try:
    # auto_content_length=False: necessario se il consumer è JMS (Java) —
    # senza content-length il messaggio arriva come TextMessage, non BytesMessage
    conn = stomp.Connection([("localhost", 61613)], auto_content_length=False)
    conn.connect(wait=True)
except Exception as e:
    print(e)
    sys.exit(-1)

message = "motor-A|FAIL"
conn.send(destination="/queue/telemetry", body=message)   # o /topic/checks
print(f"inviato: {message}")

conn.disconnect()
```

## Consumer / Subscriber (listener asincrono)

```python
import stomp
import time
import sys


class MyListener(stomp.ConnectionListener):

    def on_message(self, frame):
        body = frame.body
        print(f"[RECV] {body}")

        # parsing tipico da prova: campi separati da '|'
        component_id, status = body.split("|")
        # logica: aggiorna stato, scrivi su file, ...

    def on_error(self, frame):
        print(f"[ERROR] {frame.body}")


if __name__ == "__main__":
    try:
        conn = stomp.Connection([("localhost", 61613)])
        conn.set_listener("", MyListener())
        conn.connect(wait=True)

        # ack='auto': il broker considera consegnato appena inviato
        conn.subscribe(destination="/topic/checks", id=1, ack="auto")

        print("in ascolto... (CTRL+C per terminare)")
        # il listener gira su thread interno: il main resta vivo
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        conn.disconnect()
        print("--- subscriber terminato ---")
```

## Pattern da prova: subscriber con stato + riscrittura file

```python
class StatsListener(stomp.ConnectionListener):

    def __init__(self):
        self.stats = {}   # {"motor-A": {"OK": 0, "WARNING": 0, "FAIL": 0}, ...}

    def on_message(self, frame):
        component_id, status = frame.body.split("|")
        print(f"[STATS] componentId={component_id} status={status}")

        comp = self.stats.setdefault(
            component_id, {"OK": 0, "WARNING": 0, "FAIL": 0})
        comp[status] += 1

        # riscrittura integrale del file ad ogni messaggio
        with open("stats.txt", "w") as f:
            for cid, c in self.stats.items():
                f.write(f"{cid}: OK={c['OK']} WARNING={c['WARNING']} FAIL={c['FAIL']}\n")
```

## Subscriber durabile (topic, no messaggi persi se offline)

Topic normale: messaggi pubblicati mentre il subscriber è disconnesso = **persi**. La sottoscrizione durabile fa trattenere i messaggi al broker e li consegna al reconnect. Serve identità stabile: `client-id` (CONNECT) + `activemq.subscriptionName` (SUBSCRIBE). → [[sottoscrizioni-durabili]]

```python
import stomp, time

conn = stomp.Connection([("localhost", 61613)])
conn.set_listener("", MyListener())

# client-id sul CONNECT: identifica il subscriber tra le riconnessioni
conn.connect(wait=True, headers={"client-id": "archive-client"})

# activemq.subscriptionName: nome durable (ActiveMQ-specifico)
conn.subscribe(
    destination="/topic/checks",
    id=1,
    ack="auto",
    headers={"activemq.subscriptionName": "archive-sub"},
)

while True:
    time.sleep(1)
```

> 🎯 Esame: con la durable un riavvio del subscriber NON perde i messaggi pubblicati nel frattempo (a differenza del topic normale). Rimuovere: `UNSUBSCRIBE` con stesso `activemq.subscriptionName` o da console web. Controparte JMS: `createDurableSubscriber` + `setClientID` → [[jms-java]].

## Destinazioni

| Destinazione | Modello | Comportamento |
|---|---|---|
| `/queue/nome` | PTP | un solo consumer riceve ogni messaggio |
| `/topic/nome` | Pub-Sub | tutti i subscriber attivi ricevono ogni messaggio |

> ⚠️ Interoperabilità con JMS: usare `auto_content_length=False` quando si **invia** verso consumer Java JMS, altrimenti il messaggio arriva come `BytesMessage` invece di `TextMessage` e il cast `(TextMessage)` fallisce.

> 🎯 Esame: porta STOMP 61613 vs porta JMS/OpenWire 61616 — stesso broker ActiveMQ, protocolli diversi. Java usa JMS, Python usa STOMP, e possono scambiarsi messaggi sulla stessa destinazione.

## Collegamenti

- [[activemq]] — il broker, avvio, console web
- [[mom]] — store-and-forward, disaccoppiamento
- [[pub-sub]] — PTP vs Pub-Sub
- [[sottoscrizioni-durabili]] — topic che non perde messaggi se il subscriber è offline
- [[jms-java]] — controparte Java sullo stesso broker

## Fonti

- [[15-python-mom]], svolgimenti sim-02 e sim-03

_Aggiornato: 2026-06-12 — creazione raccolta snippet_
