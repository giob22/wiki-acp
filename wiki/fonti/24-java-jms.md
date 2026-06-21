---
tipo: fonte
titolo: "Java Message Service (JMS)"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [java, jms, activemq, mom, ptp, pub-sub, connectionfactory, session, jndi, abstract-factory, acknowledgement, transazioni, persistenza, message-listener, stomp]
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
13. **JNDI e servizio di naming**: il naming service è un livello di indirezione nome↔oggetto (binding); il client fa `lookup` per nome ignorando classe/locazione concreta dell'oggetto (disaccoppiamento → trasparenza di locazione). Concetti Name/Binding/Reference/Context. **JNDI = API standard + SPI**: l'app usa solo la JNDI API (`Context`, `lookup`, `bind`…), mentre lo specifico naming service è agganciato tramite un **Service Provider** (plugin che implementa la SPI) — JNDI è indipendente dal naming service reale (ActiveMQ, ma anche LDAP/RMI/DNS/file system); cambiare provider = cambiare plugin, non il codice (stessa logica dell'Abstract Factory). `Context` (bind/rebind/lookup/unbind/rename), `InitialContext`; le due proprietà selezionano il plugin (`java.naming.factory.initial` = factory del Service Provider) e l'URL del servizio (`java.naming.provider.url`). Bind lato amministratore/provider, lookup lato client (Administrative Tool→bind→JNDI→lookup→Client)
14. **Modello di programmazione generico (8 passi)**: lookup CF → lookup Destination → create Connection (+`start()` se consumer) → create Session → create Producer/Consumer → create Message → send/receive → cleanup
15. **Consumo sincrono vs asincrono**: sincrono = `receive()`/`receive(timeout)`/`receiveNoWait()`; asincrono = `MessageListener` con callback `onMessage`. Entrambi validi per PTP e Pub/Sub
16. **Struttura messaggio**: Header (`JMSMessageID`, `JMSCorrelationID`, `JMSReplyTo`, `JMSPriority`) + Properties (`<String,value>`, read-only se ricevuti, selettori SQL-like) + Body (5 tipi: `TextMessage`, `MapMessage`, `BytesMessage`, `StreamMessage`, `ObjectMessage`)
17. **Acknowledgement** (3 fasi: ricevi/processa/ack): `AUTO_ACKNOWLEDGE`, `CLIENT_ACKNOWLEDGE` (ack a livello sessione), `DUPS_OK_ACKNOWLEDGE` (lasco, possibili duplicati)
18. **Sessioni transacted**: `createSession(true, 0)`, `commit()`/`rollback()`, transazione confinata a una singola sessione
19. **Concorrenza**: thread-safe solo `Destination`/`ConnectionFactory`/`Connection`; `Session`/`Producer`/`Consumer` no (Session = contesto single-threaded)
20. **Persistenza**: `PERSISTENT` (default, memoria stabile) vs `NON_PERSISTENT`; via `setDeliveryMode` o parametri di `send`
21. **Interop JMS↔STOMP**: `content-length` decide Text vs Bytes message; durable in STOMP con coppia `client-id` + `activemq.subscriptionName`; lato STOMP si usa il physical-name

## Concetti introdotti

- [[jms]]
- [[mom]]
- [[pub-sub]]

## Domande aperte

- ~~Come si scrive concretamente un producer/consumer JMS?~~ → risolto: modello a 8 passi + esempi PTP/Pub-Sub in [[jms]]
- ~~Ricezione asincrona con MessageListener?~~ → risolto: `setMessageListener` + `onMessage` in [[jms]]

## Domande da esame

- Cos'è JMS? Perché è un'API standard?
- Differenza tra PTP e Pub-Sub in JMS — interfacce coinvolte
- Cos'è il pattern Abstract Factory? Come si applica a JMS?
- Cos'è JNDI? Cos'è un administered object? Cosa sono Name/Binding/Reference/Context?
- Quali sono le interfacce JMS principali e il loro ruolo?
- Quali sono gli 8 passi del modello di programmazione JMS? Dove differiscono sender e receiver? (`start()`)
- Differenza tra consumo sincrono e asincrono (`receive` vs `MessageListener`/`onMessage`)
- Com'è strutturato un messaggio JMS? Quali sono i 5 tipi di body? Cosa sono i selettori SQL-like?
- Le 3 modalità di acknowledgement e le 3 fasi del consumo
- Cos'è una sessione transacted? Cosa succede su `commit()`/`rollback()` (anche in PTP)?
- Quali oggetti JMS sono thread-safe e quali no? Perché?
- `PERSISTENT` vs `NON_PERSISTENT`: cosa garantiscono? Qual è il default?
- "Conviene attivare transazioni + persistenza + durable tutte insieme?" → no, overhead: solo quando servono
- Interop JMS↔STOMP: come si decide il tipo di messaggio? Come si fa una durable subscription da STOMP?
