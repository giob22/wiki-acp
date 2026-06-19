---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc, protocol-buffers, socket]
---

## Definizione

**gRPC** è un middleware RPC **universale, ad alte prestazioni e open source** sviluppato da Google e oggi progetto della **Cloud Native Computing Foundation (CNCF)**. Usa **HTTP/2** come trasporto e **Protocol Buffers** come formato di serializzazione e IDL. È un framework **multilinguaggio e multipiattaforma**: può essere eseguito in qualsiasi ambiente. Supporta streaming bidirezionale e interoperabilità tra linguaggi diversi.

## Spiegazione

### Scenari d'uso e diffusione

Principali scenari: collegare **microservizi poliglotti** con stile richiesta-risposta; connettere **dispositivi mobili** e browser ai servizi di backend; generare **librerie client efficienti**. È usato da molte aziende e sistemi distribuiti (Google, Dropbox, Netflix, Square, etcd, CockroachDB).

### Caratteristiche principali

- **HTTP/2** per il trasporto (streaming bidirezionale e multiplexing);
- **Protocol Buffers** come IDL → generazione automatica del codice; i **contratti rigorosi** definiti nei `.proto` **prevengono gli errori**;
- supporto integrato per **autenticazione**, **streaming bidirezionale** e **controllo di flusso**;
- supporto sia per comunicazione **bloccante** sia **non bloccante**:
  - *blocking/synchronous stub* → il chiamante attende che il server risponda; ritorna la risposta o solleva un'eccezione;
  - *non-blocking/asynchronous stub* → il chiamante non attende, la risposta arriva in modo asincrono.

### Perché HTTP/2: "RPC come riferimenti a oggetti HTTP"

L'idea di base di gRPC è **trattare le RPC come riferimenti a oggetti HTTP**, trasportando dati e richieste su **HTTP/2**, importante revisione di HTTP che dà vantaggi prestazionali rispetto a HTTP 1.x:
- **Binary Framing Layer**: richieste/risposte sono suddivise in **messaggi di piccole dimensioni** con frame in **formato binario**, rendendo efficiente la trasmissione;
- **gerarchia stream → message → frame**:
  - **Stream**: flusso bidirezionale di byte dentro una connessione stabilita, può trasportare uno o più messaggi;
  - **Message**: sequenza completa di frame corrispondente a una richiesta o risposta logica;
  - **Frame**: la più piccola unità di comunicazione in HTTP/2; ogni frame ha un'intestazione che identifica lo stream a cui appartiene;
- **Multiplexing richiesta/risposta**: una singola connessione TCP per client → uso efficiente delle connessioni, evita il blocco *head-of-line* a livello HTTP;
- **streaming bidirezionale nativo**;
- **compressione dell'intestazione** HTTP per ridurre l'overhead.

**Vantaggi di HTTP/2 su HTTP/1.1** (in sintesi):
- **Multiplexing**: più richieste/risposte sulla stessa connessione TCP
- **Header compression**: riduce overhead
- **Server push**: il server può inviare dati senza richiesta esplicita
- **Binario**: frame binari, non testuale

**Workflow gRPC — 4 passi**:

1. **Installazione**:
   ```bash
   pip install grpcio grpcio-tools
   ```

2. **Definire il servizio** in `.proto`:
   ```protobuf
   syntax = "proto3";
   package helloworld;
   
   service Greeter {
       rpc SayHello (HelloRequest) returns (HelloReply) {}
   }
   message HelloRequest { string name = 1; }
   message HelloReply { string message = 1; }
   ```

