---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc, grpc, mom, jms, protocol-buffers]
---

#flashcards/acp

## Definizione

La **trasparenza alla distribuzione** è la proprietà per cui il middleware nasconde la complessità della comunicazione distribuita al codice applicativo. In senso specifico, la **trasparenza dalle implementazioni commerciali** è la capacità di scrivere codice che funziona con qualsiasi provider/implementazione concreta del middleware senza modifiche.

## Spiegazione

### Cos'è la trasparenza

Il middleware si interpone tra applicazione e rete, astraendo: serializzazione, localizzazione del servizio, protocollo di trasporto, gestione della connessione. Il programmatore vede API locali — non socket raw.

Tre forme di trasparenza rilevanti nel corso:
- **Trasparenza di accesso**: chiamata remota identica a chiamata locale (RPC/gRPC — stub)
- **Trasparenza di locazione**: il client non conosce l'indirizzo fisico del server
- **Trasparenza dal provider**: il codice non dipende dal prodotto concreto (JMS + Abstract Factory)

### Meccanismo 1 — IDL + generazione codice (gRPC / RPC)

Il file `.proto` descrive il servizio in modo neutro rispetto al linguaggio e al prodotto. Stub e skeleton sono **generati automaticamente** — il codice applicativo chiama funzioni che sembrano locali:

```python
stub = helloworld_pb2_grpc.GreeterStub(channel)
response = stub.SayHello(helloworld_pb2.HelloRequest(name="World"))
# il codice non sa nulla del linguaggio/prodotto del server
```

La **trasparenza commerciale** è garantita dalla specifica del wire format: qualunque implementazione gRPC (Python, Java, Go, C++...) serializza protobuf su HTTP/2 in modo identico per specifica. Client Python + Server Java = compatibile per specifica, non per accordo tra vendor.

### Meccanismo 2 — API standard + Abstract Factory (JMS)

Il codice Java usa **solo** `javax.jms.*` — interfacce pure, nessun codice eseguibile. Il provider concreto (ActiveMQ, WebSphere MQ, TIBCO...) viene iniettato tramite **JNDI lookup**:

```java
ConnectionFactory factory = (ConnectionFactory) ctx.lookup("ConnectionFactory");
// il codice non sa e non deve sapere cosa c'è dietro
Queue queue = (Queue) ctx.lookup("myQueue");
QueueSender sender = session.createSender(queue);
```

Cambio provider = cambio configurazione JNDI, **zero modifiche al codice applicativo**. Pattern applicato: `javax.jms.*` = AbstractFactory + AbstractProduct; ActiveMQ = ConcreteFactory. Identica struttura al pattern Proxy/stub di [[rpc]], ma a livello di API Java invece che di wire protocol.

### Meccanismo 3 — Protocollo wire standard (STOMP / AMQP / MQTT)

Il client Python usa `stomp.py` e parla il protocollo **STOMP**. Il broker può essere ActiveMQ, RabbitMQ, Apollo — qualunque broker che rispetta la spec STOMP è intercambiabile:

```python
conn = stomp.Connection([("localhost", 61613)])
conn.send("/queue/ordini", "messaggio")
# funziona con qualsiasi broker STOMP-compatibile — senza toccare il codice
```

Il codice client non contiene riferimento al prodotto concreto, solo all'indirizzo host:port.

### Specifica vs implementazione — i middleware del corso

| Middleware | Tipo | Dettaglio |
|---|---|---|
| **RPC** (paradigma) | paradigma teorico | concetto architetturale, non prodotto |
| **gRPC** | specifica aperta + impl di riferimento | spec Google/CNCF open source; impl: grpcio, grpc-java, grpc-go — intercambiabili |
| **Protocol Buffers** | specifica aperta + impl di riferimento | spec Google open source; impl in ogni linguaggio |
| **JMS** (JSR 914) | **pura specifica** | solo interfacce `javax.jms.*`; zero codice eseguibile; impl: ActiveMQ, WebSphere MQ, TIBCO EMS... |
| **Apache ActiveMQ** | **pura implementazione** | prodotto concreto; implementa JMS + STOMP + AMQP + MQTT simultaneamente |
| **STOMP** | specifica (protocollo wire) | documento pubblico; impl: ActiveMQ, RabbitMQ, Artemis... |
| **AMQP** | standard ISO/IEC 19464 | spec formale; impl: RabbitMQ, IBM MQ, ActiveMQ Artemis... |
| **MQTT** | standard ISO/IEC 20922 | spec formale; impl: Mosquitto, HiveMQ, ActiveMQ... |

**JMS** è il caso più puro: è una specifica senza alcuna implementazione propria — non esiste un "runtime JMS" autonomo. Tutti gli altri sono spec con impl di riferimento. **ActiveMQ** è l'unico puro prodotto nel corso.

> 🎯 Esame: "Come JMS garantisce trasparenza dal provider?" → Abstract Factory + JNDI lookup; codice dipende solo da `javax.jms.*`. "Come gRPC garantisce interoperabilità tra linguaggi?" → wire format identico per specifica (protobuf su HTTP/2); codice generato da IDL uguale per tutti i linguaggi.

Come JMS garantisce trasparenza dal provider e gRPC l'interoperabilità tra linguaggi?
?
JMS: Abstract Factory + JNDI lookup, il codice dipende solo da javax.jms.*. gRPC: wire format identico per specifica (protobuf su HTTP/2) e codice generato dall'IDL uguale per ogni linguaggio.


> 💡 Connessione: stub/skeleton di [[rpc]] e Abstract Factory di [[jms]] perseguono lo stesso obiettivo con tecniche diverse — separare codice applicativo dai dettagli di comunicazione. Il risultato è identico: cambio provider = cambio config, non cambio codice.

## Perché importa

La trasparenza è il valore fondamentale del middleware: senza di essa non ci sarebbe differenza tra usare il middleware e scrivere socket raw. Capire quale parte è specifica (interfaccia stabile, portabile) e quale è implementazione (prodotto sostituibile) permette di valutare la portabilità del codice e il rischio di vendor lock-in.

## Connessioni

- [[rpc]] — meccanismo stub/skeleton come forma di trasparenza di accesso
- [[grpc]] — implementazione gRPC; specifica aperta, intercambiabile tra linguaggi
- [[grpc-python]] — binding Python di gRPC (grpcio, grpcio-tools)
- [[protocol-buffers]] — IDL e wire format che garantisce interoperabilità gRPC
- [[jms]] — specifica Java pura; caso paradigmatico di trasparenza via Abstract Factory + JNDI
- [[mom]] — classe di middleware asincroni; trasparenza garantita dai protocolli wire
- [[activemq]] — implementazione broker MOM che implementa più spec (JMS, STOMP, AMQP, MQTT)
- [[pub-sub]] — modello di messaging del MOM, trasparente dal broker via protocollo wire

## Fonti

- [[13-sistemi-middleware]]
- [[14-python-rpc-grpc]]
- [[15-python-mom]]
- [[24-java-jms]]

_Aggiornato: 2026-06-06 — pagina creata da query su trasparenza middleware e specifica vs implementazione_
