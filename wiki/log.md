# Log — Advanced Computer Programming

Formato entry: `## [YYYY-MM-DD] <operazione> | <dettaglio>`
Filtra ultimi 10: `grep "^## " wiki/log.md | tail -10`

---

## [2026-06-11] canvas | Mappa esame Flask/REST (wiki/canvas/flask-websrv-mappa-esame.canvas)
## [2026-06-11] canvas | Mappa esame NoSQL/MongoDB (wiki/canvas/nosql-mappa-esame.canvas)
## [2026-06-11] canvas | Mappa esame MOM (wiki/canvas/mom-mappa-esame.canvas)
## [2026-06-11] canvas | Mappa esame gRPC (wiki/canvas/grpc-mappa-esame.canvas)

## [2026-06-04] setup | Wiki acp inizializzato

## [2026-06-04] ingest | 00_INTRODUZIONE — Introduzione al corso ACP
## [2026-06-04] ingest | 01_PYTHON_01 — Python Introduzione (interprete, bytecode, PVM)
## [2026-06-04] ingest | 01_PYTHON_02 — Tipi scalari, non scalari, Stringhe
## [2026-06-04] ingest | 01_PYTHON_03 — Costrutti di controllo
## [2026-06-04] ingest | 01_PYTHON_04 — Funzioni (+ scope complesso, passaggio parametri pp.24-27)
## [2026-06-04] ingest | 01_PYTHON_05 — Moduli e Package (+ import relativi/assoluti pp.21-22)
## [2026-06-04] ingest | 01_PYTHON_06 — Tuple, Liste, Dizionari
## [2026-06-04] ingest | 01_PYTHON_07 — Passaggio parametri
## [2026-06-04] ingest | 01_PYTHON_08 — File ed Eccezioni
## [2026-06-04] ingest | 01_PYTHON_09 — Python OOP
## [2026-06-04] ingest | 01_PYTHON_10 — Programmazione Concorrente: Richiami
## [2026-06-04] ingest | 01_PYTHON_11 — Python Concurrency (threading, GIL, multiprocessing)
## [2026-06-04] ingest | 01_PYTHON_12 — Python Networking (socket, TCP/UDP)
## [2026-06-04] ingest | 01_PYTHON_13 — Sistemi Middleware (RPC, stub, skeleton)
## [2026-06-04] ingest | 01_PYTHON_14 — Python RPC / gRPC / Protocol Buffers
## [2026-06-04] ingest | 01_PYTHON_15 — Python MOM (ActiveMQ, STOMP, pub-sub)
## [2026-06-04] ingest | 01_PYTHON_16 — Flask / REST / Web Services
## [2026-06-04] ingest | 01_PYTHON_17 — NoSQL Databases (MongoDB, PyMongo)
## [2026-06-04] ingest | 02_JAVA_01 — Java Multithreading (Thread, Runnable, lifecycle)
## [2026-06-04] ingest | 02_JAVA_02 — Sincronizzazione Java (synchronized, monitor, wait/notify, Java 1.5)
## [2026-06-04] ingest | 02_JAVA_03 — Java Networking (Socket, ServerSocket, DatagramSocket, multithread)
## [2026-06-04] ingest | 02_JAVA_04 — Proxy-Skeleton Java (pattern, esempio Contatore Remoto UDP)
## [2026-06-04] ingest | 02_JAVA_05 — JMS (ActiveMQ, PTP/PubSub, Abstract Factory, JNDI)
## [2026-06-06] nuova-pagina | gestione-errori-api — sintesi da query su eccezioni PyMongo/status HTTP, abort/errorhandler Flask, gRPC context/StatusCode
## [2026-06-06] aggiornamento | mongodb — espansa sezione query: operatori filtro/update completi, find_one_and_update, schema decisionale (da query utente)
## [2026-06-06] lint | fix pagine orfane e link rotti: 4 fonti+entità, [[asyncio]] stub, [[middleware-trasparenza]] nuova pagina, backlink grpc/mom/flask/jms aggiornati
## [2026-06-07] setup | Cartelle prove-esame e svolgimenti create — workflow genera/valuta pronto
## [2026-06-07] ingest | prove-esame-2023-2024 — 5 prove pratiche analizzate (2023-11, 2024-03, 2024-06, 2024-07, 2024-10)
## [2026-06-07] nuova-pagina | pattern-esame — pattern ricorrenti estratti dalle 5 prove (architettura, prod/cons, proxy-skeleton, routing, checklist)
## [2026-06-07] prova-simulata | 2026-06-08-sim-01 — sistema monitoraggio sensori (Python, Socket TCP + Flask + MongoDB)
## [2026-06-09] prova-simulata | 2026-06-09-sim-02 — telemetria industriale (Python gRPC + STOMP, Java JMS)
## [2026-06-10] prova-simulata | 2026-06-10-sim-03 — qualità produzione (Java proxy-skeleton Socket + JMS Topic, Python STOMP subscriber)
## [2026-06-10] prova-simulata | 2026-06-10-sim-04 — ordini produzione Python puro (gRPC multi-thread + lista+Condition + Flask)
## [2026-06-11] ingest | 02_JAVA_06-GRPC — Remote Procedure Call in Java (setup, API comparative Java/Python, Hello World)
## [2026-06-12] snippets | Creata wiki/snippets/ — 8 pagine boilerplate (proxy-skeleton py/java, gRPC py/java, STOMP, JMS, Flask, PyMongo) da slide + svolgimenti

