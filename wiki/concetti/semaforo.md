---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, concorrenza-parallelismo]
---

#flashcards/acp

## Definizione

Un **semaforo** è un **tipo di dato astratto** `s` che incapsula:
- una **variabile intera** (`s.value`)
- una **coda** (`s.queue`) dei processi sospesi in attesa di una `signal`

È il meccanismo classico per la sincronizzazione tra processi/thread, sia per la **mutua esclusione** (competizione) sia per la cooperazione.

## Spiegazione

### Operazioni

Sul semaforo sono definite tre operazioni:
- **Inizializzazione** — la variabile è posta a un valore non negativo
- **wait** — **decrementa** `s.value`; se diventa **negativo**, il processo viene **bloccato** (inserito in `s.queue` e sospeso)
- **signal** — **incrementa** `s.value`; se diventa **≤ 0**, viene **sbloccato** un processo che si era sospeso durante una `wait` (rimosso da `s.queue` e risvegliato)

```c
void wait(semaphore s) {            void signal(semaphore s) {
    s.value--;                          s.value++;
    if (s.value < 0) {                  if (s.value <= 0) {
        s.queue.insert(Process);            s.queue.remove(Process);
        suspend(Process);                   wake_up(Process);
    }                                   }
}                                   }
```

> 🎯 Esame: il valore del semaforo, se negativo, indica (in modulo) **quanti processi sono in attesa**.

Cosa indica il valore di un semaforo quando è negativo?
?
Indica, in modulo, quanti processi/thread sono in attesa (bloccati) sul semaforo.


### Mutua esclusione, risorsa critica, sezione critica

- **Risorsa critica** — risorsa a uso esclusivo (es. una stampante) che due o più processi vogliono usare
- **Sezione critica** — la porzione di codice che usa la risorsa critica
- **Mutua esclusione** — un solo processo alla volta può accedere alla sezione critica

Si realizza con un semaforo chiamato **mutex** (*mutual exclusion*), **inizializzato a 1**:
```c
semaphore mutex;   // mutex.value = 1
void P(int i) {
    ...
    wait(mutex);
    /* sezione critica */
    signal(mutex);
    ...
}
```

### Le due classi di problemi: safety e liveness

Nello sviluppo di programmi concorrenti vanno garantite:
- **Safety** (consistenza):
  - **Mutua esclusione** — le risorse condivise sono aggiornate in modo **atomico**
  - **Condition synchronization** — alcune operazioni vanno **differite** se la risorsa non è in uno stato "appropriato" (es. lettura da un buffer vuoto)
- **Liveness** (avanzamento dell'elaborazione):
  - **No Deadlock** — alcuni processi possono **sempre** accedere a una risorsa condivisa
  - **No Starvation** — tutti i processi, *prima o poi* (**eventually**), possono accedere alle risorse condivise

## Perché importa

È la base teorica della sincronizzazione. Il `Lock` di Python è un semaforo binario (mutex), il `threading.Semaphore` è il semaforo generale; il `Semaphore` di `multiprocessing` lo estende ai processi.

## Connessioni

- [[threading]] — `threading.Lock` (mutex) e `threading.Semaphore` (semaforo generale)
- [[monitor]] — costrutto di più alto livello; le **variabili condition** ≠ semafori (semantica diversa)
- [[concorrenza-parallelismo]] — il semaforo risolve i problemi di competizione (mutua esclusione)
- [[produttore-consumatore]] — risolto con semafori per coordinare deposito/prelievo
- [[java-sincronizzazione]] — Java offre `Semaphore` (java.util.concurrent) e `synchronized`/monitor

## Fonti

- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-19 — pagina creata da slide 10 (semaforo come TDA, wait/signal, mutex, risorsa/sezione critica, safety/liveness, deadlock/starvation)_
