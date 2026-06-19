---
tipo: entità
categoria: framework
---

## Cos'è

**Flask** è un **web application framework WSGI leggero** (*microframework*) per Python, per la realizzazione rapida e semplice di web app e **API RESTful**, con possibilità di scalare verso applicazioni complesse. "Micro" = il core mette a disposizione i servizi di base, estendibili tramite il meccanismo delle **estensioni** (non include ORM o form validation di default).

Nato come **wrapper** di due librerie:
- **Werkzeug** — fornisce **routing**, **debugging** e la **WSGI (Web Server Gateway Interface)**: specifica che descrive come un web server comunica con le applicazioni web Python.
- **Jinja2** — template engine.

> 💡 Un **web framework** tipicamente fornisce: *Routes* (mapping URL→funzioni), *Template* (inserimento dati server-side in HTML), autenticazione/autorizzazione, *Sessioni*.

**Installazione** (installa Flask, Werkzeug, Jinja2):
```bash
pip install Flask
```
Verifica: `>>> import flask` senza errori.

## Come si usa nel corso

Flask implementa **web service RESTful** che espongono risorse via HTTP → vedi [[rest]].

### Struttura base (3 parti)
```python
# hello.py
from flask import Flask

app = Flask(__name__)              # 1. Inizializzazione (application instance)

@app.route("/")                    # 2. Routes + view functions
def index():
    return "<h1>Hello, World!</h1>"

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

if __name__ == "__main__":
    app.run(debug=True)            # 3. Server startup
```
Esecuzione: `python hello.py`.

### 1. Inizializzazione
`app = Flask(__name__)` — l'argomento al costruttore è il **nome del main module o del package** dell'applicazione.

### 2. Routes e view functions
- **Route**: mapping tra una URL e la funzione Python che la gestisce.
- Il decoratore `@app.route('/path')` registra la funzione che segue (la **view function**) come gestore della URL. Ad ogni richiesta su quella URL la view function è invocata; il suo valore di ritorno è la risposta al client.
- Il tipo di ritorno deve essere `str`, `dict`, `list`, `tuple` (con headers/status), istanza `Response`, o callable WSGI — altrimenti `TypeError`.

**Dynamic routes** — porzioni variabili nella URL:
```python
@app.route('/user/<name>')        # <name> = parte dinamica fino al prossimo "/"
def user(name):                    # passata come parametro alla view function
    return '<h1>Hello, %s!</h1>' % name
```
Convertitori di tipo: `<int:id>`, `<string:nome>`, `<float:val>`.

**Route methods** — di default le route rispondono solo a **GET**. Per altri metodi:
```python
@app.route('/print', methods=['GET', 'POST'])
def print_method():
    if request.method == 'POST':
        return '<h1>This is a POST</h1>'
    return '<h1>This is a GET</h1>'
```
In alternativa le **shortcut** per metodo: `@app.get('/print')`, `@app.post('/print')`, ecc. (separano la gestione in funzioni diverse).

### 3. Server startup
`app.run()` avvia il web server di sviluppo integrato (loop in attesa di richieste, termina con CTRL+C). Default:
- raggiungibile su `http://127.0.0.1:5000/`, solo da **localhost**;
- **multi-threaded** (per single-threaded passare `threaded=False`);
- configurabile: `app.run(host='0.0.0.0', port=80, debug=True)`.

> ⚠️ È un *development server*: in produzione usare un server WSGI di produzione (Gunicorn, uWSGI...).

### Request object
Flask usa **context** per rendere `request` accessibile come variabile globale, ma **isolata per thread** (no interferenza tra thread).
```python
from flask import request

request.method                          # 'GET', 'POST', ...
request.headers.get('User-Agent')       # header HTTP
request.args                            # query string ?key=val (dict-like)
request.get_json(force=False, silent=False, cache=True)  # parsing JSON del body
request.get_data(cache=True, as_text=False)              # body raw (bytes/str)
```
- `request.args['name']` → parametro dopo `?` nell'URL (`/hello?name=pippo`).
- `get_json()`: `force` ignora il mimetype; `silent` ritorna `None` invece di sollevare su errore.

### Response object
Logica di **conversione del valore di ritorno** in `Response`:

