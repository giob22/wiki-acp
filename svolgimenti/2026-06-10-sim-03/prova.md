# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 10/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito **Java + Python** per il monitoraggio della qualità in una linea di assemblaggio industriale. Il sistema è caratterizzato dai seguenti componenti.

```
QualityAgent (Java)
       │
   (TCP socket)
       │
       ▼
InspectionServer (Java)  ──(JMS Topic)──►  ActiveMQ  ─┬─(JMS Topic)──►  AlertConsumer (Java)
 [Skeleton ereditarietà]  /topic/checks                │                  → alerts.txt
     [synchronized]                                    │
                                                       └─(STOMP Topic)──►  StatsCollector (Python)
                                                                            → stats.txt
```

---

### QualityAgent (Java)

È un client che invia rapporti di ispezione al server. L'invio consiste nell'invocazione del metodo `void inspect(String componentId, String status)` specificato nell'interfaccia `IQualityService`.

La richiesta è caratterizzata da:
1. **componentId** *(String)*: identificatore del componente ispezionato, scelto casualmente tra `motor-A`, `motor-B`, `motor-C`
2. **status** *(String)*: esito dell'ispezione, scelto casualmente tra `OK`, `WARNING`, `FAIL`

Il QualityAgent genera **15 ispezioni**, invocando `inspect` per ciascuna e attendendo **1 secondo** tra le invocazioni. Per ogni invocazione stampa: `[SEND] componentId=... status=...`.

Il QualityAgent utilizza un `QualityServiceProxy` che implementa `IQualityService` usando **Socket TCP**.

---

### InspectionServer (Java)

Estende `QualityServiceSkeleton` implementando il pattern **skeleton per ereditarietà** (come da interfaccia `IQualityService`).

Il metodo `inspect(String componentId, String status)`:
- È eseguito in **mutua esclusione** (`synchronized`)
- Stampa a video: `[INSP] componentId=... status=...`
- Pubblica sul Topic ActiveMQ **`/topic/checks`** un `TextMessage` nel formato: `componentId|status` (es. `motor-A|FAIL`)

Il server si connette ad ActiveMQ su `tcp://localhost:61616` (porta JMS/OpenWire) e accetta connessioni Socket TCP sulla porta **5000**.

---

### AlertConsumer (Java)

Componente **Java** che si connette ad ActiveMQ tramite **JMS** e si iscrive in modo asincrono al Topic `/topic/checks`.

Il AlertConsumer utilizza il pattern **Abstract Factory** per la creazione degli oggetti JMS:
- `ActiveMQConnectionFactory` come implementazione concreta di `ConnectionFactory`
- `Connection`, `Session`, `Topic`, `MessageConsumer` creati tramite le interfacce JMS standard

Per ogni `TextMessage` ricevuto il AlertConsumer:
1. Stampa a video: `[ALERT CHECK] componentId=... status=...`
2. Estrae i due campi separando sul carattere `|`
3. **Se `status.equals("FAIL")`**: scrive in append sul file `alerts.txt` la riga `componentId|FAIL`
4. **Se `status` è `OK` o `WARNING`**: scarta (solo stampa, non scrive su file)

Il AlertConsumer resta in ascolto finché non viene terminato manualmente.
Si connette ad ActiveMQ su `tcp://localhost:61616`.

---

### StatsCollector (Python)

Componente **Python** che si connette ad ActiveMQ tramite **STOMP** e si iscrive al Topic **`/topic/checks`**.

Per ogni messaggio ricevuto lo StatsCollector:
1. Stampa a video: `[STATS] componentId=... status=...`
2. Estrae i due campi separando sul carattere `|`
3. Aggiorna un dizionario interno nel formato:
   ```python
   stats = {
       "motor-A": {"OK": 0, "WARNING": 0, "FAIL": 0},
       ...
   }
   ```
4. Riscrive **`stats.txt`** con i conteggi aggiornati (una riga per componente, es. `motor-A: OK=3 WARNING=1 FAIL=2`)

