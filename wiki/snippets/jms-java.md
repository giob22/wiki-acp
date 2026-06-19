---
tipo: snippet
tecnologia: jms
linguaggio: java
---

# Boilerplate — JMS (Java + ActiveMQ)

API JMS (`javax.jms.*`) verso ActiveMQ su porta **61616** (OpenWire). Bootstrap **sempre via JNDI**: la `ConnectionFactory` e le `Destination` sono **administered objects** recuperati dal servizio di naming (`InitialContext.lookup`), mai costruiti direttamente. → [[jms]] [[mom]]

> 🎯 Esame: **non** usare `new ActiveMQConnectionFactory(...)` né `session.createQueue/createTopic(...)`. Tutto passa per il naming JNDI: `lookup("QueueConnectionFactory")`, `lookup("nome-coda")`. Il provider concreto (ActiveMQ) resta nascosto dietro le interfacce `javax.jms.*` → pattern **Abstract Factory**.

## Classpath

```bash
# activemq-all contiene client JMS + InitialContextFactory + dipendenze
javac -cp .:activemq-all-5.16.6.jar *.java
java  -cp .:activemq-all-5.16.6.jar NomeClasse
```

## Bootstrap — JNDI (administered objects)

```java
import java.util.Hashtable;
import javax.naming.*;
import javax.jms.*;

Hashtable<String, String> prop = new Hashtable<>();
prop.put("java.naming.factory.initial",
         "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
prop.put("queue.telemetry", "telemetry");     // registra la coda nel naming
// per un topic: prop.put("topic.checks", "checks");

Context context = new InitialContext(prop);

// administered objects via servizio di naming
QueueConnectionFactory factory =
        (QueueConnectionFactory) context.lookup("QueueConnectionFactory");
Queue queue = (Queue) context.lookup("telemetry");
```

La chiave di property `queue.<jndiName>` / `topic.<jndiName>` registra la destinazione nel contesto: il `lookup` la restituisce come administered object. La factory è disponibile sotto i nomi standard `ConnectionFactory`, `QueueConnectionFactory`, `TopicConnectionFactory`.

## Producer (Queue, PTP)

```java
import java.util.Hashtable;
import javax.naming.*;
import javax.jms.*;

public class Producer {
    public static void main(String[] args) {
        try {
            Hashtable<String, String> prop = new Hashtable<>();
            prop.put("java.naming.factory.initial",
                     "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
            prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
            prop.put("queue.telemetry", "telemetry");   // registra la coda nel naming

            Context context = new InitialContext(prop);
            QueueConnectionFactory factory =
                    (QueueConnectionFactory) context.lookup("QueueConnectionFactory");
            Queue queue = (Queue) context.lookup("telemetry");

            QueueConnection connection = factory.createQueueConnection();

            // Session NON è thread-safe
            QueueSession session =
                    connection.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);

            MessageProducer producer = session.createProducer(queue);

            TextMessage msg = session.createTextMessage("motor-A|FAIL");
            producer.send(msg);
            System.out.println("[SENT] " + msg.getText());

            connection.close();
        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }
    }
}
```

Per pubblicare su **Topic**: registra `prop.put("topic.checks", "checks")`, poi `lookup("TopicConnectionFactory")` e `lookup("checks")` come `Topic` — il resto è identico (interfacce generali `MessageProducer`/`MessageConsumer`).

## Consumer asincrono (MessageListener)

```java
import java.util.Hashtable;
import javax.naming.*;
import javax.jms.*;

public class Consumer {
    public static void main(String[] args) {
        try {
            Hashtable<String, String> prop = new Hashtable<>();
            prop.put("java.naming.factory.initial",
                     "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
            prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
            prop.put("topic.checks", "checks");

            Context context = new InitialContext(prop);
            TopicConnectionFactory factory =
                    (TopicConnectionFactory) context.lookup("TopicConnectionFactory");
            Topic topic = (Topic) context.lookup("checks");

            TopicConnection connection = factory.createTopicConnection();

            // start(): obbligatorio per RICEVERE (non per inviare)
            connection.start();

            TopicSession session =
                    connection.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);

            MessageConsumer consumer = session.createConsumer(topic);
            consumer.setMessageListener(new MyListener());

            System.out.println("in ascolto...");
            // il main NON deve terminare: il listener gira su thread JMS
            Thread.currentThread().join();
        } catch (NamingException | JMSException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

```java
import javax.jms.*;

