# Prompt di continuazione — Estensione completa del wiki per l'orale

> Incolla il blocco "PROMPT DA INCOLLARE" qui sotto all'inizio della prossima sessione.
> Il resto del file è lo stato di avanzamento, così Claude (e tu) sapete esattamente dove eravamo rimasti.

---

## PROMPT DA INCOLLARE

```
Stiamo continuando il lavoro di estensione completa del wiki ACP iniziato in una
sessione precedente. Obiettivo: rileggere TUTTE le slide/PDF in raw/slide/ e portare
nel wiki (pagine concetto + entità) TUTTO il contenuto rilevante, in modo che le pagine
mi permettano di prendere il massimo voto all'orale. Stile: discorsivo ma non prolisso,
completo di tutto ciò che è stato trattato nelle slide.

Leggi prima output/CONTINUA-estensione-wiki.md per lo stato di avanzamento, poi continua
dal primo modulo non ancora fatto seguendo lo stesso metodo dei moduli già completati.
Lavora UN MODULO PER VOLTA: leggi per intero le slide sorgente del modulo, poi estendi
le pagine esistenti e crea quelle mancanti, aggiorna index.md e appendi al log.md.
Al termine del modulo, aggiorna anche la sezione "Stato" di questo file di continuazione.

NON parlarmi in stile cavernicolo. Risposte leggibili e chiare.
```

---

## Contesto del compito

- **Cosa**: per ogni modulo del corso, leggere le slide originali in `raw/slide/` (sono la fonte di verità, non fermarsi ai sommari in `wiki/fonti/`) ed estendere le pagine `wiki/concetti/` e `wiki/entità/` con tutto il contenuto delle slide.
- **Qualità target**: massimo voto all'orale → completezza + chiarezza discorsiva (non telegrafica, non prolissa).
- **Regole wiki** (da `CLAUDE.md`): mai toccare `raw/`; link interni `[[nome-pagina]]`; marcatori `🎯 Esame`, `💡 Connessione`, `⚠️ Contraddizione`; in fondo a ogni pagina modificata `_Aggiornato: [data] — [motivo]_`; aggiornare pagine esistenti invece di duplicare; appendere a `wiki/log.md`.
- **Metodo per modulo**:
  1. Leggere le pagine concetto/entità esistenti del modulo (per calibrare profondità e non duplicare).
  2. Leggere PER INTERO le slide sorgente del modulo (a blocchi di max 20 pagine con il parametro `pages`).
  3. Estendere le pagine esistenti con ciò che manca; creare nuove pagine per la teoria assente ma rilevante.
  4. Aggiornare `wiki/index.md` (registrare nuove pagine, aggiornare le descrizioni).
  5. Appendere una riga a `wiki/log.md`.
  6. Aggiornare la sezione "Stato" di questo file.

## Piano dei moduli (in ordine di priorità d'esame)

1. ✅ **Concorrenza** — slide `01_PYTHON_10` (80pp) + `01_PYTHON_11` (61pp) — FATTO
2. ✅ **Middleware / RPC / gRPC / Protobuf** — slide `01_PYTHON_13-SistemiMiddleware` (47pp) + `01_PYTHON_14-Python_RPC` (45pp) — FATTO
3. ✅ **MOM / pub-sub / JMS / durable** — slide `01_PYTHON_15-Python_MOM` (32pp) — FATTO
4. ⬜ **Container / deployment** — slide `03_Service_Deployment_Containers` (54pp) + `appunti_container_deployment.md` (28pp). Pagine: virtualizzazione-container, linux-namespaces, cgroups; entità docker, docker-compose, docker-swarm, kubernetes. (NB: docker-swarm già esteso con sezione "Tolleranza ai guasti".)
5. ⬜ **Networking / socket** — slide `01_PYTHON_12-Python_Networking` (54pp). Pagine: socket.
6. ⬜ **Java threading + sincronizzazione + proxy-skeleton** — slide `02_JAVA_01` (36pp) + `02_JAVA_02` (60pp) + `02_JAVA_03-Java-Networking` (26pp) + `02_JAVA_04-ProxySkeleton` (30pp). Pagine: java-threading, java-sincronizzazione, proxy-pattern, socket.
7. ⬜ **REST / Flask + NoSQL** — slide `01_PYTHON_16-Python_Flask` (70pp) + `01_PYTHON_17-NoSQL_Databases` (35pp). Pagine: rest, gestione-errori-api, nosql; entità flask, mongodb.
8. ⬜ **OOP** — slide `01_PYTHON_09-Python_OOP` (67pp). Pagine: oop, ereditarieta.
9. ⬜ **Python base** — slide `01_PYTHON_01..08` + `00_INTRODUZIONE`. Pagine: interprete-python, tipi-scalari, stringhe, costrutti-controllo, funzioni, scope, passaggio-parametri, moduli-package, strutture-dati, file-io, eccezioni.

> Nota: Java gRPC (`02_JAVA_06-GRPC`, 16pp) e Java JMS (`02_JAVA_05-MOM-JMS`, 61pp) possono essere agganciati ai moduli 2/3 o trattati a parte alla fine, insieme alle entità grpc-java / jms.

## Stato

### ✅ Modulo 1 — Concorrenza (completato 2026-06-19)

Slide lette integralmente: `01_PYTHON_10` (80pp), `01_PYTHON_11` (61pp).

