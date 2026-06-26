---
tipo: concetto
importanza_esame: bassa
prerequisiti: [costrutti-controllo, eccezioni]
---

#flashcards/acp

## Definizione

Il modulo built-in `open()` permette di leggere e scrivere file. Il **context manager** `with` garantisce la chiusura automatica del file anche in caso di eccezione.

## Spiegazione

**Apertura file**:
```python
f = open("file.txt", "r")   # 'r' read, 'w' write, 'a' append, 'rb' binary
f.close()                    # chiusura manuale — rischiosa se si lancia eccezione
```

**Context manager (raccomandato)**:
```python
with open("file.txt", "r") as f:
    contenuto = f.read()
# file chiuso automaticamente qui, anche in caso di eccezione
```

**Lettura**:
```python
f.read()          # → stringa con tutto il contenuto
f.readline()      # → una riga (con \n)
f.readlines()     # → lista di righe

for riga in f:    # iterazione pythonica — efficiente, non carica tutto in memoria
    print(riga.strip())
```

**Scrittura**:
```python
with open("out.txt", "w") as f:
    f.write("testo\n")
    f.writelines(["riga1\n", "riga2\n"])
```

**Modalità**:

| Modalità | Significato |
|----------|-------------|
| `'r'` | Lettura (default) — errore se non esiste |
| `'w'` | Scrittura — sovrascrive se esiste |
| `'a'` | Append — aggiunge in fondo |
| `'x'` | Creazione — errore se già esiste |
| `'b'` | Binario (combinare con r/w/a) |

> 🎯 Esame: Perché usare `with` invece di `open/close` espliciti.

Perché usare `with open(...)` invece di open/close espliciti?
?
Il context manager with chiude automaticamente il file alla fine del blocco, anche in caso di eccezione → niente file lasciati aperti.


## Perché importa

I/O su file è prerequisito per elaborazione dati, logging, configurazione. Il pattern `with` è idiomatico Python.

## Connessioni

- [[eccezioni]] — `with` gestisce automaticamente le eccezioni durante I/O

## Fonti

- [[08-file-eccezioni]]

_Aggiornato: 2026-06-04 — ingest iniziale_