public class MyListener implements MessageListener {

    @Override
    public void onMessage(Message message) {
        try {
            TextMessage textMessage = (TextMessage) message;
            String body = textMessage.getText();
            System.out.println("[RECV] " + body);

            String[] data = body.split("\\|");   // parsing tipico da prova
            // logica: filtra, scrivi su file, oppure delega a un worker thread

        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
}
```

Se l'elaborazione è pesante, in `onMessage` delegare a un thread (pattern da prova sim-02):

```java
public void onMessage(Message message) {
    new WorkerThread((TextMessage) message).start();
}
```

## Consumer sincrono

```java
connection.start();
MessageConsumer consumer = session.createConsumer(queue);  // queue da lookup JNDI
Message m = consumer.receive();        // blocca finché non arriva un messaggio
// consumer.receive(5000);             // timeout ms
```

## Interfacce specializzate PTP / Pub-Sub

Le prove a volte chiedono esplicitamente le interfacce di dominio invece di quelle generali. La factory e la destination arrivano comunque dal `lookup` JNDI:

```java
QueueConnectionFactory qFactory =
        (QueueConnectionFactory) context.lookup("QueueConnectionFactory");
Queue queue = (Queue) context.lookup("telemetry");

QueueConnection qConnection = qFactory.createQueueConnection();
QueueSession qSession =
        qConnection.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
QueueSender sender = qSession.createSender(queue);        // producer PTP
QueueReceiver receiver = qSession.createReceiver(queue);  // consumer PTP

// Pub-Sub: lookup("TopicConnectionFactory") + lookup("<topic>") →
//          TopicConnection / TopicSession / TopicPublisher / TopicSubscriber
```

## Subscriber durabile (Topic, no messaggi persi se offline)

```java
import java.util.Hashtable;
import javax.naming.*;
import javax.jms.*;

Hashtable<String, String> prop = new Hashtable<>();
prop.put("java.naming.factory.initial",
         "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");
prop.put("topic.checks", "checks");

Context context = new InitialContext(prop);
TopicConnectionFactory factory =
        (TopicConnectionFactory) context.lookup("TopicConnectionFactory");
Topic topic = (Topic) context.lookup("checks");

TopicConnection connection = factory.createTopicConnection();
connection.setClientID("archive-client");          // identità PRIMA di start()
TopicSession session = connection.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);

TopicSubscriber sub = session.createDurableSubscriber(topic, "archive-sub");
sub.setMessageListener(msg -> { /* gestisci */ });
connection.start();
// sub.close(); session.unsubscribe("archive-sub");  // per rimuovere la durable
```

> 🎯 Esame: `setClientID` va chiamato PRIMA di `connection.start()`. `(client-id, nome-subscription)` identifica la durable: il broker trattiene i messaggi mentre il subscriber è giù → [[sottoscrizioni-durabili]]. Controparte STOMP: `client-id` + `activemq.subscriptionName` → [[stomp-python]].

> ⚠️ Errori classici: costruire la factory con `new ActiveMQConnectionFactory(...)` invece del `lookup` JNDI (richiesto il servizio di naming); dimenticare `connection.start()` (il consumer non riceve nulla, senza errori); terminare il main del consumer asincrono (il listener muore col processo); cast `(TextMessage)` che fallisce se il producer STOMP non usa `auto_content_length=False` → [[stomp-python]].

> 🎯 Esame: `start()` serve solo a ricevere; Session è single-threaded; AUTO_ACKNOWLEDGE; tabella interfacce generali vs PTP vs Pub-Sub → [[jms]].

## Collegamenti

- [[jms]] — interfacce, Abstract Factory, JNDI, administered objects
- [[activemq]] — il broker (61616 JMS, 61613 STOMP)
- [[pub-sub]] — PTP vs Pub-Sub
- [[java-threading]] — worker thread dal listener
- [[stomp-python]] — controparte Python sullo stesso broker

## Fonti

- [[24-java-jms]], svolgimento sim-02 (`svolgimenti/2026-06-09-sim-02/DataProcessor_server/`)

_Aggiornato: 2026-06-18 — bootstrap unificato su JNDI (rimossa factory diretta ActiveMQConnectionFactory)_
