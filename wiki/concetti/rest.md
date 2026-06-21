---
tipo: concetto
importanza_esame: alta
prerequisiti: [socket, rpc]
---

## Definizione

**REST (Representational State Transfer)** è uno stile architetturale per sistemi distribuiti che espone **risorse** (corrispondono a dati e funzionalità) identificate da **URI** e le manipola tramite un'**interfaccia uniforme** (metodi HTTP). È **stateless**: ogni richiesta è autocontenuta.

Definizione del corso: *"uno stile architetturale che definisce gli attributi di qualità architetturale del World Wide Web, visto come un sistema ipermediale aperto, accoppiato lascamente, massicciamente distribuito e decentralizzato"*. Rispetto ai meccanismi [[rpc|RPC]] il focus è sulle **risorse** e non sulle *procedure*.

## Spiegazione

### Web Service (WS)

Prima di REST, il concetto contenitore è il **Web Service**. Definizione W3C: *"A Web service is a software system identified by a **URI** [RFC 2396], whose public interfaces and bindings are defined and described using XML. Its definition can be discovered by other software systems"*.

**Servizio** = modulo software che espone **funzionalità invocabili dai client**:
- il fornitore ne produce l'**implementazione** e ne fornisce la **descrizione** (che include, p.es., l'interfaccia del servizio);
- un servizio è **riusabile** e **componibile**;
- tipicamente offerto e invocato via Internet con **protocolli standard** (HTTP, URI, XML, SOAP).
- "web service" = usare richieste HTTP per avviare l'esecuzione di un programma (≠ *web server*).

### Web server vs Web service

I due termini si assomigliano ma indicano cose **diverse**, ed è una distinzione tipica d'esame.

- **Web server** — è un *processo* che ascolta su HTTP e, in risposta a una richiesta, **restituisce risorse/contenuti** (tipicamente documenti: pagine HTML, file statici, immagini, fogli di stile). Il suo compito è la **consegna di contenuti** sopra HTTP: gestire connessioni, instradare la richiesta verso il file/handler giusto, impostare status code e MIME type. Esempi: Apache, Nginx, il server di sviluppo **Werkzeug** di [[flask|Flask]]. Il client tipico è un **browser** che renderizza una pagina.

- **Web service** — è un *sistema software* che **espone funzionalità (logica applicativa) invocabili da altri programmi** via rete, usando protocolli standard (HTTP, URI, JSON/XML). Qui il punto non è consegnare un documento da visualizzare, ma realizzare un'**interazione programma-a-programma**: il client è un altro software, non un utente che guarda una pagina. È il senso della definizione del corso: *usare richieste HTTP per **avviare l'esecuzione di un programma***.

**Relazione tra i due:** non sono in alternativa, sono **a livelli diversi**. Un web service viene **ospitato/esposto attraverso** un web server: il web server è lo strato di trasporto/ascolto HTTP, il web service è la logica applicativa che gira sopra. In [[flask|Flask]] questo è esplicito: **Werkzeug** fornisce il web server WSGI, mentre le tue **view function + route** costituiscono il web service.

| | Web server | Web service |
|---|---|---|
| Cosa fa | Riceve richieste HTTP, restituisce risorse/contenuti | Espone funzionalità invocabili da altri programmi |
| Client tipico | Browser (renderizza una pagina) | Altro programma/software |
| Output | Documenti (HTML, file statici, immagini) | Dati strutturati (JSON/XML) o effetti applicativi |
| Esempi | Apache, Nginx, server di sviluppo Werkzeug | API REST/SOAP, endpoint Flask |
| Livello | Trasporto/ascolto HTTP | Logica applicativa esposta *sopra* il web server |

> 🎯 Esame: "Differenza tra web server e web service?" → il web server **serve contenuti** (consegna documenti a un browser); il web service **espone funzioni** invocabili da altri programmi. Il primo è l'infrastruttura, il secondo è ciò che vi gira sopra.

### Concetti chiave REST

**Risorsa**: entità indirizzabile tramite web — accessibile e trasferibile tra client e server.

**URI (Uniform Resource Identifier)** — standard Internet per identificare le risorse:
```
foo://example.com:8042/over/there?name=ferret#nose
  ↑        ↑           ↑          ↑           ↑
scheme  authority     path      query      fragment
```

**URI Template**: specifica come costruire/leggere una URI — `http://service.com/order/{oid}/item/{iid}`

**Interfaccia uniforme** — i client interagiscono con le risorse tramite un insieme **fissato** di metodi (in HTTP: GET/POST/PUT/DELETE):

| Metodo | CRUD | Semantica | Safe | Idempotente |
|--------|------|-----------|------|-------------|
| GET    | Read | Recupera lo stato corrente della risorsa | SÌ | SÌ |
| POST   | Create | Crea una sotto-risorsa (figlia) | NO | NO |
| PUT    | Update | Inizializza/aggiorna lo stato all'URI dato | NO | SÌ |
| DELETE | Delete | Elimina risorsa (URI non più valido) | NO | SÌ |

- **Safe**: non altera lo stato del server (read-only)
- **Idempotente**: richieste identiche producono sempre lo stesso risultato

