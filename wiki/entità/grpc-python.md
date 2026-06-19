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

## Link ai concetti correlati

- [[grpc]] — concetto architetturale
- [[protocol-buffers]] — formato IDL e serializzazione
- [[threading]] — il server usa `ThreadPoolExecutor`

## Fonti

- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-04 — ingest iniziale_
