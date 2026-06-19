---
tipo: concetto
importanza_esame: alta
prerequisiti: [socket, processo-thread]
---

## Definizione

Il **middleware** è uno strato software interposto tra il sistema operativo e le applicazioni, in grado di fornire le **astrazioni** e i **servizi** utili per lo sviluppo di applicazioni distribuite. Offre ai programmatori librerie di funzioni (**middleware API**, *Application Programming Interface*) il cui scopo è **mascherare l'eterogeneità** dei sistemi su rete. Per questa ragione le piattaforme middleware sono anche dette **software di connettività tra applicazioni** o *glue technologies* (tecnologie collante), a sottolineare il loro ruolo di tecnologie di **integrazione di applicazioni**.

## Spiegazione

### Il contesto: i sistemi distribuiti

Un **sistema distribuito** è, secondo Coulouris, «un sistema i cui componenti, localizzati in computer connessi in rete, comunicano e coordinano le loro azioni **solo attraverso scambio di messaggi**». Lamport ne dà una definizione più ironica ma efficace: «il mio programma gira su un sistema distribuito quando non funziona per colpa di una macchina di cui non ho mai sentito parlare».

Da queste definizioni discendono tre **implicazioni** fondamentali:
- **Elaborazione concorrente** — i componenti procedono in parallelo (vedi [[concorrenza-parallelismo]]);
- **Assenza di clock globale** — non esiste un riferimento temporale comune, la coordinazione avviene solo via messaggi;
- **Malfunzionamenti indipendenti** — un nodo può fallire senza che gli altri se ne accorgano direttamente (guasti parziali).

### L'eterogeneità è la norma

