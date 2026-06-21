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
- Colmano il **gap tra le interfacce JMS standard e la tecnologia specifica del provider**: incapsulano dettagli provider-dependent, ma sono recuperati tramite meccanismo standard (JNDI) e acceduti tramite interfacce standard JMS
- Registrati in **JNDI** (Java Naming and Directory Interface) — naming service
- I client li recuperano tramite JNDI lookup (per nome) — ignorano i dettagli del provider
- Il programma JMS deve conoscere **solo** il nome JNDI e l'interfaccia JMS dell'administered object, **non** i dettagli del provider

### Il servizio di naming (JNDI)

**A cosa serve un naming service** — è un **livello di indirezione** tra un *nome logico* e l'*oggetto reale*. Un naming service mantiene un insieme di **binding** tra nomi e riferimenti a oggetti (o direttamente a oggetti). Il client chiede l'oggetto **per nome** (`lookup`) e riceve il riferimento, **senza sapere** dove l'oggetto si trovi né di che classe concreta sia. In JMS questo è ciò che permette il disaccoppiamento: il client conosce solo il nome JNDI e l'interfaccia JMS dell'administered object, mentre la classe concreta provider-dependent (es. una `ActiveMQConnectionFactory`) viene risolta a runtime dal naming service. È un caso applicato di **trasparenza di locazione/accesso** → [[middleware-trasparenza]].

| Concetto JNDI | Significato |
|---|---|
| **Name** | nome dato all'oggetto registrato |
| **Binding** | associazione nome ↔ oggetto |
| **Reference** | puntatore a un oggetto |
| **Context** | insieme di associazioni nome-oggetto; tutte le operazioni avvengono rispetto a un Context |

**JNDI = API standard + architettura a Service Provider (SPI)** — **Java Naming and Directory Interface (JNDI)** è un'interfaccia che espone le funzionalità *comuni* a qualsiasi naming service. Il punto chiave: **JNDI è indipendente dallo specifico servizio di naming**. È strutturata su due livelli:

- **API** (lato client): ciò che il programma JMS usa — `Context`, `lookup`, `bind`… L'applicazione parla **solo** con questa API, sempre uguale.
- **SPI — Service Provider Interface** (lato implementazione): lo specifico naming service è "agganciato" a JNDI tramite un **plugin chiamato Service Provider**, che implementa la SPI traducendo le chiamate JNDI standard verso il naming service reale.

```
[Applicazione JMS]
      ↓  usa
[JNDI API]   (Context, lookup, bind, ...)   ← sempre identica
      ↓  delega via SPI
[Service Provider]  (plugin intercambiabile)
      ↓
[Naming service reale]  (es. quello di ActiveMQ, ma anche LDAP, RMI registry, DNS, file system...)
```

> 💡 Stessa idea dell'Abstract Factory di JMS: l'app dipende da un'**interfaccia standard** (JNDI API), l'implementazione concreta (Service Provider) è sostituibile senza toccare il codice client. Cambiare provider = cambiare il plugin SPI, non l'applicazione.

**Quale Service Provider e come si raggiunge** — il client seleziona il Service Provider e localizza il naming service configurando due proprietà:
- `java.naming.factory.initial` → la **factory del Context**, ovvero la classe del Service Provider da caricare (per ActiveMQ: `org.apache.activemq.jndi.ActiveMQInitialContextFactory`);
- `java.naming.provider.url` → l'**URL** dove il naming service è raggiungibile (es. `tcp://127.0.0.1:61616`).

**API del Context** — `Context` è l'interfaccia coi metodi per aggiungere/cercare/rimuovere binding; ogni operazione JNDI avviene **rispetto a un Context** (che rappresenta un insieme di binding). `InitialContext` ne è l'implementazione, punto d'ingresso del naming.

| Metodo `Context` | Azione |
|---|---|
| `void bind(String name, Object o)` | crea il binding (il nome **non** deve essere già associato) |
| `void rebind(String name, Object o)` | crea/sovrascrive il binding |
| `Object lookup(String name)` | risolve il nome → ritorna l'oggetto/riferimento |
| `void unbind(String name)` | rimuove il binding |
| `void rename(String old, String new)` | rinomina un binding |

> Nota: in JMS gli administered objects vengono **bindati** dall'amministratore/provider (lato setup) e il client tipicamente fa solo `lookup` (lato uso) — è il diagramma *Administrative Tool → bind → JNDI Namespace → lookup → JMS Client* della slide.

```java
Hashtable<String,String> prop = new Hashtable<>();
prop.put("java.naming.factory.initial",
         "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
prop.put("queue.test", "mytestqueue");   // jndi-name → physical-queue-name
Context jndiContext = new InitialContext(prop);
```
> 💡 Il prefisso `queue.` (o `topic.`) serve solo a dichiarare la destination nelle proprietà: **non** fa parte del nome JNDI usato nel `lookup` (`lookup("test")`, non `lookup("queue.test")`).

