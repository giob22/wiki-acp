# Discorso orale — REST

> Export discorsivo da [[rest]] per l'esposizione orale. Testo da leggere/parlare,
> non schematico. Segue l'ordine logico (non quello delle slide): cornice Web Service →
> distinzione server/service → principi REST → REST su HTTP → rappresentazioni →
> confronto con RPC → progettazione → contorno (HTML/DOM, OpenAPI).
> _Generato: 2026-06-21 — fonte: wiki/concetti/rest.md_

---

## Apertura (la frase con cui cominciare)

"REST è uno **stile architetturale** per i sistemi distribuiti, non un protocollo e non una tecnologia. La definizione che userei è quella del corso: REST definisce gli attributi di qualità architetturale del World Wide Web, visto come un sistema ipermediale aperto, accoppiato lascamente, massicciamente distribuito e decentralizzato. Il punto centrale, e la differenza rispetto a RPC, è il **soggetto** dell'interazione: in RPC sono le *procedure*, in REST sono le **risorse**. Tutto il resto discende da questa scelta."

## La cornice: cos'è un Web Service (e perché ne parlo prima)

"Prima di REST conviene chiarire il concetto contenitore, cioè il **Web Service**. Secondo la definizione del W3C, un web service è un sistema software identificato da un **URI**, le cui interfacce pubbliche e i cui binding sono descritti tramite XML, e la cui definizione può essere scoperta da altri sistemi software.

In termini più semplici: un **servizio** è un modulo software che espone funzionalità invocabili dai client. Chi lo fornisce ne produce l'implementazione e ne pubblica la descrizione, che include l'interfaccia; un servizio è pensato per essere **riusabile** e **componibile**, e tipicamente è offerto e invocato via Internet con protocolli standard — HTTP, URI, XML, SOAP. La frase chiave è: *web service significa usare richieste HTTP per avviare l'esecuzione di un programma*."

## La distinzione che il prof chiede: web server vs web service

"Qui anticipo una distinzione che spesso viene chiesta, perché i due termini si somigliano ma indicano cose diverse e a livelli diversi.

Un **web server** è un processo che ascolta su HTTP e, in risposta a una richiesta, **restituisce contenuti** — tipicamente documenti: pagine HTML, file statici, immagini. Il suo mestiere è la consegna di contenuti: gestire le connessioni, instradare la richiesta verso il file o l'handler giusto, impostare status code e MIME type. Esempi sono Apache, Nginx, o il server di sviluppo Werkzeug di Flask. Il client tipico è un **browser** che renderizza una pagina.

Un **web service**, invece, è un sistema software che **espone funzionalità invocabili da altri programmi** via rete. Qui il punto non è consegnare un documento da guardare, ma realizzare un'interazione **programma-a-programma**: il client è un altro software, non un utente davanti a una pagina.

La relazione tra i due è la cosa importante: non sono in alternativa, sono **a livelli diversi**. Un web service viene *ospitato attraverso* un web server. Il web server è lo strato di trasporto e ascolto HTTP; il web service è la logica applicativa che gira sopra. In Flask questo è esplicito: Werkzeug fornisce il web server WSGI, mentre le mie view function e le route costituiscono il web service. In sintesi: il web server serve contenuti, il web service espone funzioni.

E qui aggiungo il punto di contatto tra i due livelli, cioè **WSGI** (Web Server Gateway Interface): è una specifica Python che definisce *come* il web server comunica con l'applicazione Python. Attenzione a non fraintenderlo: WSGI non fa il parsing dell'HTTP grezzo che arriva dalla rete — quello è compito del server, che legge il socket e interpreta la richiesta. WSGI è lo **strato di confine** subito dopo: il server impacchetta la richiesta già parsata in un dizionario `environ` (con metodo, path, header, body) e invoca l'applicazione come un callable, `app(environ, start_response)`; l'app restituisce il corpo della risposta e il server lo riconverte in HTTP da rispedire fuori. La frase sintetica che userei è: **il server parla HTTP verso l'esterno e parla WSGI verso l'applicazione**. Quindi WSGI è esattamente il protocollo di confine tra il web server e il web service."

## I principi REST (il cuore)

"Entrando nel merito di REST, i concetti chiave sono pochi e si tengono insieme.

Primo, la **risorsa**: è l'entità indirizzabile via web, accessibile e trasferibile tra client e server. È la risorsa, non la procedura, l'oggetto dell'interazione.

Secondo, l'**URI**, lo standard Internet per identificare le risorse. Un URI si scompone in scheme, authority, path, query e fragment — per esempio `foo://example.com:8042/over/there?name=ferret#nose`. Esiste anche il concetto di **URI Template**, che specifica come costruire o leggere un URI con dei segnaposto, per esempio `http://service.com/order/{oid}/item/{iid}`.

Terzo, e qui c'è il principio architetturale forte, l'**interfaccia uniforme**: i client interagiscono con tutte le risorse tramite un insieme **fissato** di metodi. In HTTP sono GET, POST, PUT, DELETE, che mappano sulle operazioni CRUD. Di ciascuno conviene saper dire due proprietà:
- **GET** è Read, recupera lo stato della risorsa, ed è **safe** (non altera lo stato del server) e **idempotente**.
- **POST** è Create, crea una sotto-risorsa figlia, e non è né safe né idempotente.
- **PUT** è Update, inizializza o aggiorna lo stato all'URI dato; non è safe ma è idempotente.
- **DELETE** elimina la risorsa; non è safe ma è idempotente.

