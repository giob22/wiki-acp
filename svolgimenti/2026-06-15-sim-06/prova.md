# Università degli Studi di Napoli Federico II
## Esame di Advanced Computer Programming
*Proff. De Simone, Della Corte*

### Prova pratica (simulata) — 15/06/2026
### Durata della prova: 120 minuti

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

*Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.*
*La mancata compilazione dell'elaborato, la compilazione con errori o l'esecuzione errata daranno luogo alla valutazione come prova non superata.*
*Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.*

°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

## Testo della prova

```
  registra(String,int)
  ┌──────────┐           ┌─────────────────┐        ┌──────────────────┐
  │  Gateway │──socket──▶│  Telemetry      │~~STOMP~▶│  Channel Router  │
  └──────────┘    TCP    │  Collector      │  topic  │     (Python)     │
  ┌──────────┐           │  (Java)         │ /telemetria  └────────┬─────┘
  │  Gateway │──socket──▶│   ⚙ ⚙           │                       │ POST
  └──────────┘    TCP    └─────────────────┘                       ▼ /persist
                          ITelemetry                       ┌──────────────────┐
                                                           │  Archive Server  │
  ──────▶  Invocazione su socket (proxy-skeleton TCP)      │     (Python)     │
  ~~~~~▶  Invocazione su MOM (STOMP / ActiveMQ)            │     (Flask)      │──▶ archivio.txt
  ─ ─ ─▶  Invocazione su REST (HTTP POST)                  └──────────────────┘
```

Il candidato implementi un sistema distribuito **ibrido Java/Python** per la raccolta di dati di telemetria
da una rete di gateway, basato su **proxy-skeleton con socket TCP**, **MOM (ActiveMQ/STOMP)** e **Flask**.
Il sistema è caratterizzato dai seguenti componenti.

**Gateway.** È un client (**Java**) che genera le misure di telemetria da inviare al Telemetry Collector.
L'invio di una misura consiste nell'invocazione del metodo `void registra(String, int)` specificato
nell'interfaccia `ITelemetry`. La richiesta è caratterizzata da: 1) `grandezza` (String), ossia il tipo di
grandezza misurata, 2) `valore` (int), ossia il valore della misura. Il Gateway genera **10 misure**,
invocando il metodo `registra` per ogni misura (attendendo **1 secondo** tra le invocazioni). Per ciascuna
misura, `grandezza` è generata in maniera casuale scegliendo tra `temperatura`, `pressione` e `vibrazione`,
mentre `valore` è generato in maniera casuale come intero tra 0 e 100 (estremi inclusi).

**Telemetry Collector.** Fornisce l'interfaccia `ITelemetry` ed il relativo metodo `void registra(String, int)`
(**Java**). Il metodo `registra` avvia un thread, il quale costruisce un messaggio contenente la grandezza ed
il valore ricevuti e lo pubblica sul **topic** JMS/STOMP `telemetria` dell'broker ActiveMQ. Il messaggio
pubblicato deve riportare, nel proprio body, la concatenazione della grandezza e del valore separati da un
trattino, e.g., `temperatura-37`. Il metodo `void registra(String, int)` deve essere eseguito in **mutua
esclusione**.

**Channel Router.** È un componente (**Python**) che implementa la **ricezione asincrona** sul topic
`telemetria` (subscriber STOMP). Alla ricezione di ciascun messaggio, il Channel Router estrae grandezza e
valore dal body e: se `valore` è **maggiore o uguale a 80**, classifica la misura come `critica`, altrimenti
come `nominale`. Successivamente effettua una **richiesta di tipo POST** verso l'Archive Server, inserendo nel
body, in formato json, la grandezza, il valore e la classe assegnata, e.g.,
`{"grandezza":"temperatura", "valore":37, "classe":"nominale"}`, attendendo la risposta prima di proseguire.

**Archive Server.** Implementa un server **Flask** (**Python**) che espone una REST API con l'endpoint
`persist`. Tale endpoint accetta richieste di tipo POST con payload in formato json (descritto in precedenza).
Ricevuta una richiesta, l'Archive Server scrive (in **append**) sul file `archivio.txt` una stringa che è la
concatenazione dei tre campi ricevuti tramite il payload, separati da trattino, e.g., `temperatura-37-nominale`,
e ritorna un ack al chiamante.

---

Il candidato utilizzi **proxy-skeleton con socket TCP** per la comunicazione tra **Gateway** e **Telemetry
Collector**, e **topic STOMP/JMS** per quella tra **Telemetry Collector** e **Channel Router**. A tal fine, il
candidato predisponga le opportune interfacce e le classi **Proxy-Skeleton**. Si utilizzi inoltre **skeleton
per ereditarietà** per il Telemetry Collector.
