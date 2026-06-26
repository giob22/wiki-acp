---
tipo: concetto
importanza_esame: alta
prerequisiti: [socket, funzioni]
---

#flashcards/acp

## Definizione

**RPC (Remote Procedure Call)** è un paradigma di comunicazione tra processi distribuiti che permette a un processo di invocare funzioni su un processo remoto come se fossero locali, nascondendo la comunicazione di rete.

## Spiegazione

**Problema**: chiamare una funzione su un altro host richiede serializzazione, trasmissione, deserializzazione — complessità nascosta al programmatore.

**Soluzione RPC**: stub/skeleton generati automaticamente da un IDL.

**RPC come estensione del modello procedurale**: il modello RPC è un'**estensione ai sistemi distribuiti del modello procedurale** dei linguaggi tradizionali. Il programma `main` su un host cliente, invece di chiamare solo procedure locali (`proc1`, `proc2`...), può chiamare anche procedure che risiedono su un host servente, percependo la chiamata remota come del tutto identica a quella locale. È un modello di middleware **orientato alla comunicazione** (vedi [[middleware]]).

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
- **Sincrono e bloccante**: nei sistemi RPC la comunicazione tra processi è **intrinsecamente sincrona e bloccante** — il processo chiamante resta **sospeso fino al completamento** della procedura remota. La disponibilità di **meccanismi asincroni** (non bloccanti) in RPC è da considerarsi **un'eccezione**.
- **Trasparenza alla distribuzione**: il programmatore vede una chiamata locale
- **Accoppiamento temporale**: client e server devono essere attivi contemporaneamente

**Limiti vs MOM**:
- Se il server è giù, la chiamata RPC fallisce
- Non scala bene con N client (ogni client blocca il server per la durata della chiamata)
- Soluzione: [[mom]] con comunicazione asincrona

### Il ruolo degli stub nel dettaglio

Gli stub vengono generati **in fase di compilazione** (uno lato cliente, uno lato servente) e collegati alle due parti dell'applicazione. Implementano in maniera (in gran parte) trasparente al programmatore lo scambio parametri e la comunicazione su rete, accedendo direttamente ai servizi di trasporto dei protocolli di rete.

**Stub cliente**:
1. preleva i parametri di scambio dal chiamante;
2. li impacchetta (*marshalling*) in un messaggio e lo affida al software di rete per la trasmissione alla macchina del servente;
3. attende il messaggio di risposta che indica il completamento della procedura remota;
4. spacchetta il messaggio prelevando i valori dei parametri di uscita;
5. restituisce i parametri al programma chiamante, che riprende il controllo.

**Stub servente**:
1. attende (dal software di rete) un messaggio di invocazione;
2. spacchetta il messaggio prelevando i parametri di scambio;
3. trasmette i parametri alla procedura chiamata, cui cede il controllo;
4. al termine, impacchetta i parametri di uscita in un messaggio di risposta;
5. invia la risposta e si rimette in attesa di una nuova richiesta.

In sintesi: il **programma chiamante invoca una procedura a tutti gli effetti locale** (lo stub cliente); la **procedura remota viene invocata come procedura locale dallo stub servente**.

### Marshalling dei parametri nel dettaglio

Il *marshalling* (impacchettamento) / *unmarshalling* (spacchettamento) consiste di **due operazioni**:
- una **conversione di formato** dei dati, per tener conto delle differenze di rappresentazione tra cliente e servente, che in generale sono piattaforme eterogenee. Esempi di differenze: interi in **complemento alla base** o complemento diminuito; a parità di rappresentazione, ordinamento dei byte **big endian** o **little endian**;
- una **serializzazione (linearizzazione)** dei dati, trasformati in **sequenze di byte** secondo un formato compreso da entrambi; in particolare occorre linearizzare i dati strutturati (array e record).

Per consentire a due nodi (*sender* e *receiver*) di scambiare dati esistono **due metodi** generali:
- i dati sono convertiti dal sender in un **formato esterno concordato** tra le parti, trasmessi, e riconvertiti dal receiver nel proprio formato locale → si parla di **external data representation**;
- i dati sono trasmessi **nel formato del sender**, accompagnati da un'indicazione sul formato usato.

Alcuni approcci di external data representation / marshalling: **CORBA CDR** (Common Data Representation), **Sun XDR** (eXternal Data Representation, usato in Sun RPC), **Java object serialization**, **Protobuf** (gRPC, vedi [[protocol-buffers]]), **XML** (formato testuale).

### Semantica delle RPC

Nel paradigma RPC possono verificarsi **malfunzionamenti** nella rete o nei singoli nodi, che causano: perdita del messaggio di **richiesta**; perdita del messaggio di **risposta**; **caduta del nodo servente** dopo la ricezione della richiesta ma prima dell'invio della risposta. A seconda di come il sistema gestisce questi guasti, si distinguono quattro **semantiche** possibili:

