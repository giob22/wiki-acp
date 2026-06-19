---
tipo: fonte
titolo: "Java — Socket e networking client-server"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [java, socket, serversocket, tcp, udp, datagramsocket, datagrampacket, multithread, stream]
---

## Sommario

Slide su programmazione di rete in Java. Si trattano `Socket` e `ServerSocket` per TCP, stream tipizzati (`DataInputStream`/`DataOutputStream`), server multithread, e `DatagramSocket`/`DatagramPacket` per UDP.

## Punti chiave

1. Java fornisce `Socket` (client TCP) e `ServerSocket` (server TCP) nel package `java.net`
2. **Server TCP**:
   ```java
   ServerSocket server = new ServerSocket(port);  // backlog default = 50
   Socket client = server.accept();  // blocca fino a connessione
   // usa client.getInputStream() / client.getOutputStream()
   ```
3. **Client TCP**:
   ```java
   Socket conn = new Socket(host, port);  // esegue 3-way handshake
   ```
4. `ServerSocket` costruttori: `(port)`, `(port, backlog)`, `(port, backlog, InetAddress)`
5. `accept()` restituisce un nuovo oggetto `Socket` per la connessione con il client
6. Chiamando `accept()` di nuovo il server si rimette in attesa di nuove connessioni
7. **Comunicazione**: `conn.getInputStream()` e `conn.getOutputStream()` — raw bytes
8. **Stream tipizzati** (raccomandati):
   ```java
   DataInputStream in = new DataInputStream(new BufferedInputStream(s.getInputStream()));
   int val = in.readInt();
   String str = in.readUTF();
   ```
9. **Server Multithread**: per ogni connessione si crea un Worker Thread:
   ```java
   while(true) {
       Socket client = server.accept();
       MyWorker worker = new MyWorker(client);
       worker.start();
   }
   // MyWorker extends Thread; nel run() legge/scrive su InputStream/OutputStream
   ```
10. **UDP** — `DatagramSocket` + `DatagramPacket`:
    - `DatagramPacket`: contiene `address` + `data`
    - `DatagramSocket.send(pkt)` / `receive(pkt)` (blocca)
    - Buffer di ricezione pre-allocato; dati extra scartati se buffer troppo piccolo
    - UDP è connectionless → stessa socket per destinazioni diverse

## Concetti introdotti

- [[socket]]
- [[java-threading]]

## Domande aperte

- Nessuna

## Domande da esame

- Sequenza server TCP in Java: classi e metodi usati
- Cosa fa `accept()`? Cosa restituisce?
- Come realizzare un server multithread in Java?
- Differenza tra `DataInputStream` e `InputStream` raw
- Come si invia/riceve un datagramma UDP in Java?
