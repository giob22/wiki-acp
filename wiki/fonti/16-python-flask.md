---
tipo: fonte
titolo: "Flask e Web Services REST"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [flask, rest, http, uri, web-service, json, html, routing, crud]
---

## Sommario

Slide su Flask e Web Services RESTful (20+ pagine). Si introduce il concetto di Web Service, l'architettura REST come stile architetturale basato su risorse identificate da URI, i metodi HTTP (GET/POST/PUT/DELETE) e la loro semantica CRUD. Si trattano anche cenni di HTML, JSON/XML come formati di rappresentazione, e Flask come framework Python per creare web service RESTful.

## Punti chiave

1. **Web Service (WS)**: sistema software identificato da URI, interfaccia descritta in XML, comunica tramite protocolli Internet standard (HTTP, URI, XML, SOAP)
2. **Servizio**: modulo software che espone funzionalità invocabili dai client tramite Internet
3. **REST (Representational State Transfer)**: stile architetturale per web API — focus sulle **risorse** (non procedure come RPC)
4. **Concetti chiave REST**:
   - **Risorsa**: entità identificabile tramite web, accessibile e trasferibile
   - **URI**: identifica la risorsa (`scheme://authority/path?query#fragment`)
   - **URI Template**: pattern parametrico — `http://service.com/order/{oid}/item/{iid}`
   - **Interfaccia uniforme**: metodi fissi (HTTP verbs)
   - **Stateless**: ogni richiesta è indipendente; nessuna sessione lato server
5. **Metodi HTTP**:

   | Metodo | CRUD | Safe | Idempotent |
   |--------|------|------|------------|
   | GET    | Read | YES  | YES        |
   | POST   | Create | NO | NO        |
   | PUT    | Update | NO | YES       |
   | DELETE | Delete | NO | YES       |

6. **Safe**: non altera lo stato del server (read-only)
7. **Idempotente**: richieste identiche producono lo stesso risultato
8. POST vs PUT: POST crea risorsa **figlia**; PUT crea o aggiorna risorsa all'URI dato
9. URI best practices: usare **nomi** non verbi (`DELETE /book/15` OK, `GET /book?action=delete` NO)
10. **Formati di rappresentazione**: JSON e XML (text-based); gRPC usa binario (protobuf)
11. **RPC vs REST**: RPC ha vocabolario custom per ogni servizio; REST ha vocabolario fisso (metodi HTTP)
12. **Flask**: micro-framework Python per web application; installazione `pip install flask`
13. Flask routing:
    ```python
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/path', methods=['GET', 'POST'])
    def handler():
        return "risposta"
    
    @app.route('/user/<int:id>')  # route dinamica
    def get_user(id):
        ...
    ```
14. **Request object** (`flask.request`): `request.method`, `request.args`, `request.json`, `request.form`
15. **Response object**: `flask.jsonify()`, codici HTTP, `flask.make_response()`
16. **Libreria `requests`** (client HTTP): `requests.get(url)`, `requests.post(url, json=data)`
17. HTML = HyperText Markup Language — struttura elementi visivi web (`<tag>...</tag>`)

## Concetti introdotti

- [[rest]]
- [[rpc]]
- [[flask]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è REST? In cosa differisce da RPC?
- Differenza tra safe e idempotente — esempi per ogni metodo HTTP
- Cos'è una risorsa in REST? Come si identifica?
- Come si crea una route Flask con parametro dinamico?
- Differenza tra POST e PUT
- Cosa sono JSON e XML? In cosa differiscono da protobuf?
