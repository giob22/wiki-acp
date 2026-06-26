---
tipo: concetto
importanza_esame: media
prerequisiti: []
---

#flashcards/acp

## Definizione

CPython è l'implementazione di riferimento dell'interprete Python (scritto in C). Trasforma il codice sorgente `.py` in **bytecode** (`.pyc`) e lo esegue sulla **Python Virtual Machine (PVM)**.

## Spiegazione

Il ciclo di vita di un programma Python:

```
file.py  →  [compilatore CPython]  →  bytecode (.pyc)  →  [PVM]  →  esecuzione
```

1. **Compilazione in bytecode**: il sorgente viene analizzato e tradotto in istruzioni intermedie compatte — non è codice macchina nativo
2. **PVM (Python Virtual Machine)**: interprete che legge ed esegue il bytecode istruzione per istruzione
3. I file `.pyc` sono salvati in `__pycache__/` e riutilizzati se il sorgente non cambia (evita ricompilazione)

**Modalità d'uso**:
- **Interattiva** (REPL): `python3` da terminale → prompt `>>>` per sperimentazione rapida
- **Script**: `python3 script.py` per eseguire un file completo

**Altre implementazioni Python** (non CPython):
- PyPy (JIT compilation, più veloce per CPU-bound)
- Jython (gira su JVM)
- IronPython (gira su .NET CLR)

> 🎯 Esame: La domanda tipica è "descrivere il ciclo sorgente → bytecode → PVM" e la differenza tra modalità interattiva e script.

Qual è il ciclo di esecuzione di un programma Python in CPython?
?
Sorgente .py → compilato in bytecode (.pyc in __pycache__) → eseguito istruzione per istruzione dalla PVM (Python Virtual Machine). Non è codice macchina nativo.


## Perché importa

Capire che Python è interpretato (non compilato nativamente) spiega il GIL, le prestazioni, e perché `__pycache__` esiste.

## Connessioni

- [[gil]] — il GIL vive dentro CPython
- [[processo-thread]] — la PVM è un processo che esegue bytecode

## Fonti

- [[01-python-introduzione]]

_Aggiornato: 2026-06-04 — ingest iniziale_
