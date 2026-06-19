---
tipo: fonte
titolo: "Java Message Service (JMS)"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [java, jms, activemq, mom, ptp, pub-sub, connectionfactory, session, jndi, abstract-factory]
---

## Sommario

Slide su JMS (Java Message Service). JMS è lo standard Java (JSR 914) per l'accesso ai sistemi MOM. Si descrivono le interfacce JMS (ConnectionFactory, Connection, Session, MessageProducer/Consumer), i modelli PTP e Pub-Sub, il pattern Abstract Factory usato da JMS, JNDI e gli administered objects.

## Punti chiave

1. **JMS (JSR 914)**: set di interfacce che definiscono come un client Java accede a un sistema MOM — standard indipendente dal provider
2. **JMS definisce lo standard**; i programmi scritti con JMS funzionano con qualsiasi MOM compatibile (ActiveMQ, WebSphere MQ, TIBCO, SonicMQ...)
3. Il provider usato nel corso: **Apache ActiveMQ**
4. **Architettura**: Java Application → `javax.jms.*` (JMS API) → Provider-specific impl → ActiveMQ
5. **Domini di messaging JMS**:
   - **PTP**: `Queue` — ogni messaggio ha un solo consumer; queue conserva il messaggio finché non scade o viene consumato; consumer fa ACK
   - **Pub-Sub**: `Topic` — messaggi a N subscriber; topic conserva finché non consegnato ai subscriber correnti
6. **Interfacce JMS principali**:

   | High-level | PTP Domain | Pub/Sub Domain |
   |---|---|---|
   | `ConnectionFactory` | `QueueConnectionFactory` | `TopicConnectionFactory` |
   | `Connection` | `QueueConnection` | `TopicConnection` |
   | `Destination` | `Queue` | `Topic` |
   | `Session` | `QueueSession` | `TopicSession` |
   | `MessageProducer` | `QueueSender` | `TopicPublisher` |
   | `MessageConsumer` | `QueueReceiver`, `QueueBrowser` | `TopicSubscriber` |

7. **Session**: contesto single-threaded per inviare/ricevere messaggi
8. **MessageProducer**: invia messaggi; **MessageConsumer**: riceve messaggi (sincrono o asincrono)
9. **Pattern Abstract Factory in JMS**:
   - `javax.jms.*` definisce le interfacce (AbstractFactory, AbstractProduct)
   - Il provider (es. ActiveMQ) fornisce le implementazioni concrete
   - Il codice JMS è indipendente dal provider
10. **Administered Objects** — oggetti JMS pre-configurati:
    - `ConnectionFactory` e `Destination` (Queue/Topic)
    - Creati dall'amministratore del sistema e registrati in **JNDI**
    - I client recuperano gli administered objects tramite **JNDI lookup**
11. **JNDI (Java Naming and Directory Interface)**: naming service — mappa nomi → riferimenti a oggetti
12. Il programma JMS deve conoscere il nome JNDI e l'interfaccia JMS degli administered objects, **non** i dettagli del provider

## Concetti introdotti

- [[jms]]
- [[mom]]
- [[pub-sub]]

## Domande aperte

- Come si scrive concretamente un producer/consumer JMS?
- Ricezione asincrona con MessageListener?

## Domande da esame

- Cos'è JMS? Perché è un'API standard?
- Differenza tra PTP e Pub-Sub in JMS — interfacce coinvolte
- Cos'è il pattern Abstract Factory? Come si applica a JMS?
- Cos'è JNDI? Cos'è un administered object?
- Quali sono le interfacce JMS principali e il loro ruolo?
