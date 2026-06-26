---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc, socket]
---

#flashcards/acp

## Definizione

Il **Message-Oriented Middleware (MOM)** è uno strato software che permette la comunicazione **asincrona** tra applicazioni distribuite tramite un **message broker**. Il broker riceve, conserva e consegna messaggi, disaccoppiando sender e receiver nello spazio e nel tempo.

## Spiegazione

**Motivazione**: i MOM sono di solito usati per **rimpiazzare** i sistemi basati sul paradigma [[rpc]].
- le chiamate RPC sono **sincrone** → problemi di **scalabilità**; le richieste RPC arretrate rallentano l'intero sistema → soluzione: un **meccanismo asincrono** per aumentare la scalabilità;
- servono per sistemi con **high availability** e **scalability**: il sistema deve restare funzionante anche dopo il fallimento di uno o più server → soluzione: con i **broker** ci si può spostare da un server all'altro in caso di fallimento.

### Comunicazione indiretta

La **comunicazione indiretta** è la comunicazione tra entità di un sistema distribuito tramite un **intermediario**, **senza accoppiamento diretto** tra sender e receiver. La "natura" dell'intermediario dipende dall'approccio:

| Approccio | Astrazione | Cardinalità |
|---|---|---|
| **Group communication** | gruppo: un messaggio è mandato a un gruppo e recapitato ai membri | uno-a-gruppo |
| **Shared memory** | *distributed shared memory*, **tuple space** (vedi TS in [[middleware]]) | condivisa |
| **Code di messaggi** | coda: il sender inserisce, **un solo** receiver rimuove (point-to-point) | uno-a-uno |
| **Publish-subscribe** | il publisher genera messaggi, il subscriber esprime interesse per un tipo | **uno-a-molti** |

Le soluzioni middleware basate su **code** o su **publish-subscribe** sono note come **Message-Oriented Middleware (MOM)**; i sistemi pub-sub sono anche detti **distributed event-based systems**.

**Architettura MOM**:
```
[Applicazione X] → API → [Message Broker (MOM)] → API → [Applicazione Y]
```

Il MOM gioca il ruolo di **intermediario (message broker)** nella comunicazione indiretta basata su messaggi: garantisce lo scambio con tecniche di **store-and-forward** e solleva il programmatore dai dettagli di basso livello (RPC, protocolli di rete), esponendo una **API di alto livello** con primitive **send/receive message**.

**Aspetti chiave di un MOM**:
- recapita il messaggio all'applicazione B, che può **risiedere su una macchina diversa** da A;
- **gestisce la comunicazione tramite rete**: può conservare il messaggio finché la rete diventa disponibile, poi lo inoltra (**store-and-forward**);
- B potrebbe **non essere in esecuzione** quando A invia: il MOM **conserva** il messaggio finché B diventa disponibile, e **A non si blocca** in attesa (comunicazione **asincrona**).

**Proprietà di disaccoppiamento** — i MOM forniscono integrazione **flessibile e disaccoppiata**:
1. **Disaccoppiamento spaziale**: il sender **non conosce** (né ha bisogno di conoscere) l'identità del receiver e viceversa → i partecipanti possono essere sostituiti, migrati, aggiornati;
2. **Disaccoppiamento temporale**: sender e receiver possono avere **cicli di vita differenti** → non devono necessariamente essere in esecuzione allo stesso tempo per comunicare.

**Domini di messaging**:

**PTP (Point-to-Point)**:
- Astrazione: **coda** (queue)
- Ogni messaggio ha **un solo consumer**
- Il messaggio persiste finché non viene consumato o scaduto
- Il consumer invia **ACK** alla corretta ricezione
```
Producer → [Queue] → Consumer (uno solo)
```

**Publish-Subscribe (Pub-Sub)**:
- Astrazione: **topic**
- I publisher pubblicano messaggi su un topic
- I subscriber si iscrivono a topic di interesse
- Ogni messaggio può essere ricevuto da **N subscriber**
- Il topic conserva il messaggio finché non è stato consegnato a tutti i subscriber correnti
```
Publisher → [Topic] → Subscriber 1
                   → Subscriber 2
                   → Subscriber N
```

