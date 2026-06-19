---
tipo: entità
categoria: framework
---

## Cos'è

**Apache ActiveMQ** è un popolare message broker open-source, scritto in Java, che supporta protocolli standard: AMQP, MQTT, STOMP. Funziona da intermediario (broker) nei sistemi MOM.

## Come si usa nel corso

ActiveMQ è usato come broker MOM nel corso; i client Python si connettono tramite il protocollo **STOMP**.

**Versione usata nel corso**: **5.16.6**

**Avvio**:
```bash
# Dalla directory di installazione
./bin/activemq start    # avvia il broker
./bin/activemq stop     # ferma il broker
```

**Interfaccia web di amministrazione**:
- URL: `http://localhost:8161/`
- Credenziali default: `admin / admin`
- Funzionalità: monitoraggio code e topic, invio messaggi di test, statistiche

**Protocollo STOMP in Python**:
```bash
pip install stomp.py
```

```python
import stomp

class MessageListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print(f"Ricevuto: {frame.body}")

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', MessageListener())
conn.connect('admin', 'admin', wait=True)

# Subscribe (riceve messaggi)
conn.subscribe('/queue/test', id=1, ack='auto')

# Send (invia messaggio)
conn.send('/queue/test', body='Ciao!', headers={})

# Disconnect
conn.disconnect()
```

**Destinazioni STOMP**:
- `/queue/nome` — Point-to-Point (un solo consumer)
- `/topic/nome` — Publish-Subscribe (tutti i subscriber)

**Porta default STOMP**: 61613

**Sottoscrizioni durabili** (topic che trattiene messaggi se il subscriber è offline):
- richiede `client-id` sul CONNECT + `activemq.subscriptionName` sul SUBSCRIBE
- messaggi persistenti via KahaDB (default) → sopravvivono anche al restart del broker
- → [[sottoscrizioni-durabili]]

## Link ai concetti correlati

- [[mom]] — ActiveMQ è l'implementazione del MOM usata nel corso
- [[pub-sub]] — ActiveMQ supporta entrambi i modelli PTP e Pub-Sub
- [[sottoscrizioni-durabili]] — durable subscription via `activemq.subscriptionName`
- [[socket]] — STOMP comunica su socket TCP sulla porta 61613

## Fonti

- [[15-python-mom]]

_Aggiornato: 2026-06-04 — ingest iniziale_
