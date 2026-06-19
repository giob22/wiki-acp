---
tipo: fonte
titolo: "Java — Proxy, Skeleton e oggetti remoti"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [java, proxy, skeleton, rpc, pattern, delega, ereditarieta, udp, interfaccia]
---

## Sommario

Slide sulla realizzazione di oggetti remoti in Java tramite pattern Proxy-Skeleton (27+ pagine). Si tratta il problema della separazione tra logica applicativa e meccanismi di comunicazione, il pattern Proxy (lato client), il Skeleton per ereditarietà e per delega (lato server), e un esempio completo con socket UDP (Contatore Remoto).

## Punti chiave

1. **Problema**: in applicazioni client-server con socket, la logica di comunicazione (connessione, serializzazione, invio, ricezione) si mescola con la logica applicativa
2. **Soluzione**: separare le due responsabilità
   - Lato client: usa un'**interfaccia** e un oggetto **Proxy** che implementa l'interfaccia ma al suo interno gestisce la comunicazione
   - Lato server: usa un oggetto **Skeleton** che gestisce la comunicazione e fa **upcall** all'oggetto reale
3. **Pattern Proxy** (lato client):
   - `InterfacciaServer` — interfaccia Java che definisce il servizio
   - `ServerProxy implements InterfacciaServer` — implementa i metodi serializzando e inviando via socket
   - `ServerImpl implements InterfacciaServer` — implementazione reale lato server
   - Il client usa solo `InterfacciaServer` — non sa se è locale o remoto
4. **Skeleton per Ereditarietà**:
   - `ServerSkeleton` (classe astratta) — implementa comunicazione, lascia metodi dell'interfaccia astratti
   - `ServerImpl extends ServerSkeleton` — implementa solo la logica applicativa
5. **Skeleton per Delega**:
   - `ServerSkeleton` ha riferimento a `InterfacciaServer` (delegate)
   - I metodi delegano: `void Servizio1() { delegate.Servizio1(); }`
6. **Schema concettuale** (equivalente a RPC):
   - Client → chiama Proxy (locale) → Proxy invia messaggio via rete → Skeleton riceve → upcall all'oggetto remoto → risposta percorre path inverso
7. **Esempio Contatore Remoto** (socket UDP):
   - Interfaccia: `ICounter` con `setCount(id, s)`, `sum(s)`, `increment()`
   - `CounterProxy implements ICounter` — serializza i parametri come stringa `"sum#15#"`, invia via `DatagramSocket` su porta 9000, attende risposta
   - `CounterSkeleton` / `CounterImpl` — skeleton riceve datagramma, fa dispatch al metodo giusto su `CounterImpl`
   - `CounterWorker extends Thread` — worker thread che gestisce ogni richiesta
   - Client: `ICounter counter = new CounterProxy(); counter.setCount("user-ACP", 10);`
   - Server: `CounterImpl counter = new CounterImpl(); counter.runSkeleton();`

## Concetti introdotti

- [[proxy-pattern]]
- [[rpc]]
- [[java-threading]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è il pattern Proxy? Quando si usa nella programmazione client-server?
- Differenza tra Skeleton per ereditarietà e per delega
- Descrivere il flusso end-to-end di una chiamata con Proxy-Skeleton
- Struttura delle classi nell'esempio Contatore Remoto
