---
tipo: fonte
titolo: "Message-oriented Middleware in Python"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [mom, activemq, stomp, pub-sub, ptp, comunicazione-indiretta, broker, observer, amqp, mqtt]
---

## Sommario

Slide sul Message-Oriented Middleware (MOM) in Python. Si motivano i MOM come alternativa asincrona agli RPC per scalabilità e alta disponibilità. Si descrivono i modelli Point-to-Point e Publish-Subscribe, il pattern Observer e la sua estensione con Notification Service, i protocolli AMQP/MQTT/STOMP, Apache ActiveMQ come broker e il client Python STOMP.

## Punti chiave

1. **Motivazione MOM**: RPC è sincrono → collo di bottiglia; MOM usa **comunicazione asincrona** per scalabilità e high availability
2. **Comunicazione indiretta**: sender e receiver comunicano tramite **intermediario** (broker) — no accoppiamento diretto
3. **Tipi di comunicazione indiretta**: group communication, shared memory, **code di messaggi** (PTP), **publish-subscribe**
4. **MOM (Message-Oriented Middleware)**: middleware che gioca il ruolo di **message broker** tramite store-and-forward
5. **Aspetti chiave MOM**:
   - Recapita messaggi anche su macchine diverse
   - Conserva messaggi se il receiver non è attivo (disaccoppiamento temporale)
   - Il sender non si blocca (comunicazione asincrona)
6. **Disaccoppiamento spaziale**: sender non conosce l'identità del receiver
7. **Disaccoppiamento temporale**: sender e receiver non devono essere attivi contemporaneamente
8. **Domini di messaging**:
   - **PTP (Point-to-Point)**: coda di messaggi; ogni messaggio ha **un solo consumer**; receiver invia ACK
   - **Publish-Subscribe**: messaggi associati a **topic**; ogni messaggio può avere **N subscriber**
9. **Pattern Observer**: subject mantiene lista di observer; notifica su evento — problema: scarsa scalabilità
10. **Notification Service**: terza entità (NS) gestisce subscriptions e notifiche — risolve i limiti di Observer
11. **Evento** = condizione rilevata; **Notifica** = atto di informare i subscriber
12. **Protocolli MOM**:
    - **AMQP**: binario wire-level, molto popolare
    - **MQTT**: leggero, pub-sub, ISO standard, per IoT/edge
    - **STOMP**: testo-based, semplice, interoperabile con qualsiasi broker compatibile
13. **Apache ActiveMQ**: broker open-source Java-based, supporta AMQP, MQTT, STOMP; versione usata nel corso: **5.16.6**
14. Avvio: `./activemq start`; interfaccia web: `http://localhost:8161/` (admin/admin)
15. **STOMP in Python**: libreria `stomp.py`; connessione → subscribe/send → disconnect

## Concetti introdotti

- [[mom]]
- [[pub-sub]]
- [[rpc]]
- [[activemq]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è un MOM? Perché si usa al posto di RPC?
- Differenza tra PTP e Publish-Subscribe
- Cos'è il disaccoppiamento spaziale e temporale?
- Pattern Observer: cos'è e quali sono i suoi limiti?
- Cos'è il Notification Service?
- Differenza tra AMQP, MQTT e STOMP
- Come si avvia ActiveMQ?