| Semantica | Garanzia |
|---|---|
| **Exactly once** | la procedura viene eseguita **una ed una sola volta** |
| **At most once** | non garantito che sia eseguita, ma **se eseguita, una sola volta** |
| **At least once** | la procedura viene eseguita **almeno una volta** (possibili ripetizioni) |
| **Zero or more** | non è possibile dire **se** né **quante volte** è stata eseguita |

> 🎯 Esame: la semantica desiderata (es. *exactly once*) dipende dal trasporto e dai meccanismi di ritrasmissione. Operazioni **idempotenti** tollerano semantiche più deboli (*at least once*) senza effetti collaterali.

Da cosa dipende la semantica RPC e cosa tollerano le operazioni idempotenti?
?
Dipende dal trasporto e dai meccanismi di ritrasmissione. Le operazioni idempotenti tollerano semantiche più deboli (at least once) senza effetti collaterali.


### Sun RPC — un'implementazione concreta

L'implementazione di **Sun Microsystems** prevede, su una macchina servente, un **programma** che contiene una o più **procedure** invocabili remotamente:
- le procedure dello stesso programma operano nello **stesso ambiente d'esecuzione**, quindi possono **condividere variabili** (dati globali condivisi);
- è possibile avere attive **più versioni** dello stesso programma su un nodo;
- una **tripla di interi `(programma, versione, procedura)`** identifica univocamente la procedura da invocare;
- è garantita la **mutua esclusione tra le procedure dello stesso programma**: al più una procedura in esecuzione in un dato istante, anche in presenza di più client;
- per l'esternalizzazione dei dati adotta lo standard **XDR**;
- si basa su **TCP o UDP**:
  - **UDP** → se il client riceve risposta, *at least once*; se non la riceve, *zero or more*. Utile per richieste brevi, bassa latenza, operazioni idempotenti, overhead basso;
  - **TCP** → se il client riceve risposta, *exactly once*; se non la riceve, *at most once*. Utile per maggiore affidabilità, messaggi grandi, comportamento prevedibile.

**Binding dinamico e port mapper** — Normalmente, nella programmazione socket TCP/UDP, client e server devono **concordare preventivamente il numero di porta**. Sun RPC adotta invece un **binding dinamico**:
- il servente ottiene **dinamicamente** una porta disponibile, ignota al client finché il server non è attivo;
- sul nodo server gira un processo **RPC port mapper** che gestisce la lista dei serventi attivi, operando su una **socket a porta prefissata (111)**, uguale per ogni nodo server;
- all'attivazione, il programma RPC **registra** presso il port mapper la coppia `(numero programma, numero porta)`;
- il client, prima di eseguire la RPC, contatta il port mapper (porta 111) presentando il numero di programma e ricevendo il numero di porta.

Algoritmo del port mapper: ① crea una socket alla porta 111; ② accetta indefinitamente richieste di **registrazione** (dai serventi) e di **ricerca** (dai clienti). Il binding dinamico realizza così la **trasparenza alla locazione**.

**Dispatcher** — Trovata la porta, il client chiama il proprio **stub locale**, che contatta lo stub opportuno tramite un componente chiamato **dispatcher**: sul nodo servente il dispatcher **inoltra i messaggi dei clienti agli opportuni stub lato server** (uno per procedura), che a loro volta invocano la procedura reale.

> 🎯 Esame: Descrivere il flusso completo di una chiamata RPC con stub e skeleton, cos'è il marshalling. Spiegare il **binding dinamico** del port mapper Sun RPC (porta 111) e come realizza la trasparenza alla locazione. Elencare le 4 semantiche RPC e collegarle a TCP/UDP.

Come funziona il binding dinamico di Sun RPC e quali sono le 4 semantiche?
?
Il server prende una porta dinamica; il port mapper (porta fissa 111) mappa (programma,versione)→porta (trasparenza di locazione). Semantiche: exactly once, at most once, at least once, zero or more (TCP→exactly/at-most; UDP→at-least/zero-or-more).


## Perché importa

RPC è il fondamento di gRPC. Capire stub/skeleton e marshalling è essenziale per usare gRPC correttamente.

## Connessioni

- [[middleware]] — RPC è un modello di middleware orientato alla comunicazione; il DOM (oggetti distribuiti) è il suo analogo a oggetti
- [[grpc]] — implementazione moderna di RPC
- [[mom]] — alternativa asincrona all'RPC
- [[socket]] — RPC usa socket TCP/UDP per la comunicazione; Sun RPC sceglie la semantica in base al trasporto
- [[protocol-buffers]] — IDL e formato di serializzazione (marshalling) usato da gRPC
- [[proxy-pattern]] — il pattern Proxy-Skeleton implementa manualmente lo schema stub/skeleton

## Fonti

- [[13-sistemi-middleware]]
- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-19 — estensione MODULO 2 (slide 13): RPC come estensione modello procedurale, ruolo stub dettagliato, marshalling (conversione formato + serializzazione + external data representation), semantica RPC (4 tipi), Sun RPC (tripla, mutua esclusione, port mapper/binding dinamico, dispatcher, TCP/UDP)_
