---
tipo: fonte
titolo: "Python RPC — gRPC e Protocol Buffers"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [grpc, protobuf, http2, rpc, python, proto3, stub, skeleton, serializzazione]
---

## Sommario

Slide su gRPC e Protocol Buffers in Python (20+ pagine). gRPC è il framework RPC open-source di Google che usa HTTP/2 come trasporto e Protocol Buffers (protobuf) come formato di serializzazione. Si descrive la struttura dei file `.proto`, il workflow di compilazione, e un esempio Hello World completo.

## Punti chiave

1. **gRPC** = framework RPC moderno di Google; usa **HTTP/2** come trasporto
2. **HTTP/2**: multiplexing, header compression, server push — molto più efficiente di HTTP/1.1
3. **Protocol Buffers (protobuf)**: formato di serializzazione **binario**, fortemente tipizzato, sviluppato da Google
4. Struttura file `.proto`:
   ```protobuf
   syntax = "proto3";
   package nome.package;
   
   service NomeServizio {
     rpc NomeMetodo (TipoRequest) returns (TipoResponse);
   }
   
   message NomeMessaggio {
     tipo campo_nome = numero_tag;  // il tag identifica il campo nel binario
   }
   ```
5. **Messaggio** = record logico con coppie nome-valore chiamate **campi**; ogni campo ha un **tag numerico univoco** (usato nel formato binario)
6. **Direttiva `package`**: opzionale, evita conflitti di naming; in Python è **ignorata** (moduli organizzati per filesystem), ma raccomandata per portabilità
7. Installazione: `pip install grpcio grpcio-tools`
8. **Workflow gRPC in 4 passi**:
   1. Installare `grpcio` e `grpcio-tools`
   2. Definire servizio e messaggi nel file `.proto`
   3. Compilare con `protoc` per generare stub/skeleton
   4. Implementare client e server usando l'API gRPC
9. **Compilazione**:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. servizio.proto
   ```
   - Genera `servizio_pb2.py` — classi messaggi (serializzazione/deserializzazione)
   - Genera `servizio_pb2_grpc.py` — classi stub (client) e servicer (server skeleton)
10. **Workflow runtime**: client chiama stub → stub serializza → HTTP/2 → server stub (skeleton) deserializza → chiama funzione reale → risposta inversa
11. Esempio **Hello World**:
    - `.proto`: service `Greeter` con `rpc SayHello(HelloRequest) returns (HelloReply)`
    - `HelloRequest { string name = 1; }`, `HelloReply { string message = 1; }`

## Concetti introdotti

- [[grpc]]
- [[protocol-buffers]]
- [[rpc]]
- [[grpc-python]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è gRPC? Che trasporto usa?
- Struttura di un file `.proto`: syntax, package, service, message, field tag
- Cosa fa `grpc_tools.protoc`? Quali file genera e cosa contengono?
- Descrivere il workflow di una chiamata gRPC passo per passo
- Differenza tra `_pb2.py` e `_pb2_grpc.py`
- Perché protobuf usa rappresentazione binaria invece di JSON?
