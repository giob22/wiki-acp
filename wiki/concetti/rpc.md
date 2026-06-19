---
tipo: concetto
importanza_esame: alta
prerequisiti: [socket, funzioni]
---

## Definizione

**RPC (Remote Procedure Call)** è un paradigma di comunicazione tra processi distribuiti che permette a un processo di invocare funzioni su un processo remoto come se fossero locali, nascondendo la comunicazione di rete.

## Spiegazione

**Problema**: chiamare una funzione su un altro host richiede serializzazione, trasmissione, deserializzazione — complessità nascosta al programmatore.

**Soluzione RPC**: stub/skeleton generati automaticamente da un IDL.

**Componenti architetturali**:
```
[Client]                              [Server]
  |                                       |
  | chiama f(args) localmente             |
  ↓                                       |
[Stub client]                      [Skeleton server]
  | marshalling (serializza args)    | unmarshalling (deserializza)
  | invia su rete →→→→→→→→→→→→→→→→ | riceve dalla rete
  |                                   | chiama f_reale(args)
  | riceve risposta ←←←←←←←←←←←←←← | serializza risultato
  | unmarshalling                     |
  ↓                                   |
[Client] riceve risultato              |
```

**IDL (Interface Definition Language)**:
- Linguaggio neutro per descrivere l'interfaccia del servizio
- In gRPC: file `.proto`
- Genera automaticamente stub (client) e skeleton (server) per ogni linguaggio supportato

**Marshalling / Unmarshalling**:
- **Marshalling**: serializzare i parametri in un formato trasmissibile (binario, JSON, XML...)
- **Unmarshalling**: deserializzare il formato ricevuto nei tipi nativi del linguaggio

**Caratteristiche RPC**:
- **Sincrono**: il client si blocca in attesa della risposta (di default)
- **Trasparenza alla distribuzione**: il programmatore vede una chiamata locale
- **Accoppiamento temporale**: client e server devono essere attivi contemporaneamente

**Limiti vs MOM**:
- Se il server è giù, la chiamata RPC fallisce
- Non scala bene con N client (ogni client blocca il server per la durata della chiamata)
- Soluzione: [[mom]] con comunicazione asincrona

> 🎯 Esame: Descrivere il flusso completo di una chiamata RPC con stub e skeleton, cos'è il marshalling.

## Perché importa

RPC è il fondamento di gRPC. Capire stub/skeleton e marshalling è essenziale per usare gRPC correttamente.

## Connessioni

- [[grpc]] — implementazione moderna di RPC
- [[mom]] — alternativa asincrona all'RPC
- [[socket]] — RPC usa socket TCP per la comunicazione
- [[protocol-buffers]] — IDL e formato di serializzazione usato da gRPC

## Fonti

- [[13-sistemi-middleware]]
- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-04 — ingest iniziale_
