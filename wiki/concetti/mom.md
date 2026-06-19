---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc, socket]
---

## Definizione

Il **Message-Oriented Middleware (MOM)** è uno strato software che permette la comunicazione **asincrona** tra applicazioni distribuite tramite un **message broker**. Il broker riceve, conserva e consegna messaggi, disaccoppiando sender e receiver nello spazio e nel tempo.

## Spiegazione

**Motivazione**:
- RPC è **sincrono**: il client si blocca ad aspettare; se il server è lento, rallenta tutto
- MOM introduce comunicazione **asincrona**: sender invia e continua l'esecuzione
- Soluzione per **scalabilità** e **high availability**

**Architettura MOM**:
```
[Applicazione A] → API → [Message Broker] → API → [Applicazione B]
```

**Caratteristiche chiave**:
1. **Disaccoppiamento spaziale**: A non conosce l'identità di B (e viceversa)
2. **Disaccoppiamento temporale**: B può non essere attivo quando A invia — il broker conserva il messaggio
3. **Store-and-forward**: broker conserva il messaggio finché la rete è disponibile
4. **Comunicazione asincrona**: A non si blocca nell'attesa che B riceva

**Domini di messaging**:

**PTP (Point-to-Point)**:
- Astrazione: **coda** (queue)
- Ogni messaggio ha **un solo consumer**
- Il messaggio persiste finché non viene consumato o scaduto
- Il consumer invia **ACK** alla corretta ricezione
```
Producer → [Queue] → Consumer (uno solo)
```

**Publish-Subscribe (Pub-Sub)**:
- Astrazione: **topic**
- I publisher pubblicano messaggi su un topic
- I subscriber si iscrivono a topic di interesse
- Ogni messaggio può essere ricevuto da **N subscriber**
- Il topic conserva il messaggio finché non è stato consegnato a tutti i subscriber correnti
```
Publisher → [Topic] → Subscriber 1
                   → Subscriber 2
                   → Subscriber N
```

**Pattern Observer vs MOM**:
- Observer pattern: subject notifica direttamente i suoi observer — scarsa scalabilità, accoppiamento
- Notification Service: terza entità (NS = broker) gestisce subscriptions e notifiche — più scalabile
- Il pub-sub MOM è essenzialmente un Notification Service distribuito

**Evento e Notifica**:
- **Evento**: condizione rilevata da/in un'applicazione, comunicata al broker
- **Notifica**: atto di informare i subscriber dell'occorrenza dell'evento

**Protocolli MOM**:
- **AMQP**: binario, popolare, per interoperabilità enterprise
- **MQTT**: leggero, pub-sub, standard ISO, progettato per IoT/edge
- **STOMP**: testuale, semplice, wire-level format per qualsiasi broker compatibile

> 🎯 Esame: Differenza PTP vs Pub-Sub, disaccoppiamento spaziale/temporale, perché MOM è preferibile a RPC per scalabilità.

## Perché importa

MOM è usato in sistemi ad alta scala e alta disponibilità (SESAR, NASPI, FSE). Il corso usa ActiveMQ + STOMP come implementazione concreta.

## Connessioni

- [[pub-sub]] — modello di messaging del MOM
- [[rpc]] — alternativa sincrona al MOM
- [[socket]] — il broker comunica via socket TCP
- [[activemq]] — broker MOM open-source usato nel corso (STOMP, AMQP, MQTT)
- [[middleware-trasparenza]] — STOMP/AMQP/JMS come meccanismi di indipendenza dal provider

## Fonti

- [[15-python-mom]]
- [[13-sistemi-middleware]]

_Aggiornato: 2026-06-06 — aggiunti link a activemq, middleware-trasparenza_
