---
tipo: esame
titolo: Percorso di studio per l'orale
data: 2026-06-20
fonte: raw/prove-esame/Domande_ACP_aggiornate.pdf
---

# Percorso di studio — Orale ACP

Costruito sulle **domande che il professore fa più spesso all'orale**
(`raw/prove-esame/Domande_ACP_aggiornate.pdf`, ~120 domande in 7 aree).

L'ordine **non segue l'indice del PDF** ma i **prerequisiti concettuali**: il prof
concatena le domande seguendo le dipendenze (thread → GIL → multiprocess → IPC;
middleware → RPC → gRPC; MOM → JMS → STOMP). Studiare in quest'ordine fa sì che ogni
tappa regga la successiva.

> 🎯 Esame: le risposte ai **punti non coperti dal wiki** sono in fondo a questo file
> (sezione "Punti non coperti — risposte"), non sparse nelle pagine.

---

## TAPPA 1 — Concorrenza e Parallelismo (fondamento trasversale)

*Area 3 PDF. Il prof parte quasi sempre da qui. Ritorna dentro gRPC, Container, Java.*

**Pagine:** [[processo-thread]] → [[concorrenza-parallelismo]] → [[gil]] → [[threading]]
→ [[multiprocessing]] → [[semaforo]] → [[monitor]] → [[produttore-consumatore]]
**Java:** [[java-threading]] → [[java-sincronizzazione]]

**Domande coperte:** processi vs thread · CPU-bound vs I/O-bound · GIL e implicazioni ·
"se ho multithreading perché multiprocess?" (GIL in pratica) · 3 modi per creare un
processo + portabilità · IPC (Pipe/Queue/Event/SharedMemory) · RLock e deadlock ·
monitor Java signal-and-continue + limite (unica condition implicita) · Lock vs
ReentrantLock · semafori Java (acquire/release/tryAcquire) · stati del thread Java ·
confronto sincronizzazione Python↔Java · Thread User Level.

> ✅ Ora coperti (espansi il 2026-06-20): **Selfish Thread** in [[java-threading]] · **`static synchronized` vs `synchronized`** in [[java-sincronizzazione]]. Sintesi anche sotto.

---

## TAPPA 2 — Middleware e RPC (fondamento per gRPC e JMS)

*Area 1.1 + 2.1. Concetti astratti che il prof usa come "cappello" prima di gRPC/JMS.*

**Pagine:** [[middleware]] → [[middleware-trasparenza]] → [[rpc]] → [[proxy-pattern]]

**Domande coperte:** tipi/vantaggi middleware · 7 trasparenze · trasparenza ai guasti ·
modelli (MOM/RPC-RMI/Tuple Space/DOM) · marshalling/unmarshalling + big/little-endian
(CDR/XDR) · semantiche RPC (4 tipi) · "RPC con MOM e viceversa?" · pattern
Proxy/Skeleton: perché + delega vs ereditarietà (accoppiamento).

