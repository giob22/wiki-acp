---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread]
---

## Definizione

Un **socket** è un'astrazione software che rappresenta un endpoint di comunicazione bidirezionale tra due processi (anche su host diversi). Identifica univocamente una connessione tramite la coppia **(indirizzo IP, porta)**.

## Spiegazione

**Stack Internet (OSI semplificato)**:
```
Applicazione   ← Flask, gRPC, STOMP
Trasporto      ← TCP / UDP
Rete           ← IP
Data Link      ← Ethernet, WiFi
```

**TCP vs UDP**:
| | TCP | UDP |
|---|---|---|
| Connessione | Sì (3-way handshake) | No |
| Affidabilità | Garantita (ACK, ritrasmissione) | Non garantita |
| Ordine | Garantito | Non garantito |
| Velocità | Più lento | Più veloce |
| Uso | HTTP, gRPC, STOMP | DNS, video streaming |

**Indirizzo IP**: identifica l'host (IPv4: `192.168.1.1`; IPv6: `::1`)
**Porta**: identifica il processo/servizio sull'host (0-65535; < 1024 sono well-known)

**Socket in Python**:
```python
import socket

# Creazione
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
```

**Server TCP**:
```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))  # associa IP:porta
server.listen(5)                 # coda di max 5 connessioni pendenti
while True:
    conn, addr = server.accept()  # blocca — aspetta client
    data = conn.recv(1024)        # riceve fino a 1024 byte
    conn.send(b"risposta")        # invia risposta
    conn.close()
```

**Client TCP**:
```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))  # 3-way handshake
client.send(b"richiesta")
risposta = client.recv(1024)
client.close()
```

**Context manager**:
```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("host", porta))
    ...  # socket chiuso automaticamente
```

> 🎯 Esame: Sequenza server TCP (bind → listen → accept → recv/send), differenza TCP/UDP.

## Perché importa

I socket sono il fondamento di tutto il networking del corso: gRPC, STOMP/ActiveMQ e Flask comunicano tutti su socket TCP.

## Connessioni

- [[threading]] — server socket usano thread per gestire più client contemporaneamente
- [[rpc]] — gRPC usa socket TCP sotto (via HTTP/2)
- [[mom]] — ActiveMQ/STOMP usa socket TCP

## Fonti

- [[12-python-networking]]

_Aggiornato: 2026-06-04 — ingest iniziale_
