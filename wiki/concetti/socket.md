---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, threading]
---

#flashcards/acp

## Definizione

Un **socket** è un'astrazione software che rappresenta un endpoint di comunicazione **tra processi** (eventualmente distribuiti su macchine differenti), **basata sulla rete**: fornisce ai processi il meccanismo per accedere alla rete. Nata con **Unix 4.2 BSD (1983)**. Una socket è caratterizzata da **(indirizzo IP, numero di porta)** del nodo e può essere di tipo **TCP** o **UDP**.

## Spiegazione

### Internet e stack ISO/OSI

**Internet** = rete di reti basata su **TCP/IP** (progenitrice **ARPANET**, 1969, ARPA/Dip. Difesa USA). Componenti: **nodi/host** (PC, server, smartphone), **link** di comunicazione (cavi, fibra, radio), **router** (instradano i messaggi).

**Stack ISO/OSI** (7 livelli) con **incapsulamento** (ogni livello aggiunge il proprio header):

| Liv | Nome | Esempi | Header info |
|-----|------|--------|-------------|
| 7 | Application | HTTP, FTP, DNS, SMTP | — |
| 6 | Presentation | JPEG, MPEG | — |
| 5 | Session | **RPC (Sockets)** | — |
| 4 | Transport | **TCP, UDP** | source/dest **port**, sequence |
| 3 | Network | **IP**, ICMP, IPSec | source/dest **IP**, datagram order |
| 2 | Data Link | ARP, VLAN, Ethernet | source/dest **MAC** |
| 1 | Physical | Hub, fibra | bit |

### IP, datagram, indirizzi

**Indirizzo IP** identifica un nodo sulla rete:
- **IPv4**: 32 bit (~4,3 mld indirizzi), 4 campi da 8 bit `192.168.0.4`;
- **IPv6**: 128 bit, 8 campi da 16 bit `2001:0db8:...:7344`.
- Host remoti riferiti con nomi simbolici (`www.unina.it`); traduzione nome↔indirizzo via **DNS** (Domain Name Service).

**IP datagram**: i dati end-to-end viaggiano in pacchetti, dimensione max **65.535 byte (64KB)**. IP è un **servizio best-effort**: i pacchetti possono arrivare **corrotti, duplicati, fuori ordine o essere persi**.

### TCP vs UDP

|              | TCP                                                                   | UDP                     |
| ------------ | --------------------------------------------------------------------- | ----------------------- |
| Connessione  | Sì (orientato alla connessione: instaura/usa/chiude)                  | No (**connectionless**) |
| Affidabilità | **Affidabile** (ritrasmissione)                                       | **Non affidabile**      |
| Ordine       | Garantito (elimina duplicati)                                         | Non garantito           |
| Modello      | Flusso di byte **full-duplex**                                        | **Datagramma**          |
| Uso          | HTTP dalla versione `1.0` alla `2.0`, gRPC (HTTP/2), STOMP (HTTP/1.1) | DNS, video streaming    |

- **TCP** (Transmission Control Protocol): trasporto affidabile su IP; flusso di byte, full-duplex, preserva l'ordine, ritrasmette i pacchetti persi. *(Costruito sopra IP, che è best-effort.)*
- **UDP** (User Datagram Protocol): trasporto non affidabile; molto simile a IP ma **distingue tra porte diverse** sullo stesso host; basato sul **datagramma**.

**Porta**: identifica il processo/servizio (0–65535; < 1024 = well-known). Esempi: 20/21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 69 TFTP (udp), 80 HTTP.

### Socket in Python

```python
import socket
s = socket.socket(socket_family, socket_type)
```
- **socket_family**: `AF_INET` (IPv4, default), `AF_INET6` (IPv6), `AF_UNIX` (Unix Domain Sockets, IPC locale), `AF_CAN`, `AF_PACKET`, `AF_RDS`.
- **socket_type**: `SOCK_STREAM` (TCP, default), `SOCK_DGRAM` (UDP), `SOCK_RAW` (accesso diretto al protocollo di livello inferiore).

> 💡 Tutte le funzioni del modulo `socket` sono **wrapper alle syscall** dell'OS (in Linux le socket Berkeley). A `strace` si vedono `socket()/bind()/listen()/accept4()/recvfrom()/sendto()/close()`; la socket aperta è un file descriptor (`/proc/PID/fd/N → socket:[inode]`), stato LISTEN = `0x0A`.

**Funzioni principali**:

| Funzione           | Ruolo                                                                                              |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| `socket()`         | crea la socket                                                                                     |
| `bind(address)`    | associa la socket a `(IP, porta)` — **porta 0 ⇒ OS sceglie il primo porto libero**                 |
| `listen(backlog)`  | mette in ascolto (TCP); `backlog` = max connessioni in coda                                        |
| `accept()`         | (TCP) blocca, accetta una connessione → ritorna **`(conn, addr)`** (nuova socket + indirizzo peer) |
| `connect(address)` | (client) apre connessione verso `(IP, porta)`                                                      |
| `getsockname()`    | indirizzo locale della socket (utile con porta 0: `s.getsockname()[1]`)                            |
| `close()`          | chiude la socket                                                                                   |