**Modello di programmazione generico JMS** — lo sviluppo di un client segue 8 passi fissi (prima va avviato il provider, che attiva il servizio JNDI):

1. `lookup` di una `ConnectionFactory` da JNDI
2. `lookup` di una `Destination` da JNDI
3. creazione di una `Connection` dalla ConnectionFactory — **3.1.** `connection.start()` se sei un consumer (abilita il *delivery* dei messaggi: senza `start()` il receiver non riceve nulla)
4. creazione di una (o più) `Session` dalla Connection
5. creazione di `MessageProducer` / `MessageConsumer` da Session + Destination
6. creazione di un `Message` dalla Session
7. invio / ricezione dei messaggi
8. cleanup delle risorse (`close()` su producer/consumer, session, connection)

> 🎯 Esame: l'unica differenza tra sender e receiver nei primi passi è lo **step 3.1** (`start()`): obbligatorio sul lato che riceve, assente sul lato che invia.

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

## Consumo dei messaggi: sincrono vs asincrono

Un `MessageConsumer` (receiver/subscriber) può consumare in due modalità — valide sia per PTP che per Pub/Sub.

**Sincrono** — il client preleva esplicitamente il messaggio con `receive`:
- `receive()` — **blocca** finché non arriva un messaggio
- `receive(long timeout)` — riceve un messaggio entro il timeout, poi ritorna
- `receiveNoWait()` — riceve solo se il messaggio è **immediatamente** disponibile (≈ receive con timeout minimo)

**Asincrono** — il client registra un `MessageListener` sul consumer; il provider invoca `onMessage` a ogni arrivo (callback). L'interfaccia `MessageListener` ha un solo metodo, `onMessage(Message m)`.

```java
public class TextMsgListener implements MessageListener {
    public void onMessage(Message m) {
        try { System.out.println(((TextMessage) m).getText()); }
        catch (JMSException e) { e.printStackTrace(); }
    }
}
// registrazione sul consumer
receiver.setMessageListener(new TextMsgListener());
```

## Struttura di un messaggio JMS

Ogni messaggio ha tre parti: **Header · Properties · Body**.

- **Header** — campi standard per invio/identificazione, acceduti con `getJMS*`/`setJMS*`:
  - `JMSMessageID` — identificativo univoco
  - `JMSCorrelationID` — collega un messaggio a un altro (es. richiesta ↔ risposta)
  - `JMSReplyTo` — `Destination` (definita dal client) verso cui inviare la risposta
  - `JMSPriority` — priorità 0–9 (9 = più alta)
- **Properties** — coppie `<String, value>` (proprietà applicative, standard JMS o del vendor); gestite con `set*Property`/`get*Property`; in un messaggio ricevuto sono **read-only**. Supportano **selettori con sintassi SQL-like** per filtrare i messaggi lato consumer:
  ```java
  session.createSubscriber(topic, "prop1 > 6 AND prop2 = 'test'");
  ```
- **Body** — il contenuto vero e proprio; 5 tipologie:

| Tipo | Contiene | Metodi tipici |
|---|---|---|
| `TextMessage` | `String` | `getText`, `setText` |
| `MapMessage` | coppie nome/valore | `setString`, `setDouble`, `getDouble`… |
| `BytesMessage` | stream di byte non interpretati | `writeBytes`, `readBytes` |
| `StreamMessage` | stream di valori primitivi | `writeString`, `readString`… |
| `ObjectMessage` | oggetto `Serializable` | `setObject`, `getObject` |

## Acknowledgement

Il corretto consumo di un messaggio avviene in **3 fasi**: il client (1) riceve, (2) processa, (3) fa l'**acknowledge**. Chi fa l'ack dipende dalla modalità, fissata dal **secondo parametro** di `createSession`:

| Modalità | Comportamento |
|---|---|
| `AUTO_ACKNOWLEDGE` | la sessione conferma automaticamente quando il client ritorna da `receive` (o quando `onMessage` termina). Con receive sincrona, ricezione e ack avvengono in un'unica fase |
| `CLIENT_ACKNOWLEDGE` | il client conferma esplicitamente con `message.acknowledge()`; l'ack è **a livello di sessione** → confermare un messaggio conferma **tutti** quelli consumati nella sessione |
| `DUPS_OK_ACKNOWLEDGE` | ack "lasco" (ack ogni N messaggi o a intervalli); più efficiente ma in caso di malfunzionamento del provider può generare **messaggi duplicati** |

## Sessioni transacted

```java
QueueSession s = conn.createQueueSession(true, 0); // transacted=true → 2° param ignorato (0)
```
Una sessione **transacted** raggruppa una serie di operazioni JMS (send/receive) in una transazione, confinata a **una singola sessione**. Termina con `commit()` (tutto ok) o `rollback()` (anomalia):

```java
try { /* ... send/receive ... */ session.commit(); }
catch (Exception e) { session.rollback(); }
```

- **commit()** — i messaggi inviati diventano disponibili per la consegna; i messaggi ricevuti vengono acknowledged (JMS non li riconsegna). In PTP vengono **rimossi dalle code**.
- **rollback()** — i messaggi inviati vengono scartati; i messaggi ricevuti tornano disponibili (in PTP rimessi in coda e di nuovo visibili agli altri).