Lo StatsCollector resta in ascolto finché non viene terminato manualmente (CTRL+C).
Si connette ad ActiveMQ su `localhost:61613` (porta STOMP).

---

## Vincoli tecnici

- Usare **Socket TCP** per la comunicazione tra QualityAgent e InspectionServer
- Il metodo `inspect()` nell'InspectionServer deve essere **thread-safe** (`synchronized`)
- Usare **JMS Topic** (`/topic/checks`) per la pubblicazione dei messaggi da InspectionServer
- AlertConsumer e StatsCollector si iscrivono **entrambi** allo stesso Topic `/topic/checks`
- Il AlertConsumer deve essere implementato in **Java** con le API **JMS** (ActiveMQ classic client)
- Lo StatsCollector deve essere implementato in **Python** con **`stomp.py`**
- `alerts.txt` è scritto in append dal solo AlertConsumer, **solo per `status == FAIL`**
- `stats.txt` è riscritto integralmente dallo StatsCollector ad ogni messaggio ricevuto

---

## File da consegnare

```
IQualityService.java        ← interfaccia con metodo inspect()
QualityServiceProxy.java    ← proxy: implementa IQualityService via Socket TCP
QualityServiceSkeleton.java ← skeleton astratto: gestisce accept/receive TCP
InspectionServer.java       ← estende Skeleton, override inspect() + JMS publisher
AlertConsumer.java          ← JMS Topic subscriber, filtra FAIL → alerts.txt
QualityAgent.java           ← client: genera 15 ispezioni via Proxy
stats_collector.py          ← STOMP Topic subscriber → stats.txt
alerts.txt                  ← generato a runtime da AlertConsumer
stats.txt                   ← generato a runtime da StatsCollector
```

---

## Sequenza di avvio

1. Avviare **ActiveMQ**
2. Avviare **AlertConsumer**
3. Avviare **StatsCollector**
4. Avviare **InspectionServer**
5. Avviare **QualityAgent**

---

## Test attesi

Il sistema è testato con: **1 QualityAgent**, **1 InspectionServer**, **1 AlertConsumer**, **1 StatsCollector**

Verifica finale:
- QualityAgent stampa 15 righe `[SEND]`
- InspectionServer stampa 15 righe `[INSP]`
- AlertConsumer stampa 15 righe `[ALERT CHECK]`
- StatsCollector stampa 15 righe `[STATS]`
- `alerts.txt` contiene solo le righe con `status == FAIL` (variabile, mediamente 4–6 su 15)
- `stats.txt` contiene 3 righe (una per ogni componentId), con i conteggi per `OK`, `WARNING`, `FAIL`
- Somma dei conteggi in `stats.txt` = 15

---

## Suggerimento struttura InspectionServer.java

```java
// Struttura minima — il candidato completi la logica synchronized e JMS
import org.apache.activemq.ActiveMQConnectionFactory;
import javax.jms.*;
import java.net.*;
import java.io.*;

public abstract class QualityServiceSkeleton implements IQualityService {
    // gestisce il loop di accept e delegazione a inspect()
    // il candidato implementa il ciclo TCP
}

public class InspectionServer extends QualityServiceSkeleton {
    private MessageProducer producer;
    private Session session;

    @Override
    public synchronized void inspect(String componentId, String status) {
        // TODO: stampa, crea TextMessage, pubblica su topic
    }
}
```

---

## Suggerimento struttura stats_collector.py

```python
import stomp
import time

class StatsListener(stomp.ConnectionListener):
    def __init__(self):
        self.stats = {}

    def on_message(self, frame):
        # TODO: parsing body, aggiornamento stats, riscrittura stats.txt
        pass

conn = stomp.Connection([('localhost', 61613)])
conn.set_listener('', StatsListener())
conn.connect(wait=True)
conn.subscribe(destination='/topic/checks', id=1, ack='auto')

# resta in ascolto
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    conn.disconnect()
```

---

*Prova generata il 2026-06-10 — Java proxy-skeleton + JMS Topic + Python STOMP subscriber*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-10-sim-03` dopo aver completato la soluzione*
