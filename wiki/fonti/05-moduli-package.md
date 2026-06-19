---
tipo: fonte
titolo: "Python — Moduli e Package"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, moduli, package, import, pip, sys.path, __init__, namespace]
---

## Sommario

Slide su moduli e package in Python (22 pagine). Un modulo è un file `.py`; un package è una directory con `__init__.py`. Si trattano le varie forme di `import`, il meccanismo di ricerca (`sys.path`, `PYTHONPATH`), la variabile `__name__`, `pip` come gestore di pacchetti, e gli import assoluti/relativi tra sottopackage.

## Punti chiave

1. **Modulo** = file `.py` con funzioni, classi, variabili
2. `import modulo` — accesso con `modulo.nome`
3. `from modulo import nome` — importa direttamente nel namespace corrente
4. `import modulo as alias` — rinomina il modulo
5. `__name__ == "__main__"` — guard per codice eseguito solo come script, non quando importato
6. Ricerca moduli: directory corrente → `PYTHONPATH` → `sys.path` → standard library
7. `pip install pacchetto` — installa da PyPI
8. `dir(modulo)` — elenca attributi/funzioni del modulo
9. **Package** = directory con `__init__.py` (può essere vuoto)
10. `__all__` in `__init__.py` — controlla cosa viene esportato con `from pkg import *`
11. **Import assoluti**: `from sound.effects import echo` (raccomandati)
12. **Import relativi**: `from . import echo`, `from .. import formats` (punto = package corrente)
13. `__path__` — variabile che controlla dove il package cerca i suoi sottomoduli

## Concetti introdotti

- [[moduli-package]]

## Domande aperte

- Nessuna

## Domande da esame

- Come funziona il meccanismo di ricerca dei moduli?
- Differenza tra `import modulo` e `from modulo import nome`
- A cosa serve `if __name__ == "__main__":`?
- Cosa serve per creare un package? Cosa fa `__init__.py`?
- Differenza tra import assoluto e relativo
