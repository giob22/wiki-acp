---
tipo: fonte
titolo: "Prove d'esame ACP 2023-2024"
data_ingest: 2026-06-07
formato: esercizi
argomenti: [socket, stomp, jms, grpc, flask, mongodb, proxy-skeleton, multiprocessing, threading, produttore-consumatore]
---

## Sommario

Raccolta di 5 prove pratiche d'esame (Nov 2023 – Ott 2024). Ogni prova richiede di implementare un sistema distribuito con 3-4 componenti che comunicano via protocolli misti. Durata sempre 120 minuti. Il codice deve essere funzionante e verificato dalla commissione.

---

## Prove

### 2023-11-06 — Sistema di stampa (Python, Socket + STOMP)

**Componenti:** User · Printer Server · BW Printer · Color Printer

**Flusso:**
- User → `print(pathFile, tipo)` → Proxy TCP → Printer Server (Skeleton per ereditarietà)
- Printer Server: processo produttore → `multiprocessing.Queue` → processo consumatore → STOMP
- STOMP Queue `color` se tipo=color, STOMP Queue `bw` altrimenti
- BW Printer: parametro CLI `bw|gs` → filtra → scrive `bw.txt`
- Color Printer: parametro CLI `doc|txt` → filtra → scrive `color.txt`

**Tecnologie:** Socket TCP, proxy-skeleton per ereditarietà (`IPrinter`), `multiprocessing.Queue`, STOMP Queue

**Punti chiave:**
- 10 richieste, 1 sec tra l'una e l'altra
- pathFile = `/user/file_{0-100}.{doc|txt}` generato casualmente
- tipo = `bw | gs | color` casuale

---

### 2024-03-19 — Sistema biglietti concerti (Java + Python, JMS + STOMP)

**Componenti:** Client (Java) · Manager (Java) · Stats (Python)

**Flusso:**
- Client → JMS Topic `request` → MapMessage `{type: buy|stats, value: artista|"Sold"}`
- Manager: listener JMS → se `buy` → scrive `tickets.txt` + JMS Topic `tickets`; se `stats` → JMS Topic `stats`
- Stats: listener STOMP su `tickets` → processo produttore → `multiprocessing.Queue`; listener STOMP su `stats` → se `value==Sold` → processo consumatore → svuota queue → dizionario conteggi → `stats.txt`

**Tecnologie:** JMS Topic (`request`, `tickets`, `stats`), STOMP, MapMessage, TextMessage, `multiprocessing.Queue`

**Punti chiave:**
- Client lancia da CLI: `java Client buy` o `java Client stats`
- 20 richieste, 2 sec tra l'una e l'altra
- Test: 2 Client (buy + stats), 1 Manager, 1 Stats
- stats.txt: per ogni artista → numero biglietti venduti

---

### 2024-06-26 — Compravendita laptop (Python, gRPC + Flask)

**Componenti:** User · Product Manager (gRPC) · History Server (Flask)

**Flusso:**
- User: 10 thread → ciascuno chiama `sell(serial_number)` o `buy()` via gRPC
- Product Manager: `sell` → inserisce in `laptop_queue` (lista, Condition, maxsize=5); `buy` → preleva dalla queue; entrambi → POST `/update_history` su History Server prima di ritornare
- History Server: `POST /update_history` → scrive append `{operation}-{serial_number}` su `history.txt`

**Tecnologie:** gRPC (metodi `sell`, `buy`), Flask REST, threading, lista + Condition

**Punti chiave:**
- `buy` ritorna `serial_number` estratto; `sell` ritorna `bool` ack
- Queue implementata con **lista** (non `queue.Queue`) + `Condition` — maxsize=5
- POST avviene **prima** di ritornare al chiamante gRPC

---

### 2024-07-26 — Prenotazione hotel (Python, STOMP + Flask + MongoDB)

**Componenti:** Operator · Booking Manager · DB Server (Flask + MongoDB)

**Flusso:**
- Operator: 6 thread (4 × CREATE, 2 × UPDATE) → frame STOMP su topic `request`; risposta asincrona su topic `response`
- Booking Manager: listener STOMP su `request` → parse tipo (CREATE/UPDATE) → POST/PATCH al DB Server → risposta → frame STOMP su topic `response`
- DB Server (Flask + MongoDB):
  - `POST /booking` → crea documento MongoDB con tutti i campi
  - `PATCH /booking` → aggiorna costo (`max(0, cost - discount)`) dove `operator==op AND nights>=N`

