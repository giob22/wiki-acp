---
tipo: concetto
importanza_esame: alta
prerequisiti: [mom, pub-sub, oop]
---

## Definizione

**JMS (Java Message Service)** è lo standard Java (JSR 914) per l'accesso ai sistemi MOM. Definisce un insieme di interfacce (`javax.jms.*`) che i provider MOM devono implementare — il codice JMS funziona con qualsiasi provider compatibile.

## Spiegazione

**Architettura a strati**:
```
[Java Application]
     ↕
[javax.jms.* — JMS API]
     ↕
[Provider-specific impl]
     ↕
[ActiveMQ / WebSphere MQ / TIBCO / ...]
```

**Interfacce principali**:

| Interfaccia | Ruolo |
|---|---|
| `ConnectionFactory` | Crea connessioni al broker |
| `Connection` | Connessione fisica al provider |
| `Session` | Contesto single-threaded per send/receive |
| `MessageProducer` | Invia messaggi |
| `MessageConsumer` | Riceve messaggi |
| `Destination` | Queue (PTP) o Topic (Pub/Sub) |

**Specializzazione per dominio**:

| Generale | PTP | Pub/Sub |
|---|---|---|
| `ConnectionFactory` | `QueueConnectionFactory` | `TopicConnectionFactory` |
| `Connection` | `QueueConnection` | `TopicConnection` |
| `Destination` | `Queue` | `Topic` |
| `Session` | `QueueSession` | `TopicSession` |
| `MessageProducer` | `QueueSender` | `TopicPublisher` |
| `MessageConsumer` | `QueueReceiver` | `TopicSubscriber` |

**Pattern Abstract Factory in JMS**:
- `javax.jms.*` = interfacce (AbstractFactory + AbstractProduct)
- ActiveMQ = `ConcreteFactory` che implementa le interfacce
- Il codice client dipende solo dalle interfacce — può essere usato con qualsiasi provider

**Administered Objects** e **JNDI**:
- `ConnectionFactory` e `Destination` sono **administered objects** — oggetti pre-configurati dall'amministratore
- Registrati in **JNDI** (Java Naming and Directory Interface) — naming service
- I client li recuperano tramite JNDI lookup (per nome) — ignorano i dettagli del provider

**Flusso tipico**:
```java
// JNDI lookup degli administered objects
Context ctx = new InitialContext(env);
QueueConnectionFactory factory = (QueueConnectionFactory) ctx.lookup("ConnectionFactory");
Queue queue = (Queue) ctx.lookup("myQueue");

// Creazione connessione e sessione
QueueConnection conn = factory.createQueueConnection();
QueueSession session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);

// Producer
QueueSender sender = session.createSender(queue);
TextMessage msg = session.createTextMessage("Ciao!");
sender.send(msg);

// Consumer (sincrono)
QueueReceiver receiver = session.createReceiver(queue);
conn.start();
Message m = receiver.receive();  // blocca

// Consumer asincrono — MessageListener
consumer.setMessageListener(msg -> { /* gestisci */ });
```

**Sottoscrizione durabile (Topic)**:
```java
connection.setClientID("archive-client");                       // identità
TopicSubscriber sub = session.createDurableSubscriber(topic, "archive-sub");
connection.start();
// ...
sub.close();                        // chiude la connessione, la durable resta
session.unsubscribe("archive-sub"); // rimuove definitivamente la durable
```
Il broker trattiene i messaggi del topic mentre il subscriber è offline e li consegna al reconnect → [[sottoscrizioni-durabili]].

> 🎯 Esame: Struttura interfacce JMS, ruolo JNDI e administered objects, come JMS applica il pattern Abstract Factory. Durable subscriber = `setClientID` + `createDurableSubscriber(topic, nome)`.

## Perché importa

JMS è il modo Java-standard per usare MOM. ActiveMQ nel corso è il provider JMS. Capire JMS significa capire come il pattern Abstract Factory disaccoppia il codice dal provider.

## Connessioni

- [[mom]] — JMS è l'API per accedere ai sistemi MOM in Java
- [[pub-sub]] — JMS supporta entrambi i modelli PTP e Pub/Sub
- [[sottoscrizioni-durabili]] — `createDurableSubscriber` per topic senza perdita messaggi
- [[proxy-pattern]] — il pattern Abstract Factory in JMS è concettualmente simile al pattern Proxy
- [[middleware-trasparenza]] — JMS come caso paradigmatico di specifica pura + Abstract Factory + JNDI

## Fonti

- [[24-java-jms]]

_Aggiornato: 2026-06-06 — aggiunto link a middleware-trasparenza_
