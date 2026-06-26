---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc, oop, ereditarieta, socket]
---

#flashcards/acp

## Definizione

Il **pattern Proxy-Skeleton** è un design pattern architetturale per sistemi distribuiti che separa la logica applicativa dai meccanismi di comunicazione client-server. È l'implementazione manuale di RPC in Java senza framework.

## Spiegazione

**Problema**: nella programmazione socket, la logica di comunicazione (serializzazione, invio, ricezione) si sovrappone alla logica applicativa.

**Soluzione**:
```
[Client]           [Proxy]          [Rete]       [Skeleton]        [ServerImpl]
   |                  |                               |                  |
   | chiama           |                               |                  |
   | metodo()  →  serializza   →→→→→→→→→→→→→→  deserializza  →  upcall metodo()
   |            e invia                            e invia         (logica reale)
   |   ←←←←←  deserializza   ←←←←←←←←←←←←←  serializza    ←←  ritorna risultato
```

**Struttura delle classi**:
```
InterfacciaServer           ← interface Java — definisce il servizio
    ↑             ↑
ServerProxy       ServerImpl   ← entrambi implementano l'interfaccia
(Proxy/stub)      (impl reale)
```

**Proxy** (lato client):
- Implementa `InterfacciaServer`
- Ogni metodo serializza i parametri, invia via socket, attende risposta, deserializza
- Il client usa l'interfaccia — ignora completamente la rete

**Skeleton** — due approcci:
1. **Per ereditarietà**: `ServerSkeleton` (abstract class) → `ServerImpl extends ServerSkeleton`
   - Skeleton gestisce comunicazione; ServerImpl implementa solo metodi astratti
2. **Per delega**: `ServerSkeleton` ha un riferimento `delegate: InterfacciaServer`
   - I metodi delegano a `delegate.Servizio1()`; ServerImpl è un oggetto separato

**Esempio Contatore Remoto** (UDP):
```java
// Interfaccia
public interface ICounter {
    void setCount(String id, int s);
    int sum(int s);
    int increment();
}

// Client usa il proxy come se fosse locale:
ICounter counter = new CounterProxy();
counter.setCount("user-ACP", 10);   // in realtà invia UDP a porta 9000

// Server:
CounterImpl counter = new CounterImpl();
counter.runSkeleton();  // avvia loop di attesa datagrammi
```

**Serializzazione manuale nel Proxy** (UDP):
```java
String message = "sum#" + s + "#";
// invia come DatagramPacket; riceve risposta; parsa stringa
```

> 🎯 Esame: Struttura Proxy-Skeleton, differenza skeleton per ereditarietà vs delega, schema concettuale della chiamata remota.

Struttura del Proxy-Skeleton e differenza ereditarietà vs delega?
?
Proxy (client) serializza/invia; Skeleton (server) deserializza/fa upcall; entrambi implementano l'interfaccia. Ereditarietà: Impl extends Skeleton (accoppiamento forte). Delega: Skeleton ha un delegate (accoppiamento debole).


## Perché importa

Il pattern Proxy-Skeleton è il modo Java per implementare RPC manualmente. gRPC genera automaticamente proxy e skeleton — capire questo pattern spiega cosa fa `protoc`.

> 💡 Connessione: Il `CounterProxy` fa esattamente ciò che fa il file `_pb2_grpc.py` generato da gRPC — un proxy che serializza e invia sulla rete.

## Connessioni

- [[rpc]] — il pattern Proxy-Skeleton è un'implementazione manuale di RPC
- [[grpc]] — gRPC genera automaticamente proxy e skeleton da `.proto`
- [[socket]] — Proxy e Skeleton comunicano via socket TCP o UDP

## Fonti

- [[23-java-proxy-skeleton]]

_Aggiornato: 2026-06-04 — ingest iniziale_
