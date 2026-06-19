# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 09/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito **Python + Java** per la raccolta e filtraggio di dati di telemetria industriale. Il sistema è caratterizzato dai seguenti componenti.

```
TelemetryProbe (Python)
        │
      (gRPC)
        │
        ▼
CollectorServer (Python gRPC)  ──(STOMP)──►  ActiveMQ  ──(JMS)──►  DataProcessor (Java)
                                            /queue/telemetry               │
                                                                     value > 75.0?
                                                                           │
                                                                           ▼
                                                                     telemetry.txt
```

---

### TelemetryProbe (Python)

È un client che raccoglie misurazioni da sensori industriali e le invia al CollectorServer.
L'invio di una misurazione consiste nell'invocazione del metodo `SendMeasurement` definito nel file `.proto`.

La richiesta è caratterizzata da:
1. **device_id** *(String)*: identificatore del dispositivo, scelto casualmente tra `sensor-A`, `sensor-B`, `sensor-C`
2. **value** *(float)*: valore di telemetria casuale nell'intervallo `[0.0, 100.0]` con due cifre decimali (es. `82.34`)

Il TelemetryProbe genera **10 misurazioni**, invocando `SendMeasurement` per ciascuna e attendendo **1 secondo** tra le invocazioni. Per ogni risposta ricevuta stampa: `[SENT] device_id=... value=... → status=OK`.

---

### CollectorServer (Python gRPC)

Implementa il servizio gRPC `TelemetryService` con il metodo:

```
rpc SendMeasurement (Measurement) returns (Ack)
```

Per ogni misurazione ricevuta il CollectorServer:
1. Stampa a video: `[RECV] device_id=... value=...`
2. Pubblica un messaggio sulla coda ActiveMQ **`/queue/telemetry`** tramite STOMP
3. Il messaggio STOMP ha corpo nel formato `device_id|value` (es. `sensor-A|82.34`)
4. Restituisce al probe un `Ack` con campo `status = "OK"`

Il CollectorServer è un **server gRPC sincrono** (non asincrono).
Si connette ad ActiveMQ su `localhost:61613` (porta STOMP).

---

### DataProcessor (Java JMS)

Componente **Java** che si connette ad ActiveMQ tramite **JMS** e consuma in modo asincrono i messaggi dalla coda `telemetry`.

Il DataProcessor utilizza il pattern **Abstract Factory** per la creazione degli oggetti JMS:
- `ActiveMQConnectionFactory` come implementazione concreta di `ConnectionFactory`
- `Connection`, `Session`, `Queue`, `MessageConsumer` creati tramite le interfacce JMS standard

Per ogni `TextMessage` ricevuto il DataProcessor:
1. Stampa a video nel formato: `[RECV] device_id|value`
2. Estrae i due campi separando sulla pipe `|`
3. **Se `value > 75.0`**: scrive in append sul file `telemetry.txt` la riga `device_id|value`
4. **Se `value ≤ 75.0`**: scarta (solo stampa, non scrive su file)

Il DataProcessor resta in ascolto finché non viene terminato manualmente (es. con CTRL+C).
Si connette ad ActiveMQ su `tcp://localhost:61616` (porta JMS/OpenWire).

---

## Vincoli tecnici

- Usare **gRPC** (`grpcio`, `grpcio-tools`) per la comunicazione tra TelemetryProbe e CollectorServer
- Usare **STOMP** (`stomp.py`) per la pubblicazione su ActiveMQ dal CollectorServer
- Il DataProcessor deve essere implementato in **Java** con le API **JMS** (ActiveMQ classic client)
- Il file `telemetry.txt` è scritto in **append** dal solo DataProcessor, solo per `value > 75.0`
- ActiveMQ deve essere in esecuzione su `localhost` (porta STOMP `61613`, porta JMS `61616`)

---

## File da consegnare

```
telemetry.proto           ← definizione servizio gRPC
telemetry_pb2.py          ← generato da protoc (non modificare)
telemetry_pb2_grpc.py     ← generato da protoc (non modificare)
probe.py                  ← TelemetryProbe
collector_server.py       ← CollectorServer (gRPC server + STOMP publisher)
DataProcessor.java        ← consumer JMS Java
telemetry.txt             ← generato a runtime dal DataProcessor
```

---

## Test attesi

Il sistema è testato con: **1 TelemetryProbe**, **1 CollectorServer**, **1 DataProcessor**

Sequenza di avvio:
1. Avviare ActiveMQ
2. Avviare `DataProcessor`
3. Avviare `CollectorServer`
4. Avviare `TelemetryProbe`

Verifica finale:
- Il TelemetryProbe stampa 10 righe `[SENT]`
- Il CollectorServer stampa 10 righe `[RECV]`
- Il DataProcessor stampa 10 righe `[RECV]`
- `telemetry.txt` contiene solo le righe con `value > 75.0` (variabile, mediamente 2–4 su 10)
- Ogni riga di `telemetry.txt` ha formato `device_id|value` (es. `sensor-B|91.23`)

---

## Schema `.proto` (fornito)

```protobuf
syntax = "proto3";
package telemetry;

service TelemetryService {
  rpc SendMeasurement (Measurement) returns (Ack);
}

message Measurement {
  string device_id = 1;
  float  value     = 2;
}

message Ack {
  string status = 1;
}
```

Il candidato **non deve modificare** questo schema. Eseguire:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. telemetry.proto
```

---

## Suggerimento struttura DataProcessor.java

```java
// Struttura minima — il candidato completi la logica di filtraggio e scrittura file
import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;
import java.io.*;

public class DataProcessor {
    public static void main(String[] args) throws Exception {
        ConnectionFactory factory = new ActiveMQConnectionFactory("tcp://localhost:61616");
        Connection conn = factory.createConnection();
        conn.start();
        Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue("telemetry");
        MessageConsumer consumer = session.createConsumer(queue);

        consumer.setMessageListener(msg -> {
            // TODO: casting a TextMessage, parsing, stampa, filtro, scrittura file
        });

        // il main resta in ascolto
        Thread.currentThread().join();
    }
}
```

---

*Prova generata il 2026-06-09 — combinazione gRPC (Python) + STOMP (Python) + JMS (Java)*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-09-sim-02` dopo aver completato la soluzione*