## [2026-06-12] update | snippet grpc-python: sezione liste `repeated`
## [2026-06-12] ingest | 03_Service_Deployment_Containers — Container-based Virtualization and Services Deployment (Docker, Swarm, K8s, Namespaces, Cgroups)
## [2026-06-14] prova-simulata | 2026-06-14-sim-05 — prenotazione biglietti (Python Socket TCP proxy-skeleton + threading.Lock + Flask)

## [2026-06-15] prova-simulata | 2026-06-15-sim-06 — telemetria gateway (Java proxy-skeleton Socket TCP + skeleton ereditarietà, MOM STOMP/ActiveMQ, Python Channel Router subscriber + Flask Archive Server) — testo senza soluzione

## [2026-06-15] update | snippet proxy-skeleton-java: marshalling con DataInputStream/DataOutputStream (writeUTF/readUTF) al posto di PrintWriter/BufferedReader, conforme slide 22-java-networking

## [2026-06-15] update | snippet flask-boilerplate: sezione "abort — uso corretto" (guard clause, codici standard, make_response, errorhandler unico HTTPException)

## [2026-06-15] prova-simulata | 2026-06-15-sim-08 — smistamento pacchi (Java proxy-skeleton Socket TCP + skeleton ereditarietà, REST/Flask Python + MongoDB) — testo senza soluzione, no JMS/gRPC Java

## [2026-06-15] nuova-pagina | sottoscrizioni-durabili — gap segnalato dall'utente (non in slide raw): durable subscription STOMP (client-id + activemq.subscriptionName) e JMS (setClientID + createDurableSubscriber); aggiornati snippet stomp-python/jms-java, entità activemq, concetto jms, index

## [2026-06-16] update | snippet proxy-skeleton (py+java) — aggiunta variante trasporto UDP

## [2026-06-16] prova | sim-09 — Java puro: gRPC client/server + JMS producer/consumer asincrono (no Python)

## [2026-06-18] prova-simulata | 2026-06-18-sim-11 — bike-sharing (Python proxy-skeleton Socket TCP + skeleton ereditarietà, produttore/consumatore lista size 5, Flask + MongoDB) — testo senza soluzione

## [2026-06-19] update | docker-swarm: nuova sezione "Tolleranza ai guasti" — distinzione quorum Raft (manager) vs reschedule task (worker)

## [2026-06-19] estensione | MODULO 1 Concorrenza — riletto slide 10+11 (richiami concorrente + Python concurrency). Estese processo-thread (scheduler/context-switch 3 procedure/ULT-KLT/vantaggi), gil (vantaggi-svantaggi/GIL oggi 3.13-3.14), threading (Lock/RLock/Condition/Semaphore/Event/daemon/thread-local completi), multiprocessing (spawn-fork-forkserver/Pipe/Queue/Shared Memory). Create 4 nuove pagine: concorrenza-parallelismo (Amdahl), semaforo, monitor, produttore-consumatore. Aggiornato index.

