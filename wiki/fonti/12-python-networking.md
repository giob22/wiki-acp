---
tipo: fonte
titolo: "Python — Networking"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, socket, tcp, udp, networking, osi, ip, porta]
---

## Sommario

Slide sul networking con Python (20 pagine). Si descrive lo stack protocollare Internet/OSI, i concetti di indirizzo IP, porta e socket. Si introduce il modulo `socket` di Python per creare applicazioni client-server su TCP e UDP.

## Punti chiave

1. **Stack OSI**: Applicazione, Presentazione, Sessione, Trasporto, Rete, Data Link, Fisico
2. **TCP** (Transmission Control Protocol): connesso, affidabile, ordinato — handshake a 3 vie
3. **UDP** (User Datagram Protocol): senza connessione, non affidabile, più veloce
4. **Indirizzo IP**: identifica il host (IPv4: 32 bit, IPv6: 128 bit)
5. **Porta**: identifica il processo sul host (16 bit, 0-65535); porte well-known < 1024
6. **Socket**: astrazione SW per comunicazione bidirezionale tra processi (anche su host diversi)
7. Creazione socket Python:
   ```python
   import socket
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
   ```
8. **Server TCP**:
   ```python
   s.bind((host, port))
   s.listen()
   conn, addr = s.accept()  # blocca fino a connessione
   data = conn.recv(1024)
   conn.send(data)
   ```
9. **Client TCP**:
   ```python
   s.connect((host, port))
   s.send(b"messaggio")
   data = s.recv(1024)
   ```
10. `s.close()` — chiude il socket; usare `with socket.socket(...) as s:` come context manager

## Concetti introdotti

- [[socket]]

## Domande aperte

- Nessuna

## Domande da esame

- Differenza tra TCP e UDP
- Cos'è un socket? Come si crea in Python?
- Sequenza di chiamate per un server TCP
- Cosa sono IP e porta?
