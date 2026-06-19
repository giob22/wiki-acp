---
tipo: concetto
importanza_esame: alta
prerequisiti: [semaforo, oop]
---

## Definizione

Il **monitor** è un **costrutto sintattico** che abbina un insieme di **operazioni** a una **struttura dati (risorsa) condivisa** tra processi. È sintatticamente simile al costrutto `class`, ma usato per la **gestione di risorse condivise**: facilita la programmazione concorrente e permette di creare **politiche di accesso**.

## Spiegazione

### Monitor come Tipo di Dato Astratto (TDA)

- **Variabili membro private** — la risorsa e il suo stato
- **Funzioni membro pubbliche** — per l'accesso alla risorsa
- **Funzioni membro private** — per uso interno

> 🎯 Esame: le **funzioni pubbliche del monitor sono eseguite in modo mutuamente esclusivo** (un solo processo alla volta). Il monitor garantisce la mutua esclusione *automaticamente*, senza che il programmatore gestisca i lock.

### Le due politiche di accesso

1. **Competizione** — un solo processo alla volta accede alla risorsa (mutua esclusione, garantita dal monitor: concettualmente `enter_monitor()` / `leave_monitor()` attorno alle operazioni)
2. **Cooperazione** — i processi seguono un determinato **ordine di accesso**: un processo si sospende se non è verificata una **condizione logica** di accesso

### Variabili condition

Per la sospensione si usa una **variabile condition** interna al monitor (`var_cond x`), con due operazioni:
- `x.wait_cond()` — **sospende sempre** il processo chiamante (mentre attende, il monitor diventa libero e un altro processo può entrare)
- `x.signal_cond()` — risveglia un processo in attesa su `x`; **non ha effetto** se nessuno è in attesa

Schema tipico di cooperazione:
```c
void metodo1() {
    enter_monitor();
    while (! condizione_logica) {   // while, NON if (vedi sotto)
        x.wait_cond();
    }
    // operazioni sulla risorsa
    y.signal_cond();
    leave_monitor();
}
```

**Variabili condition ≠ semafori**:
- `wait_cond()` **sospende sempre** il chiamante; `wait_sem()` sospende solo se il valore intero del semaforo lo impone (condizionato)
- `signal_cond()` non ha effetto se non c'è nessuno in attesa; `signal_sem()` incrementa comunque il contatore

### Semantica della signal (problema della mutua esclusione)

Quando Q fa `signal_cond()` per risvegliare P, **entrambi non possono eseguire** dentro il monitor (violerebbero la mutua esclusione). Non esiste una soluzione unica; i sistemi adottano semantiche diverse:

- **Signal-and-wait** — il processo **segnalato P riprende subito**, il **segnalante Q viene sospeso** (per evitare che modifichi di nuovo la condizione)
- **Soluzione di Hoare** (`signal-and-urgent-wait`) — caso particolare: Q ha **priorità** sui processi che vogliono entrare nel monitor, sospeso in un'apposita `urgent_queue` separata dal mutex
- **Signal-and-continue** (`wait-and-notify`) — privilegia il **segnalante**: Q **prosegue** mantenendo l'accesso esclusivo; P segnalato **non viene attivato subito** ma spostato nella coda di ingresso

> 🎯 Esame: nella semantica **signal-and-continue** (quella di Python!), tra il risveglio e l'effettiva esecuzione di P la condizione potrebbe essere **invalidata** da un altro processo K. Per questo `wait_cond()` va usata dentro un **`while`** (ri-verifica la condizione), non un `if`. È esattamente il motivo del `while ... cv.wait()` in [[threading]].

- `signal_cond()` risveglia al più **un** processo; `signal_all()` risveglia **tutti** quelli in attesa sulla condition, che andranno nella entry queue e rientreranno uno alla volta (più robusta: i risvegliati ricontrollano la condizione). Corrisponde a `notify()` / `notify_all()` di Python.

## Perché importa

Il monitor è il modello concettuale dietro la classe `Condition` di Python e il meccanismo `synchronized` + `wait/notify` di Java. Spiega perché in pratica si usa sempre `while + wait()`.

## Connessioni

- [[semaforo]] — meccanismo di più basso livello; il monitor lo astrae
- [[threading]] — `threading.Condition` (lock di default `RLock`) implementa un monitor; `wait`/`notify`/`notify_all` ↔ `wait_cond`/`signal_cond`/`signal_all`
- [[java-sincronizzazione]] — `synchronized` + `wait()`/`notify()` realizzano un monitor con semantica signal-and-continue
- [[produttore-consumatore]] — risolto elegantemente con un monitor + condition variables

## Fonti

- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-19 — pagina creata da slide 10 (monitor come TDA, condition variable, competizione/cooperazione, semantica signal: signal-and-wait/Hoare/signal-and-continue, signal_all, while vs if)_
