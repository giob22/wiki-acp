---
tipo: concetto
importanza_esame: alta
prerequisiti: [interprete-python]
---

#flashcards/acp

## Definizione

Un **processo** è un programma in esecuzione — un'entità dinamica con spazio di indirizzamento proprio. Un **thread** è un flusso di esecuzione all'interno di un processo — condivide la memoria con gli altri thread dello stesso processo.

## Spiegazione

**Programma vs Processo**:
- **Programma**: file su disco (entità statica)
- **Processo**: istanza del programma in esecuzione (entità dinamica)

**Struttura di un processo**:
- Spazio di indirizzamento (codice, dati, heap, stack)
- Program Counter (PC)
- Registri CPU
- Descrittori di file aperti
- Informazioni di stato (running, ready, blocked...)

**PCB (Process Control Block)**:
Struttura dati del SO che descrive un processo:
- PID (process ID), stato, PC, registri CPU
- Informazioni di memoria (page table)
- Lista file aperti
- Priorità, statistiche di scheduling

**Astrazione di processo** — incorpora due concetti:
- **Esecuzione**: ogni processo ha un *flusso di controllo* e uno *stato di esecuzione* (Running, Ready, Blocked...)
- **Possesso di risorse (e protezione)**: ogni processo definisce un proprio spazio di indirizzamento e può avere risorse di memoria e I/O assegnate

> Processi differenti possono eseguire **più istanze dello stesso programma**.

**Scheduler di breve termine (BT)**: il componente del SO che seleziona un processo dalla **coda dei processi pronti** e lo fa transitare in esecuzione (anche detto *scheduler della CPU*). L'algoritmo dipende dagli obiettivi del SO.

**Context Switch**:
Il SO salva il PCB del processo corrente e ripristina quello del prossimo da eseguire. Ha un **overhead non nullo** (decine/centinaia di μs).

Il context switch è il **prerilascio** di un processo a favore di un altro scelto dalla coda dei pronti. È il risultato di **tre procedure**:
```
Context_Switch() {
   Salvataggio_stato()   // salva il contesto del processo prelazionato nel suo PCB
   Scheduling_CPU()      // sceglie il prossimo processo tra i "pronti"
   Ripristino_stato()    // copia il contesto del processo scelto dal PCB ai registri CPU
}
```
Il **contesto** salvato include: Program Counter, Stack Pointer, registri general-purpose, registri di gestione memoria.

**Quando avviene un context switch**:
- **Timeout** — il quanto di tempo assegnato al processo è scaduto
- **Interruzioni di I/O**
- **Memory fault** — accesso a un indirizzo non valido
- **Trap** — errore/eccezione (può causare la terminazione del processo)
- **System call** — il processo richiede un servizio al SO

**Thread** (concetto chiave: **separazione tra esecuzione e possesso di risorse**):
- Flusso di esecuzione (di controllo) sequenziale dentro un processo
- Condivide: memoria globale (codice, dati, file aperti)
- Ha proprio: stack, PC (counter), registri. **Non** ha una propria area heap né dati statici (a differenza dei processi)
- Creazione e context switch molto più leggeri dei processi
- Un processo è detto **pesante** (porta dietro spazio di indirizzamento e stato); un thread è detto **leggero** (contesto più semplice)
- Diversi thread nello stesso processo **condividono** lo spazio di indirizzamento; processi differenti **non** condividono le proprie risorse

**Vantaggi dei thread** / perché realizzare programmi multithread:
- Creazione/terminazione molto più efficiente di un processo
- Comunicazione tra thread più semplice ed efficiente (non coinvolge il kernel)
- Context switch tra thread con overhead minore di quello tra processi
- Bloccare parte del processo non implica bloccare tutto il processo
- Rispecchia la natura intrinseca di molti programmi (task indipendenti, applicazioni server, calcoli numerici)

| | Processo | Thread |
|---|---|---|
| Memoria | Isolata | Condivisa |
| Overhead creazione | Alto | Basso |
| Comunicazione | IPC (pipe, socket) | Memoria condivisa |
| Fallimento | Isolato | Può crashare l'intero processo |

**ULT (User Level Thread)**:
- Gestiti da libreria utente (invisible al SO)
- Un blocco I/O blocca **tutto il processo** (il SO vede solo il processo)
- Context switch veloce (nessuna syscall)

**KLT (Kernel Level Thread)**:
- Gestiti dal SO (scheduling, sincronizzazione, gestione)
- Ogni thread può bloccarsi indipendentemente; consente esecuzione **simultanea** su CPU/core diversi
- Più *pesanti* degli ULT: richiedono context switch in **modalità kernel**
- Offrono migliore isolamento e controllo; sfruttano più CPU/core
- Python `threading` usa KLT

**Modelli di implementazione** (mapping ULT↔KLT): *pure user-level* (tutti gli ULT su un solo processo kernel), *pure kernel-level* (1:1), *combined* (M ULT mappati su N KLT).

> 🎯 Esame: Differenza processo/thread in termini di memoria e overhead, cos'è il PCB, le 3 procedure del context switch e quando avviene, differenza ULT/KLT.

Differenza processo/thread, cos'è il PCB e le fasi del context switch?
?
Processo: memoria isolata, pesante, IPC. Thread: memoria condivisa, leggero. PCB = struttura del SO che descrive un processo. Context switch: salvataggio stato → scheduling → ripristino stato. ULT (invisibili al SO) vs KLT (parallelismo reale).


## Perché importa

Fondamentale per capire perché il GIL esiste, quando usare threading vs multiprocessing, e come funziona la concorrenza in Python.

## Connessioni

- [[gil]] — il GIL limita l'uso dei KLT in CPython
- [[threading]] — modulo Python per KLT
- [[multiprocessing]] — alternativa ai thread per CPU-bound
- [[concorrenza-parallelismo]] — multitasking (più processi) e multithreading (più flussi nello stesso processo) sono le due forme di concorrenza
- [[semaforo]] — primitiva di sincronizzazione tra processi/thread

## Fonti

- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-04 — ingest iniziale_
_Aggiornato: 2026-06-19 — astrazione di processo, scheduler BT, context switch (3 procedure + quando avviene), vantaggi dei thread, processo pesante/leggero, modelli ULT/KLT pure/combined; da slide 10_
