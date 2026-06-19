---
tipo: concetto
importanza_esame: alta
prerequisiti: [interprete-python]
---

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

**Context Switch**:
Il SO salva il PCB del processo corrente e ripristina quello del prossimo da eseguire. Ha un **overhead non nullo** (decine/centinaia di μs).

**Thread**:
- Flusso di esecuzione dentro un processo
- Condivide: memoria globale, heap, file aperti
- Ha proprio: stack, PC, registri
- Creazione e context switch molto più leggeri dei processi

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
- Gestiti dal SO
- Ogni thread può bloccarsi indipendentemente
- Sfrutta CPU multiple (multicore)
- Python `threading` usa KLT

> 🎯 Esame: Differenza processo/thread in termini di memoria e overhead, cos'è il PCB, differenza ULT/KLT.

## Perché importa

Fondamentale per capire perché il GIL esiste, quando usare threading vs multiprocessing, e come funziona la concorrenza in Python.

## Connessioni

- [[gil]] — il GIL limita l'uso dei KLT in CPython
- [[threading]] — modulo Python per KLT
- [[multiprocessing]] — alternativa ai thread per CPU-bound

## Fonti

- [[10-programmazione-concorrente-richiami]]

_Aggiornato: 2026-06-04 — ingest iniziale_