## [2026-06-19] estensione | MODULO 3 MOM/pub-sub/JMS/durable — riletto slide 15 (Python MOM, 32pp). Estese: mom (comunicazione indiretta 4 forme group/shared-memory/code/pub-sub, aspetti chiave+disaccoppiamento spaziale/temporale, Observer→Notification Service con code, sistemi event-based SESAR/NASPI/FSE, AMQP/MQTT/STOMP dettaglio), pub-sub (meccanismo PTP ack vs Pub-Sub 0..N subscriber correnti, Observer 3 passi+inconvenienti), sottoscrizioni-durabili (allineata a slide 15 p.32: non-durable default, client-id=hostname, persistent=True — rimossa nota errata "non in slide"), entità activemq (multiprotocollo/administered objects, STOMP frame, porte 61613/62613 SSL, API stomp.py completa, transazioni begin/commit/abort). Aggiornato index. Fix contraddizione durable.

## [2026-06-19] canvas | container-mappa-esame — mappa completa container (virtualizzazione VM vs container, namespaces, cgroups, 2 pilastri, docker engine/immagini, dockerfile+CLI, compose, swarm tolleranza guasti, kubernetes CRI/OCI, domande esame) — 12 nodi, 15 edge

## [2026-06-19] estensione | MODULO 2 Middleware/RPC/gRPC/Protobuf — riletto slide 13 (Sistemi Middleware, 47pp) + 14 (Python RPC, 45pp). Creata pagina middleware (sistemi distribuiti Coulouris/Lamport, eterogeneità, EAI/COTS/legacy, glue technologies, 7 trasparenze, tassonomia RDA/TP/RPC/MOM/TS/DOM/CM/WS, DOM/ORB/IDL/Java RMI). Estese: rpc (estensione modello procedurale, ruolo stub, marshalling+external data rep CDR/XDR/protobuf/XML, semantica 4 tipi, Sun RPC port mapper 111/binding dinamico/dispatcher/TCP-UDP), protocol-buffers (Proxy-Skeleton, campi nome-valore, package), grpc (CNCF/scenari, HTTP/2 stream-message-frame, blocking/non-blocking, 4 tipi RPC+generator/yield, thread-safety+so_reuseport, errori, limitazioni gRPC-Web). Estesa entità grpc-python (streaming/thread-safety/errori). Aggiornato index.

## [2026-06-20] estensione | MODULO 4 Web Services/Persistenza — riletto slide 16 (Flask, 70pp) + 17 (NoSQL, 35pp). Estese: rest (Web Service W3C+servizi riusabili/componibili, entity-body req/resp, XML/JSON external data rep, RPC-style vs RESTful esteso, progettazione 4 passi, HTML/DOM cenni, OpenAPI/Swagger), flask (microframework WSGI wrapper Werkzeug+Jinja2, view function+tipi ritorno, dynamic routes+convertitori, route methods+shortcut get/post, server multi-thread default/threaded=False/host-port, request get_json/get_data/args, Response conversion logic+tuple+make_response+set_cookie, Jinja2 render_template/{{}}/{%%}, requests lib completa+r.json/raise_for_status, curl), nosql (Database/DBMS+features, ruolo back-end persistenza, relazionali schema/keys/entità/ACID+svantaggi big data/migrazione, NoSQL schema-free/orizzontale/BASE pro-contro), mongodb (cenni mongo shell, intro PyMongo driver ufficiale documents=dict). Aggiornati index (rest/nosql/flask).

## [2026-06-20] estensione | MODULO 5 Networking — riletto slide 12 (Python Networking, 54pp). Riscritta socket: Internet/ARPANET+rete di reti, stack ISO/OSI 7 livelli con incapsulamento (RPC=Sockets liv.5), IP/IPv6/DNS, IP datagram best-effort (max 65535B, corrotti/duplicati/persi), TCP (flusso byte full-duplex/connection-oriented/ritrasmissione) vs UDP (connectionless/datagramma/distingue porte), socket.socket family (AF_INET/INET6/UNIX/CAN/PACKET/RDS)+type (STREAM/DGRAM/RAW), funzioni socket/bind(porta 0=primo libero)/listen/accept→(conn,addr)/connect/close+wrapper syscall+socket inode strace, localhost vs 127.0.0.1 vs 0.0.0.0 wildcard, send/recv(TCP) vs sendto/recvfrom→(string,addr)(UDP), encode/decode utf-8, numero socket TCP=3/UDP=2, SERVER MULTITHREAD/MULTIPROCESS (socket non thread-safe: TCP conn-socket per thread; UDP socket condivisa, recvfrom solo nel main), link Proxy-Skeleton (slide 12 lo introduce → proxy-pattern), utility ip a/netstat -tulpn/ping. Aggiornato index.