I sistemi distribuiti sono in generale **eterogenei**: l'eterogeneità di hardware e software è da considerarsi la **norma, non l'eccezione**, anche all'interno di una stessa grande organizzazione. Le fonti di eterogeneità sono molteplici:
- applicazioni distribuite su una rete di calcolatori con **hardware e sistemi operativi diversi e spesso incompatibili** (mainframe, server, workstation, PC);
- **linguaggi di programmazione diversi**: linguaggi di alto livello (C#, Java) per *presentation logic* e *business logic*; linguaggi tradizionali (COBOL, C, C++) per funzionalità *legacy* o di basso livello; linguaggi di scripting (Python, PHP, JSP, ASP.NET) per funzionalità server-side;
- **dati distribuiti** su più nodi, memorizzati con DBMS diversi e condivisi da applicazioni locali e remote.

Nello sviluppo su rete — anche in ambiente omogeneo — vanno affrontati problemi (sicurezza, guasti, contesa e condivisione delle risorse) molto più complessi che nei sistemi centralizzati; l'eterogeneità aggiunge ulteriore complessità. Il paradigma più generale è dunque l'**heterogeneous distributed computing**: componenti interoperanti in ambiente distribuito ed eterogeneo.

### Il problema dell'EAI

I sistemi complessi raramente vengono sviluppati integralmente *ex novo*: tipicamente **evolvono a partire da sistemi esistenti già funzionanti**. L'**Enterprise Application Integration (EAI)** è il problema — centrale nelle tecnologie software — di integrare sistemi informativi sviluppati in momenti, con linguaggi e tecniche diversi, operanti su piattaforme eterogenee. Si richiede sempre più di:
- **utilizzare applicazioni di terze parti** (sistemi **COTS**, *Commercial Off-The-Shelf*);
- **riutilizzare applicazioni esistenti** (sistemi ereditati o *legacy*).

L'integrazione (EAI) è spesso **più complessa dello sviluppo ex novo**:

| Sviluppo di applicazioni | Integrazione di applicazioni |
|---|---|
| Nuove applicazioni | Riuso di applicazioni esistenti spesso mal documentate + COTS |
| Libertà di scelta di tecnologie | Vincoli su SO, protocolli, linguaggi; tecnologie spesso non interoperanti |
| Competenze di analisi/progettazione/programmazione | Competenze di architetture software, reingegnerizzazione, riuso, progettazione interfacce |
| Eseguibile da giovani sviluppatori | Richiede specialisti con anni di esperienza |

In questa prospettiva la programmazione (codifica) è una fase **meno critica** del passato; assume maggiore importanza la capacità di **adattare componenti esistenti e non pensati per interoperare**, tramite l'attenta progettazione delle interfacce. Le **tecnologie middleware nascono proprio per fornire una risposta al problema dell'EAI**.

### Le proprietà (trasparenze) del livello middleware

Il middleware maschera le eterogeneità mediante diverse forme di **trasparenza**:

1. **Trasparenza del sistema operativo** — operando al di sopra del SO, i servizi delle API middleware sono definiti in modo indipendente da esso, consentendo la **portabilità** delle applicazioni tra SO diversi.
2. **Trasparenza del linguaggio di programmazione** — componenti scritti in linguaggi diversi pongono problemi di tipi di dato e meccanismi di scambio parametri differenti; il middleware definisce un **sistema di tipi intermedio** e regole non ambigue di corrispondenza con i tipi dei linguaggi più diffusi.
3. **Trasparenza alla locazione** (*location transparency*) — le risorse sono accessibili a livello logico, senza conoscerne l'effettiva locazione fisica: è il middleware a farsi carico della localizzazione su rete del processo partner.
4. **Trasparenza della migrazione** (*migration transparency*) — dati e servizi possono essere **rilocati** durante il ciclo di vita; il middleware consente l'accesso a componenti mobili in modo trasparente ai client.
5. **Trasparenza ai guasti** (*failure transparency*) — un'elaborazione distribuita può fallire anche solo **parzialmente**; il middleware offre meccanismi ad alto livello per mantenere uno **stato globale consistente** e mascherare i guasti.
6. **Trasparenza della replicazione** (*replication transparency*) — la **replicazione** di componenti serve sia per la **tolleranza ai guasti** sia per **migliorare le prestazioni** (bilanciamento del carico); l'esistenza di più copie deve essere trasparente ai client.
7. **Trasparenza delle implementazioni commerciali** — molte tecnologie middleware sono **specifiche di riferimento** recepite dagli enti di standardizzazione; le varie implementazioni commerciali, realizzate in maniera conforme allo standard, restano **interoperabili** (vedi [[middleware-trasparenza]] per l'approfondimento specifica-vs-implementazione).

### Tassonomia dei sistemi middleware

I middleware si classificano in due grandi famiglie:

```
                    middleware
            ┌───────────┴────────────┐
   orientati all'accesso      orientati alla
        ai dati                comunicazione
      ┌────┴────┐        ┌────┬────┬────┬────┬────┐
     RDA       TP       RPC  MOM  TS  DOM   CM   WS
```

| Modello | Sigla | Esempi |
|---|---|---|
| Remote Data Access | **RDA** | ODBC, JDBC, Oracle DB Integrators |
| Transaction Processing | **TP** | X/Open DTP |
| Remote Procedure Call | **RPC** | SunRPC, OSF DCE RPC → vedi [[rpc]] |
| Message-Oriented Middleware | **MOM** | IBM MQSeries, AMQP, **JMS**, DDS → vedi [[mom]] |
| Tuple Space | **TS** | Linda, JavaSpaces, Jini |
| Distributed Objects Middleware | **DOM** | **Java/RMI**, OMG CORBA, MS DCOM, .NET remoting |
| Component Model | **CM** | OMG CCM, EJB |
| Web Services | **WS** | JAX-WS, MS WCF |

> 🎯 Esame: distinguere middleware **orientati ai dati** (RDA, TP) da quelli **orientati alla comunicazione** (RPC, MOM, TS, DOM, CM, WS), saper collocare gRPC (RPC), JMS/ActiveMQ (MOM), RMI/CORBA (DOM).

### Il modello a oggetti distribuiti (DOM)

Il **modello a oggetti distribuiti** è un'estensione in ambiente distribuito della programmazione ad oggetti. In forma sintetica:

```
DO = OOP + C/S
```

I componenti di un'applicazione sono **oggetti su macchine diverse** che comunicano mediante **invocazione di metodi**: una piattaforma DOM permette di invocare un metodo su un oggetto remoto come fosse locale. È considerata la **seconda generazione** di sistemi distribuiti (dopo mainframe monolitici e prima generazione client/server). Il meccanismo è **analogo a quello RPC** e usa strumenti simili: **procedure stub** e **IDL** (Interface Definition Language) con relativi compilatori.

Le piattaforme DOM si presentano spesso come **Object Request Broker (ORB)**: una sorta di **bus software** per la comunicazione tra oggetti su rete (esempi: OMG CORBA, Microsoft COM). L'ORB si presenta al programmatore come un insieme di API e supporta l'interazione client-oggetto secondo lo schema **stub–ORB–skeleton**.

L'**IDL** rappresenta un **contratto** tra client e server: serve a generare automaticamente il codice degli stub e, nel tempo, ha assunto valenza più generale come strumento di **specifica ad alto livello e documentazione strutturale** del sistema.

**Java RMI** è un middleware a oggetti **specifico per la piattaforma Java** (ambiente distribuito **omogeneo**, macchine virtuali Java). I processi serventi creano oggetti e ne registrano il nome in un **catalogo** (*RMI registry*); i client ottengono riferimenti agli oggetti remoti (tramite ricerca nel catalogo) e ne invocano i metodi. RMI fornisce meccanismi per scambiare oggetti come parametri/valori di ritorno, trasferire su richiesta il codice di un oggetto, serializzare e trasferire lo stato di un oggetto — abilitando sistemi con **codice mobile**.

> 💡 Connessione: RMI registry e Sun RPC port mapper (vedi [[rpc]]) risolvono lo stesso problema — la **trasparenza alla locazione** — con un servizio di naming/directory che il client interroga prima di invocare il servizio remoto.

## Perché importa

Il middleware è il filo conduttore di tutta la seconda parte del corso: RPC/gRPC, MOM/JMS, REST sono tutte istanze concrete di modelli middleware. Capire il quadro generale (sistemi distribuiti → eterogeneità → EAI → trasparenze → tassonomia) permette di collocare ogni tecnologia studiata e di rispondere alle domande d'esame "di cornice".

## Connessioni

- [[middleware-trasparenza]] — approfondimento sulla trasparenza dalle implementazioni commerciali (specifica vs implementazione)
- [[rpc]] — modello RPC, primo middleware orientato alla comunicazione del corso
- [[grpc]] — implementazione moderna del modello RPC
- [[mom]] — modello a scambio messaggi, asincrono e disaccoppiato
- [[pub-sub]] — modello publish-subscribe adottato dai MOM
- [[socket]] — il middleware si appoggia ai servizi di trasporto di rete
- [[concorrenza-parallelismo]] — l'elaborazione concorrente è implicazione dei sistemi distribuiti

## Fonti

- [[13-sistemi-middleware]]

_Aggiornato: 2026-06-19 — pagina creata: estensione MODULO 2 (slide 13), teoria fondante middleware (sistemi distribuiti, EAI, trasparenze, tassonomia, DOM/ORB/IDL/RMI)_
