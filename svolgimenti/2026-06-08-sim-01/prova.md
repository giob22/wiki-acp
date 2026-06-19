# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 08/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito in **Python** per il monitoraggio di sensori ambientali basato su **Socket**, **Flask** e **MongoDB**. Il sistema è caratterizzato dai seguenti componenti.

```
Sensor ──(TCP socket)──► Monitor Server ──(HTTP POST)──► DB Server (Flask+MongoDB)
                         [Prod] [Cons]                    /readings
                              ↕                           /stats
                           readings
                            queue                      readings.txt
```

---

### Sensor

È un client che genera letture di temperatura da inviare al Monitor Server. L'invio di una lettura consiste nella invocazione del metodo `void send_reading(String location, float temperature)` specificato nell'interfaccia `ISensor`.

La richiesta è caratterizzata da:
1. **location** *(String)*: la stanza in cui si trova il sensore, scelta casualmente tra `sala`, `cucina`, `bagno`
2. **temperature** *(float)*: valore casuale tra `15.0` e `35.0` (con una cifra decimale, es. `21.3`)

Il Sensor genera **12 letture**, invocando il metodo `send_reading` per ogni lettura, attendendo **1 secondo** tra le invocazioni.

---

### Monitor Server

Fornisce l'interfaccia `ISensor` e il relativo metodo `void send_reading(String location, float temperature)`.

Il metodo `send_reading` avvia un **processo produttore** che inserisce in una coda *(process-safe, che implementi il problema del produttore/consumatore)* una stringa che concatena i due parametri nel formato `location-temperature` (ad es., `cucina-23.4`).

I dati inseriti nella coda sono consumati da un **processo consumatore** avviato al lancio del Monitor Server. Quando un nuovo dato è disponibile nella coda, il processo consumatore:
1. Preleva la stringa dalla coda
2. Separa i due campi (`location` e `temperature`)
3. Invia una richiesta **POST** all'endpoint `/readings` del DB Server, inserendo nel body JSON i due campi: `{"location": "cucina", "temperature": 23.4}`
4. Scrive in append sul file **readings.txt** la stringa prelevata dalla coda

Il candidato predisponga le opportune interfacce e le classi **Proxy-Skeleton**. Si utilizzi **skeleton per ereditarietà** per il Monitor Server.

---

### DB Server

Implementa un server **Flask** che gestisce una collection **MongoDB** contenente le letture ricevute, ed espone una REST API con due endpoint:

- **`POST /readings`** — riceve un payload JSON `{"location": ..., "temperature": ...}` e inserisce un documento nella collection MongoDB `readings`. Ritorna `200 OK`.

- **`GET /stats`** — legge tutti i documenti dalla collection `readings` e calcola la **temperatura media** per ogni location. Ritorna un JSON nel formato:
  ```json
  {
    "sala": 22.5,
    "cucina": 28.1,
    "bagno": 19.7
  }
  ```

Lo studente progetti la REST API, scegliendo opportunamente i metodi HTTP da utilizzare.

---

## Vincoli tecnici

- Usare **Socket TCP** per la comunicazione tra Sensor e Monitor Server
- La coda nel Monitor Server deve essere **process-safe** (`multiprocessing.Queue`)
- Il DB Server deve usare **Flask** e **MongoDB** (PyMongo)
- Il candidato predisponga un file `readings.txt` scritto in append dal consumatore

## Test attesi

Il sistema sarà testato con: **1 Sensor**, **1 Monitor Server**, **1 DB Server**

Verifica finale:
- `readings.txt` contiene 12 righe nel formato `location-temperature`
- `GET /stats` ritorna le medie corrette per le 3 location

---

## Suggerimento architetturale

```
ISensor (interfaccia)
    ↑               ↑
SensorProxy     MonitorSkeleton (gestisce socket + accetta connessioni)
(usa socket)        ↑
                MonitorImpl (eredita da MonitorSkeleton, implementa send_reading)
```

---

*Prova generata il 2026-06-07 — basata su pattern prove ACP 2023-2024*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-08-sim-01` dopo aver scritto soluzione.md*