> 🎯 Esame ("conviene attivarli tutti?"): transazioni, persistenza e durable subscription danno **garanzie** ma costano **overhead** (memoria stabile, coordinamento) → si attivano solo quando servono davvero, non per default.

## Concorrenza e thread-safety

La specifica garantisce l'accesso concorrente **solo** su `Destination`, `ConnectionFactory`, `Connection`.
`Session`, `MessageProducer`, `MessageConsumer` **non** sono pensati per uso multithread, perché:
- le Session supportano le transazioni (difficili da rendere thread-safe);
- la ricezione asincrona multithread non è supportata.

> Conseguenza pratica: una Session è un **contesto single-threaded** — per più thread si creano più Session dalla stessa Connection.

## Persistenza dei messaggi

Due **delivery mode** che decidono se i messaggi sopravvivono a un crash del provider:
- `PERSISTENT` (**default**) — ogni messaggio è scritto su memoria stabile → non si perde in caso di guasto del provider.
- `NON_PERSISTENT` — nessuna garanzia di memorizzazione.

Si imposta sul producer o per singolo invio:
```java
producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
producer.send(msg, DeliveryMode.NON_PERSISTENT, 3, 1000); // mode, priority, time-to-live(ms)
```

## Interoperabilità JMS ↔ STOMP

STOMP è un protocollo testuale semplice che **non conosce** i tipi di messaggio JMS (`TextMessage`/`BytesMessage`). L'interoperabilità si gestisce così:

- **Tipo di body via `content-length`**: ActiveMQ usa l'header `content-length` per decidere il tipo nel passaggio STOMP→JMS — header **presente** → `BytesMessage`, header **assente** → `TextMessage` (in Python `stomp.py` si controlla con `auto_content_length`). Stessa logica nel verso JMS→STOMP.
- **Durable subscriber in STOMP** (analogo a JMS): gli header custom `client-id` (comando `CONNECT`) e `activemq.subscriptionName` (comando `SUBSCRIBE`) vanno usati **in coppia** e la coppia identifica univocamente la sottoscrizione — esattamente come `clientID` + nome subscription in JMS. Se non impostato, `client-id` assume l'hostname.
- Lato STOMP va usato il **physical-name** della queue/topic (non il nome JNDI lato JMS).

```python
conn.connect(wait=True, headers={"client-id": "IDtestsub_durable"})
conn.subscribe(destination='/topic/mytesttopic', id=1, ack='auto',
               headers={"activemq.subscriptionName": "IDtestsubscription"})
```
> 💡 Connessione: stessa logica dei durable JMS → [[sottoscrizioni-durabili]]; STOMP è il protocollo usato dai client non-Java (es. Python) verso [[activemq]].

## Perché importa

JMS è il modo Java-standard per usare MOM. ActiveMQ nel corso è il provider JMS. Capire JMS significa capire come il pattern Abstract Factory disaccoppia il codice dal provider.

## Connessioni

- [[mom]] — JMS è l'API per accedere ai sistemi MOM in Java
- [[pub-sub]] — JMS supporta entrambi i modelli PTP e Pub/Sub
- [[sottoscrizioni-durabili]] — `createDurableSubscriber` per topic senza perdita messaggi
- [[proxy-pattern]] — il pattern Abstract Factory in JMS è concettualmente simile al pattern Proxy
- [[middleware-trasparenza]] — JMS come caso paradigmatico di specifica pura + Abstract Factory + JNDI
- [[activemq]] — il provider JMS usato nel corso; espone anche STOMP per i client non-Java
- [[produttore-consumatore]] — PTP è un produttore-consumatore distribuito mediato dal broker

## Fonti

- [[24-java-jms]]

_Aggiornato: 2026-06-06 — aggiunto link a middleware-trasparenza_
_Aggiornato: 2026-06-21 — approfondita la teoria del servizio di naming: a cosa serve (livello di indirezione nome↔oggetto, trasparenza di locazione), architettura JNDI API + SPI con i Service Provider come plugin intercambiabili (parallelo con l'Abstract Factory), ruolo delle due proprietà (factory.initial=plugin SPI, provider.url=URL), tabella metodi Context, bind lato admin vs lookup lato client_
_Aggiornato: 2026-06-21 — estensione modulo JMS (slide 02_JAVA_05): JNDI in dettaglio (Context/InitialContext, bind/lookup, proprietà), modello di programmazione a 8 passi, consumo sincrono (receive/receiveNoWait) vs asincrono (MessageListener/onMessage), struttura messaggio (header/properties/selettori SQL-like/5 tipi di body), acknowledgement (AUTO/CLIENT/DUPS_OK + 3 fasi), sessioni transacted (commit/rollback), thread-safety, persistenza (PERSISTENT/NON_PERSISTENT), interop JMS↔STOMP (content-length, durable client-id+subscriptionName)_
