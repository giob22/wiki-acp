---
tipo: fonte
titolo: "02_JAVA_06 — Remote Procedure Call in Java (gRPC)"
data_ingest: 2026-06-11
formato: slide-pdf
argomenti: [grpc, java, protobuf, rpc, threading]
---

## Sommario

Le slide introducono gRPC in Java partendo dal setup del toolchain (protoc + plugin protoc-gen-grpc-java v1.73.0 + dipendenze JAR), per poi mostrare le API Java in forma di tabelle comparative con la controparte Python. Java utilizza il builder pattern per channel, stub e messaggi, eccezioni checked (`StatusRuntimeException`) e il pattern `StreamObserver` per le risposte asincrone — tutto più verboso ma più esplicito del binding Python. L'esempio Hello World completo (server, client, impl) mostra il workflow pratico.

## Punti chiave

1. gRPC Java usa lo stesso protocollo (HTTP/2 + protobuf) e gli stessi concetti (channel, stub) di Python — channel e stub sono thread-safe in entrambi
2. Compilazione `.proto`: `protoc --java_out=. --grpc-java_out=. --plugin=protoc-gen-grpc-java=PATH nome.proto`
3. Aggiungere `option java_multiple_files = true;` nel `.proto` — migliora organizzazione classi generate
4. Campo `package` nel `.proto` **non è ignorato** in Java — determina il path del package generato (a differenza di Python)
5. Dipendenze JAR versione 1.73.0: grpc-api, grpc-core, grpc-netty-shaded, grpc-protobuf, grpc-protobuf-lite, grpc-stub (stessa versione del plugin protoc-gen-grpc-java)
6. Server Java: `Grpc.newServerBuilderForPort(port, credentials).executor(pool).addService(new ServiceImpl()).build().start()`
7. Client Java: `Grpc.newChannelBuilder(target, InsecureChannelCredentials.create()).build()` → stub → chiamata bloccante
8. Implementazione servizio: classe estende `MyServiceGrpc.MyServiceImplBase`, override dei metodi, risposta via `responseObserver.onNext(response)` + `responseObserver.onCompleted()`
9. Gestione errori: `catch (StatusRuntimeException e)` lato client; `responseObserver.onError(StatusException)` lato server
10. Chiamate asincrone: stub asincrono + `StreamObserver<Response>` come callback (pattern Observer)

## Concetti introdotti

- [[grpc]] — approfondimento binding Java: setup, API, pattern
- [[grpc-java]] — nuova entità: binding Java gRPC
- [[rpc]] — conferma pattern stub/skeleton in Java
- [[protocol-buffers]] — differenze proto3 in Java (`java_multiple_files`, `package` non ignorato, `java_package`)
- [[java-threading]] — `ExecutorService` custom per thread pool gRPC server

## Domande aperte

- Quando conviene chiamata bloccante vs asincrona (StreamObserver) in Java?
- Come gestire TLS con `TlsServerCredentials` vs `InsecureServerCredentials`?

## Domande da esame

- Descrivi le differenze principali tra le API gRPC Java e Python (verbosità, builder pattern, eccezioni checked, StreamObserver vs return)
- Come si implementa un servente gRPC in Java? Quale classe si estende e come si invia la risposta?
- Cosa fa `responseObserver.onNext()` e `responseObserver.onCompleted()`? Perché entrambi sono necessari?
- In Java gRPC, cosa differisce nel comportamento del campo `package` del `.proto` rispetto a Python?
- Elenca le fasi di creazione di un server gRPC in Java (da `Grpc.newServerBuilderForPort` a `server.awaitTermination`)

_Aggiornato: 2026-06-11 — ingest iniziale_