3. **Compilare** il `.proto`:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. \
       --grpc_python_out=. helloworld.proto
   ```
   Genera:
   - `helloworld_pb2.py` — classi messaggi; usate per **serializzare/deserializzare**
   - `helloworld_pb2_grpc.py` — classi stub (client) e servicer/skeleton (server)

4. **Implementare server**:
   ```python
   import grpc
   import helloworld_pb2, helloworld_pb2_grpc
   from concurrent import futures
   
   class Greeter(helloworld_pb2_grpc.GreeterServicer):
       def SayHello(self, request, context):
           return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")
   
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
   server.add_insecure_port("[::]:50051")
   server.start()
   server.wait_for_termination()
   ```

   **Implementare client**:
   ```python
   channel = grpc.insecure_channel("localhost:50051")
   stub = helloworld_pb2_grpc.GreeterStub(channel)
   response = stub.SayHello(helloworld_pb2.HelloRequest(name="World"))
   print(response.message)  # → "Hello, World!"
   ```

**Workflow runtime** (dettaglio):
1. Client chiama metodo sullo stub (come se fosse locale)
2. Stub serializza i parametri con protobuf
3. Invia messaggio via HTTP/2 (formato: Tag|Value|Tag|Value|...|0)
4. Server riceve, skeleton deserializza
5. Skeleton chiama la funzione reale nel server
6. Risultato percorre il path inverso

**Nota su `package`**: in Python è **ignorata** (moduli organizzati per filesystem). In **Java non è ignorata** — determina il package Java delle classi generate (sovrascrivibile con `option java_package`).

> 🎯 Esame: I 4 passi del workflow gRPC, cosa contengono `_pb2.py` e `_pb2_grpc.py`, come funziona una chiamata end-to-end.

### I 4 tipi di RPC call in gRPC

gRPC supporta **quattro tipi** di chiamata, distinti nel `.proto` dalla presenza della keyword `stream` su richiesta e/o risposta. gRPC **garantisce l'ordinamento dei messaggi** all'interno di una singola chiamata RPC.

| Tipo | `.proto` | Comportamento |
|---|---|---|
| **Unary** (semplice) | `rpc SayHello (Req) returns (Reply)` | richiesta singola → risposta singola, come una normale chiamata di funzione |
| **Server streaming** | `rpc f (Req) returns (stream Reply)` | richiesta singola → il client legge un **flusso** di risposte finché non ce ne sono più |
| **Client streaming** | `rpc f (stream Req) returns (Reply)` | il client invia un **flusso** di richieste, poi attende che il server le legga tutte e risponda |
| **Bidirectional streaming** | `rpc f (stream Req) returns (stream Reply)` | entrambi inviano un flusso; i due flussi sono **indipendenti** (ognuno legge/scrive nell'ordine che preferisce), ma l'ordine **dentro ciascun flusso** è mantenuto |

**Generators e `yield`** — le funzioni di streaming si realizzano in Python con i **generator** (funzioni che ritornano un *iteratore*). Si usa `yield` al posto di `return`: produce un valore **senza terminare la funzione** (usando `return` la funzione si interromperebbe al primo ciclo). Una funzione che contiene `yield` è automaticamente un generator.

```python
# SERVER streaming: la funzione del servicer è un generator (yield)
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello_v1(self, request, context):
        for i in range(0, 5):
            yield helloworld_pb2.HelloReply(message=f"Hello, {request.name}! - {i}")

# client legge il flusso iterando sullo stub
for response in stub.SayHello_v1(helloworld_pb2.HelloRequest(name="you")):
    print(response.message)
```

```python
# CLIENT streaming: il servicer riceve un request_iterator; il client passa un generator
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello_v2(self, request_iterator, context):
        names = []
        for request in request_iterator:
            names.append(request.name)
        return helloworld_pb2.HelloReply(message="Hello, " + ' '.join(names) + "!")

def generate_requests():
    for n in ['Raf', 'Gigi', 'Pippo']:
        yield helloworld_pb2.HelloRequest(name=n)
response = stub.SayHello_v2(generate_requests())
```

```python
# BIDIRECTIONAL: servicer riceve request_iterator e fa yield; client itera la risposta
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello_v3(self, request_iterator, context):
        for request in request_iterator:
            yield helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")
for response in stub.SayHello_v3(generate_requests()):
    print(response.message)
