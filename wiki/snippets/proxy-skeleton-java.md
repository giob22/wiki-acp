---
tipo: snippet
tecnologia: proxy-skeleton
linguaggio: java
---

# Boilerplate — Proxy-Skeleton (Java, Socket TCP)

Implementazione manuale di RPC in Java, variante **skeleton per ereditarietà** (quella richiesta nelle prove). → [[proxy-pattern]]

## Struttura file

```
IService.java         ← interfaccia del servizio
ServiceProxy.java     ← lato client: implementa IService via Socket TCP
ServiceSkeleton.java  ← abstract: accept loop + upcall
ServerImpl.java       ← extends Skeleton, logica reale (synchronized)
Client.java           ← usa il proxy come oggetto locale
```

## Interfaccia — `IService.java`

```java
public interface IService {
    void inspect(String componentId, String status);
}
```

## Proxy (lato client) — `ServiceProxy.java`

```java
import java.io.*;
import java.net.*;

public class ServiceProxy implements IService {

    private final String host;
    private final int port;

    public ServiceProxy(String host, int port) {
        this.host = host;
        this.port = port;
    }

    @Override
    public void inspect(String componentId, String status) {
        try (Socket socket = new Socket(host, port);
             DataOutputStream out = new DataOutputStream(socket.getOutputStream());
             DataInputStream in = new DataInputStream(socket.getInputStream())) {

            // marshalling manuale: un writeUTF per ogni parametro
            out.writeUTF(componentId);
            out.writeUTF(status);
            out.flush();

            // riscontro dal server
            String ack = in.readUTF();
            System.out.println("[ACK] " + ack);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Skeleton (lato server, ereditarietà) — `ServiceSkeleton.java`

```java
import java.io.*;
import java.net.*;

public abstract class ServiceSkeleton implements IService {

    private final int port;

    public ServiceSkeleton(int port) {
        this.port = port;
    }

    // resta astratto: lo implementa la sottoclasse
    @Override
    public abstract void inspect(String componentId, String status);