## [2026-06-20] esame | percorso-orale — percorso di studio per orale in 7 tappe (ordinate per prerequisiti, non per indice PDF) da Domande_ACP_aggiornate.pdf (~120 domande, 7 aree). Incrocio domande↔wiki: copertura ~90%. Risposte ai 5 punti non coperti incluse nel file: selfish thread, static synchronized vs synchronized, JMS ReplyTo, GC Java vs reference counting Python, flusso gRPC↔MongoDB. Pandas/NumPy escluso (marcato 2024/2025 NO). Aggiornato index sezione Esame.

## [2026-06-20] estensione | MODULO Concorrenza Java — rilette slide 02_JAVA_01 (Multithreading, 38pp) + 02_JAVA_02 (Sincronizzazione, 38pp). Estesa java-threading: multithread a livello di linguaggio (vs pthread), perché 2 tecniche (no ereditarieta multipla), costruttore Thread(ThreadGroup,Runnable,String), modello memoria JVM (method-area/heap condivisi vs PC/JVM-stack per thread; statiche/istanza vs locali), context switch JVM <100 istruzioni, stati thread (tabella), scheduling (priorita 1-10/fixed-priority/FCFS/time-slicing/green threads/mapping piattaforma), selfish thread (yield/sleep), interruzione (interrupt/InterruptedException/interrupted vs isInterrupted/deprecati suspend-resume-stop), sleep/join, ThreadGroup. Estesa java-sincronizzazione: mutex per oggetto, metodi vs blocchi synchronized, static synchronized (lock classe vs istanza), coppia check+write corretta/non corretta, monitor Java (unica condition implicita), signal-and-continue vs Hoare, modello Entry-Set/Owner/Wait-Set, wait/notify cooperazione (while non if), Java 1.5 Lock/ReentrantLock/Semaphore. Verificati i 40 wikilink di percorso-orale (tutti validi); aggiornati gap selfish-thread e static-synchronized da \"non coperti\" a \"coperti\" con tabella stato copertura.

## [2026-06-20] estensione | polimorfismo — creata pagina concetto [[polimorfismo]]: nominale (Java, basato sulla classe + relazioni extends/implements dichiarate, statico/compile-time) vs strutturale/duck typing (Python, basato sulla struttura dell'oggetto, dinamico/runtime, no base comune necessaria). Forme Java (override/runtime, overload/compile-time, generics), tabella confronto (idoneita/quando/base comune/errore/dispatch/interfacce), ABC e typing.Protocol, collegamenti a Thread/run e stub gRPC. Linkata da ereditarieta (nota duck typing), oop (connessioni), index (sez. OOP) e percorso-orale Tappa 7.

## [2026-06-20] estensione | grpc — aggiunta glossa alla frase del professore "trattare le RPC come riferimenti a oggetti HTTP" (verificata testuale alla slide 14, riga 83 del PDF). Chiarito il meccanismo concreto: gRPC mappa ogni RPC su una risorsa HTTP/2 indirizzabile (endpoint /package.Service/Metodo, invocazione = POST HTTP/2, messaggi protobuf negli stream come frame binari). Marcatore 💡 Glossa + footer aggiornato.

## [2026-06-20] estensione | grpc — aggiunta sezione "Gerarchia HTTP/2 in dettaglio" (connessione→stream→message→frame con diagramma). Chiarita la trappola d'esame dei due significati di "header": frame header (prefisso 9 byte in ogni frame: Length/Type/Flags/Stream ID) vs frame HEADERS (tipo di frame che porta i campi header HTTP). Precisato che tutto è binario, header inclusi, compressi via HPACK (tabella statica+dinamica+Huffman). Message = frame HEADERS + frame DATA.

