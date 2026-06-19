---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc, protocol-buffers, socket]
---

## Definizione

**gRPC** è un framework RPC open-source sviluppato da Google. Usa **HTTP/2** come trasporto e **Protocol Buffers** come formato di serializzazione e IDL. Supporta streaming bidirezionale e interoperabilità tra linguaggi diversi.

## Spiegazione

**Vantaggi di HTTP/2 su HTTP/1.1**:
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
- [[java-threading]] — `ExecutorService` per thread pool server Java

## Fonti

- [[14-python-rpc-grpc]]
- [[25-java-grpc]]

_Aggiornato: 2026-06-11 — aggiunta sezione gRPC Java: setup, API comparative, Hello World_
