# Università degli Studi di Napoli Federico II
# Esame di Advanced Computer Programming
## Proff. De Simone, Della Corte

### Prova pratica simulata — 18/06/2026
### Durata della prova: 120 minuti

---

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*La mancata compilazione dell'elaborato, la compilazione con errori o l'esecuzione errata daranno luogo alla valutazione come prova non superata.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

---

## Testo della prova

Il candidato implementi un sistema distribuito in **Python** per la gestione di una stazione di **bike-sharing** basato su **Proxy-Skeleton (socket TCP)**, **Flask** e **MongoDB**. Il sistema è caratterizzato dai seguenti componenti.

```
                rent()              POST /update_history
 Rider ──(TCP socket)──► Station Manager ──(HTTP POST)──► DB Server
        return_bike(int)   [Prod][Cons]                  (Flask+MongoDB)
                              ↕                            /update_history
                          bike_queue                      /stats
                          (size = 5)                       collection: trips
```

---

### Rider

È un client utilizzato per richieste di noleggio/restituzione verso lo **Station Manager**.

- L'invio di una richiesta di **noleggio** consiste nell'invocazione del metodo `int rent()`, che non prevede parametri.
- L'invio di una richiesta di **restituzione** consiste nell'invocazione del metodo `bool return_bike(int serial_number)`. La richiesta è caratterizzata dal `serial_number` *(int)* che identifica la bici da restituire.

Entrambi i metodi sono specificati nell'interfaccia `IStation`.

Il Rider avvia **10 thread**: ogni thread genera **casualmente** o una richiesta di restituzione — invocando `return_bike` con un `serial_number` casuale (intero tra **1 e 100**) — oppure una richiesta di noleggio, invocando `rent`.

---

### Station Manager

Fornisce l'interfaccia `IStation` e i relativi metodi `int rent()` e `bool return_bike(int serial_number)`. È un **server** raggiungibile via **socket TCP**.

- Il metodo `return_bike` inserisce il `serial_number` nella coda `bike_queue` *(produttore)*.
- Il metodo `rent` consuma un elemento dalla coda `bike_queue` *(consumatore)*.

> N.B.: è necessario utilizzare una **lista** per implementare la coda, prevedendo i meccanismi di **sincronizzazione** per il problema produttore/consumatore; la coda ha **dimensione pari a 5**.

Prima di ritornare, **entrambi** i metodi `rent` e `return_bike` generano una richiesta di tipo **POST** verso il DB Server (endpoint `/update_history`), inserendo nel body il tipo di operazione effettuata (cioè `rent` o `return`) ed il `serial_number` della bici, in formato JSON — es. `{"operation": "return", "serial_number": 10}` — **attendendo la risposta prima di ritornare**.

- Il metodo `rent` ritorna al chiamante il `serial_number` della bici estratta dalla coda.
- Il metodo `return_bike` ritorna un semplice **ack** (valore booleano).

Il candidato predisponga le opportune **interfacce** e le classi **Proxy-Skeleton**. Si utilizzi **skeleton per ereditarietà** per lo Station Manager.

---

### DB Server

Implementa un server **Flask** che gestisce una collection **MongoDB** denominata `trips`, ed espone una REST API con i seguenti endpoint:

- **`POST /update_history`** — riceve un payload JSON `{"operation": ..., "serial_number": ...}` e inserisce un documento nella collection `trips`. Ritorna un ack (`200 OK`).

- **`GET /stats`** — interroga la collection `trips` e ritorna il numero di operazioni per tipo, nel formato:
  ```json
  {
    "rent": 4,
    "return": 6
  }
  ```

Lo studente progetti la REST API, scegliendo opportunamente i metodi HTTP da utilizzare.

---

## Vincoli tecnici

- Usare **Proxy-Skeleton con socket TCP** per la comunicazione tra Rider e Station Manager.
- La coda `bike_queue` deve essere implementata con una **lista** e protetta dai meccanismi di sincronizzazione per il problema produttore/consumatore (es. `threading.Condition` o `Semaphore`), con **dimensione massima 5**.
- Il DB Server deve usare **Flask** e **MongoDB** (PyMongo).
- I metodi `rent` e `return_bike` devono attendere la risposta HTTP dal DB Server prima di ritornare.

## Test attesi

Il sistema sarà testato da terminale con: **1 Rider** (10 thread), **1 Station Manager**, **1 DB Server**.

Verifica finale:
- La collection `trips` su MongoDB contiene **10 documenti** (uno per richiesta).
- `GET /stats` ritorna il conteggio corretto delle operazioni `rent` e `return` (somma = 10).
- La coda non supera mai i 5 elementi e non si verificano deadlock/race condition.

---

## Suggerimento architetturale

```
IStation (interfaccia: rent(), return_bike(serial))
    ↑                    ↑
StationProxy        StationSkeleton (gestisce socket + accetta connessioni)
(usa socket,             ↑
 serializza chiamate)  StationImpl (eredita da StationSkeleton,
                        implementa rent/return_bike + bike_queue + POST)
```

---

*Prova generata il 2026-06-18 — basata su pattern prove ACP 2023-2024 (fusione 2024-06-26 buy/sell + 2024-10-18 proxy-skeleton).*
*Valutazione: eseguire `valuta svolgimento svolgimenti/2026-06-18-sim-11` dopo aver scritto soluzione.md*
