# Università degli Studi di Napoli Federico II

**Esame di Advanced Computer Programming**

**Proff. De Simone, Della Corte**

**Prova pratica simulata**

**Durata della prova: 120 minuti**

000000000000000000000000000000000000000000000000000000000000000000000000

Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.

Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.

000000000000000000000000000000000000000000000000000000000000000000000000

### Testo della prova

Plaintext

```
                             Fleet 
  Operator                  Manager                  DB Server (Flask)
   |                          |                              |
   |---- request topic ------>|                              |
   |                          |------- REST API (HTTP) ----->| 
   |<--- response topic ------|                              |-----> MongoDB
   |                          |<-----------------------------|
```

Il candidato implementi un sistema distribuito in Python per il monitoraggio ed il controllo di una flotta di veicoli aziendali, basato su **STOMP**, **Flask** e **MongoDB**.

Il sistema è caratterizzato dai seguenti componenti:

**Operator.** E' un client che può effettuare richieste di aggiornamento telemetria (REPORT) e richieste di interrogazione dello stato della flotta (QUERY) verso il Fleet Manager. L'invio di una richiesta consiste nella creazione di un frame STOMP nel quale inserire una stringa che concateni il tipo di richiesta ed i relativi parametri (separati da un trattino `-`). Le richieste sono inviate sul topic `request`.

- Per inviare i dati di un veicolo, l'Operator invia una richiesta di tipo `REPORT` con i seguenti attributi: `vehicle_id` (identificativo del veicolo), `battery` (livello di batteria, intero da 0 a 100), `status` (stato del veicolo, stringa tra "active" o "maintenance"). _Esempio di stringa STOMP: `REPORT-VEICOLO1-75-active`_.
    
- Per interrogare il sistema sui veicoli a rischio, l'Operator invia una richiesta di tipo `QUERY` con un singolo attributo: `threshold` (soglia critica di batteria). _Esempio di stringa STOMP: `QUERY-20`_.
    

Le risposte alle sole richieste di tipo `QUERY` saranno ricevute in maniera asincrona sul topic `response`. Una volta ricevuta una risposta, l'Operator mostra a video il suo contenuto.

L'Operator avvia **6 thread**: i primi 4 thread generano una richiesta `REPORT`, mentre i successivi 2 generano una richiesta `QUERY`.

_N.B.: i valori dei campi delle richieste possono essere scelti in maniera casuale._

**Fleet Manager.** E' un gestore centrale che riceve le richieste da un Operator in maniera asincrona attraverso il topic `request`. Ricevuta una richiesta, il Fleet Manager analizza il frame STOMP, ed estrae il tipo di richiesta (i.e., `REPORT` o `QUERY`) ed i relativi parametri. In base al tipo di richiesta, il Fleet Manager genera una richiesta verso uno degli endpoint esposti dal DB Server:

- Nel caso di `REPORT`, la richiesta HTTP dovrà essere di tipo POST e prevedere nel body i parametri ricevuti dall'Operator convertiti in formato JSON, e.g., `{"vehicle_id": "VEICOLO1", "battery": 75, "status": "active"}`.
    
- Nel caso di `QUERY`, la richiesta HTTP dovrà essere di tipo GET verso il DB Server, passando il parametro `threshold` (es. tramite query string o path parameter).
    
    Inviata una richiesta di tipo `QUERY` al DB Server, il Fleet Manager si mette in attesa della risposta (lista dei veicoli formattata in JSON), che invierà poi all'Operator attraverso un frame STOMP sul topic `response`.
    

**DB Server.** Implementa un server Flask che gestisce una collection **MongoDB** contenente i dati della flotta, e che espone una REST API con due endpoint:

- **Un endpoint per l'aggiornamento della telemetria** che, ricevuta una richiesta POST, crea o aggiorna un document all'interno di una collection MongoDB. Se il `vehicle_id` è già presente, aggiorna i valori di `battery` e `status`; se non è presente, crea un nuovo document con tutti i campi forniti.
    
- **Un endpoint per la ricerca di veicoli critici** che, ricevuta una richiesta GET con la soglia `threshold`, cerca nella collection MongoDB tutti i veicoli che si trovano in stato di `"maintenance"` OPPURE che hanno un livello di `battery` strettamente minore della soglia specificata. L'endpoint deve restituire al chiamante la lista di questi veicoli in formato JSON.
    

Lo studente progetti la REST API, scegliendo opportunamente i path per i metodi HTTP da utilizzare. Il sistema sarà testato avviando prima il DB Server, poi il Fleet Manager e infine l'Operator.