    public void runSkeleton() {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("listening on port " + port);

            while (true) {
                Socket conn = serverSocket.accept();

                DataInputStream in = new DataInputStream(conn.getInputStream());
                DataOutputStream out = new DataOutputStream(conn.getOutputStream());

                // unmarshalling: stesso ordine di scrittura del proxy
                String componentId = in.readUTF();
                String status = in.readUTF();

                // upcall: invoca il metodo della sottoclasse
                this.inspect(componentId, status);

                out.writeUTF("ack");
                out.flush();
                conn.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Implementazione server — `ServerImpl.java`

```java
public class ServerImpl extends ServiceSkeleton {

    public ServerImpl(int port) {
        super(port);
    }

    @Override
    public synchronized void inspect(String componentId, String status) {
        // synchronized: mutua esclusione se lo skeleton è multithread
        System.out.println("[INSP] componentId=" + componentId + " status=" + status);
    }

    public static void main(String[] args) {
        ServerImpl server = new ServerImpl(5000);
        server.runSkeleton();
    }
}
```

## Client — `Client.java`

```java
public class Client {
    public static void main(String[] args) throws InterruptedException {
        // il client vede solo l'interfaccia: la rete è trasparente
        IService service = new ServiceProxy("localhost", 5000);

        for (int i = 0; i < 15; i++) {
            service.inspect("motor-A", "OK");
            Thread.sleep(1000);
        }
    }
}
```

## Variante: skeleton multithread

Un thread per connessione — `inspect` deve essere `synchronized` se tocca stato condiviso:

```java
while (true) {
    Socket conn = serverSocket.accept();
    new Thread(() -> {
        try (DataInputStream in = new DataInputStream(conn.getInputStream());
             DataOutputStream out = new DataOutputStream(conn.getOutputStream())) {

            String componentId = in.readUTF();
            String status = in.readUTF();
            this.inspect(componentId, status);
            out.writeUTF("ack");
            out.flush();
            conn.close();
        } catch (IOException e) { e.printStackTrace(); }
    }).start();
}
```

## Variante: skeleton per delega

Lo skeleton non è astratto ma contiene un riferimento all'implementazione:

```java
public class ServiceSkeleton {            // NON implementa IService
    private final IService delegate;      // riferimento all'impl reale

    public ServiceSkeleton(IService delegate, int port) {
        this.delegate = delegate;
        ...
    }
    // nel loop: delegate.inspect(data[0], data[1]);
}
```

## Variante: trasporto UDP

Stessa architettura, ma `DatagramSocket` + `DatagramPacket` al posto di `Socket`/`ServerSocket`. UDP è **connectionless**: niente accept loop, una sola socket serve tutti i client. È la variante dell'esempio **Contatore Remoto** delle slide → [[22-java-networking]]. Stessa `IService`.

Proxy UDP — `ServiceProxy.java`:

```java
import java.net.*;

public class ServiceProxy implements IService {

    private final InetAddress address;
    private final int port;

    public ServiceProxy(String host, int port) throws UnknownHostException {
        this.address = InetAddress.getByName(host);
        this.port = port;
    }

    @Override
    public void inspect(String componentId, String status) {
        try (DatagramSocket socket = new DatagramSocket()) {
            // marshalling manuale in stringa: campi separati da '#'
            String message = "inspect#" + componentId + "#" + status;
            byte[] data = message.getBytes();

            DatagramPacket req = new DatagramPacket(data, data.length, address, port);
            socket.send(req);

            // riscontro: buffer pre-allocato
            byte[] buf = new byte[1024];
            DatagramPacket resp = new DatagramPacket(buf, buf.length);
            socket.receive(resp);   // blocca
            System.out.println("[ACK] " + new String(resp.getData(), 0, resp.getLength()));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

Skeleton UDP — `ServiceSkeleton.java`:

```java
import java.net.*;

public abstract class ServiceSkeleton implements IService {

    private final int port;

    public ServiceSkeleton(int port) {
        this.port = port;
    }

    @Override
    public abstract void inspect(String componentId, String status);

    public void runSkeleton() {
        try (DatagramSocket socket = new DatagramSocket(port)) {   // bind sulla porta
            System.out.println("listening on port " + port);
            byte[] buf = new byte[1024];

            while (true) {
                DatagramPacket pkt = new DatagramPacket(buf, buf.length);
                socket.receive(pkt);   // blocca finché arriva un datagramma

                String message = new String(pkt.getData(), 0, pkt.getLength());
                String[] parts = message.split("#");   // ["inspect", componentId, status]

                // upcall verso la sottoclasse
                this.inspect(parts[1], parts[2]);

                // rispondi al mittente: addr e porta li dà il pacchetto ricevuto
                byte[] ack = "ack".getBytes();
                DatagramPacket resp = new DatagramPacket(
                        ack, ack.length, pkt.getAddress(), pkt.getPort());
                socket.send(resp);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

`ServerImpl.java` e `Client.java` restano identici alla variante TCP.

> 🎯 Esame: TCP→UDP. `DatagramPacket` porta sia i dati sia l'indirizzo; sul server `pkt.getAddress()`/`pkt.getPort()` danno il mittente a cui rispondere. Buffer di ricezione pre-allocato → dati extra scartati se troppo piccolo. Nessuna connessione: una `DatagramSocket` serve tutti i client → [[socket]].

## Compilazione ed esecuzione

```bash
javac *.java
java ServerImpl     # terminale 1
java Client         # terminale 2
```

> 🎯 Esame: differenza ereditarietà (ServerImpl `extends` Skeleton, metodo astratto + upcall) vs delega (Skeleton ha un campo `delegate: IService`). Le prove chiedono quasi sempre l'ereditarietà.

> 💡 Marshalling con stream tipizzati (stile slide → [[22-java-networking]]): un `write*` per ogni parametro, e sul server `read*` **nello stesso ordine**. Usa il tipo giusto: `writeUTF`/`readUTF` (String), `writeInt`/`readInt` (int), `writeDouble`/`readDouble` (double), `writeBoolean`/`readBoolean` (boolean — comodo per l'ack). Sempre `flush()` dopo le write. Niente `PrintWriter`/`BufferedReader`.

## Collegamenti

- [[proxy-pattern]] — il pattern e l'esempio Contatore Remoto UDP delle slide
- [[java-sincronizzazione]] — `synchronized` sul metodo di business
- [[proxy-skeleton-python]] — stessa architettura in Python
- [[rpc]] — stub/skeleton concettuale

## Fonti

- [[23-java-proxy-skeleton]], [[22-java-networking]], prova sim-03 (`svolgimenti/2026-06-10-sim-03/`)

_Aggiornato: 2026-06-15 — marshalling con DataInputStream/DataOutputStream (writeUTF/readUTF) al posto di PrintWriter/BufferedReader, conforme alle slide_
_Aggiornato: 2026-06-16 — aggiunta variante trasporto UDP (DatagramSocket/DatagramPacket, Contatore Remoto)_