```

> 🎯 Esame: riconoscere il tipo di RPC dalla posizione di `stream` nel `.proto`; sapere che server-streaming e bidirectional richiedono `yield` (generator) lato server, mentre client-streaming e bidirectional richiedono un generator/`request_iterator` lato client.

### Thread-safety e GIL

- I **channel** creati con il modulo `grpc` sono **thread-safe**;
- gli **stub client** generati (es. `GreeterStub(channel)`) sono **thread-safe**;
- la **parte servente** (server multithread tramite `ThreadPoolExecutor`) resta comunque **soggetta al GIL** (vedi [[gil]]), nonostante gRPC usi il package `concurrent`.

Opzione utile lato server: `grpc.so_reuseport` impostata a `0` evita che più socket siano create da più processi sullo stesso `IP:PORTA`:
```python
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                     options=(('grpc.so_reuseport', 0),))
```

### Aggiornare un servizio gRPC

Per aggiungere un metodo: ① aggiungerlo al `.proto`; ② rigenerare il codice con `protoc`; ③ aggiornare il server per implementarlo; ④ aggiornare il client per invocarlo.

### Errori tipici in gRPC

Gli errori lato client si manifestano come `grpc.RpcError` con uno **StatusCode**:
- **`UNAVAILABLE`** — server non attivo o irraggiungibile (`Failed to connect ... Connection refused`);
- **`UNKNOWN`** — es. uso di un **campo inesistente** in un messaggio (`Protocol message ... has no "xxx" field`); oppure, lato Python, `ValueError: Protocol message Order has no "itemsaa" field`;
- streaming server senza generator → `Exception iterating responses: 'Order' object is not an iterator`;
- streaming client senza generator → `Exception iterating requests!`.

### Limitazioni di gRPC

- **Supporto limitato nei browser**: manca il supporto completo a HTTP/2; serve **gRPC-Web**, che però supporta solo RPC semplice e streaming server limitato;
- **Formato non human-readable**: protobuf è efficiente ma binario; servono strumenti aggiuntivi (es. CLI gRPC) per ispezionare i payload, scrivere richieste a mano, fare debugging.

---

## gRPC in Java — differenze rispetto a Python

Stessi concetti (channel, stub, messaggi Protobuf, thread-safe), ma Java è più **verboso**: usa builder pattern, costruttori espliciti, eccezioni checked.

### Setup Java

```bash
# compilazione .proto
protoc --java_out=. \
       --grpc-java_out=. \
       --plugin=protoc-gen-grpc-java=/PATH/plugin-1.73.0.exe \
       servizio.proto