**Tecnologie:** STOMP Topic, Flask REST, MongoDB PyMongo, threading

**Punti chiave:**
- Operator riceve il proprio username da CLI
- UPDATE: sconto applicato solo a prenotazioni dello stesso operator E con nights ≥ soglia
- Costo non può scendere sotto 0

---

### 2024-10-18 — Gestione log (Java, Socket + JMS)

**Componenti:** Service · Logging Server · Error Checker · Info Filter

**Flusso:**
- Service → `log(messaggioLog, tipo)` → Proxy TCP → Logging Server (Skeleton per ereditarietà)
- Logging Server: ogni `log()` avvia un **thread** → MapMessage JMS → Queue `error` se tipo=2, Queue `info` altrimenti; `log()` in mutua esclusione
- Error Checker: parametro CLI `fatal|exception` → filtra → scrive `error.txt`
- Info Filter: filtra tipo==1 → scrive `info.txt`

**Tecnologie:** Socket TCP, proxy-skeleton per ereditarietà (`ILogging`), JMS Queue (`error`, `info`), MapMessage, synchronized

**Punti chiave:**
- tipo: 0=DEBUG, 1=INFO, 2=ERROR
- messaggioLog: `success|checking` se tipo 0-1; `fatal|exception` se tipo 2
- 10 entry, 1 sec tra l'una e l'altra
- `log()` deve essere thread-safe (synchronized)

---

## Schema tecnologie per prova

| Data | Lingua | Comm. 1 | Comm. 2 | Comm. 3 | Concorrenza |
|------|--------|---------|---------|---------|-------------|
| 2023-11 | Python | Socket TCP | STOMP Queue | — | multiprocessing |
| 2024-03 | Java+Python | JMS Topic | STOMP Topic | — | multiprocessing |
| 2024-06 | Python | gRPC | Flask REST | — | threading (lista+Condition) |
| 2024-07 | Python | STOMP Topic | Flask REST | MongoDB | threading |
| 2024-10 | Java | Socket TCP | JMS Queue | — | threading |

---

## Punti chiave

1. Ogni prova ha sempre 3-4 componenti con architettura a layer
2. Il client genera sempre N richieste con sleep (10 o 20, 1-2 sec)
3. Sempre produttore/consumatore — `multiprocessing.Queue` (process-safe) o `lista + Condition` (thread-safe)
4. Sempre scrittura su file da parte del consumatore finale
5. Routing messaggi su canali diversi in base a un campo (`tipo`, `type`, etc.)
6. Quando c'è Socket TCP → sempre proxy-skeleton per ereditarietà
7. Quando thread/processi multipli accedono allo stesso metodo → mutua esclusione esplicita

## Concetti introdotti

- [[pattern-esame]] — analisi dei pattern ricorrenti estratti da queste prove
- [[proxy-pattern]] — usato in 2023-11 (Python) e 2024-10 (Java)
- [[multiprocessing]] — Queue process-safe in 2023-11 e 2024-03
- [[threading]] — lista+Condition in 2024-06 e 2024-07
- [[jms]] — usato in 2024-03 e 2024-10
- [[mom]] — STOMP in 2023-11, 2024-03, 2024-07
- [[grpc]] — usato in 2024-06
- [[flask]] — usato in 2024-06 e 2024-07
- [[mongodb]] — usato in 2024-07
- [[socket]] — usato in 2023-11 e 2024-10

## Domande aperte

- `lista + Condition` vs `queue.Queue` — sono intercambiabili? (in 2024-06 la lista è esplicitamente richiesta)
- In 2024-03 il testo usa `artist` ma il MapMessage usa `value` — incoerenza nella traccia originale

## Domande da esame

1. Descrivi il pattern proxy-skeleton per ereditarietà. Come differisce dalla delega?
2. Quando usare `multiprocessing.Queue` vs `threading.Condition + lista`?
3. Come implementare il routing di messaggi STOMP su queue diverse in base al contenuto?
4. Qual è la differenza tra JMS Queue e JMS Topic? Quando usarli?
5. In gRPC, dove avviene la serializzazione? Chi genera proxy e skeleton?

_Aggiornato: 2026-06-07 — ingest 5 prove d'esame 2023-2024_
