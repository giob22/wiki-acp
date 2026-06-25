---
tipo: esame
titolo: Risposte alle domande d'esame (Domande_ACP_aggiornate)
data: 2026-06-25
fonte_domande: raw/prove-esame/Domande_ACP_aggiornate.pdf
---

# Risposte alle domande d'esame — ACP

Risposte dettagliate a tutte le domande del file `Domande_ACP_aggiornate.pdf`, raggruppate come nell'originale. Ogni risposta è ancorata alle pagine del wiki tramite link `[[pagina]]` per la verifica.

> Nota di copertura: le risposte si basano sul materiale `raw/` sintetizzato nel wiki. Dove un punto è una mia inferenza o esce dal materiale esplicito, è segnalato.

---

## 1. Middleware (MOM, JMS, STOMP)

### 1.1 Concetti Generali

**Quali sono i tipi e i vantaggi dei middleware? (trasparenze, scalabilità, interoperabilità)**
→ [[middleware]]. Il middleware è uno strato software tra SO e applicazioni che fornisce astrazioni e servizi per le applicazioni distribuite, mascherando l'**eterogeneità** dei sistemi in rete (per questo è detto *glue technology*, tecnologia collante / di integrazione). Si classifica in due famiglie:
- **Orientati ai dati**: RDA (ODBC, JDBC), TP (X/Open DTP);
- **Orientati alla comunicazione**: RPC (SunRPC, gRPC), MOM (JMS, ActiveMQ, AMQP), TS/Tuple Space (Linda, JavaSpaces), DOM/oggetti distribuiti (Java RMI, CORBA), CM/Component Model (EJB), WS/Web Services (REST, JAX-WS).

Vantaggi = le **trasparenze** (vedi sotto): portabilità tra SO, interoperabilità tra linguaggi, location/migration transparency, tolleranza ai guasti, replicazione, indipendenza dal vendor. Più scalabilità (es. MOM asincroni) e riuso/integrazione di componenti legacy e COTS (problema **EAI**, Enterprise Application Integration).

**Web Service**
→ [[middleware]], [[rest]]. È la famiglia di middleware **WS** (orientato alla comunicazione): espone funzionalità applicative come servizi accessibili via rete con protocolli standard (HTTP). Nel corso l'istanza concreta è **REST** su HTTP/JSON (→ [[rest]], [[flask]]); altri esempi sono JAX-WS, MS WCF. Differenza chiave con RPC: il web service è orientato alle **risorse** e ai metodi HTTP standard, non alla chiamata di procedura.

**Quali sono le proprietà di trasparenza dei middleware?**
→ [[middleware]], [[middleware-trasparenza]]. Sette forme:
1. **Trasparenza del SO** — API indipendenti dal sistema operativo → portabilità;
2. **Trasparenza del linguaggio** — sistema di tipi intermedio + corrispondenze coi tipi dei linguaggi;
3. **Trasparenza alla locazione** — accesso logico alle risorse senza conoscerne la posizione fisica;
4. **Trasparenza della migrazione** — dati/servizi rilocabili senza impatto sui client;
5. **Trasparenza ai guasti** — maschera i guasti parziali, mantiene stato globale consistente;
6. **Trasparenza della replicazione** — più copie per fault tolerance e load balancing, invisibili al client;
7. **Trasparenza dalle implementazioni commerciali** — implementazioni conformi a una specifica restano interoperabili (es. JMS, gRPC).

