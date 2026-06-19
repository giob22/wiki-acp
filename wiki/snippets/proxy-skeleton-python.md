---
tipo: snippet
tecnologia: proxy-skeleton
linguaggio: python
---

# Boilerplate — Proxy-Skeleton (Python, Socket TCP)

Implementazione manuale di RPC: il client usa l'interfaccia tramite il Proxy, il server estende lo Skeleton (variante per ereditarietà). → [[proxy-pattern]]

## Struttura file

```
IService.py        ← interfaccia ABC
service_proxy.py   ← lato client: serializza e invia via TCP
service_skeleton.py← lato server: accept loop + upcall
server_impl.py     ← logica reale, estende lo skeleton
client.py          ← usa il proxy come oggetto locale
```

## Interfaccia — `IService.py`

```python
from abc import ABC, abstractmethod

class IService(ABC):

    @abstractmethod
    def send_reading(self, location: str, temperature: float):
        pass
```

## Proxy (lato client) — `service_proxy.py`

```python
import socket
from IService import IService

class ServiceProxy(IService):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_reading(self, location: str, temperature: float):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, self.port))

            # serializzazione manuale: campi separati da '-'
            message = location + "-" + str(temperature)
            sock.send(message.encode("utf-8"))

            # riscontro dal server
            ack = sock.recv(1024).decode("utf-8")
            print(f"ricevuto: {ack}")
```

## Skeleton (lato server, ereditarietà) — `service_skeleton.py`

```python
import socket
from abc import ABC, abstractmethod
from IService import IService

class ServiceSkeleton(IService, ABC):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @abstractmethod
    def send_reading(self, location, temperature):
        pass

    def run_skeleton(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with sock:
            try:
                sock.bind((self.ip, self.port))
                self.ip, self.port = sock.getsockname()  # utile con porta 0
                sock.listen(5)
                print(f"listening on {self.ip}:{self.port}")

                while True:
                    conn, addr = sock.accept()
                    print(f"serving: {addr}")

                    message = conn.recv(1024).decode("utf-8")
                    data = message.split('-')

                    # upcall: deserializza e invoca il metodo della sottoclasse
                    self.send_reading(data[0], float(data[1]))

                    conn.send("ack".encode("utf-8"))
                    conn.close()
            except KeyboardInterrupt:
                print("server terminato con successo")
```

## Implementazione server — `server_impl.py`

```python
from service_skeleton import ServiceSkeleton

class ServerImpl(ServiceSkeleton):

    def send_reading(self, location, temperature):
        # logica applicativa reale
        print(f"[RECV] location={location} temperature={temperature}")

if __name__ == "__main__":
    server = ServerImpl("localhost", 5000)
    server.run_skeleton()
```

## Client — `client.py`

```python
from service_proxy import ServiceProxy

if __name__ == "__main__":
    # il client vede solo l'interfaccia: la rete è trasparente
    service = ServiceProxy("localhost", 5000)
    service.send_reading("sala-A", 23.5)
```

## Variante: skeleton multithread

Per servire più client in parallelo, sostituire il corpo del `while True` con un thread per connessione:

```python
import threading

def handle(self, conn, addr):
    message = conn.recv(1024).decode("utf-8")
    data = message.split('-')
    self.send_reading(data[0], float(data[1]))
    conn.send("ack".encode("utf-8"))
    conn.close()

# nel loop:
while True:
    conn, addr = sock.accept()
    threading.Thread(target=self.handle, args=(conn, addr), daemon=False).start()
```

Se `send_reading` tocca stato condiviso, proteggerlo con `Lock` → [[threading]].

> 🎯 Esame: lo skeleton riceve byte, deserializza, fa upcall al metodo astratto implementato dalla sottoclasse. Il proxy fa l'inverso. Entrambi implementano la stessa interfaccia.

## Variante: trasporto UDP

Stessa architettura Proxy/Skeleton, ma socket `SOCK_DGRAM` invece di `SOCK_STREAM`. UDP è **connectionless**: niente `connect`/`listen`/`accept`, si usano `sendto`/`recvfrom`. Stessa `IService`.

Proxy UDP — `service_proxy.py`:

```python
import socket
from IService import IService

class ServiceProxy(IService):

    def __init__(self, ip, port):
        self.addr = (ip, port)

    def send_reading(self, location: str, temperature: float):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # serializzazione manuale, stesso formato del TCP
            message = location + "-" + str(temperature)
            sock.sendto(message.encode("utf-8"), self.addr)

            # riscontro: recvfrom torna (dati, addr_mittente)
            ack, server_addr = sock.recvfrom(1024)
            print(f"ricevuto: {ack.decode('utf-8')}")
```

Skeleton UDP — `service_skeleton.py`:

```python
import socket
from abc import ABC, abstractmethod
from IService import IService

class ServiceSkeleton(IService, ABC):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    @abstractmethod
    def send_reading(self, location, temperature):
        pass

    def run_skeleton(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with sock:
            try:
                sock.bind((self.ip, self.port))   # solo bind: niente listen/accept
                print(f"listening on {self.ip}:{self.port}")

                while True:
                    # recvfrom blocca: torna dati + indirizzo del client
                    message, addr = sock.recvfrom(1024)
                    data = message.decode("utf-8").split('-')
                    print(f"serving: {addr}")

                    # upcall verso la sottoclasse
                    self.send_reading(data[0], float(data[1]))

                    # rispondi allo stesso addr da cui hai ricevuto
                    sock.sendto("ack".encode("utf-8"), addr)
            except KeyboardInterrupt:
                print("server terminato con successo")
```

`server_impl.py` e `client.py` restano identici alla variante TCP: il transport è incapsulato in proxy e skeleton.

> 🎯 Esame: differenze TCP→UDP. Client: `sendto(dati, addr)` + `recvfrom`. Server: solo `bind`, poi loop `recvfrom`/`sendto`; nessuna connessione persistente, una socket sola serve tutti i client. UDP non garantisce consegna né ordine → [[socket]].

## Collegamenti

- [[proxy-pattern]] — il pattern, varianti ereditarietà vs delega
- [[socket]] — TCP client/server sottostante
- [[rpc]] — concetto generale stub/skeleton
- [[proxy-skeleton-java]] — stessa architettura in Java

## Fonti

- [[23-java-proxy-skeleton]] (pattern), svolgimento sim-01 (`svolgimenti/2026-06-08-sim-01/`)

_Aggiornato: 2026-06-12 — creazione raccolta snippet_
_Aggiornato: 2026-06-16 — aggiunta variante trasporto UDP (sendto/recvfrom)_
