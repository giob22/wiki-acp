---
tipo: concetto
importanza_esame: alta
prerequisiti: [mom]
---

## Definizione

**Publish-Subscribe (Pub-Sub)** è un pattern di comunicazione asincrona in cui i **publisher** producono messaggi associati a un **topic** senza conoscere i receiver, e i **subscriber** si iscrivono ai topic di interesse senza conoscere i producer.

## Spiegazione

**Flusso Pub-Sub**:
```
Publisher                  Broker/Topic              Subscriber
   |                           |                          |
   |── publish("ordine.nuovo") →|                          |
   |                           |── deliver ──────────────→|  (Sub1)
   |                           |── deliver ──────────────→|  (Sub2)
   |                           |── deliver ──────────────→|  (Sub3)
```

**Confronto PTP vs Pub-Sub**:

| | Point-to-Point (PTP) | Publish-Subscribe |
|---|---|---|
| Astrazione | Coda (Queue) | Topic |
| Consumer | 1 solo per messaggio | N subscriber |
| Persistenza | Finché non consumato | Finché non consegnato ai sub correnti |
| ACK | Il consumer fa ACK | Dipende dall'implementazione |
| Caso d'uso | Task queue, job processing | Notifiche eventi, log |

**Pattern Observer vs Pub-Sub**:

Observer (design pattern GoF):
- Subject mantiene lista diretta di observer
- Subject chiama direttamente `observer.update()`
- Problemi: scarsa scalabilità, gli observer devono conoscere il subject

Notification Service (evoluzione):
- Il broker (NS) gestisce subscriptions e notifiche
- Subject e observer non si conoscono

Pub-Sub MOM (distribuzione):
- Il broker è distribuito, persistente, affidabile
- Disaccoppiamento spaziale e temporale completo

**In Apache ActiveMQ**:
```
# Queue (PTP): prefisso /queue/
conn.subscribe("/queue/ordini", ...)   # un solo consumer riceve

# Topic (Pub-Sub): prefisso /topic/
conn.subscribe("/topic/eventi", ...)   # tutti i subscriber ricevono
```

**Sistemi event-based**: i sistemi pub-sub distribuiti sono detti **distributed event-based systems** — usati in scenari critici (SESAR per traffico aereo, NASPI per reti elettriche, FSE per sistemi sanitari).

> 🎯 Esame: Differenza Queue vs Topic in ActiveMQ, limitazioni del pattern Observer, cos'è un sistema event-based.

## Perché importa

Pub-Sub è il modello architetturale dietro molti sistemi distribuiti moderni (Kafka, MQTT, Redis Pub/Sub).

## Connessioni

- [[mom]] — il pub-sub è uno dei domini di messaging del MOM
- [[rpc]] — alternativa sincrona; pub-sub è asincrono

## Fonti

- [[15-python-mom]]

_Aggiornato: 2026-06-04 — ingest iniziale_