| Valore ritornato | Risultato |
|---|---|
| oggetto `Response` | ritornato direttamente |
| `str` | body = stringa, status 200, mimetype `text/html` |
| `dict` / `list` | `jsonify()` automatico (dati JSON-serializable) |
| iterator/generator | *streaming response* |
| `tuple` | `(body, status)`, `(body, headers)`, `(body, status, headers)` |
| altro | assunto callable WSGI valido |

```python
return jsonify(data)                      # JSON, 200
return jsonify(data), 201                 # JSON, 201 Created
return '<h1>Bad Request</h1>', 400        # status override
return '<h1>Bad Request</h1>', 400, {'X-App': 'Flask'}   # + headers
```

**make_response** — costruire e configurare esplicitamente la risposta (es. cookie):
```python
from flask import make_response
resp = make_response('<h1>...</h1>')
resp.set_cookie('Last-access', str(time.time()))
return resp
```

### HTML templating: Jinja2
Per separare *business logic* da *presentation logic*. Template = file (parte statica) con **placeholder** popolati al **rendering**.
- Default in `./templates/` (override: `Flask(__name__, template_folder=...)`); file `.html`.
- Rendering: `render_template(template_name_or_list, **context)`.
```python
from flask import render_template
@app.route("/index")
def index():
    return render_template('index.html')          # templates/index.html
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)  # {{ name }} nel template
```
- **Variabili**: `{{ var }}`, `{{ mydict['key'] }}`, `{{ mylist[3] }}`, `{{ myobj.method() }}`.
- **Strutture di controllo**: `{% if user %}...{% else %}...{% endif %}`, `{% for x in lista %}...{% endfor %}`.

## Client HTTP: libreria `requests`

Libreria HTTP per Python — crea facilmente richieste **HTTP/1.1**. Basata su **urllib3** (Keep-alive, connection pooling). Supporta tutti i metodi HTTP.
```python
import requests
requests.head(url, **kwargs)
requests.get(url, params=None, **kwargs)       # params → query string
requests.post(url, data=None, json=None, **kwargs)
requests.put(url, data=None, **kwargs)
requests.delete(url, **kwargs)
```
- **params** (dict/lista tuple): query string. Chiavi con valore nullo escluse; valore lista → ripetizione (`?key=v2&key=v3`).
- **data** (POST/PUT): payload **form-encoded**; **json**: payload JSON serializable.

**Response object** (`requests.models.Response`, ≠ Response di Flask) — decodifica automatica:
```python
r.text          # contenuto in unicode (usa r.encoding, autodetect)
r.content       # contenuto in byte
r.json()        # parsing JSON → dict/list (solleva JSONDecodeError se fallisce)
r.status_code   # status code
r.url           # URL finale
r.headers['Content-Type']
r.raise_for_status()   # solleva HTTPError se status è un errore HTTP
```
> ⚠️ `r.json()` decodifica solo il contenuto: una chiamata andata a buon fine **non** implica successo della richiesta (molti server ritornano JSON anche su HTTP 500). Verificare con `r.status_code` o `raise_for_status()`.

### curl (test da terminale)
```bash
curl https://example.com            # GET (default)
curl -I https://example.com         # solo Headers (HEAD)
curl -d "name=curl" https://...     # POST con data (metodo POST automatico)
curl --json '{"name":"pippo"}' ...  # POST con body JSON
curl -X DELETE https://...          # forza metodo HTTP
```

## Link ai concetti correlati

- [[rest]] — Flask implementa l'architettura REST (risorse, URI, metodi HTTP, stateless)
- [[strutture-dati]] — il JSON è gestito come dict/list Python
- [[nosql]] — Flask tipicamente accede a MongoDB nel backend (Archive/Query Server)
- [[gestione-errori-api]] — eccezioni PyMongo↔status HTTP, abort(), @app.errorhandler
- [[threading]] — il dev server è multi-threaded di default; i context isolano `request` per thread

## Fonti

- [[16-python-flask]]

_Aggiornato: 2026-06-20 — MODULO 4: estensione completa (WSGI/Werkzeug/Jinja2, view function, server threading, request/response, templating, requests lib, curl)_
