# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 16/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito **interamente in Java** per il monitoraggio dei consumi energetici di una rete di contatori industriali. Il sistema è caratterizzato dai seguenti componenti.

```
MeterProbe (Java)
      │
    (gRPC)
      │
      ▼
EnergyCollector (Java gRPC server)  ──(JMS Queue)──►  ActiveMQ  ──(JMS)──►  ConsumptionAnalyzer (Java)
                                       /queue/energy                             kwh > 50.0?
                                                                                     │
                                                                                     ▼
                                                                              high_consumption.txt
```

---

### MeterProbe (Java)

È un client che raccoglie letture dai contatori e le invia all'EnergyCollector.
L'invio di una lettura consiste nell'invocazione del metodo `ReportConsumption` definito nel file `.proto`.

La richiesta è caratterizzata da:
1. **meter_id** *(String)*: identificatore del contatore, scelto casualmente tra `meter-1`, `meter-2`, `meter-3`
2. **kwh** *(float)*: consumo casuale nell'intervallo `[0.0, 100.0]` con due cifre decimali (es. `63.41`)

Il MeterProbe genera **12 letture**, invocando `ReportConsumption` per ciascuna e attendendo **1 secondo** tra le invocazioni. Per ogni risposta ricevuta stampa: `[SENT] meter_id=... kwh=... → status=OK`.

Il MeterProbe usa uno **stub bloccante** (`BlockingStub`).

---

### EnergyCollector (Java gRPC server)

Implementa il servizio gRPC `EnergyService` con il metodo:

```
rpc ReportConsumption (Reading) returns (Ack)
```

Per ogni lettura ricevuta l'EnergyCollector:
1. Stampa a video: `[RECV] meter_id=... kwh=...`
2. Pubblica un `TextMessage` sulla coda ActiveMQ **`/queue/energy`** tramite **JMS**, con corpo nel formato `meter_id|kwh` (es. `meter-2|63.41`)
3. Restituisce al probe un `Ack` con campo `status = "OK"` (tramite `onNext()` + `onCompleted()`)

L'EnergyCollector è un **server gRPC sincrono** in ascolto sulla porta **50051**.
Per la pubblicazione JMS usa il pattern **Abstract Factory**: `ActiveMQConnectionFactory` come implementazione concreta di `ConnectionFactory`, e crea `Connection`, `Session`, `Queue`, `MessageProducer` tramite le interfacce JMS standard.
Si connette ad ActiveMQ su `tcp://localhost:61616` (porta JMS/OpenWire).

> La connessione e il `MessageProducer` JMS vanno creati **una sola volta** all'avvio del server, non ad ogni RPC. Il metodo di servizio si limita a costruire e inviare il `TextMessage`.

---

### ConsumptionAnalyzer (Java JMS)

Componente **Java** che si connette ad ActiveMQ tramite **JMS** e consuma in modo **asincrono** (`MessageListener`) i messaggi dalla coda `energy`.

Anche il ConsumptionAnalyzer usa il pattern **Abstract Factory** per gli oggetti JMS.

Per ogni `TextMessage` ricevuto il ConsumptionAnalyzer:
1. Stampa a video nel formato: `[ANALYZE] meter_id|kwh`
2. Estrae i due campi separando sulla pipe `|`
3. **Se `kwh > 50.0`**: scrive in append sul file `high_consumption.txt` la riga `meter_id|kwh`
4. **Se `kwh ≤ 50.0`**: scarta (solo stampa, non scrive su file)

Il ConsumptionAnalyzer resta in ascolto finché non viene terminato manualmente (es. CTRL+C).
Ricorda che il `MessageListener` gira su un thread del provider JMS: il `main` non deve terminare (es. `Thread.currentThread().join()`).
Si connette ad ActiveMQ su `tcp://localhost:61616`.

---

## Vincoli tecnici

- Usare **gRPC** (plugin `protoc-gen-grpc-java`) per la comunicazione tra MeterProbe e EnergyCollector
- I messaggi gRPC si costruiscono con il **Builder** (`newBuilder().set...().build()`)
- La risposta del servizio si invia con `responseObserver.onNext(...)` seguito da `onCompleted()`
- Sia EnergyCollector (producer) sia ConsumptionAnalyzer (consumer) devono usare le API **JMS** (ActiveMQ classic client)
- Per ricevere, il consumer deve invocare `connection.start()`
- Il file `high_consumption.txt` è scritto in **append** dal solo ConsumptionAnalyzer, solo per `kwh > 50.0`
- ActiveMQ deve essere in esecuzione su `localhost` (porta JMS/OpenWire `61616`)