**Evento e Notifica** — la comunicazione indiretta è molto usata per la **propagazione (dissemination) di eventi**:
- **Evento**: condizione rilevata da/in un'applicazione, comunicata all'intermediario (il MOM) sotto forma di messaggio;
- **Notifica**: atto di informare un insieme di applicazioni dell'occorrenza dell'evento.

L'approccio evento-notifica richiama il pattern **Observer**: ① l'observer dichiara interesse agli eventi del subject tramite una **sottoscrizione**; ② il subject rileva l'occorrenza di un evento; ③ il subject **notifica** gli osservatori invocandone un'apposita funzione.

**Dall'Observer al Notification Service** — l'Observer riduce l'accoppiamento e supporta la comunicazione **uno-a-molti**, ma ha inconvenienti: il subject deve mantenere una **lista di observer** e relative sottoscrizioni, è **responsabile di notificarli** (scarsa scalabilità) e **gli observer devono conoscere il subject**. Per risolverli, la responsabilità di gestire osservatori/sottoscrizioni e di notificarli è delegata a una terza entità detta **Notification Service (NS)** — il broker. Importante: il **pub-sub non è l'unico modello** per i sistemi event-based; un NS può anche usare **code di messaggi** (il sender, all'occorrenza di un evento, inserisce il messaggio in una coda; il messaggio viene recapitato ai receiver sottoscritti alla coda).

**Sistemi event-based nell'industria**: SESAR (controllo traffico aereo Europa), NASPI (monitoraggio rete elettrica Nord America), FSE (fascicolo sanitario elettronico).

**Protocolli di messaging dei broker MOM**:
- **AMQP** (Advanced Message Queuing Protocol): protocollo **binario wire-level**, progettato per **rimpiazzare** middleware di messaggistica proprietari e per l'**interoperabilità tra fornitori diversi**; ancora molto popolare;
- **MQTT** (Message Queuing Telemetry Transport): protocollo **publish-subscribe leggero**, standard **ISO** (ISO/IEC PRF 20922), su **TCP/IP**; progettato per **basso consumo energetico e banda limitata** (scenari fog/edge computing, IoT);
- **STOMP** (Simple/Streaming Text Oriented Message Protocol): protocollo **testuale**, semplice, pensato per i MOM; fornisce un formato **wire-level** che consente ai client STOMP di parlare con **qualsiasi broker** che supporti il protocollo.

> 🎯 Esame: Differenza PTP vs Pub-Sub, disaccoppiamento spaziale/temporale, perché MOM rimpiazza RPC per scalabilità/availability, le 4 forme di comunicazione indiretta, AMQP/MQTT/STOMP (binario/leggero-IoT/testuale).

Differenza PTP vs Pub-Sub e perché il MOM rimpiazza l'RPC?
?
PTP (queue): un consumer per messaggio. Pub-Sub (topic): N subscriber. Il MOM è asincrono → disaccoppiamento spaziale/temporale, scalabilità e availability. Protocolli: AMQP (binario), MQTT (leggero/IoT), STOMP (testuale).


## Perché importa

MOM è usato in sistemi ad alta scala e alta disponibilità (SESAR, NASPI, FSE). Il corso usa ActiveMQ + STOMP come implementazione concreta.

## Connessioni

- [[pub-sub]] — modello di messaging del MOM
- [[rpc]] — alternativa sincrona al MOM
- [[socket]] — il broker comunica via socket TCP
- [[activemq]] — broker MOM open-source usato nel corso (STOMP, AMQP, MQTT)
- [[middleware]] — il MOM è un middleware orientato alla comunicazione; comunicazione indiretta e tuple space (TS)
- [[middleware-trasparenza]] — STOMP/AMQP/JMS come meccanismi di indipendenza dal provider
- [[sottoscrizioni-durabili]] — disaccoppiamento temporale esteso ai topic

## Fonti

- [[15-python-mom]]
- [[13-sistemi-middleware]]

_Aggiornato: 2026-06-19 — estensione MODULO 3 (slide 15): comunicazione indiretta (4 forme: group/shared memory/code/pub-sub), aspetti chiave + disaccoppiamento spaziale/temporale dettaglio, Observer→Notification Service (NS può usare code), sistemi event-based industria, protocolli AMQP/MQTT/STOMP in dettaglio_
