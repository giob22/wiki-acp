---
tipo: fonte
titolo: "Python — Introduzione"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, interprete, cpython, bytecode, pvm, ide]
---

## Sommario

Slide introduttive al linguaggio Python. Si descrive l'architettura dell'interprete CPython: il codice sorgente `.py` viene compilato in bytecode `.pyc` eseguito dalla Python Virtual Machine (PVM). Vengono illustrate le due modalità d'uso (interattiva e script) e i principali ambienti di sviluppo (VSCodium, Anaconda, PyCharm).

## Punti chiave

1. Python è un linguaggio **interpretato** — non compilato in codice macchina nativo
2. L'interprete di riferimento è **CPython** (scritto in C)
3. Il sorgente `.py` viene compilato in **bytecode** (`.pyc`), poi eseguito dalla **PVM** (Python Virtual Machine)
4. Modalità **interattiva**: REPL (`>>>`) per esperimenti rapidi
5. Modalità **script**: esecuzione di file `.py` da terminale
6. I file `.pyc` sono salvati nella cartella `__pycache__`
7. IDE consigliati nel corso: VSCodium, Anaconda (Jupyter), PyCharm

## Concetti introdotti

- [[interprete-python]]

## Domande aperte

- Nessuna — slide introduttive chiare

## Domande da esame

- Descrivere il ciclo di vita di un programma Python dall'esecuzione al bytecode
- Differenza tra modalità interattiva e script
- Cosa è la PVM?
