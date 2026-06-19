---
tipo: entità
categoria: framework
---

## Cos'è

**gRPC Java** è il binding Java del framework gRPC di Google. Usa librerie JAR distribuite su Maven (pacchetto `io.grpc.*`). Non ha un compilatore protobuf integrato: richiede `protoc` + plugin `protoc-gen-grpc-java` separati.

## Setup

**1. Compilatore `protoc`**: scaricare da github.com/protocolbuffers/protobuf/releases e installare in `/usr/local/bin/protoc`.

**2. Plugin gRPC Java** (versione da usare: **1.73.0**):
```bash
# Linux
chmod +x protoc-gen-grpc-java-1.73.0-linux-x86_64.exe
```

**3. Compilazione `.proto`**:
```bash
protoc --java_out=. \
       --grpc-java_out=. \
       --plugin=protoc-gen-grpc-java=/PATH/TO/protoc-gen-grpc-java-1.73.0-linux-x86_64.exe \
       nome_servizio.proto
```
Genera classi Java per messaggi (da `--java_out`) e per stub/canali/serventi (da `--grpc-java_out`).

**4. Dipendenze JAR** (classpath):

| JAR | Versione |
|-----|----------|
| grpc-api | 1.73.0 |
| grpc-core | 1.73.0 |
| grpc-netty-shaded | 1.73.0 |
| grpc-protobuf | 1.73.0 |
| grpc-protobuf-lite | 1.73.0 |
| grpc-stub | 1.73.0 |
| protobuf-java | 4.31.1 |
| guava | 33.4.8-jre |
| perfmark-api | 0.26.0 |
| failureaccess | 1.0 |
| javax.annotation-api | 1.3.2 |

> Le versioni `grpc-*` devono coincidere con la versione del plugin protoc-gen-grpc-java usato.

## Come si usa nel corso

**Pattern proto per Java** — aggiungere dopo `syntax`:
```protobuf
option java_multiple_files = true;
```
Il campo `package` **non è ignorato** in Java (diverso da Python): determina il package Java delle classi generate. Usare `option java_package = "..."` per sovrascriverlo.

**Pattern server**:
```java
ExecutorService executor = Executors.newFixedThreadPool(4);
Server server = Grpc.newServerBuilderForPort(port, InsecureServerCredentials.create())
    .executor(executor)
    .addService(new MyServiceImpl())
    .build()
    .start();
server.awaitTermination();
```

**Pattern client** (chiamata bloccante):
```java
ManagedChannel channel = Grpc.newChannelBuilder(
    "localhost:50051", InsecureChannelCredentials.create()
).build();
MyServiceGrpc.MyServiceBlockingStub stub = MyServiceGrpc.newBlockingStub(channel);
try {
    MyResponse resp = stub.myMethod(MyRequest.newBuilder().setField(value).build());
} catch (StatusRuntimeException e) {
    // gestione errore: e.getStatus()
} finally {
    channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
}
```

**Pattern client** (chiamata asincrona con StreamObserver):
```java
MyServiceGrpc.MyServiceStub asyncStub = MyServiceGrpc.newStub(channel);
asyncStub.myMethod(request, new StreamObserver<MyResponse>() {
    public void onNext(MyResponse resp) { /* gestisce risposta */ }
    public void onError(Throwable t) { /* gestisce errore */ }
    public void onCompleted() { /* chiamata terminata */ }
});
```

**Pattern implementazione servizio**:
```java
public class MyServiceImpl extends MyServiceGrpc.MyServiceImplBase {
    @Override
    public void myMethod(MyRequest req, StreamObserver<MyResponse> responseObserver) {
        MyResponse reply = MyResponse.newBuilder().setResult(...).build();
        responseObserver.onNext(reply);      // invia risposta
        responseObserver.onCompleted();      // segnala fine (obbligatorio)
    }
}
```

**Shutdown server** con hook JVM:
```java
Runtime.getRuntime().addShutdownHook(new Thread(() -> server.shutdown()));
```

## Link ai concetti correlati

- [[grpc]] — concetto architetturale + confronto Java vs Python
- [[protocol-buffers]] — IDL `.proto` con opzioni Java specifiche
- [[java-threading]] — `ExecutorService` per thread pool server
- [[rpc]] — pattern stub/skeleton implementato da gRPC Java

## Fonti

- [[25-java-grpc]]

_Aggiornato: 2026-06-11 — ingest iniziale_
