---
tipo: concetto
importanza_esame: alta
prerequisiti: [socket, rpc]
---

## Definizione

**REST (Representational State Transfer)** è uno stile architetturale per sistemi distribuiti che espone **risorse** identificate da **URI** e le manipola tramite un'**interfaccia uniforme** (metodi HTTP). È **stateless**: ogni richiesta è autocontenuta.

## Spiegazione

**Concetti chiave**:

**Risorsa**: entità indirizzabile tramite web — accessibile e trasferibile tra client e server.

**URI (Uniform Resource Identifier)**:
```
foo://example.com:8042/over/there?name=ferret#nose
  ↑        ↑           ↑          ↑           ↑
scheme  authority     path      query      fragment
```

**URI Template**: pattern parametrico — `http://service.com/order/{oid}/item/{iid}`

**Interfaccia uniforme** — metodi HTTP:

| Metodo | CRUD | Semantica | Safe | Idempotente |
|--------|------|-----------|------|-------------|
| GET    | Read | Recupera risorsa | SÌ | SÌ |
| POST   | Create | Crea sotto-risorsa | NO | NO |
| PUT    | Update | Crea o aggiorna all'URI | NO | SÌ |
| DELETE | Delete | Elimina risorsa | NO | SÌ |

- **Safe**: non altera lo stato del server (read-only)
- **Idempotente**: richieste identiche producono sempre lo stesso risultato

**Stateless**: il server non mantiene stato tra richieste — ogni richiesta è completa di tutte le info necessarie.

**RPC vs REST**:
- RPC: vocabolario custom per ogni servizio (`insertOrder()`, `deleteOrder()`...)
- REST: vocabolario fisso (HTTP verbs) — tutti i servizi REST hanno la stessa interfaccia base

**Esempio CRUD su Orders**:
```
POST   /Orders/8    → CREATE nuovo ordine
GET    /Orders/1    → READ ordine 1
PUT    /Orders/12   → UPDATE ordine 12
DELETE /Orders/12   → DELETE ordine 12
```

**URI best practices**:
- Usare **nomi** non verbi: `DELETE /book/15` OK, `GET /book?action=delete` NO
- POST crea risorsa **figlia** rispetto al padre; PUT crea o modifica all'URI esatto

**Formati rappresentazione**: JSON e XML (testuali); JSON è dominante nell'ecosistema REST moderno.

**Progettazione REST** (passi):
1. Identificare le risorse da esporre
2. Definire le URI
3. Scegliere i metodi HTTP adeguati per ogni risorsa
4. Definire le rappresentazioni (JSON, XML)

> 🎯 Esame: Definire safe e idempotente con esempi, differenza POST/PUT, principi REST (stateless, uniform interface).

## Perché importa

REST è l'architettura dominante per API web. Flask nel corso è usato per creare API RESTful.

## Connessioni

- [[rpc]] — confronto: RPC sincrono/procedurale vs REST resource-oriented
- [[protocol-buffers]] — gRPC usa protobuf binario; REST usa JSON testuale
- [[nosql]] — MongoDB è tipicamente esposto via API REST

## Fonti

- [[16-python-flask]]

_Aggiornato: 2026-06-04 — ingest iniziale_
