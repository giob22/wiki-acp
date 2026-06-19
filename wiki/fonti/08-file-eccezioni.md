---
tipo: fonte
titolo: "Python — File ed Eccezioni"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, file, eccezioni, try, except, finally, raise, context-manager]
---

## Sommario

Slide su I/O su file e gestione delle eccezioni in Python. Si tratta l'apertura di file con `open()` e il context manager `with`, le modalità di lettura/scrittura, e il meccanismo delle eccezioni con `try/except/else/finally`, la gerarchia delle eccezioni, e la creazione di eccezioni custom.

## Punti chiave

1. `open(filename, mode)` — modalità: `'r'` (read), `'w'` (write, sovrascrive), `'a'` (append), `'b'` (binario)
2. **Context manager** `with open(...) as f:` — chiude automaticamente il file anche in caso di eccezione
3. `f.read()` — legge tutto, `f.readline()` — legge una riga, `f.readlines()` — lista di righe
4. `f.write(s)` — scrive stringa; `f.writelines(lst)` — scrive lista
5. Iterazione pythonica: `for line in f:` — efficiente, non carica tutto in memoria
6. **Eccezioni**: meccanismo per gestire errori runtime senza crash del programma
7. Struttura `try/except`:
   ```python
   try:
       codice_rischioso()
   except TipoEccezione as e:
       gestisci(e)
   else:
       # eseguito se NON si è verificata eccezione
   finally:
       # eseguito sempre
   ```
8. Eccezioni comuni: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, `ZeroDivisionError`
9. `raise EccezioneCustom("msg")` — lancia eccezione manualmente
10. Eccezioni **custom**: ereditare da `Exception`
    ```python
    class MiaEccezione(Exception):
        pass
    ```
11. Gerarchia: `BaseException` → `Exception` → eccezioni specifiche

## Concetti introdotti

- [[file-io]]
- [[eccezioni]]

## Domande aperte

- Nessuna

## Domande da esame

- Cosa fa il context manager `with`? Perché è preferibile a `open/close` espliciti?
- Struttura completa del blocco `try/except/else/finally`
- Come si crea un'eccezione personalizzata?
- Differenza tra `except Exception` e `except BaseException`