Pagine **estese**:
- `concetti/processo-thread.md` — astrazione processo, scheduler BT, context switch (3 procedure + quando avviene), vantaggi thread, processo pesante/leggero, modelli ULT/KLT.
- `concetti/gil.md` — vantaggi/svantaggi, "GIL oggi" (free-threaded 3.13/3.14, --disable-gil), multithread vs multiprocess CPU-bound.
- `concetti/threading.md` — costruttore Thread completo, ciclo di vita, daemon, Lock/RLock/Condition/Semaphore/Event dettagliati, thread-local + race condition.
- `concetti/multiprocessing.md` — start method (spawn/fork/forkserver), Process, Pipe, Queue (+varianti), Shared Memory (Value/Array/ctypes), modulo multiprocess.

Pagine **create**:
- `concetti/concorrenza-parallelismo.md` (concorrenza vs parallelismo, speed-up, legge di Amdahl, competizione/cooperazione/interferenza)
- `concetti/semaforo.md` (TDA, wait/signal, mutex, sezione critica, safety/liveness)
- `concetti/monitor.md` (condition variable, semantica signal: signal-and-wait/Hoare/signal-and-continue)
- `concetti/produttore-consumatore.md` (vincoli, soluzioni, lettori/scrittori)

Aggiornati: `index.md` (sezione Concorrenza), `log.md`.

### ✅ Modulo 2 — Middleware / RPC / gRPC / Protobuf (completato 2026-06-19)

Slide lette integralmente: `01_PYTHON_13-SistemiMiddleware` (47pp), `01_PYTHON_14-Python_RPC` (45pp).

Pagina **creata**:
- `concetti/middleware.md` — sistemi distribuiti (def. Coulouris/Lamport, 3 implicazioni), eterogeneità, EAI (COTS/legacy, tabella sviluppo vs integrazione), definizione middleware + glue technologies, le 7 trasparenze, tassonomia (orientati ai dati RDA/TP vs comunicazione RPC/MOM/TS/DOM/CM/WS), modello a oggetti distribuiti (DO=OOP+C/S, ORB, IDL, Java RMI/registry/codice mobile).

Pagine **estese**:
- `concetti/rpc.md` — RPC come estensione modello procedurale, sincrono-bloccante (asincrono=eccezione), ruolo stub dettagliato, marshalling (conversione formato endian/complementi + serializzazione/linearizzazione + external data representation: CDR/XDR/Java/protobuf/XML), semantica RPC (exactly/at-most/at-least-once, zero-or-more + cause guasti), Sun RPC (tripla programma-versione-procedura, mutua esclusione, XDR, semantiche TCP/UDP, port mapper porta 111/binding dinamico→location transparency, dispatcher).
- `concetti/protocol-buffers.md` — doppio ruolo IDL+interscambio, modello Proxy-Skeleton, messaggi come record di campi nome-valore con tag numerici, package raccomandato anche se ignorato in Python.
- `concetti/grpc.md` — universale/CNCF/scenari, "RPC come riferimenti a oggetti HTTP", HTTP/2 (binary framing, stream/message/frame, multiplexing, header compression), blocking vs non-blocking stub, **4 tipi di RPC call** (unary/server-stream/client-stream/bidirectional) con generators/yield ed esempi Python, thread-safety (channel+stub thread-safe, server soggetto a GIL), so_reuseport, aggiornare servizio, errori tipici (UNAVAILABLE/UNKNOWN/iteratore), limitazioni (gRPC-Web, non human-readable).
- `entità/grpc-python.md` — streaming con generator/yield, so_reuseport, thread-safety, errori RpcError.

Aggiornati: `index.md` (sezione Middleware, nuova pagina middleware + descrizioni), `log.md`.

### ✅ Modulo 3 — MOM / pub-sub / JMS / durable (completato 2026-06-19)

Slide letta integralmente: `01_PYTHON_15-Python_MOM` (32pp).

Pagine **estese**:
- `concetti/mom.md` — comunicazione indiretta (4 forme: group communication / shared memory-tuple space / code di messaggi / publish-subscribe), motivazioni (rimpiazza RPC sincrono, high availability/scalability via broker), aspetti chiave + disaccoppiamento spaziale/temporale dettagliato, Evento/Notifica + Observer → Notification Service (NS può usare anche code, non solo pub-sub), sistemi event-based industria (SESAR/NASPI/FSE), protocolli AMQP (binario wire-level)/MQTT (leggero ISO IoT TCP-IP)/STOMP (testuale).
- `concetti/pub-sub.md` — meccanismo dei due domini (PTP coda+ack+un consumer vs Pub-Sub topic+0..N subscriber correnti), Observer in 3 passi (subscription/event/notification) + inconvenienti.
- `concetti/sottoscrizioni-durabili.md` — **fix contraddizione**: i durable subscriber SONO nelle slide (15 p.32), rimossa nota errata; aggiunti subscribe non-durable di default, client-id=hostname se non impostato, persistent=True.
- `entità/activemq.md` — multiprotocollo/administered objects (avviare provider prima), formato STOMP Frame (COMMAND/headers/body^@), porte 61613 plain / 62613 SSL + IPv6, API stomp.py completa (Connection failover list, connect wait/headers/with_connect_command, send content_type, subscribe id/ack auto-client-client_individual, Listener asincrono ConnectionListener/PrintingListener + on_message frame.body/headers/cmd), transazioni STOMP (begin/commit/abort).

Aggiornati: `index.md` (sezione Middleware + entità activemq), `log.md`.

### ⬜ Prossimo: Modulo 4 — Container / deployment

Slide `03_Service_Deployment_Containers` (54pp) + `appunti_container_deployment.md`. NB: pagine container già abbastanza complete (virtualizzazione-container, linux-namespaces, cgroups, docker, docker-compose, docker-swarm, kubernetes) — rileggere le slide per eventuali dettagli mancanti, ma il grosso è già fatto. Esiste anche il canvas `container-mappa-esame.canvas` appena creato.

---

_File creato: 2026-06-19. Aggiornare la sezione "Stato" alla fine di ogni modulo._
