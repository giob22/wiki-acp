---
tipo: fonte
titolo: "Sistemi Middleware"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [middleware, rpc, stub, skeleton, idl, trasparenza, sistemi-distribuiti]
---

## Sommario

Slide sui sistemi middleware (20 pagine). Si introduce il concetto di middleware come strato software che disaccoppia applicazioni distribuite dall'infrastruttura di rete. Si tratta in dettaglio il paradigma RPC (Remote Procedure Call) con i concetti di IDL, stub/skeleton, e trasparenza alla distribuzione.

## Punti chiave

1. **Middleware** = software che si interpone tra applicazioni e sistema operativo/rete; fornisce servizi di comunicazione ad alto livello
2. Problema fondamentale dei sistemi distribuiti: **eterogeneità** (linguaggi, OS, protocolli diversi)
3. **RPC (Remote Procedure Call)**: paradigma che permette di chiamare funzioni su macchine remote come se fossero locali
4. Componenti RPC:
   - **IDL (Interface Definition Language)**: linguaggio neutro per descrivere l'interfaccia del servizio
   - **Stub client**: codice generato automaticamente; riceve la chiamata locale, la serializza (marshalling) e la invia
   - **Skeleton server**: codice generato automaticamente; riceve il messaggio, lo deserializza (unmarshalling) e chiama la funzione reale
5. **Marshalling**: processo di serializzazione dei parametri per la trasmissione in rete
6. **Trasparenza alla distribuzione**: il programmatore invoca metodi remoti come se fossero locali
7. Classificazione middleware:
   - **RPC**: chiamate sincrone, procedural
   - **MOM**: asincrono, basato su messaggi
   - **Object-oriented**: CORBA, RMI
8. Limiti RPC: accoppiamento temporale (client e server devono essere attivi contemporaneamente)

## Concetti introdotti

- [[rpc]]
- [[mom]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è il middleware? Perché è necessario nei sistemi distribuiti?
- Come funziona RPC? Descrivere il ruolo di stub e skeleton
- Cos'è il marshalling?
- Differenza tra middleware RPC e MOM
