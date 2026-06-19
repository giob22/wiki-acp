---
tipo: concetto
importanza_esame: media
prerequisiti: [pub-sub, mom, activemq]
---

## Definizione

Una **sottoscrizione durabile** (durable subscription) è una sottoscrizione a un **topic** in cui il broker memorizza i messaggi pubblicati mentre il subscriber è **disconnesso**, e glieli consegna alla riconnessione. Estende il disaccoppiamento temporale (proprio delle code PTP) anche al modello pub-sub.

## Spiegazione

Nel modello Publish-Subscribe standard, un subscriber su `/topic/...` riceve un messaggio **solo se è attivo nel momento della pubblicazione**. Se è disconnesso (crash, riavvio, manutenzione), i messaggi pubblicati in quella finestra sono **persi per sempre**. Il topic normale NON ha disaccoppiamento temporale → [[pub-sub]] [[mom]].

La sottoscrizione durabile risolve questo: il broker tiene traccia del subscriber tramite un'**identità stabile** e accumula per lui i messaggi mentre è offline.

**Identità stabile = due elementi:**
1. **`client-id`** — identificativo univoco del client (sul CONNECT)
2. **subscription name** — nome della sottoscrizione (sul SUBSCRIBE)

La coppia `(client-id, subscription-name)` dice al broker "sono lo stesso subscriber di prima" → riprende da dove era rimasto.

**Requisito**: i messaggi devono essere **persistent** (default in ActiveMQ con KahaDB) per sopravvivere anche a un riavvio del broker.

### STOMP — Python (`stomp.py`)

```python
conn = stomp.Connection([("localhost", 61613)])
conn.set_listener("", MyListener())

# client-id sul CONNECT → identità persistente
conn.connect(wait=True, headers={"client-id": "archive-client"})

# activemq.subscriptionName = header ActiveMQ-specifico per la durabilità
conn.subscribe(
    destination="/topic/checks",
    id=1,
    ack="auto",
    headers={"activemq.subscriptionName": "archive-sub"},
)
```

- `client-id` → header del **CONNECT**
- `activemq.subscriptionName` → header del **SUBSCRIBE** (STOMP 1.2 standard userebbe `durable-subscription-name`)
- Rimuovere la durable: `UNSUBSCRIBE` con stesso `activemq.subscriptionName`, oppure dalla console web → [[activemq]]

### JMS — Java

```java
connection.setClientID("archive-client");          // identità sul Connection
TopicSubscriber sub =
        session.createDurableSubscriber(topic, "archive-sub");  // nome subscription
connection.start();
// ...
sub.close();                       // chiude ma la durable resta registrata
session.unsubscribe("archive-sub"); // rimuove definitivamente la durable
```

→ [[jms]] [[jms-java]]

### Confronto

| | Topic normale | Topic durabile | Queue (PTP) |
|---|---|---|---|
| Offline → riconnessione | messaggi **persi** | messaggi **consegnati** | trattenuti |
| Disaccoppiamento temporale | ❌ | ✅ | ✅ |
| N consumer per messaggio | tutti gli attivi | per subscription | uno solo |

## Perché importa

È l'**unico modo** per ottenere insieme i due vantaggi: distribuzione a N subscriber (pub-sub) **e** disaccoppiamento temporale (nessun messaggio perso se un subscriber è giù). Scenario tipico da prova: un subscriber di archiviazione che non deve perdere nessun evento anche se riavviato.

> 🎯 Esame: domanda classica "se il subscriber si riavvia perde i messaggi pubblicati nel frattempo?" → **sì** con topic normale, **no** con sottoscrizione durabile. Serve `client-id` (CONNECT) + subscription name (SUBSCRIBE).

> 💡 Connessione: il topic durabile colma la differenza con la coda PTP — la queue dà disaccoppiamento temporale per natura (un consumer), la durable lo dà al pub-sub (N consumer) mantenendo identità per subscriber.

## Connessioni

- [[pub-sub]] — la durabile è una variante del modello Publish-Subscribe che aggiunge persistenza per subscriber offline
- [[mom]] — realizza il disaccoppiamento temporale, aspetto chiave dei MOM, anche sui topic
- [[activemq]] — broker che implementa le durable via header `activemq.subscriptionName` + KahaDB
- [[jms]] — controparte Java: `createDurableSubscriber` + `setClientID`
- [[stomp-python]] / [[jms-java]] — snippet con il boilerplate pronto

## Fonti

- [[15-python-mom]] / [[24-java-jms]] — base MOM/pub-sub/JMS
- Approfondimento esterno (STOMP 1.2 + ActiveMQ docs): le durable subscription **non compaiono esplicitamente nelle slide del corso** — aggiunte per colmare un gap di copertura

_Aggiornato: 2026-06-15 — creazione (gap segnalato dall'utente; non presente nelle slide raw)_