---

## File da consegnare

```
energy.proto              ← definizione servizio gRPC
EnergyServiceGrpc.java    ← generato da protoc-gen-grpc-java (non modificare)
Reading.java, Ack.java... ← generati da protoc (non modificare)
MeterProbe.java           ← client gRPC
EnergyServiceImpl.java    ← implementazione del servizio (RPC + JMS producer)
EnergyCollector.java      ← bootstrap del server gRPC
ConsumptionAnalyzer.java  ← consumer JMS asincrono, filtra kwh > 50.0
high_consumption.txt      ← generato a runtime dal ConsumptionAnalyzer
```

---

## Test attesi

Il sistema è testato con: **1 MeterProbe**, **1 EnergyCollector**, **1 ConsumptionAnalyzer**

Sequenza di avvio:
1. Avviare ActiveMQ
2. Avviare `ConsumptionAnalyzer`
3. Avviare `EnergyCollector`
4. Avviare `MeterProbe`

Verifica finale:
- Il MeterProbe stampa 12 righe `[SENT]`
- L'EnergyCollector stampa 12 righe `[RECV]`
- Il ConsumptionAnalyzer stampa 12 righe `[ANALYZE]`
- `high_consumption.txt` contiene solo le righe con `kwh > 50.0` (variabile, mediamente 5–7 su 12)
- Ogni riga di `high_consumption.txt` ha formato `meter_id|kwh` (es. `meter-3|81.07`)

---

## Schema `.proto` (fornito)

```protobuf
syntax = "proto3";

option java_multiple_files = true;

package energy;

service EnergyService {
  rpc ReportConsumption (Reading) returns (Ack);
}

message Reading {
  string meter_id = 1;
  float  kwh      = 2;
}

message Ack {
  string status = 1;
}
```

Il candidato **non deve modificare** questo schema. Compilare con:
```bash
protoc --java_out=. \
       --grpc-java_out=. \
       --plugin=protoc-gen-grpc-java=/PATH/TO/protoc-gen-grpc-java-1.73.0-linux-x86_64 \
       energy.proto
```

Esecuzione (classpath con gRPC JAR + `activemq-all`):
```bash
javac -cp .:activemq-all-5.16.6.jar:grpc/* *.java
java  -cp .:activemq-all-5.16.6.jar:grpc/* ConsumptionAnalyzer
java  -cp .:activemq-all-5.16.6.jar:grpc/* EnergyCollector
java  -cp .:activemq-all-5.16.6.jar:grpc/* MeterProbe
```

---

## Suggerimento struttura EnergyServiceImpl.java

```java
// Struttura minima — il candidato completi la logica gRPC + JMS
import io.grpc.stub.StreamObserver;
import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;
import energy.*;

public class EnergyServiceImpl extends EnergyServiceGrpc.EnergyServiceImplBase {

    private final Session session;
    private final MessageProducer producer;

    public EnergyServiceImpl() throws JMSException {
        ConnectionFactory factory = new ActiveMQConnectionFactory("tcp://localhost:61616");
        Connection conn = factory.createConnection();
        conn.start();   // non strettamente necessario per il solo invio
        this.session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue("energy");
        this.producer = session.createProducer(queue);
    }

    @Override
    public void reportConsumption(Reading request, StreamObserver<Ack> responseObserver) {
        // TODO: stampa [RECV], crea TextMessage "meter_id|kwh", producer.send(...)
        //       Ack reply = Ack.newBuilder().setStatus("OK").build();
        //       responseObserver.onNext(reply); responseObserver.onCompleted();
    }
}
```

## Suggerimento struttura ConsumptionAnalyzer.java

```java
// Struttura minima — il candidato completi parsing, filtro e scrittura file
import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;
import java.io.*;

public class ConsumptionAnalyzer {
    public static void main(String[] args) throws Exception {
        ConnectionFactory factory = new ActiveMQConnectionFactory("tcp://localhost:61616");
        Connection conn = factory.createConnection();
        conn.start();   // OBBLIGATORIO per ricevere
        Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue("energy");
        MessageConsumer consumer = session.createConsumer(queue);

        consumer.setMessageListener(msg -> {
            // TODO: cast a TextMessage, parsing su "|", stampa [ANALYZE],
            //       se kwh > 50.0 append su high_consumption.txt
        });

        // il main resta in ascolto (il listener gira su thread JMS)
        Thread.currentThread().join();
    }
}
```

---

*Prova generata il 2026-06-16 — Java puro: gRPC (Java) client/server + JMS producer/consumer asincrono*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-16-sim-09` dopo aver completato la soluzione*