```

Aggiungere nel `.proto` dopo `syntax`:
```protobuf
option java_multiple_files = true;
```

### API comparative: client-side

| Concetto | Java | Python |
|----------|------|--------|
| Import | `import io.grpc.*` | `import grpc` |
| Channel | `Grpc.newChannelBuilder(target, InsecureChannelCredentials.create()).build()` | `grpc.insecure_channel(target)` |
| Stub bloccante | `MyServiceGrpc.newBlockingStub(channel)` | unico tipo di stub |
| Stub asincrono | `MyServiceGrpc.newStub(channel)` — usa `StreamObserver` callback | `.future()` o asyncio |
| Messaggio | `MyReq.newBuilder().setField(v).build()` | `MyReq(field=v)` |
| Chiamata bloccante | `blockingStub.myMethod(request)` | `stub.MyMethod(request)` |
| Accesso campi risposta | `response.getField()` | `response.field` |
| Errore client | `catch (StatusRuntimeException e)` | `except grpc.RpcError` |
| Cleanup canale | `channel.shutdownNow().awaitTermination(t, unit)` | `channel.close()` |

### API comparative: server-side

| Concetto | Java | Python |
|----------|------|--------|
| Creare server | `Grpc.newServerBuilderForPort(port, credentials)` | `grpc.server(executor)` |
| Aggiungere servente | `.addService(new ServiceImpl())` | `add_XxxServicer_to_server(impl, server)` |
| Avviare | `.build().start()` | `server.start()` |
| Thread pool | `.executor(ExecutorService)` | `futures.ThreadPoolExecutor(max_workers=N)` |
| Implementare servizio | `class Impl extends XxxGrpc.XxxImplBase` + override metodi | `class Impl(XxxServicer)` + override metodi |
| Risposta unary | `responseObserver.onNext(resp)` + `responseObserver.onCompleted()` | `return response` |
| Risposta streaming | multiple `onNext()` + `onCompleted()` | `yield response` (generator) |
| Errore server | `responseObserver.onError(StatusException)` | `context.abort(StatusCode, msg)` |
| Attesa terminazione | `server.awaitTermination()` | `server.wait_for_termination()` |
| Shutdown hook | `Runtime.getRuntime().addShutdownHook(thread)` | signal handler / context manager |

### Pattern completo Java — Hello World

**Servente (impl)**:
```java
public class GreeterImpl extends GreeterGrpc.GreeterImplBase {
    @Override
    public void sayHello(HelloRequest req, StreamObserver<HelloReply> responseObserver) {
        HelloReply reply = HelloReply.newBuilder()
            .setMessage("Hello " + req.getName()).build();
        responseObserver.onNext(reply);
        responseObserver.onCompleted();
    }
}
```

**Server**:
```java
ExecutorService executor = Executors.newFixedThreadPool(2);
Server server = Grpc.newServerBuilderForPort(50051, InsecureServerCredentials.create())
    .executor(executor)
    .addService(new GreeterImpl())
    .build()
    .start();
server.awaitTermination();
```

**Client**:
```java
ManagedChannel channel = Grpc.newChannelBuilder(
    "localhost:50051", InsecureChannelCredentials.create()).build();
GreeterGrpc.GreeterBlockingStub stub = GreeterGrpc.newBlockingStub(channel);
try {
    HelloReply resp = stub.sayHello(HelloRequest.newBuilder().setName("World").build());
    System.out.println(resp.getMessage());
} catch (StatusRuntimeException e) {
    System.err.println("RPC failed: " + e.getStatus());
} finally {
    channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
}
```

> 🎯 Esame: Differenze Java vs Python nelle API gRPC. Cosa fa `responseObserver.onNext()` + `onCompleted()`. Perché `package` in Java non è ignorato.

> 💡 Connessione: `StreamObserver` in Java async corrisponde al pattern Observer di [[pub-sub]] — il client si registra come osservatore della risposta.

## Perché importa

gRPC è uno degli argomenti avanzati del corso — integra RPC, protobuf, HTTP/2 e concorrenza in un unico framework.

## Connessioni

- [[protocol-buffers]] — IDL e serializzazione di gRPC
- [[rpc]] — gRPC implementa il paradigma RPC
- [[threading]] — il server gRPC usa un thread pool (`ThreadPoolExecutor`)
- [[socket]] — HTTP/2 gira su TCP/socket
- [[grpc-python]] — binding Python (grpcio, grpcio-tools)
- [[grpc-java]] — binding Java (io.grpc, protoc-gen-grpc-java)
- [[gestione-errori-api]] — gestione errori via context, StatusCode, abort()
- [[middleware-trasparenza]] — gRPC come specifica aperta intercambiabile tra linguaggi
- [[middleware]] — gRPC è un'implementazione del modello middleware RPC (orientato alla comunicazione)
- [[java-threading]] — `ExecutorService` per thread pool server Java
- [[gil]] — il server gRPC Python multithread resta soggetto al GIL

## Fonti

- [[14-python-rpc-grpc]]
- [[25-java-grpc]]

_Aggiornato: 2026-06-19 — estensione MODULO 2 (slide 14): scenari/CNCF, HTTP/2 (binary framing, stream/message/frame, multiplexing), blocking vs non-blocking stub, 4 tipi di RPC call con generators/yield, thread-safety+so_reuseport, aggiornare servizio, errori tipici, limitazioni (gRPC-Web, non human-readable)_