**Come i middleware garantiscono la trasparenza ai guasti?**
→ [[middleware]], [[jms]]. Con meccanismi ad alto livello per mantenere uno **stato globale consistente** nonostante i guasti **parziali**. Concretamente nei MOM: **store-and-forward** (il broker conserva il messaggio finché il destinatario torna disponibile), **persistenza** dei messaggi su memoria stabile, **transazioni** (commit/rollback), **sottoscrizioni durabili**, e **replicazione** dei server (con i broker ci si sposta da un server fallito all'altro → high availability).

**Quali sono i principali modelli di middleware? (MOM, RPC/RMI, Tuple Space, DOM)**
→ [[middleware]]. Vedi tassonomia sopra: RDA, TP (dati); RPC, MOM, TS, DOM, CM, WS (comunicazione). RMI è un'istanza del modello **DOM** (oggetti distribuiti), `DO = OOP + C/S`: oggetti su macchine diverse comunicano via invocazione di metodi tramite stub/skeleton e IDL, spesso esposti da un **ORB** (Object Request Broker).

**A cosa serve il Marshalling/Unmarshalling? (big-endian/little-endian)**
→ [[rpc]], [[protocol-buffers]]. Il **marshalling** è la conversione dei parametri/dati in un formato adatto alla trasmissione su rete; l'**unmarshalling** è l'operazione inversa lato ricevente. Serve perché nodi eterogenei usano **rappresentazioni diverse** dei dati: ordine dei byte (**big-endian vs little-endian**), dimensione dei tipi, allineamento, codifica caratteri. Il marshalling include conversione di formato + serializzazione + **external data representation** (un formato neutro condiviso). Approcci: CORBA CDR, **Sun XDR**, Java serialization, **Protobuf** (gRPC), XML.

**Quali meccanismi di fault tolerance nei MOM?**
→ [[mom]], [[jms]]. **Store-and-forward** + disaccoppiamento **temporale** (il destinatario non deve essere attivo all'invio); **persistenza** dei messaggi (delivery mode `PERSISTENT`, su memoria stabile → sopravvivono al crash del broker); **transazioni** di sessione (commit/rollback); **sottoscrizioni durabili** sui topic (→ [[sottoscrizioni-durabili]]); **acknowledgement** (AUTO/CLIENT/DUPS_OK); **replicazione** dei broker per high availability.

**Semantiche RPC**
→ [[rpc]]. Quattro semantiche a seconda di come il sistema gestisce perdita richiesta/risposta e caduta del server:
- **Exactly once** — eseguita una e una sola volta;
- **At most once** — se eseguita, una sola volta (può non essere eseguita);
- **At least once** — almeno una volta (possibili ripetizioni);
- **Zero or more** — non si sa se né quante volte.

La semantica dipende dal **trasporto + meccanismi di ritrasmissione**. In Sun RPC: **TCP** → risposta ricevuta = *exactly once*, persa = *at most once*; **UDP** → risposta ricevuta = *at least once*, persa = *zero or more*. Operazioni **idempotenti** tollerano semantiche più deboli (at least once) senza effetti collaterali.

**È possibile un middleware RPC con MOM e viceversa?**
→ [[mom]], [[rpc]]. Sì, sono modelli interscambiabili a livello di obiettivo (far comunicare componenti distribuiti), con paradigmi opposti: RPC = **sincrono**, accoppiato, request/response; MOM = **asincrono**, disaccoppiato, a messaggi. Si può **emulare RPC su MOM** usando due code (request/reply) e correlando richiesta-risposta (header `JMSCorrelationID` + `JMSReplyTo`, → [[jms]]); e si può **fare scambio di messaggi su RPC** (es. gRPC streaming che trasporta messaggi). I MOM nascono proprio per **rimpiazzare** RPC dove serve scalabilità/availability (le RPC sincrone arretrate rallentano tutto il sistema).

### 1.2 JMS (Java Message Service)

#### 1.2.1 Panoramica

**Come funziona JMS in generale? (code e topic, lookup degli Administered Object, Session single-thread, JNDI)**
→ [[jms]]. JMS è lo standard Java (JSR 914) per accedere ai MOM: definisce solo interfacce `javax.jms.*`. Flusso a 8 passi: (1) `lookup` di una `ConnectionFactory` da **JNDI**; (2) `lookup` di una `Destination` (Queue per PTP, Topic per pub/sub); (3) creazione `Connection` (+ `start()` se consumer); (4) creazione `Session` (contesto **single-thread**); (5) creazione `MessageProducer`/`MessageConsumer`; (6) creazione `Message`; (7) send/receive; (8) cleanup. `ConnectionFactory` e `Destination` sono **administered objects** pre-configurati, recuperati da **JNDI** (naming service) per nome — il client ignora i dettagli del provider.

**Perché JMS necessita di un provider (es. ActiveMQ)? (JMS è specifica/interfaccia)**
→ [[jms]], [[middleware-trasparenza]], [[activemq]]. Perché JMS è **pura specifica**: solo interfacce `javax.jms.*`, **zero codice eseguibile**, nessun "runtime JMS" autonomo. Serve un'implementazione concreta (provider) che fornisca il broker e le classi concrete: **ActiveMQ**, WebSphere MQ, TIBCO EMS. È il caso più puro di **trasparenza dal provider** (pattern Abstract Factory + JNDI): cambiare provider = cambiare configurazione, non codice.

**Administered Objects**
→ [[jms]]. Sono `ConnectionFactory` e `Destination` (Queue/Topic): oggetti **pre-configurati dall'amministratore**, che colmano il gap tra interfacce JMS standard e tecnologia specifica del provider. Incapsulano dettagli provider-dependent ma sono recuperati tramite meccanismo standard (**JNDI lookup**) e usati tramite interfacce standard. Il client conosce solo il nome JNDI + l'interfaccia, non il provider.

**Qual è la struttura di un messaggio JMS? (Header, Proprietà, Body)**
→ [[jms]]. Tre parti:
- **Header** — campi standard (`getJMS*`/`setJMS*`): `JMSMessageID` (id univoco), `JMSCorrelationID` (collega richiesta↔risposta), `JMSReplyTo` (destination di risposta), `JMSPriority` (0–9).
- **Properties** — coppie `<String, value>` applicative; read-only nei messaggi ricevuti; supportano **selettori SQL-like** lato consumer (`"prop1 > 6 AND prop2 = 'test'"`).
- **Body** — 5 tipi: `TextMessage` (String), `MapMessage` (coppie nome/valore), `BytesMessage` (byte grezzi), `StreamMessage` (primitivi), `ObjectMessage` (oggetto `Serializable`).

**Spiegare come si istanziano gli oggetti JMS (JNDI, Context, ConnectionFactory, Administered Objects)**
→ [[jms]]. Si configurano due proprietà JNDI: `java.naming.factory.initial` (classe del Service Provider, es. `ActiveMQInitialContextFactory`) e `java.naming.provider.url` (es. `tcp://127.0.0.1:61616`). Si crea un `InitialContext` con quelle proprietà; da esso si fa `lookup` degli administered objects (`ConnectionFactory`, `Queue`/`Topic`). Dalla `ConnectionFactory` si crea la `Connection`, da questa la `Session`, e da Session + Destination i producer/consumer. JNDI è un **livello d'indirezione** nome↔oggetto (API client uguale, **SPI** lato provider con Service Provider come plugin intercambiabile).

**Cosa è thread-safe e cosa no?**
→ [[jms]]. Thread-safe (accesso concorrente garantito dalla specifica): `Destination`, `ConnectionFactory`, `Connection`. **Non** thread-safe: `Session`, `MessageProducer`, `MessageConsumer` — perché le Session gestiscono transazioni (difficili da rendere thread-safe) e la ricezione asincrona multithread non è supportata. Conseguenza: la `Session` è un **contesto single-threaded**; per più thread si creano più Session dalla stessa Connection.

**C'è un meccanismo per dare priorità a una sessione? (priorità al thread in cui è creata)**
→ [[jms]] (inferenza ancorata al materiale). JMS non espone una "priorità di sessione" diretta; la priorità è sui **messaggi** (`JMSPriority` 0–9). Poiché la Session è un contesto single-threaded legato al thread che la usa, dare priorità a quel **thread** (priorità del thread Java) influenza indirettamente la sessione. La priorità applicativa dei messaggi resta `JMSPriority` (9 = massima).

#### 1.2.2 Trasparenza ai guasti

**JMS e i meccanismi per la trasparenza ai guasti (Transazioni, Persistenza, Subscriber durabili)**
→ [[jms]], [[sottoscrizioni-durabili]]. Tre meccanismi:
- **Transazioni** — sessione `transacted` (`createSession(true, 0)`): raggruppa send/receive in una transazione confinata alla singola sessione; `commit()` rende disponibili gli invii e fa ack dei ricevuti, `rollback()` scarta gli invii e rimette in coda i ricevuti.
- **Persistenza** — delivery mode `PERSISTENT` (default): ogni messaggio scritto su memoria stabile → non si perde al crash del provider (vs `NON_PERSISTENT`).
- **Subscriber durabili** — sui topic, il broker trattiene i messaggi mentre il subscriber è offline (`setClientID` + `createDurableSubscriber`).

**Conviene attivarli tutti? No, perché generano overhead**
→ [[jms]]. Corretto: transazioni, persistenza e durable danno **garanzie** ma costano **overhead** (scrittura su memoria stabile, coordinamento, stato mantenuto dal broker). Si attivano **solo quando servono davvero**, non per default, per non penalizzare throughput e latenza.

#### 1.2.3 Domini di Messaggistica

**Quali sono i due domini di messaggistica e come si usano? (PTP/Queue, Pub-Sub/Topic)**
→ [[pub-sub]], [[mom]], [[jms]]. **Point-to-Point (PTP)** — astrazione **Queue**: ogni messaggio ha **un solo consumer**, persiste finché consumato o scaduto, il consumer fa **ACK**; uso tipico: task queue, job processing. **Publish-Subscribe** — astrazione **Topic**: il messaggio è ricevuto da **N subscriber** correnti; uso tipico: notifiche eventi, log. In ActiveMQ: `/queue/nome` vs `/topic/nome`.

**Cos'è un Durable Subscriber e come garantisce la ricezione?**
→ [[sottoscrizioni-durabili]]. È un subscriber a un **topic** per cui il broker memorizza i messaggi pubblicati mentre è **disconnesso** e glieli consegna al reconnect, estendendo il **disaccoppiamento temporale** al pub-sub. Serve un'**identità stabile**: `client-id` (sul CONNECT; in ActiveMQ = hostname se non impostato) + **subscription name** (`activemq.subscriptionName` sul SUBSCRIBE; in JMS il nome di `createDurableSubscriber`). La coppia identifica univocamente la sottoscrizione. Richiede messaggi **persistent** (KahaDB) per sopravvivere anche al restart del broker.

**Come funziona la ricezione asincrona tramite coda e MessageListener?**
→ [[jms]]. Il client registra un `MessageListener` sul consumer (`setMessageListener`); il provider invoca la callback `onMessage(Message m)` ad ogni arrivo, senza che il client blocchi su `receive()`. È il modello a callback, opposto al consumo sincrono.

**Come gestisce JMS gli Acknowledgement? (AUTO_ACKNOWLEDGE, CLIENT_ACKNOWLEDGE)**
→ [[jms]]. Consumo in 3 fasi (ricevi, processa, **ack**). Modalità (2° parametro di `createSession`):
- `AUTO_ACKNOWLEDGE` — ack automatico al ritorno da `receive`/fine `onMessage`;
- `CLIENT_ACKNOWLEDGE` — ack esplicito `message.acknowledge()`, **a livello di sessione** (conferma tutti i messaggi consumati nella sessione);
- `DUPS_OK_ACKNOWLEDGE` — ack "lasco", più efficiente ma può generare **duplicati** in caso di guasto.

**Cosa significa che la comunicazione JMS è transazionale?**
→ [[jms]]. Che una serie di operazioni send/receive può essere raggruppata in una **transazione** confinata a una singola sessione: o vanno a buon fine tutte (`commit`) o nessuna (`rollback`). Garantisce atomicità del gruppo di operazioni di messaggistica.

**Come si gestisce una transazione (Commit/Rollback) e come si imposta (SESSION_TRANSACTED)?**
→ [[jms]]. Si crea la sessione con `createQueueSession(true, 0)` (transacted=true → il 2° parametro ack è ignorato). Poi: `try { ...send/receive...; session.commit(); } catch(Exception e){ session.rollback(); }`. `commit` → invii disponibili e ricevuti acknowledged (in PTP rimossi dalle code); `rollback` → invii scartati, ricevuti rimessi in coda.

**Differenza ricezione asincrona/sincrona**
→ [[jms]]. **Sincrona**: il client preleva esplicitamente con `receive()` (blocca), `receive(timeout)`, `receiveNoWait()` (solo se subito disponibile). **Asincrona**: registra un `MessageListener`, il provider chiama `onMessage` (callback) ad ogni arrivo. Sincrona = pull bloccante; asincrona = push a callback.

**A cosa devo stare attento se creo una comunicazione STOMP/JMS?**
→ [[jms]], [[stomp-python]]. STOMP è **testuale** e non conosce i tipi JMS. Punti critici: (1) **tipo di body** — ActiveMQ decide via header `content-length`: presente → `BytesMessage`, assente → `TextMessage`; in `stomp.py` usare `auto_content_length=False` quando si invia verso un consumer Java JMS, altrimenti il cast `(TextMessage)` fallisce; (2) usare il **physical-name** della destinazione lato STOMP (non il nome JNDI); (3) per le **durable** servono `client-id` + `activemq.subscriptionName` in coppia; (4) porte diverse sullo stesso broker: STOMP **61613**, JMS/OpenWire **61616**.

**Reply To di JMS**
→ [[jms]]. L'header `JMSReplyTo` contiene una `Destination` (definita dal client mittente) verso cui il ricevente deve inviare la **risposta**. Combinato con `JMSCorrelationID` (che collega la risposta alla richiesta) realizza il pattern **request/reply** su MOM — il modo per emulare una semantica RPC sopra JMS.

### 1.3 STOMP e Interoperabilità

**Cos'è il protocollo STOMP e come funziona?**
→ [[activemq]], [[mom]]. **STOMP** (Simple/Streaming Text Oriented Messaging Protocol) è un protocollo **testuale, frame-based**, che assume un trasporto **2-way streaming** (TCP). Client e server scambiano **STOMP Frame**: `COMMAND` + header `chiave:valore` + riga vuota + `Body` terminato dal byte NULL (`^@`). Fornisce un formato **wire-level interoperabile** → un client STOMP parla con qualsiasi broker compatibile (ActiveMQ, Artemis, RabbitMQ) e tra linguaggi diversi. In Python: `stomp.py`. Porte ActiveMQ: 61613 (plain), 62613 (SSL).

**Perché si definisce la classe MyListener?**
→ [[activemq]], [[stomp-python]]. Per abilitare la **ricezione asincrona**: si crea una sottoclasse di `stomp.ConnectionListener` e si **ridefinisce `on_message(self, frame)`**, che la libreria invoca (su un thread interno) ad ogni messaggio ricevuto (`frame.body`, `frame.headers`, `frame.cmd`). Si registra con `conn.set_listener("", MyListener())`. È l'equivalente STOMP del `MessageListener.onMessage` di JMS. Senza il listener il client non avrebbe un punto dove gestire i messaggi in arrivo in modo asincrono.

**Come far interoperare JMS e STOMP? (broker come ActiveMQ che supporta entrambi)**
→ [[activemq]], [[jms]]. Tramite un broker **multiprotocollo** (ActiveMQ supporta JMS/OpenWire + STOMP + AMQP + MQTT): un producer Python via STOMP e un consumer Java via JMS scambiano messaggi sulla **stessa destinazione**. Il broker traduce tra i protocolli. Attenzione al `content-length` per il tipo di body e all'uso del physical-name.

**Ruolo degli header nei messaggi STOMP e relazione con quelli JMS (Frame.headers in Python vs getJMSProperty() in Java)**
→ [[activemq]], [[jms]]. Gli header STOMP (`frame.headers`, mappa chiave-valore testuale) trasportano metadati del frame e si **mappano** sulle proprietà/header JMS: lato Java si leggono con `getJMSProperty()`/`getJMS*`. Esempi: `content-length` (→ tipo di body), `client-id`/`activemq.subscriptionName` (→ durable, equivalenti a `setClientID` + nome subscription JMS), header applicativi custom (→ properties JMS).

**Quali sono i limiti di STOMP rispetto a JMS? (gestione delle transazioni)**
→ [[activemq]], [[jms]]. STOMP è volutamente **semplice e testuale**: non conosce i **tipi di messaggio** JMS (serve il trucco del `content-length`); il supporto a **transazioni** è più limitato (`begin`/`commit`/`abort` su invii, senza la ricchezza delle sessioni transacted JMS); selettori, modalità di ack e gestione tipata dei body sono meno espressivi rispetto alle interfacce `javax.jms.*`. In cambio offre interoperabilità cross-linguaggio e semplicità.

---

## 2. gRPC e Web Services (REST, Flask)

### 2.1 Concetti RPC e Pattern

**Spiegare il pattern Proxy/Skeleton: perché si usa e come si implementa**
→ [[proxy-pattern]], [[rpc]]. Separa la **logica applicativa** dai **meccanismi di comunicazione** in un sistema distribuito (è l'implementazione manuale di RPC). Il **Proxy** (lato client) implementa l'interfaccia del servizio: ogni metodo serializza i parametri, li invia via socket, attende e deserializza la risposta — il client usa l'interfaccia ignorando la rete. Lo **Skeleton** (lato server) riceve il messaggio, deserializza, fa l'**upcall** al metodo reale dell'implementazione, serializza e rispedisce il risultato. Entrambi Proxy e Impl implementano la stessa `InterfacciaServer`. Si usa per dare **trasparenza di accesso** (chiamata remota = chiamata locale). gRPC genera automaticamente proxy (`_pb2_grpc` stub) e skeleton (servicer) da `.proto` — è ciò che fa `protoc`.

**Confrontare l'accoppiamento del Proxy/Skeleton via delega o ereditarietà**
→ [[proxy-pattern]]. Due modi di realizzare lo Skeleton:
- **Per ereditarietà**: `ServerImpl extends ServerSkeleton` (astratta). Lo skeleton gestisce la comunicazione, l'impl implementa solo i metodi astratti. **Accoppiamento forte**: impl e skeleton legati dalla gerarchia di ereditarietà (l'impl *è-un* skeleton), non si può ereditare altro.
- **Per delega**: lo skeleton ha un riferimento `delegate: InterfacciaServer` e i metodi delegano a `delegate.metodo()`. L'impl è un oggetto **separato**. **Accoppiamento debole**: impl e skeleton indipendenti, l'impl può avere la sua gerarchia; più flessibile e testabile. La delega favorisce il principio "composizione over inheritance".

**Che semantica ha gRPC? È possibile implementare scambio di messaggi con RPC o viceversa?**
→ [[rpc]], [[grpc]], [[mom]]. **Semantica** (non scritta esplicitamente nel materiale per gRPC; inferenza dalla regola di [[rpc]]): gRPC usa **HTTP/2 su una sola connessione TCP**, quindi eredita la famiglia del trasporto TCP → **at most once** di default (il canale affidabile evita duplicati, ma una caduta lascia il client nell'incertezza sull'esecuzione); con i retry lato client si va verso *at least once*, sicuro solo per operazioni **idempotenti**; non c'è *exactly once* garantito a livello applicativo. **Scambio di messaggi con RPC**: sì, gRPC supporta lo **streaming** (server/client/bidirezionale), che è di fatto scambio di messaggi su RPC; e si può emulare RPC su MOM con code request/reply (→ §1.1 ultima domanda). RPC (sincrono) e messaggi (asincrono) sono modelli intercambiabili come obiettivo.

### 2.2 gRPC

**Come funziona la serializzazione in gRPC? (Protobuf, deserializzazione e riconoscimento dei campi)**
→ [[protocol-buffers]], [[grpc]]. gRPC usa **Protocol Buffers**: i dati sono **messaggi** (record di coppie nome-valore = **campi**). Ogni campo ha un **field tag** (numero univoco) usato nel **formato binario** per identificarlo — non i nomi. La serializzazione produce una sequenza compatta `Tag|Value|Tag|Value|...`. In **deserializzazione** il ricevente legge i tag e, conoscendo lo schema dal `.proto`, ricostruisce ogni campo associando il valore al campo giusto tramite il numero (i nomi non viaggiano sul filo → compattezza + retrocompatibilità). Vantaggi su JSON/XML: binario (3–10× più compatto), più veloce, schema enforcement, backward compatibility via tag. Svantaggio: non human-readable, richiede compilazione del `.proto`.

**Protocollo HTTP/2 per lo scambio di messaggi**
→ [[grpc]]. gRPC tratta le RPC come **riferimenti a oggetti HTTP**: ogni metodo del `.proto` diventa un endpoint HTTP/2 con path `/package.Service/Metodo`, invocato come un `POST` HTTP/2; i messaggi (serializzati protobuf) viaggiano negli **stream** HTTP/2 come frame binari. Gerarchia HTTP/2: **una connessione TCP** (di norma TLS) → più **stream** (multiplexing) → **message** → **frame** (unità minima, header di 9 byte che identifica lo stream). Vantaggi ereditati: **multiplexing** richiesta/risposta su una sola connessione (evita head-of-line blocking a livello HTTP), **streaming bidirezionale**, **header compression HPACK** (binario, tabelle statica/dinamica + Huffman). Tutto è binario, header inclusi.

**Come comunicano gRPC e MongoDB?**
→ [[grpc]], [[mongodb]], [[gestione-errori-api]]. Sono due livelli distinti: il **servicer gRPC** (lato server) riceve la richiesta, la deserializza e nella logica di business usa il driver **PyMongo** per leggere/scrivere su MongoDB (`collection.find_one`, `insert_one`, `find_one_and_update`...). Il risultato (dict/BSON) viene rimappato in un messaggio protobuf di risposta. Gli errori PyMongo (`DuplicateKeyError`, `PyMongoError`...) vengono tradotti in `grpc.StatusCode` via `context.abort()` (es. `ALREADY_EXISTS`, `INTERNAL`). Attenzione: `_id` è un `ObjectId`, va convertito in stringa per il campo protobuf.

**Interoperabilità gRPC-Flask: come strutturo i messaggi e come si convertono?**
→ [[grpc]], [[flask]], [[rest]]. Si espone un servizio gRPC anche come **REST API** mettendo Flask davanti come gateway: la view Flask riceve JSON (`request.get_json()`), costruisce il messaggio protobuf (`servizio_pb2.Request(campo=...)`), invoca lo **stub** gRPC, riceve la response protobuf e la riconverte in dict/JSON con `jsonify`. La conversione è **JSON ↔ messaggio protobuf**: i campi JSON si mappano sui campi del messaggio (stessi nomi). È il modo di realizzare un metodo di serializzazione per esporre gRPC come REST (vedi anche §2.3 ultima domanda).

**Messaggi streaming in gRPC: come si implementano e cosa ritornano?**
→ [[grpc]], [[grpc-python]]. Si implementano con **generator/`yield`**:
- **Server streaming**: il servicer fa `yield` di più response; il client **itera** sullo stub (`for r in stub.Metodo(req)`).
- **Client streaming**: il servicer riceve un `request_iterator`; il client passa un **generator** di richieste; ritorna una singola response.
- **Bidirezionale**: il servicer riceve `request_iterator` e fa `yield`; il client itera.

Lato Python ritornano **iteratori** di messaggi protobuf. Errore tipico: streaming senza `yield`/generator → `object is not an iterator`.

**Come avviene la generazione degli stub in Java e Python da un .proto?**
→ [[grpc-python]], [[grpc]], [[protocol-buffers]]. Si compila il `.proto` con `protoc`:
- **Python**: `python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. servizio.proto` → genera `servizio_pb2.py` (classi messaggi), `servizio_pb2_grpc.py` (Stub client + Servicer skeleton), `servizio_pb2.pyi` (type hints).
- **Java**: si usa il plugin protobuf (build Maven/Gradle o `protoc` con `--java_out`/`--grpc-java_out`) → genera le classi dei messaggi (con Builder), la classe `XxxGrpc` con `BlockingStub`/`Stub`/`FutureStub` e la `ImplBase` (servicer). In Java il `package` del `.proto` **non è ignorato** (determina il package generato; override con `option java_package`); in Python è ignorato (moduli per filesystem) ma raccomandato.

**Perché gRPC non usa UDP?**
→ [[grpc]], [[socket]] (inferenza ancorata al materiale). Perché gira su **HTTP/2**, che richiede un trasporto **affidabile, ordinato e orientato alla connessione** = **TCP**. gRPC sfrutta multiplexing di stream, controllo di flusso, ordine dei frame e header compression: tutte cose che presuppongono la consegna affidabile e ordinata del TCP. UDP non garantisce ordine né consegna né controllo di flusso (con UDP, dati complessi vanno gestiti in un unico pacchetto con separatore, → [[socket]]) → incompatibile con il modello a stream di HTTP/2.

**Dal punto di vista della serializzazione, a cosa serve il Marshalling/Unmarshalling?**
→ [[rpc]], [[protocol-buffers]]. (Vedi §1.1) A convertire i parametri/dati in un formato trasmissibile su rete (marshalling) e ricostruirli lato ricevente (unmarshalling), gestendo l'**eterogeneità** delle rappresentazioni (endianness, dimensione tipi, codifica). In gRPC il marshalling è fatto da protobuf (external data representation binaria).

**Come è caratterizzato lo stato di un'eccezione in una chiamata gRPC? (Status, es. UNKNOWN)**
→ [[gestione-errori-api]], [[grpc]]. Tramite un **`grpc.StatusCode`** impostato sul `context`: `context.set_code(...)` + `set_details(...)` (non interrompono, serve `return`) oppure `context.abort(code, details)` (imposta code+details e **lancia un'eccezione**, interrompe l'handler). Il client intercetta con `grpc.RpcError` e legge `e.code()` / `e.details()`. Codici principali: `INVALID_ARGUMENT` (~400), `NOT_FOUND` (~404), `ALREADY_EXISTS` (~409), `UNAVAILABLE` (~503), `DEADLINE_EXCEEDED` (~504), `INTERNAL` (~500), `OK` (~200). **`UNKNOWN`** = errore non classificato/imprevisto — tipicamente sollevato quando qualcosa va storto senza uno status specifico (es. eccezione non gestita lato server, o campo inesistente: `Protocol message X has no "y" field`).

**Cosa sono e quali vantaggi offrono gli stream in gRPC? (yield e generator)**
→ [[grpc]], [[grpc-python]]. Sono RPC in cui richiesta e/o risposta sono **flussi** di messaggi (non un singolo messaggio), realizzati con generator/`yield`. Vantaggi: invio incrementale di grandi quantità di dati senza caricarli tutti in memoria, latenza ridotta (il client elabora i messaggi man mano), comunicazione bidirezionale continua su un'unica connessione (multiplexing HTTP/2), meno overhead rispetto a molte RPC singole (vedi domanda seguente).

**Perché lo streaming gRPC ha meno overhead di molte RPC singole? (stack frame)**
→ [[grpc]]. Ogni RPC singola comporta costi fissi ripetuti: instaurazione/gestione della chiamata, creazione dello **stack frame** della chiamata, serializzazione di header e metadata, round-trip. Con lo **streaming** questi costi si pagano **una volta sola** per l'intero flusso: una sola RPC apre uno stream HTTP/2 e ci spedisce dentro N messaggi, ammortizzando setup, header (compressi con HPACK) e gestione della connessione su molti messaggi invece che ripeterli N volte.

**gRPC Java e differenze con Python**
→ [[grpc]], [[grpc-java]], [[grpc-python]]. Stesso `.proto` e stesso wire format (interoperabili). Differenze pratiche: in Java il `package` del proto **conta** (package generato); gli stub Java sono tipizzati e ne esistono varianti **BlockingStub** (sincrono bloccante), **Stub** asincrono e **FutureStub**; il server estende `ImplBase`; i messaggi si costruiscono con il **Builder pattern**. In Python si usa `grpcio`/`grpcio-tools`, lo streaming usa generator/`yield`, lo stub è dinamico e thread-safe, il server usa `ThreadPoolExecutor` (soggetto al **GIL**, → [[gil]]). Java sfrutta il vero parallelismo dei thread (no GIL).

**Con RPC posso implementare scambio di messaggi o viceversa? Che semantica è gRPC?** — duplicato di §2.1 (vedi sopra: streaming = scambio messaggi su RPC; semantica at most once su TCP/HTTP/2).

**Come si può implementare un server gRPC multiprocesso?**
→ [[grpc-python]], [[gil]]. Avviando **più processi** che condividono la stessa porta tramite l'opzione socket **`SO_REUSEPORT`**: ogni processo crea un `grpc.server(...)` con `options=(('grpc.so_reuseport', 1),)` e fa `add_insecure_port` sulla stessa porta (es. 50051); il kernel distribuisce le connessioni tra i processi. Serve perché il server gRPC Python è multithread ma soggetto al **GIL** (no parallelismo CPU reale con i soli thread): per task CPU-bound si scala con più **processi**. (Nota: `so_reuseport=0` serve invece a *impedire* che più processi aprano la stessa porta per errore.)

### 2.3 REST, Flask e Interazione

**Cos'è una REST API?**
→ [[rest]]. Un'interfaccia di **web service** secondo lo stile **REST**: espone **risorse** identificate da **URI**, manipolate tramite un'**interfaccia uniforme** (metodi HTTP GET/POST/PUT/DELETE), **stateless** (ogni richiesta autocontenuta, nessuna sessione), con rappresentazioni tipicamente in **JSON**. Focus sulle risorse (non sulle procedure come RPC): vocabolario fisso uguale per tutti i servizi.

**In Flask, cos'è il concetto di rotta (@app.route)?**
→ [[flask]]. Una **route** è il mapping tra una URL e la **view function** che la gestisce. Il decoratore `@app.route('/path')` registra la funzione seguente come handler di quella URL; ad ogni richiesta la view è invocata e il suo valore di ritorno è la risposta. Supporta parti dinamiche (`/user/<name>`, con convertitori `<int:id>`) e metodi (`methods=['GET','POST']` o shortcut `@app.get`/`@app.post`). Di default risponde solo a **GET**.

**Convenzioni sui nomi dei metodi in Flask e perché il metodo HTTP è il discriminante dell'azione**
→ [[flask]], [[rest]]. In REST l'**azione** è determinata dal **metodo HTTP** (interfaccia uniforme), non dal nome della funzione: la stessa URL/risorsa risponde diversamente a GET (leggi) vs POST (crea) vs PUT (aggiorna) vs DELETE (elimina). Le view si nominano per chiarezza ma è il verbo HTTP a decidere l'operazione (vocabolario fisso REST, vs RPC-style dove ogni funzione ha un nome proprio come `getOrder`/`insertOrder`). Flask permette di separare i metodi in view diverse con `@app.get`/`@app.post`.

**Semantica dei metodi HTTP: GET, POST, PUT, DELETE**
→ [[rest]]. **GET** (Read) — recupera lo stato della risorsa; **safe** (read-only) e **idempotente**. **POST** (Create) — crea una sotto-risorsa figlia; **non** safe, **non** idempotente (due POST = due risorse). **PUT** (Update) — inizializza/aggiorna lo stato all'URI dato; non safe ma **idempotente** (ripeterlo dà lo stesso stato). **DELETE** (Delete) — elimina la risorsa; non safe ma **idempotente**. Safe = non altera lo stato; idempotente = richieste identiche → stesso risultato.

**Perché in Flask sono preferiti dict e list? (serializzati nativamente in JSON)**
→ [[flask]], [[strutture-dati]]. Perché Flask converte automaticamente il valore di ritorno: un `dict` o una `list` ritornati da una view vengono passati a **`jsonify()`** automaticamente (body JSON, mimetype `application/json`). Sono le strutture che mappano direttamente sul **JSON** (oggetto ↔ dict, array ↔ list), quindi si serializzano senza codice extra. È il formato dominante delle REST API.

**Qual è il gap semantico tra un messaggio JSON e un messaggio RPC?**
→ [[rest]], [[rpc]], [[protocol-buffers]]. Un messaggio **JSON** è **testuale, senza schema rigido e senza tipi forti** (numeri/stringhe/oggetti generici), auto-descrittivo (i nomi dei campi viaggiano col dato), orientato alla **risorsa**. Un messaggio **RPC** (protobuf) è **binario, fortemente tipizzato, con schema (`.proto`) e field tag** (i nomi non viaggiano), orientato alla **chiamata di procedura**. Il "gap" è colmato dal marshalling/conversione: passando da REST/JSON a gRPC si deve mappare campi testuali non tipati su campi tipati con tag, e l'invocazione di risorsa su invocazione di metodo.

**Mapping dei porti in Flask (Repliche)**
→ [[flask]], [[virtualizzazione-container]] (inferenza). Per **replicare** un servizio Flask si avviano più istanze su **porte diverse** (`app.run(port=5000)`, `5001`, ...) o in container distinti con **port mapping** Docker (`-p hostPort:containerPort`); un reverse proxy/load balancer distribuisce le richieste. Il dev server è multi-threaded di default; in produzione si usa un server WSGI (Gunicorn) con più worker. (Vedi §5 per il networking dei container.)

**Come realizzare un metodo di serializzazione per esporre un servizio gRPC come REST API?**
→ [[grpc]], [[flask]], [[rest]]. Si scrive un **gateway Flask**: per ogni endpoint REST, la view (1) legge il JSON/parametri della richiesta (`request.get_json()`, `request.args`), (2) costruisce il messaggio **protobuf** richiesto (`pb2.Request(campo=valore)`), (3) invoca lo **stub** gRPC (`stub.Metodo(req)`), (4) riceve la response protobuf e la **serializza in JSON** (costruendo un dict campo-per-campo, o con `google.protobuf.json_format.MessageToDict`) e la ritorna con `jsonify(...)`, mappando gli `StatusCode` gRPC sugli status HTTP corrispondenti (→ [[gestione-errori-api]]). In pratica si traduce JSON↔protobuf nei due versi e REST(risorsa)↔RPC(metodo).

---

## 3. Concorrenza e Parallelismo

### 3.1 Concetti Generali (Sistemi Operativi)

**Differenza tra processi e thread**
→ [[processo-thread]]. Un **processo** è un programma in esecuzione con spazio di indirizzamento **proprio e isolato** (codice, dati, heap, stack), descritto dal **PCB**; è "pesante", overhead di creazione alto, comunica via **IPC** (pipe, socket), un suo crash è isolato. Un **thread** è un flusso di esecuzione **dentro** un processo: condivide memoria globale (codice, dati, heap, file aperti), ha **proprio** solo stack, PC e registri; è "leggero", creazione e context switch economici, comunica via **memoria condivisa**, ma un suo crash può abbattere l'intero processo. Concetto chiave: il thread separa **esecuzione** da **possesso di risorse**.

**Differenza task CPU-bound e I/O-bound e influenza su multithreading vs multiprocessing**
→ [[gil]], [[concorrenza-parallelismo]]. **CPU-bound** = limitato dalla potenza di calcolo (loop, calcoli); **I/O-bound** = passa il tempo in attesa di I/O (rete, file, DB). In Python il **GIL** fa sì che i thread non eseguano bytecode in parallelo: per **I/O-bound** il threading va bene (il GIL è **rilasciato durante l'I/O**, i thread si sovrappongono utilmente); per **CPU-bound** il threading **non scala** (un solo thread esegue alla volta) → serve il **multiprocessing** (ogni processo ha il suo interprete e GIL → parallelismo reale sui core).

**I meccanismi di locking sono interoperabili tra multithread e multiprocess?**
→ [[threading]], [[multiprocessing]] (inferenza ancorata al materiale). **No.** Le primitive di `threading` (`Lock`, `RLock`, `Condition`, `Semaphore`...) operano sulla **memoria condivisa di un singolo processo** e non sincronizzano thread di processi diversi. Per i processi servono le primitive **equivalenti** di `multiprocessing` (stessi nomi: `Lock`, `Semaphore`, `Condition`, `Event`), che si appoggiano a meccanismi del **SO** (e a IPC) per funzionare tra processi che **non** condividono memoria. Le API sono volutamente simmetriche, ma gli oggetti non sono intercambiabili tra i due mondi.

**Cos'è un "Selfish Thread"?**
→ [[java-threading]]. È un thread **CPU-bound** che, una volta ottenuta la CPU, **non la cede volontariamente**: non fa I/O e non si blocca (es. un `while` di conteggio). Su sistema **non time-slicing** arriva fino in fondo al suo `run()` prima che parta un altro thread; thread di **pari priorità** rischiano la **starvation**. Poiché la specifica Java **non impone il time-slicing**, la soluzione portabile è far cedere la CPU esplicitamente con `yield()` (o `sleep`), che rende l'esecuzione deterministica (round-robin). È l'analogo Java del thread che terrebbe il **GIL** in Python.

**Se ho multithreading perché ho bisogno di multiprocess? (il GIL in pratica)**
→ [[gil]], [[multiprocessing]]. Perché in CPython il **GIL** permette a **un solo thread alla volta** di eseguire bytecode: i thread danno **concorrenza ma non parallelismo** sui core. Per i task **CPU-bound** una soluzione multithread è **più lenta** della stessa multiprocess. Il **multiprocessing** aggira il GIL (ogni processo ha il proprio interprete + GIL), ottenendo parallelismo reale. Quindi il multithreading basta solo per l'I/O-bound; per sfruttare più core su calcolo serve il multiprocessing.

**Thread User Level (ULT vs KLT)**
→ [[processo-thread]]. **ULT (User Level Thread)**: gestiti da una libreria in spazio utente, **invisibili al SO**; context switch velocissimo (nessuna syscall), ma un blocco I/O di un thread **blocca tutto il processo** (il SO vede solo il processo) e non sfruttano più core. **KLT (Kernel Level Thread)**: gestiti dal SO, ogni thread si blocca indipendentemente ed esegue **simultaneamente** su core diversi; più pesanti (context switch in modalità kernel). Python `threading` usa **KLT**. Modelli di mapping: pure user-level (M:1), pure kernel-level (1:1), combined (M:N).

### 3.2 Java

**Come si realizza un monitor in Java? Che tipo di monitor è (signal and continue) e qual è il limite principale?**
→ [[java-sincronizzazione]], [[monitor]]. Una classe con metodi `synchronized` **è un monitor**: ogni oggetto ha un mutex intrinseco, i metodi sincronizzati garantiscono mutua esclusione automatica; la cooperazione usa `wait()`/`notify()`/`notifyAll()` (ereditati da `Object`, invocabili solo dentro `synchronized`). È un monitor con semantica **signal-and-continue**: chi fa `notify()` **mantiene il monitor e prosegue**; il thread svegliato non riprende subito ma torna a competere per il lock → per questo la condizione va rivalutata in un **`while`**, non in un `if`. **Limite principale**: ha **una sola condition variable implicita** (un solo wait set) → non si possono distinguere più condizioni di attesa, a differenza dei monitor con più condition esplicite.

**Limiti di synchronized e come superarli (Lock, ReentrantLock, Semaphore)**
→ [[java-sincronizzazione]]. `synchronized` ha limiti: lock **non interrompibile**, nessun tentativo non bloccante, nessun timeout, niente fairness, **una sola condition** implicita. Si superano con `java.util.concurrent` (Java 1.5): `Lock`/`ReentrantLock` (lock espliciti con `lock()`/`unlock()` in `finally`, `tryLock`, lock interrompibili, più `Condition`), `Semaphore` (controllo di N permessi), `CountDownLatch`.

**Differenza tra Lock e ReentrantLock**
→ [[java-sincronizzazione]]. `Lock` è l'**interfaccia** (`java.util.concurrent.locks.Lock`); `ReentrantLock` è la sua **implementazione rientrante**: lo stesso thread può riacquisire un lock che già possiede senza auto-bloccarsi (recursion count), esattamente come fa `synchronized`. Quindi non sono allo stesso livello: una è il contratto, l'altra l'implementazione concreta.

**Comportamento di un metodo synchronized e uno static synchronized chiamati contemporaneamente**
→ [[java-sincronizzazione]]. **Non si bloccano a vicenda**: il metodo d'istanza `synchronized` acquisisce il lock sull'**istanza** (`this`), quello `static synchronized` acquisisce il lock sull'oggetto **`Class`**. Sono **monitor distinti** → eseguono in concorrenza. (Due `static synchronized` invece eseguono in sequenza, stesso lock di classe; due d'istanza sullo stesso oggetto, in sequenza.)

**Come funzionano i semafori in Java? (acquire, release, tryAcquire)**
→ [[java-sincronizzazione]], [[semaforo]]. `Semaphore sem = new Semaphore(N)` gestisce N permessi: `acquire()` decrementa (blocca se 0), `release()` incrementa (e risveglia un thread in attesa), `tryAcquire()` tenta senza bloccare (ritorna `boolean`). Limita a N gli accessi concorrenti a una risorsa; con N=1 è un mutex. Concettualmente: `value` se negativo indica quanti thread sono in attesa.

**Si può usare un ThreadPoolExecutor in Java? (Sì)**
→ [[java-threading]] (inferenza ancorata al materiale). Sì: `java.util.concurrent` offre gli **Executor**/`ThreadPoolExecutor` (e `Executors.newFixedThreadPool(n)`), un pool di thread riusabili a cui si **sottomettono task** (`Runnable`/`Callable`) con `submit`/`execute`, evitando di creare/distruggere un thread per task. È l'equivalente Java del `ThreadPoolExecutor` usato dal server gRPC Python.

**Quali sono gli stati di un thread in Java e come avvengono le transizioni?**
→ [[java-threading]]. `New` → con `start()` diventa `Runnable` (ready-to-run, in attesa del turno) → lo scheduler lo porta in `Running`. Da `Running`: a `Runnable` con `yield()` o swap-out dello scheduler; a `Blocked/Waiting` quando si blocca (`sleep`, `wait`, lock `synchronized`, I/O); a `STOP` quando `run()` termina (o `stop()` deprecato). Da `Blocked/Waiting` torna `Runnable` al cessare della causa (timeout di sleep, `notify`, fine I/O, lock acquisito, interruzione). Stati di blocco: Sleeping/Waiting (interrompibili), Blocked I/O, Blocked synch.

### 3.3 Python

**Cos'è il GIL e quali sono le sue implicazioni?**
→ [[gil]]. Il **Global Interpreter Lock** è un mutex interno a CPython che garantisce che **un solo thread alla volta** esegua bytecode Python, anche su multicore. Esiste perché la gestione memoria di CPython usa **reference counting** non thread-safe (senza lock, due thread corromperebbero i contatori). Implicazioni: i thread danno **concorrenza ma non parallelismo** sul calcolo; il GIL è **rilasciato durante l'I/O** e ogni N bytecode → ottimo per I/O-bound, inutile per CPU-bound (lì serve `multiprocessing`). Vantaggi: interprete più semplice, single-thread più veloce, integrazione di librerie C non thread-safe. In Python 3.13+ esiste una build *free-threaded* (`--disable-gil`), opzionale.

**Dato il GIL, quando multithreading (I/O-bound) e quando multiprocessing (CPU-bound)?**
→ [[gil]], [[multiprocessing]]. **Multithreading** per **I/O-bound**: durante l'attesa di rete/file/DB il GIL è rilasciato e altri thread avanzano → buona sovrapposizione con overhead basso e memoria condivisa. **Multiprocessing** per **CPU-bound**: ogni processo ha il suo GIL → parallelismo reale sui core; costa più overhead (fork/IPC) ma è l'unico modo di scalare il calcolo.

**Quali sono le primitive del modulo multiprocessing per creare e gestire processi?**
→ [[multiprocessing]]. `Process(target, args)` con `start()`/`join()`/`is_alive()` (firma analoga a `threading.Thread`); `Pool(processes=n)` con `map`/`apply`; `concurrent.futures.ProcessPoolExecutor` (astrazione con `submit`/`result`). Per la comunicazione: `Queue`, `Pipe`, `Value`/`Array` (shared memory via `ctypes`); per la sincronizzazione le primitive equivalenti a threading (`Lock`, `Semaphore`, `Event`, `Condition`).

**Quali sono i tre modi per creare un processo in Python? Sono tutti ugualmente portabili?**
→ [[multiprocessing]]. Tre **start method**: 
- **spawn** (default Windows/macOS, disponibile ovunque, il più lento): avvia un **nuovo interprete** e **re-importa** il modulo (→ richiede `if __name__ == "__main__"`); trasferisce al figlio solo l'essenziale via **pickling**.
- **fork** (solo Unix, default fino a 3.13): usa `os.fork()`, il figlio **eredita tutto** (copy-on-write), niente re-import; ma è **unsafe** (lock acquisiti da altri thread restano bloccati → rischio deadlock).
- **forkserver** (Unix, default da 3.14): un server single-threaded fa le fork su richiesta → **safe**.

Non sono ugualmente portabili: **fork/forkserver solo su Unix**, **spawn ovunque**. Quindi codice portabile deve assumere spawn (idiom `__main__`, oggetti picklabili).

**Come funziona il multithreading, come funziona il multiprocessing, perché serve anche il multiprocessing (GIL)**
→ [[threading]], [[multiprocessing]], [[gil]]. Il **multithreading** (`threading`, KLT) crea più flussi nello stesso processo che condividono memoria — ideale I/O-bound, ma soggetto al **GIL** (un thread per volta esegue bytecode). Il **multiprocessing** crea processi separati, ognuno col proprio interprete e GIL, che comunicano via IPC (Queue/Pipe) — vero parallelismo. Serve **proprio per il GIL**: sul CPU-bound i thread non sfruttano i core, i processi sì.

**Quali sono i meccanismi di comunicazione tra processi in Python? (Pipe, Queue, Event, SharedMemory)**
→ [[multiprocessing]]. **Pipe** — coppia di `Connection` (endpoint), `send`/`recv`, bidirezionale di default (i dati si corrompono se due processi usano lo stesso endpoint). **Queue** — coda FIFO process-safe (su pipe + lock), `put`/`get` bloccanti, varianti `SimpleQueue`/`JoinableQueue`. **Value/Array (Shared Memory)** — dati semplici condivisi via `ctypes`, con lock opzionale. **Event** — flag booleano per segnalazione tra processi. (Non c'è memoria condivisa implicita: tutto passa per canali espliciti.)

**Reentrant Lock in threading e problema del deadlock**
→ [[threading]]. Un `RLock` può essere acquisito **più volte dallo stesso thread** (tiene owning thread + recursion level): `acquire` dell'owner non blocca e incrementa il livello, `release` lo decrementa e libera solo a zero. Serve per **funzioni ricorsive**, **metodi sincronizzati che ne chiamano altri sincronizzati**, **sezioni critiche annidate**: con un `Lock` normale il secondo `acquire()` dello **stesso** thread si bloccherebbe in attesa di sé stesso → **deadlock**. L'`RLock` evita questo auto-deadlock.

**Quali sono i meccanismi di sincronizzazione in Python e confronto con Java?**
→ [[threading]], [[java-sincronizzazione]], [[semaforo]], [[monitor]]. Python `threading`: `Lock` (mutex), `RLock` (rientrante), `Condition` (monitor: `wait`/`notify`/`notify_all`, di default su un `RLock`), `Semaphore`, `Event`, `threading.local`. Confronto con Java:

| Python | Java | Note |
|---|---|---|
| `Lock` | `ReentrantLock` (o blocco `synchronized`) | mutex |
| `RLock` | `ReentrantLock` / `synchronized` (rientrante per natura) | rientranza |
| `Condition` + `while wait()` | `synchronized` + `wait()`/`notify()` in `while` | monitor signal-and-continue in entrambi |
| `Semaphore` | `java.util.concurrent.Semaphore` | semaforo a N permessi |
| `Event` | (CountDownLatch / wait-notify) | segnalazione |

Differenza di fondo: in Java il monitor è **integrato nel linguaggio** (`synchronized` su ogni oggetto) e i thread sono paralleli (no GIL); in Python la sincronizzazione è via oggetti del modulo `threading` e il **GIL** già serializza il bytecode (ma i lock restano necessari perché un'operazione "atomica" a livello Python può essere interrotta tra i bytecode). Entrambi i monitor sono **signal-and-continue** → in entrambi si usa `while` (non `if`) sulla condizione.

---

## 4. Linguaggi: Python vs Java

### 4.1 Performance e Gestione Memoria

**È più performante Python o Java? (JIT di Java vs GIL di Python)**
→ [[gil]], [[interprete-python]]. **Dipende dal contesto.** Java compila in bytecode eseguito dalla JVM con **JIT** (Just-In-Time): il codice hot viene compilato a codice macchina nativo a runtime → throughput elevato e thread realmente paralleli (no GIL). **CPython** interpreta il bytecode sulla PVM (nessun JIT) ed è vincolato dal **GIL** (no parallelismo di calcolo coi thread) → tipicamente più lento sul **CPU-bound** puro. Però: per **I/O-bound** la differenza si assottiglia (si aspetta l'I/O); con estensioni C/NumPy o con `multiprocessing` Python recupera; PyPy (JIT) accelera il CPU-bound. Java vince sul calcolo intensivo multithread; Python vince in produttività/velocità di sviluppo.

**Confrontare gestione memoria e garbage collector in Python e Java**
→ [[interprete-python]], [[oop]] (parte oltre il materiale esplicito, segnalata). **Python (CPython)**: gestione memoria automatica basata principalmente su **reference counting** (un oggetto è deallocato appena il suo contatore di riferimenti va a zero — è il motivo per cui esiste il GIL, → [[gil]]), più un **garbage collector** ciclico che recupera i cicli di riferimenti che il solo reference counting non libera; `__del__` è il distruttore invocato dal GC. **Java**: nessun reference counting, la JVM usa un **garbage collector tracing** (mark-and-sweep generazionale: young/old generation) che individua gli oggetti non più raggiungibili dalle radici; la deallocazione non è deterministica (a differenza del reference counting Python che spesso libera subito). In entrambi il programmatore **non libera la memoria a mano**. *(Il dettaglio sugli algoritmi GC va oltre quanto trattato esplicitamente nel materiale del corso.)*

### 4.2 Programmazione a Oggetti (OOP) e Interfacce

**Principali differenze nell'OOP tra Python e Java**
→ [[oop]], [[polimorfismo]], [[ereditarieta]]. (1) **Tipizzazione**: Python dinamica (duck typing), Java statica (controlli a compile-time). (2) **Polimorfismo**: Python **strutturale** (conta cosa l'oggetto sa fare), Java **nominale** (conta la classe/relazione dichiarata). (3) **Interfacce**: Python implicite (protocolli; opzionali `ABC`/`Protocol`), Java esplicite (`interface`, `implements`). (4) **Ereditarietà multipla**: Python la supporta (con MRO), Java no per le classi (solo interfacce). (5) **Incapsulamento**: Python per convenzione (`_`, name mangling `__`), Java con modificatori reali (`private`/`protected`/`public`). (6) **`self` esplicito** in Python vs `this` implicito in Java.

**Come funziona l'OOP in Python?**
→ [[oop]]. Si definiscono **classi** (template) con `class`; gli **oggetti** sono istanze. Il costruttore è `__init__(self, ...)`; `self` è il riferimento all'istanza (primo parametro di ogni metodo). Attributi di **classe** (condivisi) vs di **istanza** (`self.x`). Metodi **dunder** (`__str__`, `__eq__`, `__add__`, `__len__`...) per integrare l'oggetto con le operazioni del linguaggio. Incapsulamento per convenzione (`_attr`, `__attr` con name mangling). Supporta i tre pilastri: incapsulamento, ereditarietà, polimorfismo (duck typing).

**Cos'è self in Python?**
→ [[oop]]. È il **riferimento all'istanza corrente**, primo parametro esplicito di ogni metodo d'istanza. Quando si chiama `p.metodo()`, Python passa automaticamente `p` come `self`. Serve ad accedere agli attributi/metodi dell'oggetto (`self.nome`). È esplicito (a differenza del `this` implicito di Java) — conseguenza del modello a dizionari di Python.

**Differenza nell'uso delle interfacce e riflesso sulla generazione di codice (es. gRPC)**
→ [[polimorfismo]], [[grpc]], [[oop]]. In **Java** le interfacce sono **esplicite**: il servicer gRPC **implementa** l'interfaccia generata dal `.proto` (relazione dichiarata, verificata a compile-time → polimorfismo nominale). In **Python** le interfacce sono **implicite** (duck typing): il servicer eredita dalla classe `...Servicer` generata, ma ciò che conta è che **esponga i metodi giusti** (verifica a runtime). Riflesso sulla generazione di codice: in Java `protoc` genera **interfacce/classi astratte tipizzate** (`ImplBase`, stub `BlockingStub`/`Stub`/`FutureStub`) e il package conta; in Python genera classi più dinamiche (`Stub`, `Servicer`) e il binding è strutturale. Stesso `.proto`, ma il contratto è imposto staticamente in Java, convenzionalmente in Python.

**Come funziona il polimorfismo in Python?**
→ [[polimorfismo]]. **Duck typing**: polimorfismo **strutturale e dinamico** — "if it walks like a duck and quacks like a duck, it's a duck". Un oggetto è idoneo se **possiede i metodi/attributi attesi**, indipendentemente dalla sua classe o da una base comune; il metodo è risolto a **runtime** (lookup lungo l'MRO), se manca → `AttributeError`. Non serve una superclasse comune (l'override con ereditarietà è solo un caso particolare). Contrapposto al **nominale statico** di Java (idoneità per classe/relazione dichiarata, verificata dal compilatore). Trade-off: flessibilità e genericità vs sicurezza a compile-time.

### 4.3 Eccezioni

**Come funziona la gestione delle eccezioni in Python? (try, except, else, finally)**
→ [[eccezioni]]. Il blocco `try` racchiude l'operazione rischiosa; `except TipoErrore as e` cattura un tipo specifico (si possono concatenare più `except`, o catturare tuple `(Tipo1, Tipo2)`, o `except Exception` come catch-all); `else` viene eseguito **solo se NON** si è verificata alcuna eccezione nel `try`; `finally` viene eseguito **sempre** (con o senza eccezione), per il cleanup (chiusura file/connessioni). Le eccezioni sono **oggetti/classi** che ereditano da `Exception` (a sua volta da `BaseException`); `except Exception` cattura tutto tranne `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`.

**Come si crea un'eccezione custom e come si lancia (raise) e si gestisce?**
→ [[eccezioni]], [[ereditarieta]]. Si crea **sottoclassando `Exception`** (eventualmente aggiungendo attributi nel costruttore con `super().__init__(msg)`):
```python
class MiaEccezione(Exception):
    def __init__(self, msg, codice):
        super().__init__(msg)
        self.codice = codice
```
Si **lancia** con `raise MiaEccezione("errore", 42)` (oppure `raise` nudo dentro un `except` per ri-lanciare l'eccezione corrente). Si **gestisce** con `try/except MiaEccezione as e:` accedendo ai suoi attributi (`e.codice`). È il pattern usato per modellare errori applicativi specifici e tradurli poi in status HTTP/gRPC (→ [[gestione-errori-api]]).

---

## 5. Virtualizzazione e Containers (Docker)

### 5.1 Concetti di Base

**Come si implementa un'applicazione distribuita con meccanismi di virtualizzazione?**
→ [[virtualizzazione-container]], [[docker]], [[docker-compose]]. Si **containerizza** ogni servizio (Flask, gRPC server, MongoDB, ActiveMQ) in un'immagine Docker, poi si compongono i container con **Docker Compose** (`compose.yaml`: servizi, rete, volumi, dipendenze) avviando l'intero stack con `docker compose up`. I container comunicano via rete Docker (bridge/service network); lo stato persistente sta in **volumi**. Per scalare/orchestrare su più nodi si usa **Docker Swarm** (servizi replicati, load balancing) o Kubernetes. Vantaggi: deploy portabile, riproducibile e indipendente dall'host.

**Come comunicano due container via rete e che problema c'è se replico un provider Middleware come ActiveMQ?**
→ [[linux-namespaces]], [[docker]] (la parte sul broker è inferenza ancorata al materiale). Ogni container ha il proprio **network namespace** (stack TCP/IP, porte, interfacce); la comunicazione passa per una **coppia veth** collegata al **Linux bridge `docker0`** (o a una rete Docker dedicata), con risoluzione per nome del servizio e **NAT** verso l'esterno; verso l'host serve la **pubblicazione delle porte** (`-p host:container`). **Problema replicando ActiveMQ**: un broker MOM è **stateful** (code, topic, messaggi persistenti, durable subscription). Replicarlo ingenuamente crea istanze con **stato separato**: i messaggi finiscono su broker diversi, una durable subscription registrata su un broker non vede i messaggi pubblicati su un altro, i client possono connettersi a repliche diverse e "perdere" messaggi. Serve uno **storage condiviso/cluster di broker** (master-slave, shared KahaDB) e attenzione ai **namespace di rete/porte** per non avere conflitti — non basta scalare le repliche come per un servizio stateless.

**Per creare un container cosa serve? (un'immagine Docker)**
→ [[docker]]. Serve un'**immagine Docker**: un Union/Overlay File System a **layer read-only** (più il thin R/W layer aggiunto al run), costruita da un **Dockerfile**. `docker run immagine` crea un container (processo esteso) da quell'immagine. L'immagine si ottiene con `docker build` o `docker pull` da un registry (Docker Hub).

**Un disco di una macchina virtuale cos'è? (un file sull'host)**
→ [[virtualizzazione-container]]. Il disco di una VM è un **file** (virtual disk image) memorizzato sul filesystem dell'host, che l'hypervisor presenta al guest OS come se fosse un disco fisico. (È una differenza con i container, che non hanno un disco virtuale ma un rootfs ottenuto via overlay dei layer immagine.)

**Perché i container sono più veloci di una VM? (kernel condiviso, boot = processo/fork)**
→ [[virtualizzazione-container]]. Perché **non emulano l'hardware né includono un Guest OS**: condividono il **kernel host** e usano namespaces (isolamento) + cgroups (risorse). Un container è di fatto un **processo esteso**: avviarlo costa quanto avviare un processo (**~2 secondi** vs ~2 minuti di una VM). Non c'è l'overhead del **trap-and-emulate** dell'hypervisor sulle istruzioni privilegiate (ring 0): le system call del container vanno **direttamente** al kernel host. Footprint molto minore → 100–1000 container vs 10–100 VM per server.

**Container vs Virtualizzazione**
→ [[virtualizzazione-container]]. VM = virtualizzazione "pesante": hypervisor + Guest OS completo per ogni istanza, isolamento forte, overhead alto, boot lento. Container = virtualizzazione "leggera": **riusa le astrazioni del kernel host** (namespaces/cgroups), niente Guest OS/hypervisor, overhead minimo, boot quasi istantaneo, ma **isolamento più debole** (kernel condiviso = single point of failure / superficie d'attacco; no container Windows su kernel Linux). Trade-off **prestazioni ↔ isolamento** (runtime ibridi gVisor/Kata cercano un compromesso).

**A cosa fare attenzione creando più istanze (es. più broker) in container? (Namespaces)**
→ [[linux-namespaces]]. Ai **namespace**, in particolare quello di **rete**: ogni container ha il proprio stack/porte, quindi più broker possono fare bind sulla stessa porta interna **senza conflitto**; il conflitto nasce solo pubblicando entrambe sulla **stessa porta dell'host** (root namespace, unica). Va gestita la mappatura porte host↔container e, per servizi stateful come i broker, lo **stato condiviso** (vedi domanda su ActiveMQ).

**Cos'è un namespace di rete e cosa fa?**
→ [[linux-namespaces]]. È il namespace che isola lo **stack di rete**: ogni network namespace ha **una propria istanza delle strutture dati** dello stack TCP/IP (interfacce, tabelle di routing, ARP, iptables, **spazio delle porte**) — non si duplica il codice (uno solo nel kernel), si replicano i dati per namespace. Conseguenza: due container possono usare la stessa porta internamente senza conflitto. La comunicazione tra namespace usa **coppie veth** collegate a un **bridge** (`docker0`); l'uscita verso l'esterno passa per NAT.

**Cos'è il namespace mnt (Mount)?**
→ [[linux-namespaces]]. È il namespace che isola i **mount points / l'albero del filesystem**: ogni container ha la propria vista dei filesystem montati. `/proc`, `/dev`, `/sys` sono montati **privatamente** per ciascun container; combinato con `pivot_root` sul rootfs overlay, il filesystem dell'host risulta isolato da quello del container.

**Quali problemi di sicurezza/affidabilità se più container accedono allo stesso file system?**
→ [[virtualizzazione-container]], [[docker]], [[mongodb]] (parziale inferenza). Condividere lo stesso filesystem/volume tra container introduce: **race condition** e corruzione dei dati su scritture concorrenti (più scrittori senza coordinamento, problema TOCTOU — stessa natura delle race multi-thread, → [[mongodb]]); rottura dell'**isolamento** (un container compromesso può leggere/alterare dati altrui → superficie d'attacco, escalation); incoerenza se non c'è locking applicativo o atomicità demandata a un DBMS; rischio di accoppiare cicli di vita di container "usa-e-getta". In generale lo **stato condiviso** va gestito con un servizio dedicato (DB con atomicità) o volumi con accesso controllato, non con accesso libero allo stesso FS.

**Quali sono gli svantaggi della virtualizzazione dal punto di vista delle system call?**
→ [[virtualizzazione-container]]. Nelle **VM** ogni **istruzione privilegiata/sensitive** del guest (che dovrebbe girare in ring 0) genera una **trap** verso l'hypervisor, che la **intercetta ed emula/traduce** (**trap-and-emulate**): è il cuore dell'overhead della virtualizzazione pesante. Le system call del guest non vanno direttamente all'hardware ma attraversano lo strato di indirezione dell'hypervisor → costo prestazionale. Nei **container** questo non accade: il processo containerizzato esegue le system call **direttamente sul kernel host** (che applica solo le restrizioni di namespace/cgroups) → nessun overhead da hypervisor.

**Cosa sono i cgroups e a cosa servono? (limitare CPU e memoria)**
→ [[cgroups]]. I **Control Groups** sono un sottosistema del kernel Linux che **limita, contabilizza e monitora le risorse** di **gruppi** di processi (CPU, memoria, I/O, rete). Docker crea un cgroup per ogni container per imporre limiti (`--memory 512m`, `--cpus 0.5`). Moduli: `memory`, `cpu`/`cpuset`, `blkio`, `net_prio`, `devices`, `freezer`, `pids`. Limitano anche risorse **non-hardware** del kernel (es. `pids` contro le fork bomb). Differenza coi namespace: i namespace **isolano la visibilità** (per processo), i cgroups **limitano il consumo** (per gruppo).

**È possibile definire un consumo di memoria/banda specifico per evitare crash? (Sì, cgroups)**
→ [[cgroups]]. Sì, tramite **cgroups**: `--memory` limita la RAM (se la supera interviene l'**OOM killer** che uccide processi nel cgroup), `--cpus` limita la CPU, `blkio`/`net_prio` limitano I/O su disco e priorità di rete. I limiti si propagano nella gerarchia (un figlio non supera il padre). Servono proprio a evitare che un container monopolizzi le risorse e faccia crashare l'host o gli altri container (isolamento prestazionale).

**Come funziona il file system a layer delle immagini Docker?**
→ [[docker]]. L'immagine è un **Union/Overlay File System** a **layer read-only** (ogni layer identificato da hash SHA256), prodotti dalle istruzioni del Dockerfile (`FROM`/`RUN`/`COPY`/`ADD`). Al run si aggiunge un **thin R/W layer** (upperdir). In OverlayFS: **lowerdir** = layer immagine R/O (impilati), **upperdir** = layer R/W del container, **merged** = vista fusa (il rootfs). Regole: **lettura** dall'alto verso il basso (vince upperdir); **scrittura** su file di un lowerdir → **copy-on-write** (copy-up nell'upperdir); **cancellazione** → **whiteout file** che maschera l'originale. Così più container condividono i lowerdir, le immagini restano immutabili e il container è effimero (distruggerlo butta solo l'upperdir).

**Struttura Dockerfile e Docker Compose**
→ [[docker]], [[docker-compose]]. **Dockerfile** — ricetta dell'immagine, layer per layer: `FROM` (immagine base), `WORKDIR`, `COPY`, `RUN` (esegue comandi a build-time, nuovo layer), `ENTRYPOINT` (eseguibile fisso), `CMD` (argomenti di default), `EXPOSE` (documentativo). Il comando effettivo è `ENTRYPOINT + CMD`. Best practice: copiare `requirements.txt` e `pip install` **prima** del codice per sfruttare la cache dei layer. **Docker Compose** — `compose.yaml` per app **multi-container**: sezione `services` con `build`/`image`, `command`, `ports` (`host:container`), `volumes`, `environment`, `links`/reti, dipendenze. `docker compose up -d` avvia l'intero stack; con `deploy.replicas` + `docker stack deploy` si va su Swarm.

**Docker container: come replicare un servizio (namespace)**
→ [[docker-swarm]], [[linux-namespaces]]. Si replica con un **servizio Swarm**: `docker service create --replicas 3 --publish 5001:5001 immagine` crea 3 task (container) distribuiti sui nodi; l'**ingress routing mesh** (via IPVS) bilancia le richieste (round-robin) su qualsiasi replica, anche su nodi diversi. Ogni replica vive nel proprio **network namespace** (può usare la stessa porta interna senza conflitto); la porta pubblicata è aperta su tutti i nodi. Per servizi **stateless** (Flask) la replica è immediata; per servizi **stateful** servono accorgimenti (storage condiviso).

**Cosa genera overhead per quanto riguarda i container?**
→ [[virtualizzazione-container]], [[docker]] (parziale inferenza). A differenza delle VM, **non** c'è overhead di hypervisor/trap-and-emulate né di Guest OS. L'overhead residuo dei container deriva da: lo strato di **rete** (bridge `docker0`, veth, **NAT**, routing mesh in Swarm), il **copy-on-write** dell'overlay alla prima scrittura su un file dei lowerdir, l'applicazione delle policy **cgroups/namespace**, e il layer di gestione del runtime (daemon/containerd/runc). Resta comunque molto inferiore a quello di una VM.

**Mount Space / immagine a layer / file-system leggero**
→ [[docker]], [[linux-namespaces]]. Il **mount namespace** dà al container il proprio albero di mount; il rootfs è prodotto dall'**OverlayFS** che impila i **layer R/O** dell'immagine (lowerdir) + il thin R/W (upperdir) e li fonde (merged), attivato con `pivot_root`. È "leggero" perché i layer immagine sono **condivisi** tra container e immutabili: non si copia un intero filesystem, si monta un overlay sui layer esistenti + un upperdir vuoto → avvio quasi istantaneo, footprint ridotto.

**Differenza in termini di velocità di creazione tra un processo e un container**
→ [[virtualizzazione-container]], [[linux-namespaces]]. Sono **vicine**: un container è un **processo esteso**, creato con `clone()` + flag `CLONE_NEWxxx` (nuovi namespace) + setup cgroups + montaggio overlay del rootfs. Rispetto a un normale processo (`fork()` che eredita i namespace del padre), il container paga in più la creazione dei namespace, l'overlay mount/pivot_root e la configurazione di rete (veth/bridge). Quindi: leggermente più lento di un semplice `fork`, ma **ordini di grandezza** più veloce di una VM (boot di un OS).

**Problemi di sicurezza e affidabilità se più container accedono allo stesso file system** — duplicato (vedi sopra, §5.1): race condition/corruzione su scritture concorrenti, rottura isolamento, escalation; serve accesso controllato o atomicità demandata a un DBMS.

**Tra i meccanismi di namespace abbiamo visto quello di rete, che cosa fa?** — duplicato (vedi "Cos'è un namespace di rete"): isola lo stack TCP/IP (interfacce, routing, porte) per container, con veth+bridge per la comunicazione.

**Una volta eseguito un container, dove vengono scritte le modifiche al file system? (layer temporaneo scrivibile)**
→ [[docker]]. Nel **thin R/W layer** (upperdir dell'OverlayFS), specifico per quell'istanza di container. Le scritture su file provenienti dai layer immagine R/O passano per **copy-on-write** (copy-up nell'upperdir); le cancellazioni creano **whiteout file**. Questo layer è **effimero**: distruggendo il container i dati vanno persi → lo stato persistente va in **volumi** (cartelle host bind-mountate).

**Come specificare operazioni da eseguire all'avvio del container? (Entrypoint/Command o docker-compose)**
→ [[docker]], [[docker-compose]]. Con **`ENTRYPOINT`** (eseguibile fisso) e **`CMD`** (argomenti di default) nel Dockerfile — il comando d'avvio è la loro concatenazione (`ENTRYPOINT ["python3"]` + `CMD ["app.py"]`). Un argomento passato a `docker run immagine arg` sostituisce `CMD` (non l'ENTRYPOINT, per cui serve `--entrypoint`). In Compose si usa la chiave **`command`** (sovrascrive il CMD) nel servizio del `compose.yaml`.

**Ruoli dei nodi, mantenimento dello stato desiderato**
→ [[docker-swarm]]. In Swarm i nodi hanno ruolo **Manager** (gestiscono join, stato globale del cluster, orchestrazione; eleggono un **leader** via consenso **Raft**) o **Worker** (eseguono i **task** assegnati). Swarm mantiene lo **stato desiderato** (numero di repliche, porte, vincoli) per **reconciliation**: confronta di continuo stato reale e dichiarato e riallinea (es. se un worker cade, **ripianifica** i task mancanti su altri nodi → "Service converged"). I manager si tengono in numero **dispari** (quorum (N/2)+1) per evitare split-brain.

**Cos'è Docker Swarm?**
→ [[docker-swarm]]. È l'**orchestratore cluster nativo** del Docker Engine: gestisce più host Docker come un'unità, distribuendo automaticamente i container (task) sui nodi e garantendo **disponibilità** e **scaling** dei servizi. Architettura Manager (stato del cluster via **Raft**, leader) + Worker (eseguono task); **servizi** replicati o globali con stato desiderato; **ingress routing mesh** (IPVS) per il load balancing; **rolling update** + rollback per aggiornamenti online. Tolleranza ai guasti: quorum Raft per i manager, **reschedule** dei task per i worker. Alternativa più semplice a Kubernetes.

---

## 6. Networking (Socket)

### 6.1 Socket e Proxy-Skeleton

**Differenze principali tra socket TCP e UDP (connessione, affidabilità, ordine vs velocità)**
→ [[socket]]. **TCP** (Transmission Control Protocol): **orientato alla connessione** (instaura/usa/chiude), **affidabile** (ritrasmette i pacchetti persi), **ordine garantito** (elimina duplicati), modello a **flusso di byte full-duplex**; usato da HTTP, gRPC (HTTP/2), STOMP. **UDP** (User Datagram Protocol): **connectionless**, **non affidabile**, **ordine non garantito**, modello a **datagramma**; più leggero e veloce (no handshake né controllo di flusso), usato per DNS, streaming. In sintesi: TCP privilegia **affidabilità/ordine**, UDP privilegia **velocità/basso overhead**. Entrambi distinguono i processi tramite la **porta**; IP sottostante è best-effort (pacchetti persi/corrotti/duplicati/fuori ordine).

**Perché con UDP, inviando dati complessi, serve un unico pacchetto con un separatore?**
→ [[socket]], [[proxy-pattern]]. Perché UDP è basato sul **datagramma** e **non garantisce ordine né controllo di flusso né consegna**: se si spezzano dati complessi su più datagrammi, questi possono arrivare **fuori ordine, duplicati o persi**, e il ricevente non può ricomporli affidabilmente. Si mette quindi tutto in **un solo datagramma** con i campi separati da un **separatore** (es. `"sum#5#"`, `"motor-A|FAIL"`), così una singola `recvfrom` legge il messaggio completo e lo si fa il parsing splittando sul separatore. (È esattamente il marshalling manuale del Proxy UDP, → [[proxy-pattern]].)

**Come cambia l'implementazione del Proxy/Skeleton se si usa TCP o UDP?**
→ [[proxy-pattern]], [[socket]]. Cambia il livello di trasporto e quindi il codice di comunicazione interno a Proxy/Skeleton (la logica applicativa resta invariata):
- **TCP**: Proxy fa `socket→connect→send/recv→close`; Skeleton `socket→bind→listen→accept→recv/send`. Flusso di byte affidabile e ordinato; si possono inviare richieste lunghe senza preoccuparsi di ordine/perdita. Si usano **3 socket** (server: ascolto + connessione da `accept`; client: 1).
- **UDP**: Proxy fa `socket→sendto/recvfrom` (destinazione esplicita, niente connessione); Skeleton `socket→bind→recvfrom→sendto`. Niente garanzie → si impacchetta tutto in **un datagramma con separatore** e, volendo, si gestiscono a mano timeout/ritrasmissioni. Si usano **2 socket**.

**Spiegare il pattern Proxy/Skeleton: perché si usa e come si implementa** — duplicato di §2.1 (vedi: separa logica applicativa da comunicazione; Proxy serializza/invia lato client, Skeleton deserializza/fa upcall lato server; trasparenza d'accesso; è l'RPC manuale che gRPC automatizza). → [[proxy-pattern]].

**Confrontare l'accoppiamento del Proxy/Skeleton via delega o ereditarietà** — duplicato di §2.1 (ereditarietà = accoppiamento forte, l'impl *è-un* skeleton, no ereditarietà multipla; delega = accoppiamento debole, impl oggetto separato referenziato, più flessibile). → [[proxy-pattern]].

**Che differenza c'è tra bind() e connect()?**
→ [[socket]]. **`bind(address)`** associa la socket a un indirizzo **locale** `(IP, porta)` — lo usa il **server** per fissare la porta su cui ascoltare (porta 0 ⇒ l'OS sceglie il primo porto libero). **`connect(address)`** apre una connessione verso un indirizzo **remoto** `(IP, porta)` — lo usa il **client** (TCP) per collegarsi al server. In breve: `bind` dice "io sto qui" (indirizzo locale), `connect` dice "voglio raggiungere lì" (indirizzo remoto). Lato server TCP la sequenza è `bind→listen→accept`; lato client `connect`.

**Java aderisce allo standard delle socket di Berkeley?**
→ [[socket]] (parziale inferenza: il materiale colloca l'origine BSD, l'aderenza Java è conoscenza ancorata). Sì: l'astrazione socket nasce con **Unix 4.2 BSD (Berkeley sockets)** e Java la espone nel package `java.net` seguendone il modello. Per **TCP**: `Socket` (client) e `ServerSocket` (server, con `accept()`); per **UDP**: `DatagramSocket` + `DatagramPacket`. Concettualmente sono gli stessi primitivi Berkeley (`socket/bind/listen/accept/connect/send/recv`) incapsulati in classi Java, in modo **indipendente dalla piattaforma** (a differenza del C, dove si usa direttamente la libreria socket dell'OS).

**Possibilità di creare un Middleware RPC con socket UDP (cosa poco pratica)**
→ [[socket]], [[rpc]]. È **possibile** ma poco pratico: UDP è connectionless e **non affidabile**, quindi il middleware dovrebbe implementare a mano ritrasmissioni, ordinamento, deduplicazione e gestione timeout per ottenere una semantica RPC accettabile. La semantica risultante (→ [[rpc]]) sarebbe debole: con UDP *at least once* se arriva risposta, *zero or more* se non arriva. Va bene solo per richieste **brevi, idempotenti, a bassa latenza** (è il caso di Sun RPC su UDP); per RPC general-purpose si preferisce TCP (exactly once / at most once). Per questo gRPC usa TCP/HTTP/2, non UDP.

**Socket UDP e TCP in Java: come funziona la comunicazione?**
→ [[socket]] (mapping Java è inferenza ancorata). **TCP**: il server crea `ServerSocket(porta)` e fa `accept()` (blocca, ritorna una `Socket` di connessione per client); client crea `Socket(host, porta)`; si comunica con gli stream (`getInputStream`/`getOutputStream`), flusso di byte affidabile e ordinato. **UDP**: si usa `DatagramSocket` (il server fa `bind` su una porta) e si scambiano `DatagramPacket` con `send()`/`receive()`; ogni pacchetto porta indirizzo e dati, niente connessione né garanzie. È la controparte Java del modello Python `send/recv` (TCP) vs `sendto/recvfrom` (UDP).

**Nel caso UDP multithread, cosa si può passare al thread?**
→ [[socket]], [[threading]]. Poiché in UDP c'è **una sola socket server condivisa** e la socket **non è thread-safe**, la `recvfrom()` va fatta **nel thread principale**; al worker thread si passano **la socket, i dati ricevuti e l'address del mittente** (`args=(s, data, addr)`). Il worker si limita a **elaborare** e **rispondere** con `sendto(risposta, addr)` — non deve fare `recvfrom` sulla socket condivisa. (Differenza col TCP, dove `accept()` crea una **nuova socket di connessione** dedicata che si passa per intero a un solo thread.)

---

## 7. Database e Gestione Dati

### 7.1 SQL vs NoSQL

**Quali sono le differenze principali tra database SQL e NoSQL?**
→ [[nosql]]. 

| | SQL (Relazionale) | NoSQL |
|---|---|---|
| Schema | **Fisso** (template a cui ogni entry si conforma) | **Flessibile / schema-free** (campi on-the-fly) |
| Struttura | Tabelle (entità) collegate da **chiavi** | **Collection** di **documents** (semi-structured) |
| ACID | Garantito (Atomicity, Consistency, Isolation, Durability) | Garanzie ACID **rilassate** |
| Scalabilità | **Verticale** (server più potenti; distribuire tabelle su più server è difficile) | **Orizzontale** facile (documenti indipendenti distribuibili su nodi) |
| Relazioni | Chiavi esterne (join) | Documenti **embedded** o riferimenti |
| Query | **SQL** | API specifica (es. MongoDB Query Language) |

SQL: dati prevedibili, consistenza forte, ideale per relazioni complesse; rigido e difficile da scalare su big data. NoSQL: flessibile, scala orizzontalmente, ottimo per grandi volumi; ma non si può assumere la presenza di un campo e l'aggiornamento dati è più complesso (niente relazioni gestite dal DB). Tipologie NoSQL: **Key-Value** (Redis), **Document Store** (MongoDB), **Column Store** (Cassandra), **Graph** (Neo4j), **Search Engine** (Elasticsearch).

### 7.2 RDBMS e MongoDB

**MongoDB**
→ [[mongodb]], [[nosql]]. **MongoDB** è un DBMS **NoSQL document-oriented** open-source: memorizza i dati come **documenti JSON-like** (internamente **BSON**) in **collections**, schema-free. Gerarchia: Instance → Database → Collection (≈ tabella senza schema) → Document (≈ riga, JSON annidato) → Field. Ogni documento ha una primary key `_id` (un `ObjectId`, autogenerato). Supporta documenti **embedded** (al posto dei JOIN), query con operatori (`$gt`, `$in`, `$set`, `$inc`, `$push`...) e **operazioni atomiche** lato server (`find_one_and_update`) per evitare race condition read-modify-write. Driver Python: **PyMongo** (documenti = dict). Nel corso è il backend NoSQL delle web app Flask/gRPC.

**MongoDB: differenza tra database relazionali e non relazionali e i tipi di database non relazionale**
→ [[nosql]], [[mongodb]]. **Relazionali (SQL)**: schema fisso, dati in tabelle collegate da chiavi, ACID, scalabilità verticale, query SQL — prevedibili ma rigidi. **Non relazionali (NoSQL)**: schema-free, collection di documenti senza relazioni obbligatorie, garanzie ACID rilassate, scalabilità orizzontale facile (distribuzione su nodi) — flessibili ma con aggiornamento dati più complesso. MongoDB è del tipo **Document Store**. I **tipi di NoSQL**:
- **Key-Value** (Redis, DynamoDB) — coppie chiave→valore; cache, sessioni;
- **Document Store** (MongoDB, Couchbase) — documenti JSON annidati; web app, cataloghi;
- **Column Store** (Cassandra, HBase) — colonne di dati; analytics, time-series;
- **Graph** (Neo4j) — nodi e archi; social network, recommendation;
- **Search Engine** (Elasticsearch, Solr) — indice full-text; ricerca testuale.

> Nota: i meccanismi concreti della scalabilità orizzontale (**sharding**, **replica set**) e i modelli di consistenza distribuita (**eventual consistency**, teorema **CAP**, **BASE**) sono nomenclatura standard **oltre** quanto esplicitato nel materiale del corso (→ [[nosql]], TODO), da citare come conoscenza esterna.

### 7.3 Python (Pandas/Numpy) — [segnato NO per 2024/2025]

> ⚠️ Il file domande segna questa sezione come **[2024/2025 NO]** (fuori programma per l'anno corrente) e nel wiki non esistono pagine dedicate a Pandas/NumPy → **gap di copertura**. Risposte sintetiche di servizio (non ancorate al materiale del corso):

**Cosa sono i DataFrame e le Series in Python (Pandas)?** *(fuori materiale)* — Una **Series** è un array 1-D etichettato (indice + valori, tipo omogeneo); un **DataFrame** è una struttura 2-D tabellare (righe × colonne etichettate), in pratica un insieme di Series che condividono lo stesso indice. Sono le strutture base di Pandas per la manipolazione di dati tabellari.

**Perché DataFrame/Series sono spesso preferibili agli array NumPy?** *(fuori materiale)* — Per **maggiore flessibilità**: indici **etichettati** (accesso per nome, non solo per posizione), gestione di **dati eterogenei** (colonne di tipi diversi), gestione integrata dei **valori mancanti** (NaN), allineamento automatico sugli indici, e operazioni di alto livello (group-by, join, I/O da CSV/SQL). Gli array NumPy restano più efficienti per calcolo numerico omogeneo puro.

---

## Note finali

- Le risposte delle sezioni 1–6 sono ancorate al materiale `raw/` sintetizzato nel wiki; ogni `[[link]]` rimanda alla pagina di dettaglio per la verifica.
- Punti segnalati come **inferenza** o **fuori materiale**: semantica RPC di gRPC (§2.1/§2.2), gestione memoria/GC Java vs Python (§4.1), aderenza Java alle Berkeley socket e mapping Java TCP/UDP (§6.1), problema della replica di ActiveMQ e overhead container (§5.1), sharding/replica/CAP/BASE (§7.2), Pandas/NumPy (§7.3, fuori programma 2024/2025).

_Creato: 2026-06-25 — risposte alle domande di `Domande_ACP_aggiornate.pdf`, raggruppate per le 7 sezioni dell'originale._