> 🎯 Domanda di cornice: **conciliare definizione di middleware ↔ EAI ↔ scenario odierno
> (integrare componenti preesistenti) ↔ paradigma generale (heterogeneous distributed
> computing)** → traccia di discorso completa in [[middleware]] (sezione "Traccia orale":
> 5 passi + apertura/chiusura pronte, trasparenze come rovescio dell'eterogeneità).

---

## TAPPA 3 — gRPC e Protocol Buffers

*Area 2.2. Istanza concreta di RPC: si appoggia a Tappa 2.*

**Pagine:** [[protocol-buffers]] → [[grpc]] → [[grpc-python]] / [[grpc-java]]
→ [[gestione-errori-api]]

**Domande coperte:** serializzazione Protobuf + deserializzazione/riconoscimento campi
(field tag) · HTTP/2 (stream/message/frame) · perché non UDP · streaming + yield/generator
+ perché meno overhead di N chiamate (stack frame) · Status eccezioni (UNKNOWN) ·
generazione stub Java/Python da `.proto` · server gRPC multiprocesso (so_reuseport) ·
gRPC↔Flask interop · esporre gRPC come REST.

> ⚠️ Taglio debole: **gRPC↔MongoDB (flusso)** → vedi sotto.

---

## TAPPA 4 — JMS, STOMP e ActiveMQ

*Area 1.2 + 1.3. Si appoggia a Tappa 2 (MOM come modello di middleware).*

**Pagine:** [[mom]] → [[pub-sub]] → [[sottoscrizioni-durabili]] → [[jms]] → [[activemq]]

**Domande coperte:** JMS in generale (JNDI/Context/ConnectionFactory/Administered Objects,
Session single-thread) · **naming service / JNDI** (livello di indirezione nome↔oggetto via
binding; JNDI come **API standard + SPI**, naming service reale = plugin Service Provider
intercambiabile, parallelo con Abstract Factory; `factory.initial`/`provider.url`;
bind lato admin vs lookup lato client) · modello di programmazione a 8 passi · perché serve
un provider · struttura messaggio (Header/Proprietà/Body, 5 tipi di Body) · selettori SQL-like
· `JMSReplyTo`/`JMSCorrelationID` (request-reply su MOM) · cosa è thread-safe · priorità via
thread · fault tolerance (transazioni/persistenza/durable + "conviene attivarli tutti? No,
overhead") · domini Queue/Topic · durable subscriber · ricezione async (MessageListener) vs
sync (receive/receiveNoWait/timeout) · ACK (AUTO/CLIENT/DUPS_OK) · transazioni
(commit/rollback, SESSION_TRANSACTED) · STOMP + MyListener · interop JMS↔STOMP via broker ·
header STOMP vs `getJMSProperty()` · limiti STOMP.

> ✅ `ReplyTo` ora in [[jms]] (Header del messaggio); la trattazione completa del pattern
> **request-reply su MOM** (coda temporanea + CorrelationID) resta nella sezione qui sotto.

---

## TAPPA 5 — REST, Flask e Networking Socket

*Aree 2.3 + 6. Accorpate: condividono Proxy/Skeleton (Tappa 2) e il tema serializzazione.*

**Pagine:** [[rest]] → [[flask]] → [[socket]] (+ ripasso [[proxy-pattern]])

**Domande coperte:** **web server vs web service** (server = serve contenuti a un browser;
service = espone funzioni invocabili da altri programmi) · Web Service (def. W3C) ·
servizio riusabile/componibile · REST API · `@app.route` · convenzioni metodi HTTP come
discriminante · semantica GET/POST/PUT/DELETE · **safe vs idempotente** · **POST vs PUT**
(figlia vs URI esatto) · **stateless / no sessione** · entity-body req/resp per metodo ·
external data representation (XML/JSON testuali vs Protobuf binario) · RPC-style vs RESTful
(vocabolario custom vs fisso) · **4 passi di progettazione REST** + URI best practice (nomi
non verbi) · OpenAPI/Swagger · perché dict/list (JSON nativo) · gap semantico JSON↔RPC
· mapping porte/repliche · come esporre gRPC come REST · TCP vs UDP · UDP pacchetto unico +
separatore · Proxy/Skeleton TCP vs UDP · `bind()` vs `connect()` · Java aderisce a Berkeley
socket? · RPC su UDP (poco pratico) · UDP multithread (cosa passare al thread).

> ✅ Aggiunto il 2026-06-21: sottosezione **"Web server vs Web service"** in [[rest]]
> (distinzione, relazione a livelli — Werkzeug = web server / view function = web service, tabella).

---

## TAPPA 6 — Container e Docker

*Area 5. Si appoggia a Tappa 1 (namespace/cgroups = isolamento processi) e Tappa 4 (replica ActiveMQ).*

**Pagine:** [[virtualizzazione-container]] → [[linux-namespaces]] → [[cgroups]] →
[[docker]] → [[docker-compose]] → [[docker-swarm]] → [[kubernetes]]

**Domande coperte:** app distribuita con virtualizzazione · comunicazione tra container +
problema replica ActiveMQ (namespace) · immagine = base del container · disco VM = file su
host · perché container > VM (kernel condiviso, boot = fork) · namespace net/mnt · cgroups
(limitare CPU/memoria/banda) · layer fs + layer scrivibile temporaneo · Dockerfile/Compose ·
Entrypoint/Command · Swarm (ruoli nodi, stato desiderato) · overhead container · svantaggi
system call.

---

## TAPPA 7 — Database + Python vs Java (i due "leggeri")

*Aree 7 + 4. Brevi, per ultimi perché riusano tutto il resto.*

**Pagine:** [[nosql]] → [[mongodb]] · [[oop]] → [[ereditarieta]] → [[polimorfismo]] → [[scope]] → [[eccezioni]]

**Domande coperte:** SQL vs NoSQL · MongoDB + tipi DB non relazionali · OOP Python vs Java ·
`self` · polimorfismo · interfacce e generazione codice (da gRPC) · eccezioni
try/except/else/finally + custom + raise · performance JIT-Java vs GIL-Python.

> 📌 Pandas/NumPy (7.3 PDF) è marcato **[2024/2025 NO]** → **escluso**, non studiarlo.
> ⚠️ Taglio debole: **GC Java vs reference counting Python** → vedi sotto.

---

# Punti non coperti — risposte

Risposte ai gap emersi dall'incrocio domande↔wiki. **Stato copertura:**

| Punto | Stato | Pagina dedicata |
|---|---|---|
| Selfish Thread | ✅ coperto (2026-06-20) | [[java-threading]] |
| `static synchronized` vs `synchronized` | ✅ coperto (2026-06-20) | [[java-sincronizzazione]] |
| JMS ReplyTo | 🟡 voce-header in [[jms]]; pattern request-reply solo qui | [[jms]] (riga Header) |
| GC Java vs Python | ⚠️ solo qui; reference counting accennato in [[gil]] | [[gil]] |
| gRPC↔MongoDB (flusso) | ⚠️ flusso solo qui; mapping errori in [[gestione-errori-api]] | [[gestione-errori-api]] |

Le sintesi qui sotto restano come ripasso rapido; per i primi due punti la trattazione completa è ora nelle pagine dedicate.

## 1. Selfish Thread (Tappa 1) — trattazione completa in [[java-threading]]

Un **selfish thread** ("thread egoista") è un thread **CPU-bound** che, una volta ottenuto
il controllo dell'esecuzione, **non lo cede volontariamente**: non fa operazioni di I/O e
non si blocca mai, quindi monopolizza la CPU.

- **Problema:** in uno scheduling **cooperativo** (in cui un thread cede solo
  volontariamente) un selfish thread affamerebbe tutti gli altri → *starvation*
  (→ [[semaforo]]). La soluzione è uno scheduling **preemptive** a divisione di tempo, che
  toglie forzatamente la CPU al thread allo scadere del quanto.
- **In Python / GIL:** un selfish thread terrebbe il **GIL** all'infinito. CPython lo evita
  forzando il **rilascio periodico** del GIL anche per i thread puramente CPU-bound:
  - vecchio meccanismo (< 3.2): rilascio ogni N istruzioni bytecode (*check interval*);
  - moderno (≥ 3.2): rilascio a **timeout temporale** (default **5 ms**, configurabile con
    `sys.setswitchinterval()`).
  → collega a [[gil]] (rilascio periodico) e [[threading]].

> 🎯 Esame: il prof lega "Selfish Thread" alla domanda *"perché serve il multiprocess se ho
> i thread?"* — un selfish thread mostra che il threading Python non dà parallelismo reale
> su CPU-bound: i thread si **alternano** (concorrenza), non girano insieme.

## 2. `static synchronized` vs `synchronized` (Tappa 1, Java) — trattazione completa in [[java-sincronizzazione]]

In Java `synchronized` acquisisce un **monitor**, ma su oggetti diversi a seconda del tipo:

| Metodo | Lock acquisito | Granularità |
|---|---|---|
| `synchronized` (istanza) | lock sull'**oggetto** (`this`) | uno per istanza |
| `static synchronized` | lock sull'oggetto **`Class`** (`NomeClasse.class`) | uno per classe |

**Conseguenza chiave (la domanda del prof):** un thread dentro un metodo `synchronized` di
istanza e un altro thread dentro un metodo `static synchronized` della **stessa classe**
**NON si bloccano a vicenda** → procedono in parallelo, perché competono su **due monitor
diversi** (l'istanza vs l'oggetto `Class`).

- Due thread su metodi `static synchronized` della stessa classe → si escludono (stesso lock di classe).
- Due thread su metodi `synchronized` di istanza dello **stesso oggetto** → si escludono.
- Due thread su metodi `synchronized` di istanza di **oggetti diversi** → non si escludono.

→ collega a [[java-sincronizzazione]] (monitor, `synchronized`).

## 3. JMS `ReplyTo` (Tappa 4)

`JMSReplyTo` è un **campo dell'header** di un messaggio JMS che contiene una **Destination**
(una `Queue` o un `Topic`) dove il **ricevente deve inviare la risposta**. È il modo in cui
JMS implementa il pattern **request-reply** (semantica RPC-style) sopra un middleware che di
per sé è **asincrono e one-way**.

Flusso tipico:
1. Il mittente crea una destinazione di risposta (spesso una **coda temporanea**:
   `session.createTemporaryQueue()`).
2. La imposta sul messaggio: `message.setJMSReplyTo(tempQueue)` e di solito imposta anche un
   `JMSCorrelationID` per correlare richiesta e risposta.
3. Il consumatore legge `message.getJMSReplyTo()` e invia il reply su quella destinazione,
   riportando il `CorrelationID`.

→ collega a [[jms]] e alla domanda *"è possibile un middleware RPC con MOM?"* (→ [[mom]],
[[middleware-trasparenza]]): `ReplyTo` è esattamente il meccanismo che permette RPC sopra MOM.

## 4. GC Java vs reference counting Python (Tappa 7)

| Aspetto | Python (CPython) | Java (JVM) |
|---|---|---|
| Meccanismo primario | **Reference counting**: ogni oggetto ha un contatore; a 0 → dealloc **immediata** (deterministica) | **Tracing GC generazionale** (young/old gen): nessun contatore |
| Cicli di riferimento | refcount NON li cattura → GC ciclico secondario (`gc`, generazionale, 3 generazioni) | gestiti nativamente dal tracing |
| Determinismo | deallocazione immediata, bassa latenza | non deterministica (quando gira il GC) |
| Costo | overhead a ogni assegnazione + il **GIL** serve a proteggere i contatori | possibili pause *stop-the-world*, mitigate da G1/ZGC |

> 💡 Connessione: il reference counting è **la ragione d'essere del GIL** (→ [[gil]]):
> senza un lock globale, due thread potrebbero corrompere i contatori. Questo è il link che
> il prof cerca tra "GC" e "GIL" e "performance Python vs Java".

## 5. gRPC ↔ MongoDB — flusso (Tappa 3)

gRPC e MongoDB **non comunicano direttamente**: gRPC è il protocollo RPC verso il client,
MongoDB è il **back-end di persistenza**. È il **server gRPC** a fare da ponte, usando il
driver **PyMongo** dentro il metodo del servizio.

Flusso completo:
1. Client → chiamata gRPC con messaggio **Protobuf**.
2. Server **deserializza** il messaggio → estrae i campi.
3. Costruisce un **documento** (dict Python) → `collection.insert_one(doc)` /
   `collection.find(...)` su MongoDB (PyMongo converte dict ↔ **BSON**).
4. Risultato (dict) → ricostruisce il **messaggio Protobuf** di risposta → serializza → client.

**Punto chiave (il taglio del prof):** la catena di **conversioni**
`Protobuf message ↔ dict Python ↔ BSON document`. Gli errori PyMongo si mappano su
`grpc.StatusCode` tramite il `context` (→ [[gestione-errori-api]]).

---

_Aggiornato: 2026-06-20 — creazione percorso orale da Domande_ACP_aggiornate.pdf, con risposte ai 5 punti non coperti_
_Aggiornato: 2026-06-21 — TAPPA 5 estesa (web server vs web service, Web Service W3C, safe/idempotente, POST vs PUT, stateless, 4 passi REST, OpenAPI); TAPPA 4 estesa (naming service/JNDI API+SPI, 8 passi, ReplyTo, selettori, 5 Body, ACK DUPS_OK); aggiornata tabella stato gap (ReplyTo ora in jms)_
_Aggiornato: 2026-06-21 — TAPPA 2: link alla "Traccia orale" di [[middleware]] (conciliazione definizione↔EAI↔heterogeneous distributed computing)_