## [2026-06-21] estensione | MODULO JMS — riletta slide 02_JAVA_05-MOM-JMS (61pp). Estesa concetto [[jms]] con i blocchi finora mancanti (pp.22-61): JNDI in dettaglio (naming service/binding, Name/Binding/Reference/Context, Context API bind/rebind/lookup/unbind/rename, InitialContext, proprietà java.naming.factory.initial+provider.url, Service Provider plugin, prefisso queue./topic. non parte del nome JNDI); modello di programmazione generico a 8 passi (lookup CF→lookup Destination→Connection+start() solo consumer→Session→Producer/Consumer→Message→send/receive→cleanup); consumo sincrono (receive/receive(timeout)/receiveNoWait) vs asincrono (MessageListener+onMessage); struttura messaggio Header (JMSMessageID/CorrelationID/ReplyTo/Priority) + Properties (read-only se ricevuti, selettori SQL-like) + Body (5 tipi: Text/Map/Bytes/Stream/Object); acknowledgement 3 fasi + 3 modalità (AUTO/CLIENT a livello sessione/DUPS_OK lasco); sessioni transacted (createSession(true,0), commit/rollback con effetti PTP); concorrenza/thread-safety (solo Destination/ConnectionFactory/Connection; Session/Producer/Consumer no); persistenza PERSISTENT(default)/NON_PERSISTENT; interop JMS↔STOMP (content-length→Bytes/Text, durable via client-id+activemq.subscriptionName, physical-name). Aggiornata fonte [[24-java-jms]] (punti chiave 13-21, domande aperte risolte, +12 domande esame, argomenti). Aggiornato index. Coperti i punti del percorso-orale TAPPA 4 (transazioni/persistenza/durable + "conviene attivarli tutti? No, overhead").

## [2026-06-21] approfondimento | jms (servizio di naming) — espansa la teoria del naming service in [[jms]]: a cosa serve (livello di indirezione nome↔oggetto via binding, lookup per nome senza conoscere classe/locazione → trasparenza di locazione, disaccoppiamento client↔provider); architettura JNDI come API standard + SPI (Service Provider Interface): l'app usa solo la JNDI API, lo specifico naming service è un plugin Service Provider intercambiabile (ActiveMQ/LDAP/RMI/DNS/file system) — JNDI indipendente dal servizio reale, parallelo concettuale con l'Abstract Factory; ruolo delle due proprietà (factory.initial=classe del plugin SPI, provider.url=URL del servizio); tabella metodi Context; distinzione bind (lato admin/provider) vs lookup (lato client). Aggiornata fonte [[24-java-jms]] punto 13.

## [2026-06-21] estensione | rest + percorso-orale — aggiunta a [[rest]] la sottosezione "Web server vs Web service" (distinzione contenuti vs funzioni, relazione a livelli: Werkzeug=web server / view function=web service, tabella + nota esame). Ricontrollato [[percorso-orale]]: validati tutti i wikilink (nessuno rotto); TAPPA 5 estesa coi temi del MODULO 4 (web server vs service, Web Service W3C, safe/idempotente, POST vs PUT, stateless, 4 passi REST + URI best practice, OpenAPI, external data rep); TAPPA 4 estesa col naming service/JNDI (API+SPI/Abstract Factory, 8 passi, ReplyTo+CorrelationID, selettori SQL-like, 5 Body, ACK DUPS_OK); aggiornata tabella stato gap (ReplyTo ora voce-header in jms).

## [2026-06-21] estensione | middleware (traccia orale) — aggiunta a [[middleware]] la sezione "Traccia orale" che concilia definizione di middleware ↔ problema EAI ↔ scenario odierno (integrazione di componenti preesistenti) ↔ paradigma generale (heterogeneous distributed computing). Struttura in 5 passi: (1) definizione letta come "glue technology"/scopo=integrare; (2) paradigma generale (eterogeneità come norma); (3) EAI (evoluzione da sistemi esistenti, COTS/legacy, integrazione > sviluppo ex novo); (4) conciliazione (middleware = risposta diretta all'EAI; trasparenze come rovescio di ogni fonte di eterogeneità); (5) atterraggio su tassonomia/corso. Apertura e chiusura pronte. Linkata dalla TAPPA 2 del [[percorso-orale]].

## [2026-06-21] output | discorso-orale-rest — creato output/discorso-orale-rest.md: versione discorsiva (testo da parlare all'orale) che copre tutti i contenuti di [[rest]]. Sezioni: apertura (REST = stile architetturale, risorse vs procedure), cornice Web Service (def. W3C), web server vs web service, principi REST (risorsa/URI/URI template/interfaccia uniforme + safe/idempotente/stateless), REST su HTTP (entity-body), XML/JSON (testuale vs Protobuf binario), REST vs RPC, 4 passi progettazione + URI best practice, HTML/DOM + OpenAPI, chiusura (atterraggio su Flask/RPC/MOM nel corso) + promemoria domande frequenti.