**Indirizzi speciali**:
- **`localhost`** → si risolve in `127.0.0.1` (IPv4) o `::1` (IPv6); in `bind()` accetta solo connessioni dalla stessa macchina.
- **`127.0.0.1`**: loopback, esplicitamente IPv4; nodi esterni non possono collegarsi.
- **`0.0.0.0`**: **wildcard** = "tutte le interfacce di rete"; in `bind()` il server ascolta anche da host esterni. **Non valido in `connect()`**.

### Scambio dati

**TCP** (socket connessa): `send(string)` invia, `recv(bufsize)` riceve (ritorna stringa, max `bufsize` byte). I dati viaggiano come **byte** → `encode("utf-8")` / `decode("utf-8")`.

**Flusso TCP**:
```
Client:  socket → connect → send → recv → close
Server:  socket → bind → listen → accept → recv → send → close
```

**UDP** (connectionless): `sendto(string, address)` (destinazione esplicita, socket non connessa), `recvfrom(bufsize)` → ritorna **`(string, address)`** (dati + mittente).

**Flusso UDP** (no listen/accept lato server):
```
Client:  socket → sendto → recvfrom → close
Server:  socket → bind → recvfrom → sendto → close
```

**Numero di socket usate**: TCP = **3** (server: 1 di ascolto da `socket()` + 1 di connessione da `accept()`; client: 1 da `connect()`). UDP = **2** (1 server + 1 client).

### Server Multithread / Multiprocess

Migliorano l'efficienza creando **più thread/process** per gestire le richieste. ⚠️ **La socket NON è thread/process-safe** → servono modelli d'uso precisi:

- **TCP**: il thread principale gestisce la **socket di ascolto** (`listen`); `accept()` crea una **nuova socket di connessione** passata a **un solo** thread/process (non condivisa). Il worker esegue `recv()/send()/close()` su quella socket.
  ```python
  while True:
      c, addr = s.accept()
      t = threading.Thread(target=thd_fun, args=(c,))   # o mp.Process
      t.start()
  ```
- **UDP**: c'è **una sola socket server condivisa** da tutti. La `recvfrom()` va fatta **nel thread principale** (NON in un figlio); il worker riceve dati+address+socket e si limita a **elaborare e rispondere con `sendto()`**.
  ```python
  while True:
      data, addr = s.recvfrom(buffer_size)
      t = threading.Thread(target=thd_fun, args=(s, data, addr), daemon=True)
      t.start()
  ```

> 🎯 Esame: sequenza server TCP (`bind→listen→accept→recv/send`); differenza TCP/UDP; perché la socket UDP condivisa va letta solo nel main thread; numero di socket TCP (3) vs UDP (2).

Sequenza di un server TCP e numero di socket TCP vs UDP?
?
socket→bind→listen→accept→recv/send→close. TCP usa 3 socket (server: ascolto + connessione da accept; client: 1). UDP usa 2 socket; la socket UDP condivisa va letta solo nel main thread.


### Dal socket grezzo al Proxy-Skeleton

Un'applicazione client-server **basata su socket** richiede meccanismi di: connessione, **esternalizzazione** dei dati (marshalling), invio-ricezione richieste, **ricostruzione** dei valori. Rischio: l'implementazione della comunicazione **distrae** dalla logica applicativa e le due logiche si **sovrappongono**. Soluzione: separare logica applicativa e comunicazione → il **pattern Proxy-Skeleton** (introdotto qui, slide 12) incapsula i meccanismi di basso livello (TCP/UDP). Dettaglio completo → [[proxy-pattern]], snippet → [[proxy-skeleton-python]] / [[proxy-skeleton-java]].

### Utility di rete (Linux)
`ip a` (interfacce), `netstat -tulpn` (stato IP:PORTA in ascolto + PID), `ping IP_HOST` (pacchetti ICMP).

## Perché importa

I socket sono il fondamento di tutto il networking del corso: gRPC, STOMP/ActiveMQ e Flask comunicano tutti su socket TCP. Nelle prove pratiche il **proxy-skeleton su socket TCP multi-thread** è uno scheletro ricorrente → [[pattern-esame]].

## Connessioni

- [[threading]] — i server socket usano thread per gestire più client; socket non thread-safe → modelli TCP/UDP
- [[multiprocessing]] — variante multi-process del server (`mp.Process`)
- [[proxy-pattern]] — Proxy-Skeleton: separa logica applicativa dai meccanismi socket; skeleton per ereditarietà/delega
- [[rpc]] — RPC vive a livello session (Sockets); gRPC usa socket TCP via HTTP/2
- [[mom]] — ActiveMQ/STOMP usa socket TCP
- [[rest]] — HTTP/Flask sopra socket TCP

## Fonti

- [[12-python-networking]]

_Aggiornato: 2026-06-20 — MODULO 5: riscrittura completa (Internet/OSI/IP/datagram, TCP/UDP dettaglio, socket family/type, funzioni+porta 0, localhost/127/0.0.0.0, send/recv vs sendto/recvfrom, numero socket, server multithread/multiprocess TCP+UDP, link Proxy-Skeleton, utility Linux)_
