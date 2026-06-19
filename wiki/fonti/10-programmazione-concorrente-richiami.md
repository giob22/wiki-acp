---
tipo: fonte
titolo: "Programmazione Concorrente — Richiami"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [concorrenza, processo, thread, pcb, context-switch, ult, klt, scheduling]
---

## Sommario

Slide di richiami sulla programmazione concorrente a livello di sistema operativo. Si distingue tra programma (entità statica) e processo (entità dinamica), si descrive il Process Control Block (PCB), il context switch, e la differenza tra thread e processo. Si introducono User Level Thread (ULT) e Kernel Level Thread (KLT).

## Punti chiave

1. **Programma** = entità statica (file su disco); **Processo** = programma in esecuzione (entità dinamica)
2. Un processo include: spazio di indirizzamento, PC, registri, stack, heap, descrittori file
3. **PCB (Process Control Block)** — struttura dati del SO che descrive un processo: stato, PID, PC, registri, memoria, I/O, priorità
4. **Context switch** — il SO salva il PCB del processo corrente e ripristina quello del prossimo; overhead non nullo
5. **Processo vs Thread**:
   - Processo: memoria isolata, overhead alto per creazione e comunicazione (IPC)
   - Thread: condivide memoria con il processo padre, overhead basso, comunicazione tramite memoria condivisa
6. **ULT (User Level Thread)** — gestiti da libreria utente, invisibili al SO; un blocco blocca tutto il processo
7. **KLT (Kernel Level Thread)** — gestiti dal SO; può sfruttare CPU multiple; Python usa KLT tramite `threading`
8. **GIL (Global Interpreter Lock)** — in CPython un solo thread alla volta esegue bytecode Python (anche con KLT multipli)
9. Scheduling: il SO decide quale processo/thread eseguire (preemptive, round-robin, priority-based...)
10. **Race condition**: due thread accedono allo stesso dato in modo non sincronizzato → risultato non deterministico

## Concetti introdotti

- [[processo-thread]]
- [[gil]]
- [[threading]]

## Domande aperte

- Come interagisce il GIL con il multiprocessing?

## Domande da esame

- Differenza tra processo e programma
- Cos'è il PCB? Quali informazioni contiene?
- Differenza tra ULT e KLT
- Cosa succede durante un context switch?
- Cos'è una race condition?
