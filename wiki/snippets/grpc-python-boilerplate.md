---
tipo: snippet
tecnologia: grpc
linguaggio: python
---

#flashcards/acp

# Boilerplate — gRPC (Python)

Workflow completo: `.proto` → compilazione → server (Servicer) → client (Stub). → [[grpc]] [[grpc-python]]

## Setup

```bash
pip install grpcio grpcio-tools
```

## IDL — `service.proto`

```protobuf
syntax = "proto3";

package collector;

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
python -m grpc_tools.protoc -I. \
    --python_out=. \
    --pyi_out=. \
    --grpc_python_out=. \
    service.proto
```

Genera: `service_pb2.py` (messaggi), `service_pb2_grpc.py` (Stub + Servicer), `service_pb2.pyi` (type hints).

## Server — `server.py`

```python
import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc 


class CollectorServicer(service_pb2_grpc.ICollectorServicer):

    def SendMeasurement(self, request: service_pb2.Measurement,
                        context: grpc.ServicerContext):
        device_id = request.device_id
        value = request.value
        print(f"[RECV] device_id={device_id} | value={value}")

        # logica di business...

        return service_pb2.Ack(status="OK")


if __name__ == "__main__":
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_ICollectorServicer_to_server(CollectorServicer(), server)

        # porta fissa:
        server.add_insecure_port("localhost:50051")
        # oppure porta scelta dall'OS (utile nelle prove):
        # port = server.add_insecure_port("localhost:0")
        # print(f"listening on localhost:{port}")

        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("--- server terminato ---")
```

## Client — `client.py`

```python
import grpc
import service_pb2
import service_pb2_grpc

if __name__ == "__main__":
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.ICollectorStub(channel)

        response: service_pb2.Ack = stub.SendMeasurement(
            service_pb2.Measurement(device_id="sensor-A", value=23.5)
        )
        print(f"[SENT] response={response.status}")
```

## Liste — `repeated`

Nel `.proto` le liste si dichiarano con la keyword `repeated` davanti al tipo del campo:

```protobuf
message MeasurementBatch {
    string device_id = 1;
    repeated float values = 2;          // lista di scalari
    repeated Measurement history = 3;   // lista di messaggi
}

service ICollector {
    rpc SendBatch (MeasurementBatch) returns (Ack);
}
```

In Python un campo `repeated` si comporta come una lista (iterabile, indicizzabile, `len()`), ma **non si può assegnare direttamente** (`msg.values = [...]` solleva `AttributeError`): si usano `append`/`extend`, oppure si passa la lista nel costruttore.

**Lato client** — costruzione:

```python
# 1) lista passata al costruttore (caso più comune)
batch = service_pb2.MeasurementBatch(
    device_id="sensor-A",
    values=[23.5, 24.1, 22.8],
)

# 2) append/extend dopo la creazione
batch.values.append(25.0)
batch.values.extend([26.2, 27.1])

# 3) repeated di messaggi: .add() crea e appende un elemento
m = batch.history.add()
m.device_id = "sensor-A"
m.value = 23.5
# oppure: batch.history.append(service_pb2.Measurement(device_id="sensor-A", value=23.5))

stub.SendBatch(batch)
```

**Lato server** — lettura come normale sequenza Python:

```python
def SendBatch(self, request, context):
    print(f"[RECV] {len(request.values)} valori da {request.device_id}")
    for v in request.values:
        print(v)
    media = sum(request.values) / len(request.values) if request.values else 0
    return service_pb2.Ack(status="OK")
```

> 🎯 Esame: `repeated` su scalari usa la classe `RepeatedScalarContainer`, su messaggi `RepeatedCompositeContainer` — quest'ultima ha `.add()`. Un campo `repeated` vuoto è una lista vuota, mai `None`.

Come si gestiscono i campi repeated in gRPC Python?
?
Scalari → RepeatedScalarContainer; messaggi → RepeatedCompositeContainer (ha .add()). Un repeated vuoto è una lista vuota, mai None.


## Gestione errori

**Lato server** — segnalare errore tramite context:

```python
def SendMeasurement(self, request, context):
    if not request.device_id:
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details("device_id mancante")
        return service_pb2.Ack()
    ...
```

**Lato client** — intercettare `RpcError`:

```python
try:
    response = stub.SendMeasurement(request)
except grpc.RpcError as e:
    print(f"errore: {e.code()} — {e.details()}")
```

> 🎯 Esame: il servicer è lo **skeleton** generato, lo stub è il **proxy** generato — gRPC automatizza ciò che il pattern [[proxy-pattern]] fa a mano. Il `package` nel `.proto` è ignorato da Python (a differenza di Java).

Nel gRPC generato, cos'è il servicer e cos'è lo stub?
?
Servicer = skeleton (server), Stub = proxy (client): gRPC automatizza ciò che il Proxy-Skeleton fa a mano. Il package del .proto è ignorato in Python (non in Java).


## Collegamenti

- [[grpc]] — architettura, HTTP/2, workflow 4 passi
- [[protocol-buffers]] — sintassi `.proto`
- [[grpc-python]] — pagina entità (installazione, file generati)
- [[gestione-errori-api]] — StatusCode e context in dettaglio
- [[grpc-java-boilerplate]] — equivalente Java

## Fonti

- [[14-python-rpc-grpc]], svolgimenti sim-02 e sim-04 (`svolgimenti/2026-06-09-sim-02/python/`)

_Aggiornato: 2026-06-12 — aggiunta sezione liste `repeated`_
