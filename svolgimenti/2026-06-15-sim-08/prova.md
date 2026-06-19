# Università degli Studi di Napoli Federico II

**Esame di Advanced Computer Programming**

**Proff. De Simone, Della Corte**

**Prova pratica simulata — 15/06/2026**

**Durata della prova: 120 minuti**

000000000000000000000000000000000000000000000000000000000000000000000000

Lo studente legga attentamente il testo e produca il programma ed i casi di test necessari per dimostrarne il funzionamento.

La mancata compilazione dell'elaborato, la compilazione con errori o l'esecuzione errata daranno luogo alla valutazione come prova non superata.

Al termine della prova lo studente dovrà far verificare il funzionamento del programma ad un membro della Commissione.

000000000000000000000000000000000000000000000000000000000000000000000000

### Testo della prova

```
                       smista(String,double)
   Scanner                          Sorting Hub                 Archive Service
   (Java)                             (Java)                     (Python, Flask)
     |                                  |                              |
     |--- socket TCP ------------------>|                              |
     |   (proxy-skeleton)               |--- REST POST /archivia ----->|
     |                                  |                              |----> MongoDB
     |                                  |<--- ack ---------------------|

   ──────▶  Invocazione su socket (proxy-skeleton TCP)
   ─ ─ ─▶  Invocazione su REST (HTTP POST)
```

Il candidato implementi un sistema distribuito **ibrido Java/Python** per lo smistamento dei pacchi in un hub di logistica, basato su **proxy-skeleton con socket TCP**, **REST (Flask)** e **MongoDB**. Il sistema è caratterizzato dai seguenti componenti.

**Scanner.** È un client (**Java**) che genera i pacchi da smistare da inviare al Sorting Hub. L'invio di un pacco consiste nell'invocazione del metodo `void smista(String, double)` specificato nell'interfaccia `ISmistamento`. La richiesta è caratterizzata da: 1) `codice` (String), ossia il codice identificativo del pacco, 2) `peso` (double), ossia il peso del pacco in chilogrammi. Lo Scanner genera **10 pacchi**, invocando il metodo `smista` per ogni pacco (attendendo **1 secondo** tra le invocazioni). Per ciascun pacco, `codice` è generato concatenando il prefisso `PKG` ad un intero progressivo (e.g., `PKG1`, `PKG2`, ...), mentre `peso` è generato in maniera casuale come numero reale compreso tra 0.0 e 30.0.

**Sorting Hub.** Fornisce l'interfaccia `ISmistamento` ed il relativo metodo `void smista(String, double)` (**Java**). Il metodo `smista` determina la `zona` di smistamento del pacco: se `peso` è **minore o uguale a 5.0** la zona è `standard`, se è **maggiore di 5.0 e minore o uguale a 20.0** la zona è `pesante`, altrimenti (peso maggiore di 20.0) la zona è `eccezionale`. Successivamente avvia un thread, il quale effettua una **richiesta di tipo POST** verso l'Archive Service, inserendo nel body, in formato json, il codice del pacco, il peso e la zona calcolata, e.g., `{"codice":"PKG1", "peso":12.5, "zona":"pesante"}`, ed attende la risposta prima di proseguire. Il metodo `void smista(String, double)` deve essere eseguito in **mutua esclusione**.

**Archive Service.** Implementa un server **Flask** (**Python**) che espone una REST API con l'endpoint `archivia`. Tale endpoint accetta richieste di tipo POST con payload in formato json (descritto in precedenza). Ricevuta una richiesta, l'Archive Service inserisce un documento nella collezione `pacchi` di un database **MongoDB**, memorizzando i tre campi ricevuti tramite il payload (`codice`, `peso`, `zona`), e ritorna un ack al chiamante.

---

Il candidato utilizzi **proxy-skeleton con socket TCP** per la comunicazione tra **Scanner** e **Sorting Hub**, e **REST (HTTP POST)** per quella tra **Sorting Hub** e **Archive Service**. A tal fine, il candidato predisponga le opportune interfacce e le classi **Proxy-Skeleton**. Si utilizzi inoltre **skeleton per ereditarietà** per il Sorting Hub.
