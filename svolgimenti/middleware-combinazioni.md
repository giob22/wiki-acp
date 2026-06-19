# Combinazioni middleware — prove svolgimenti

Catalogo di tutti i middleware usati nelle prove simulate e delle **combinazioni** su cui mi sono esercitato (o che restano da fare). Aggiornare ad ogni nuova prova.

## Legenda middleware

| Sigla | Middleware | Trasporto / ruolo | Pagina wiki |
| --- | --- | --- | --- |
| **TCP** | Socket TCP raw (pattern proxy-skeleton) | RPC su socket | [[socket]] · [[proxy-pattern]] |
| **gRPC** | gRPC + Protocol Buffers | RPC tipato HTTP/2 | [[grpc]] · [[protocol-buffers]] |
| **JMS** | JMS su ActiveMQ (OpenWire 61616) | MOM, lato Java | [[jms]] · [[activemq]] · [[mom]] |
| **STOMP** | STOMP su ActiveMQ (61613) | MOM, lato Python | [[stomp-python]] · [[mom]] · [[pub-sub]] |
| **REST** | REST / HTTP su Flask | request-response | [[rest]] · [[flask]] |
| **Mongo** | MongoDB | persistenza NoSQL | [[mongodb]] · [[nosql]] |

> Legenda stato: ✅ svolta (codice presente) · ⬜ da fare (solo `prova.md`).

## Tabella prove

| Prova | Data | Linguaggi | Combinazione middleware | Stato | Link |
| --- | --- | --- | --- | --- | --- |
| sim-01 | 2026-06-08 | Python | **TCP** + **REST** + **Mongo** | ✅ | [prova](2026-06-08-sim-01/prova.md) |
| sim-02 | 2026-06-09 | Python + Java | **gRPC** + **STOMP** + **JMS** | ✅ | [prova](2026-06-09-sim-02/prova.md) |
| sim-03 | 2026-06-10 | Java + Python | **TCP** + **JMS** (topic) + **STOMP** (topic) | ⬜ | [prova](2026-06-10-sim-03/prova.md) |
| sim-04 | 2026-06-10 | Python | **gRPC** + **REST** | ⬜ | [prova](2026-06-10-sim-04/prova.md) |
| sim-05 | 2026-06-14 | Python | **TCP** + **REST** | ✅ | [prova](2026-06-14-sim-05/prova.md) |
| sim-06 | 2026-06-15 | Java + Python | **TCP** + **STOMP/JMS** (topic) + **REST** | ⬜ | [prova](2026-06-15-sim-06/prova.md) |
| sim-07 | 2026-06-15 | Python | **STOMP** (request/response topic) + **REST** + **Mongo** | ✅ | [prova](2026-06-15-sim-07/prova.md) |
| sim-08 | 2026-06-15 | Java + Python | **TCP** + **REST** + **Mongo** | ✅ | [prova](2026-06-15-sim-08/prova.md) |
| sim-09 | 2026-06-16 | Java | **gRPC** + **JMS** (queue) | ✅ | [prova](2026-06-16-sim-09/prova.md) |
| sim-10 | 2026-06-17 | Python | **gRPC** + **STOMP** | ✅ | [pdf](2026-06-17-sim-10/2025-06-20.pdf) |
| sim-11 | 2026-06-18 | Python | **TCP** + **REST** + **Mongo** | ✅ | [prova](2026-06-18-sim-11/prova.md) |

## Combinazioni distinte (riepilogo)

| Combinazione | Prove | Stato copertura |
| --- | --- | --- |
| TCP + REST + Mongo | sim-01 ✅, sim-08 ✅, sim-11 ✅ | esercitata |
| TCP + REST | sim-05 ✅ | esercitata |
| gRPC + STOMP + JMS | sim-02 ✅ | esercitata |
| gRPC + JMS | sim-09 ✅ | esercitata |
| gRPC + STOMP | sim-10 ✅ | esercitata |
| gRPC + REST | sim-04 ⬜ | **mai svolta** |
| TCP + JMS + STOMP (topic) | sim-03 ⬜ | **mai svolta** |
| TCP + STOMP/JMS + REST | sim-06 ⬜ | **mai svolta** |
| STOMP + REST + Mongo | sim-07 ✅ | esercitata |

## Da fare (priorità per copertura)

- **sim-04** → [prova](2026-06-10-sim-04/prova.md): unica con **gRPC + REST** puro (server gRPC Python + coda con `Condition`, `maxsize=5`). → [[grpc]] [[rest]]
- **sim-03** → [prova](2026-06-10-sim-03/prova.md): unica con stesso messaggio diffuso su **JMS topic** (Java) **e STOMP topic** (Python) — utile per [[pub-sub]] e [[sottoscrizioni-durabili]].
- **sim-06** → [prova](2026-06-15-sim-06/prova.md): catena ibrida **TCP → topic → REST/Flask** con 3 hop di middleware diversi.

## Collegamenti

- [[pattern-esame]] — pattern ricorrenti nelle prove
- [[middleware-trasparenza]] — confronto trasparenze tra i middleware
- [[mom]] · [[pub-sub]] · [[rpc]] — famiglie di middleware

_Aggiornato: 2026-06-18 — sim-11 svolta (TCP + REST + Mongo)_
