---
tipo: entità
categoria: framework
---

## Cos'è

**gRPC Python** è il binding Python del framework gRPC di Google. Si installa tramite i pacchetti `grpcio` (runtime) e `grpcio-tools` (compilatore protobuf).

## Come si usa nel corso

gRPC Python è usato per implementare servizi RPC client-server con Protocol Buffers come IDL e HTTP/2 come trasporto.

**Installazione**:
```bash
pip install grpcio grpcio-tools
```

**Compilazione `.proto`**:
```bash
python -m grpc_tools.protoc -I. \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    nome_servizio.proto

# Se il .proto è in una sottodirectory:
python -m grpc_tools.protoc -Iprotos \
    --python_out=. --pyi_out=. --grpc_python_out=. \
    protos/nome_servizio.proto
```

**File generati**:
- `nome_servizio_pb2.py` — classi messaggi protobuf
- `nome_servizio_pb2_grpc.py` — stub client + servicer skeleton server
- `nome_servizio_pb2.pyi` — type hints (da `--pyi_out`)

**Pattern server**:
```python
import grpc
from concurrent import futures
import servizio_pb2_grpc, servizio_pb2

class MioServicer(servizio_pb2_grpc.MioServizioServicer):
    def MioMetodo(self, request, context):
        # logica di business
        return servizio_pb2.MioResponse(...)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
servizio_pb2_grpc.add_MioServizioServicer_to_server(MioServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
```

**Pattern client**:
```python
channel = grpc.insecure_channel('localhost:50051')
stub = servizio_pb2_grpc.MioServizioStub(channel)
risposta = stub.MioMetodo(servizio_pb2.MioRequest(...))
```

**Porta default gRPC**: 50051

**Opzioni socket del server** — per evitare che più processi creino socket sullo stesso `IP:PORTA`:
```python
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                     options=(('grpc.so_reuseport', 0),))
```

### Streaming RPC (generator / yield)

Le RPC di streaming si scrivono con i **generator** (`yield`):
```python
# Server streaming — il servicer fa yield, il client itera la risposta
def SayHello_v1(self, request, context):
    for i in range(0, 5):
        yield servizio_pb2.HelloReply(message=f"Hello {request.name} {i}")
for response in stub.SayHello_v1(servizio_pb2.HelloRequest(name="you")):
    ...

# Client streaming — il servicer riceve request_iterator, il client passa un generator
def SayHello_v2(self, request_iterator, context):
    names = [r.name for r in request_iterator]
    return servizio_pb2.HelloReply(message=" ".join(names))
def gen():
    for n in ["Raf", "Gigi"]:
        yield servizio_pb2.HelloRequest(name=n)
response = stub.SayHello_v2(gen())
```

### Thread-safety

`channel` e `stub` generati sono **thread-safe**; il server multithread resta soggetto al **GIL** (vedi [[gil]]).

### Errori tipici (`grpc.RpcError`)

- `StatusCode.UNAVAILABLE` → server spento/irraggiungibile;
- `StatusCode.UNKNOWN` → campo inesistente (`Protocol message X has no "y" field`);
- streaming senza `yield`/generator → `object is not an iterator` / `Exception iterating requests!`.

## Link ai concetti correlati

- [[grpc]] — concetto architetturale (4 tipi di RPC, HTTP/2, thread-safety)
- [[protocol-buffers]] — formato IDL e serializzazione
- [[threading]] — il server usa `ThreadPoolExecutor`
- [[gil]] — il server multithread resta soggetto al GIL
- [[grpc-python-boilerplate]] — snippet boilerplate pronto

## Fonti

- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-19 — estensione MODULO 2 (slide 14): streaming RPC con generator/yield, so_reuseport, thread-safety, errori tipici RpcError_