## [2026-06-22] estensione + output | nosql — aggiunta a [[nosql]] la sottosezione "Scalabilità orizzontale e distribuzione su nodi" restando STRETTI alla fonte (PDF 17-NoSQL): relazionali = scalabilità verticale difficile (testuale "gestire le tabelle su differenti server è difficoltoso", server più potenti/costosi, schema rigido→no big data); NoSQL = orizzontale facile (testuale "distribuiti tra differenti nodi per migliorarne l'accessibilità", documenti indipendenti, no relazioni obbligatorie); connessione no-relazioni↔distribuibilità. Marcati esplicitamente come FUORI-FONTE (⚠️ TODO) sharding/replica-set/eventual-consistency/CAP/BASE — il PDF si ferma alla "distribuzione su nodi" e non li nomina; aggiunta nota † alla riga ACID/BASE della tabella confronto. Creato output/discorso-orale-nosql.md: traccia orale discorsiva da [[nosql]]+[[mongodb]] (apertura database/DBMS, back-end, relazionali schema/keys/ACID, svantaggi→NoSQL, tipologie, MongoDB gerarchia/_id/embedded, PyMongo, FOCUS scalabilità orizzontale, atomicità find_one_and_update vs TOCTOU, sezione finale "oltre la fonte" CAP/BASE/sharding/replica marcata come conoscenza esterna, promemoria domande). Nessuna modifica a raw/.

## [2026-06-22] lint | file md vuoti — rimosso orfano "legge di Amdahl.md" (root, 0 byte, untracked); corretto wikilink invertito in [[multiprocessing]] riga 120 ([[concorrenza-parallelismo]] → [[concorrenza-parallelismo]]) che generava il file vuoto. Amdahl già coperto in [[concorrenza-parallelismo]], nessuna pagina nuova. Verificato: nessun altro md vuoto fuori da .trash, nessun altro link invertito.

## [2026-06-23] riscrittura | java-threading — riscritta integralmente la pagina aderendo alla slide 02_JAVA_01-Multithreading-Java.pdf (38 slide). DISAMBIGUATA l'incoerenza JVM↔OS segnalata (context switch "fatto dalla JVM" slide 16 vs "thread del SO sottostante" slide 22): nuova sottosezione "Chi schedula davvero i thread? JVM vs sistema operativo" che separa il livello MODELLO/SPECIFICA (JVM: fixed-priority scheduling, 10 livelli, FCFS a pari priorità) dal livello ESECUZIONE CONCRETA (green threads = JVM multiplexa in user space, switch fatto dalla JVM; thread nativi 1:1 = scheduling+switch fatti dallo scheduler dell'OS, caso della maggior parte delle JVM moderne tipo HotSpot). Chiarito che la delega all'OS è ESATTAMENTE la ragione per cui le priorità sono solo un "suggerimento" e non garantiscono correttezza; aggiunta la tabella mapping JVM-priority→Linux nice/Windows priority (evidenziata la non-iniettività: 3&4→BELOW_NORMAL, 6&7→ABOVE_NORMAL, 8&9→HIGHEST). Coperte tutte le slide: due tecniche+no derivazione multipla, costruttore Thread, modello memoria JVM (tabella aree + frame=invocazione metodo), metodi (no exit), stati (diagramma+tabella Blocked/Interruptible), selfish thread (confronto NON time-slicing vs time-slicing, soluzione yield/sleep, round-robin deterministico), interruzione (interrupt/InterruptedException/interrupted reset vs isInterrupted/suspend-resume-stop deprecati+deadlock), sleep/join con esempi, ThreadGroup (default main). Nessuna modifica a raw/.

## [2026-06-25] esame | risposte-domande — creata wiki/esame/risposte-domande.md con risposte dettagliate a TUTTE le ~140 domande di raw/prove-esame/Domande_ACP_aggiornate.pdf, raggruppate per le 7 sezioni dell'originale (1 Middleware/MOM/JMS/STOMP, 2 gRPC/REST/Flask, 3 Concorrenza, 4 Python vs Java, 5 Virtualizzazione/Container, 6 Socket, 7 Database). Ogni risposta ancorata alle pagine wiki via [[link]] per verifica; segnalati esplicitamente i punti di inferenza o fuori-materiale (semantica RPC gRPC=at-most-once su TCP/HTTP/2, GC Java vs Python, aderenza Java alle Berkeley socket, replica ActiveMQ stateful, sharding/CAP/BASE, Pandas/NumPy sez.7.3 marcata [2024/2025 NO]→gap). Aggiornato wiki/index.md (sezione Esame). Nessuna modifica a raw/. Durante la sessione risposte a query: gRPC semantica RPC, MongoDB≠RDA (è DBMS, l'RDA-like è il driver/protocollo), XDR di PyMongo=BSON.
