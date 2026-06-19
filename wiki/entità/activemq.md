---
tipo: entità
categoria: framework
---

## Cos'è

**Apache ActiveMQ** è un popolare message broker open-source, **multiprotocollo**, scritto in **Java**, che supporta i protocolli standard del settore: **AMQP, MQTT, STOMP**. Supporta client scritti in diversi linguaggi (JavaScript, C, C++, **Python**, .Net...). Funziona da intermediario (broker) nei sistemi MOM → [[mom]].

## Come si usa nel corso

ActiveMQ è usato come broker MOM nel corso; i client Python si connettono tramite il protocollo **STOMP**.

**Versione usata nel corso**: **5.16.6** (scaricabile da activemq.apache.org/components/classic/download/).

### Administered objects: avviare il provider

È necessario **avviare il provider ActiveMQ prima** dell'esecuzione di un applicativo STOMP — il broker è un *administered object*, gestito fuori dal codice applicativo (coerente con la trasparenza dal provider, → [[middleware-trasparenza]]).

**Avvio**:
```bash
# Dalla directory di installazione
./bin/activemq start    # avvia il broker (oppure "activemq" in versioni meno recenti)
./bin/activemq stop     # ferma il broker
```

**Interfaccia web di amministrazione**:
- URL: `http://localhost:8161/`
- Credenziali default: `admin / admin`
- Funzionalità: monitoraggio code e topic, invio messaggi di test, statistiche

### Protocollo STOMP (Simple/Streaming Text Oriented Messaging Protocol)

STOMP è un protocollo **FRAME-based** che assume un **2-way streaming network protocol** (es. TCP): client e server comunicano scambiando **STOMP Frame** sullo stream. Fornisce un **formato interoperabile** (wire-level) che consente di parlare con qualsiasi broker STOMP-compatibile (ActiveMQ, Artemis, RabbitMQ) e tra linguaggi/piattaforme diverse. La libreria client Python è `stomp.py` (eseguibile anche standalone da command-line).

**Formato di uno STOMP Frame**:
```
COMMAND
Header1:value1
Header2:value2

Body^@          ← corpo terminato dal byte NULL (^@)
```

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

**Porte STOMP in ActiveMQ**: **61613** (comunicazione *plain*) · **62613** (comunicazione cifrata su **SSL**). L'IP può essere anche IPv6.

### API STOMP `stomp.py` nel dettaglio

- **`Connection([(IP, PORT), ...])`** — il parametro principale è `host_and_ports`: una **lista di coppie** `(IP, PORT)`; la lista permette al client di **provare più coppie** finché una connessione socket non riesce (failover).
- **`connect(username=None, passcode=None, wait=False, headers=None, with_connect_command=False, **keyword_headers)`** — `wait=True` attende che la connessione sia completata; `headers` = header aggiuntivi (es. `client-id`); `with_connect_command=True` usa il comando `CONNECT` invece di `STOMP`. Chiusura con `disconnect()`.
- **`send(destination, body, content_type=None, headers=None, **keyword_headers)`** — invia verso una destinazione (coda o topic); `content_type` = MIME type del messaggio.
- **`set_listener(name, Listener)`** + **`subscribe(destination, id, ack='auto', headers=None, **keyword_headers)`** — `id` = identificativo univoco della sottoscrizione; `ack` ∈ {`auto`, `client`, `client-individual`} (con `client`/`client-individual` si usano i metodi `ack`/`nack`).
- **Listener** — sottoclasse di `stomp.ConnectionListener` (esiste anche `PrintingListener` che stampa tutte le interazioni client-server). Abilita la **ricezione asincrona** (la libreria usa un solo thread). Si **ridefinisce `on_message(self, frame)`**, invocato a ogni messaggio ricevuto: `frame.body` (corpo), `frame.headers` (mappa header), `frame.cmd` (comando STOMP).

### STOMP: transazioni

STOMP permette di trasmettere messaggi a un broker dentro una **transazione**: i messaggi sono trattenuti dal server finché non si fa **`commit`** (effettivamente inoltrati) o **`abort`** (scartati). `begin()` ritorna un *transaction id* (o se ne può passare uno proprio):
```python
conn.subscribe('/queue/test', id=5)
txid = conn.begin()
conn.send('/queue/test', 'test1', transaction=txid)
conn.send('/queue/test', 'test2', transaction=txid)
conn.commit(txid)        # → i messaggi vengono inoltrati

txid = conn.begin()
conn.send('/queue/test', 'test4', transaction=txid)
conn.abort(txid)         # → i messaggi vengono scartati
```

**Sottoscrizioni durabili** (topic che trattiene messaggi se il subscriber è offline):
- richiede `client-id` sul CONNECT + `activemq.subscriptionName` sul SUBSCRIBE
- messaggi persistenti via KahaDB (default) → sopravvivono anche al restart del broker
- → [[sottoscrizioni-durabili]]

## Link ai concetti correlati

- [[mom]] — ActiveMQ è l'implementazione del MOM usata nel corso; protocolli AMQP/MQTT/STOMP
- [[pub-sub]] — ActiveMQ supporta entrambi i modelli PTP e Pub-Sub
- [[sottoscrizioni-durabili]] — durable subscription via `client-id` + `activemq.subscriptionName` + `persistent=True`
- [[middleware-trasparenza]] — administered object + STOMP wire-level = indipendenza dal provider
- [[socket]] — STOMP comunica su socket TCP (61613 plain, 62613 SSL)
- [[stomp-python]] — snippet boilerplate STOMP pronto

## Fonti

- [[15-python-mom]]

_Aggiornato: 2026-06-19 — estensione MODULO 3 (slide 15): multiprotocollo/administered objects, STOMP frame format, porte 61613/62613 SSL, API stomp.py dettagliata (Connection failover/connect/send/subscribe/Listener asincrono/ack modes), transazioni STOMP (begin/commit/abort)_