**Stateless**: ciascun ciclo richiesta-risposta rappresenta un'interazione **completa** tra client e server — **non esiste il concetto di sessione**. Ogni richiesta porta con sé tutte le info necessarie.

### REST su HTTP

Lo scenario più comune è REST implementato sul protocollo **HTTP** (HyperText Transfer Protocol), protocollo applicativo per il trasferimento di pagine web:
- ogni pagina/oggetto è identificato da un **URL (Uniform Resource Locator)**;
- prevede metodi (POST/GET/PUT/DELETE) per la gestione delle risorse → operazioni **CRUD** (create, retrieve, update, delete).

**Entity-body** (Representation) per metodo:

| Metodo | Body richiesta | Body risposta |
|--------|----------------|---------------|
| GET    | vuoto | rappresentazione della risorsa |
| DELETE | vuoto | vuoto o messaggio di stato |
| PUT    | rappresentazione proposta | vuoto / stato / copia |
| POST   | rappresentazione proposta | vuoto / stato / copia |

### XML e JSON

Formati testuali per la rappresentazione dei dati scambiati client↔servizio (**external data representation**):
- **XML** (Extensible Markup Language);
- **JSON** (JavaScript Object Notation) — serie non ordinata di coppie nome/valore; dominante in REST.

> 💡 Connessione: sono rappresentazioni **testuali**, a differenza della **serializzazione gRPC** che è **binaria** → [[protocol-buffers]].

### RPC vs REST

- **RPC-style**: ogni web service espone un proprio *vocabolario* di metodi (funzioni con nomi diversi): `insertOrder(id)`, `getOrder(id)`...
- **REST**: vocabolario **fisso** (i metodi HTTP) → tutti i servizi REST espongono la stessa interfaccia di base.

```
RPC-style:            RESTful:
insertOrder(id);      POST   Order/{id}
getOrder(id);         GET    Order/{id}
updateOrder(id);      PUT    Order/{id}
deleteOrder(id);      DELETE Order/{id}
```

### Progettazione REST (passi)

1. Identificare le **risorse** da esporre come servizi
2. Per ogni risorsa: definire le **URI**
3. Esporre un **subset adeguato** dell'interfaccia uniforme (ragionare su cosa significa GET/POST/... su quella risorsa, quali operazioni consentire)
4. Progettare le **rappresentazioni** (JSON, XML, messaggi di stato)

**URI best practices**:
- Usare **nomi** non verbi: `DELETE /book/15` OK, `GET /book?isbn=15&action=delete` NO
- GET è read-only/idempotente; POST è read-write e può modificare lo stato
- POST crea risorsa **figlia** rispetto al padre; PUT crea/modifica all'URI esatto

### HTML e DOM (cenni)

**HTML** (HyperText Markup Language): specifica la **struttura** degli elementi visivi di una web app tramite **tag** `<name>...</name>` (opening/closing). Tag principali: `<html>`/`<head>`/`<body>`, `<header>`/`<main>`/`<footer>`, heading `<h1>..<h6>`, anchor `<a href>` (hypertext), liste `<ol>`/`<ul>`/`<li>`, `<div>` (container).

I tag definiscono il **DOM (Document Object Model)**: architettura gerarchica ad **albero** dei *DOM elements*, interrogabile/manipolabile via scripting (es. JavaScript). Rilevante per Flask perché [[flask|Jinja2]] genera HTML.

### OpenAPI / Swagger

**OpenAPI Specification** (già Swagger): framework per descrivere, documentare e interagire con API RESTful in formato YAML/JSON. Definisce endpoint, parametri, schemi di richiesta/risposta; genera documentazione (Swagger UI) e **codice stub client/server** in molti linguaggi (Swagger Codegen). Usato spesso con [[flask|Flask]] per prototipazione rapida.

> 🎯 Esame: definire safe e idempotente con esempi, differenza POST/PUT, principi REST (stateless, uniform interface, risorse vs procedure), RPC-style vs RESTful.

## Perché importa

REST è l'architettura dominante per API web. Nelle prove pratiche ACP il livello di esposizione esterna (Archive/Query Server) è quasi sempre un'API RESTful realizzata con [[flask|Flask]], a valle di un livello di comunicazione [[rpc]]/[[mom]].

## Connessioni

- [[rpc]] — confronto: RPC sincrono/procedurale (vocabolario custom) vs REST resource-oriented (vocabolario fisso)
- [[protocol-buffers]] — gRPC usa protobuf binario; REST usa JSON/XML testuale
- [[flask]] — micro-framework che implementa REST nel corso
- [[nosql]] — MongoDB è tipicamente esposto via API REST
- [[gestione-errori-api]] — status code HTTP come contratto d'errore dell'API REST

## Fonti

- [[16-python-flask]]

_Aggiornato: 2026-06-20 — MODULO 4: aggiunti Web Service/servizi, entity-body, HTML/DOM, OpenAPI, RPC vs REST esteso_
_Aggiornato: 2026-06-21 — nuova sottosezione "Web server vs Web service" (distinzione, relazione a livelli, tabella, Werkzeug=server / view function=service)_
