---
tipo: snippet
tecnologia: grpc
linguaggio: java
---

# Boilerplate — gRPC (Java)

Workflow completo: `.proto` con opzioni Java → compilazione con plugin → server → client. → [[grpc]] [[grpc-java]]

## IDL — `service.proto` (opzioni Java)

```protobuf
syntax = "proto3";

option java_multiple_files = true;
// option java_package = "com.acp.collector";  // sovrascrive package

package collector;   // NON ignorato in Java: diventa il package delle classi

service ICollector {
    rpc SendMeasurement (Measurement) returns (Ack);
}

message Measurement {
    string device_id = 1;
    float value = 2;
}

message Ack {
    string status = 1;
}
```

## Compilazione

```bash
protoc --java_out=. \
       --grpc-java_out=. \
       --plugin=protoc-gen-grpc-java=/PATH/TO/protoc-gen-grpc-java-1.73.0-linux-x86_64.exe \
       service.proto
```

Dipendenze JAR nel classpath (versioni complete → [[grpc-java]]): `grpc-api`, `grpc-core`, `grpc-netty-shaded`, `grpc-protobuf`, `grpc-stub`, `protobuf-java`, `guava`, `javax.annotation-api`, ...

## Implementazione servizio — `CollectorImpl.java`

```java
import io.grpc.stub.StreamObserver;
import collector.*;

public class CollectorImpl extends ICollectorGrpc.ICollectorImplBase {

    @Override
    public void sendMeasurement(Measurement request,
                                StreamObserver<Ack> responseObserver) {
        String deviceId = request.getDeviceId();
        float value = request.getValue();
        System.out.println("[RECV] device_id=" + deviceId + " | value=" + value);

        Ack reply = Ack.newBuilder().setStatus("OK").build();

        responseObserver.onNext(reply);       // invia la risposta
        responseObserver.onCompleted();       // segnala fine — obbligatorio
    }
}
```

## Server — `CollectorServer.java`

```java
import io.grpc.*;
import java.util.concurrent.*;

public class CollectorServer {
    public static void main(String[] args) throws Exception {

        ExecutorService executor = Executors.newFixedThreadPool(4);

        Server server = Grpc.newServerBuilderForPort(50051,
                    InsecureServerCredentials.create())
                .executor(executor)
                .addService(new CollectorImpl())
                .build()
                .start();

        System.out.println("listening on 50051");

        // shutdown pulito alla terminazione della JVM
        Runtime.getRuntime().addShutdownHook(new Thread(() -> server.shutdown()));

        server.awaitTermination();
    }
}
```

## Client bloccante — `CollectorClient.java`

```java
import io.grpc.*;
import java.util.concurrent.TimeUnit;
import collector.*;

public class CollectorClient {
    public static void main(String[] args) {

        ManagedChannel channel = Grpc.newChannelBuilder(
                "localhost:50051", InsecureChannelCredentials.create()).build();

        ICollectorGrpc.ICollectorBlockingStub stub =
                ICollectorGrpc.newBlockingStub(channel);

        try {
            Ack response = stub.sendMeasurement(
                    Measurement.newBuilder()
                            .setDeviceId("sensor-A")
                            .setValue(23.5f)
                            .build());
            System.out.println("[SENT] response=" + response.getStatus());

        } catch (StatusRuntimeException e) {
            System.err.println("errore RPC: " + e.getStatus());
        } finally {
            try {
                channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
            } catch (InterruptedException ignored) {}
        }
    }
}
```

## Client asincrono (StreamObserver)

```java
ICollectorGrpc.ICollectorStub asyncStub = ICollectorGrpc.newStub(channel);

asyncStub.sendMeasurement(request, new StreamObserver<Ack>() {
    @Override public void onNext(Ack resp)      { /* gestisce risposta */ }
    @Override public void onError(Throwable t)  { /* gestisce errore */ }
    @Override public void onCompleted()         { /* chiamata terminata */ }
});
```

> 🎯 Esame: differenze Java vs Python — i messaggi si costruiscono con il **Builder** (`newBuilder().set...().build()`, immutabili), il `package` del proto **non** è ignorato, la risposta si invia con `onNext()` + `onCompleted()` invece del semplice `return`.

## Collegamenti

- [[grpc-java]] — setup completo, tabella JAR, versioni
- [[grpc]] — architettura e confronto Java/Python
- [[protocol-buffers]] — IDL
- [[java-threading]] — `ExecutorService` per il thread pool
- [[grpc-python-boilerplate]] — equivalente Python

## Fonti

- [[25-java-grpc]]

_Aggiornato: 2026-06-12 — creazione raccolta snippet_