Le due definizioni da avere pronte sono: **safe** significa che l'operazione è read-only, non modifica lo stato del server; **idempotente** significa che ripetere la stessa richiesta produce sempre lo stesso risultato. GET è entrambe le cose; PUT e DELETE sono idempotenti ma non safe; POST non è nessuna delle due.

Quarto principio: REST è **stateless**. Ogni ciclo richiesta-risposta è un'interazione completa e autocontenuta: non esiste il concetto di sessione, ogni richiesta porta con sé tutte le informazioni necessarie per essere servita."

## REST su HTTP

"Lo scenario più comune è REST realizzato sul protocollo **HTTP**, il protocollo applicativo nato per il trasferimento di pagine web. In questo contesto ogni risorsa è identificata da un **URL**, e i metodi HTTP — POST, GET, PUT, DELETE — realizzano le operazioni CRUD.

Vale la pena ricordare cosa contiene l'**entity-body**, cioè la rappresentazione, per ciascun metodo: la GET ha body di richiesta vuoto e restituisce la rappresentazione della risorsa; la DELETE ha richiesta vuota e risposta vuota o di stato; PUT e POST inviano nella richiesta la rappresentazione proposta e ricevono in risposta uno stato, niente, o una copia."

## Le rappresentazioni: XML e JSON

"I dati scambiati tra client e servizio hanno bisogno di una **rappresentazione esterna** (external data representation), cioè un formato testuale neutro. I due formati sono **XML** e **JSON**; in REST domina JSON, che è una serie non ordinata di coppie nome/valore.

Un collegamento che farei qui: queste sono rappresentazioni **testuali**, e questo le distingue dalla serializzazione di gRPC, che usa Protocol Buffers ed è **binaria**. È una delle differenze pratiche fra REST e gRPC."

## REST vs RPC (il confronto chiave)

"A questo punto si chiude il cerchio con l'apertura. Nello stile **RPC**, ogni servizio espone un proprio vocabolario di metodi con nomi diversi: `insertOrder(id)`, `getOrder(id)`, e così via. In REST, invece, il vocabolario è **fisso**: sono i metodi HTTP. Quindi tutti i servizi REST espongono la stessa interfaccia di base, e ciò che cambia è la risorsa su cui agiscono.

L'esempio che renderei a voce: dove RPC scrive `insertOrder(id)`, `getOrder(id)`, `updateOrder(id)`, `deleteOrder(id)`, REST scrive `POST Order/{id}`, `GET Order/{id}`, `PUT Order/{id}`, `DELETE Order/{id}`. Stessa semantica, ma in REST l'azione è data dal metodo e l'oggetto dall'URI."

## Come si progetta un'API REST

"Per la progettazione seguirei i quattro passi del corso:
1. identificare le **risorse** da esporre come servizi;
2. per ogni risorsa, definire le sue **URI**;
3. esporre un **sottoinsieme adeguato** dell'interfaccia uniforme, cioè ragionare su cosa significhi GET, POST e così via su quella risorsa e quali operazioni abbia senso permettere;
4. progettare le **rappresentazioni** — JSON, XML, messaggi di stato.

Aggiungerei le best practice sugli URI: si usano **nomi e non verbi** — `DELETE /book/15` è corretto, `GET /book?isbn=15&action=delete` è sbagliato perché usa una GET, che è read-only, per modificare lo stato. E ricordo la regola figlia/URI esatto: POST crea una risorsa figlia rispetto al padre, mentre PUT crea o modifica esattamente all'URI indicato."

## Il contorno: HTML/DOM e OpenAPI

"Per completezza, due cose di contorno che il prof può toccare.

L'**HTML** specifica la struttura degli elementi visivi di una web app tramite tag, in coppie apertura/chiusura: `<html>`, `<head>`, `<body>`, gli heading da `<h1>` a `<h6>`, l'anchor `<a href>` per gli hyperlink, le liste, il `<div>` come contenitore. Questi tag definiscono il **DOM**, il Document Object Model, cioè una struttura ad albero degli elementi, interrogabile e manipolabile via scripting come JavaScript. È rilevante per Flask perché il motore di template Jinja2 genera proprio HTML.

Infine la **OpenAPI Specification**, già nota come Swagger: è un framework per descrivere, documentare e interagire con API RESTful in formato YAML o JSON. Definisce endpoint, parametri e schemi di richiesta/risposta, genera la documentazione interattiva (Swagger UI) e può generare anche il codice stub di client e server in molti linguaggi. Si usa spesso insieme a Flask per prototipare in fretta."

## Chiusura (atterraggio sul corso)

"Per chiudere collocherei REST nel quadro del corso: è l'architettura dominante per le API web, e nelle prove pratiche del corso il livello di esposizione esterna — per esempio un Archive Server o un Query Server — è quasi sempre un'API RESTful realizzata con **Flask**, messa a valle di un livello di comunicazione interno basato su **RPC/gRPC** o su un **MOM** come JMS. Quindi REST è la faccia che il sistema mostra al mondo, mentre dietro ci sono gli altri middleware che ho studiato."

---

## Promemoria — i punti che il prof chiede più spesso

- **safe vs idempotente**, con esempi (GET safe+idempotente; PUT/DELETE idempotenti non safe; POST nessuno dei due);
- **differenza POST vs PUT** (figlia vs URI esatto);
- **principi REST**: stateless, interfaccia uniforme, risorse vs procedure;
- **RPC-style vs RESTful** (vocabolario custom vs fisso);
- **web server vs web service** (serve contenuti vs espone funzioni);
- **WSGI** = confine tra i due: il server parla HTTP verso l'esterno e WSGI verso l'app (non fa il parsing HTTP grezzo, lo impacchetta in `environ`);
- **REST testuale (JSON/XML) vs gRPC binario (Protobuf)**.
