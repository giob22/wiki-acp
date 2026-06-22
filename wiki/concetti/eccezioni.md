---
tipo: concetto
importanza_esame: media
prerequisiti: [funzioni, tipi-scalari]
---

## Definizione

Le **eccezioni** sono il meccanismo di gestione degli errori runtime in Python. Invece di restituire codici di errore, Python lancia (raise) oggetti eccezione che interrompono il flusso normale e possono essere catturati (catch) da blocchi `except`.

## Spiegazione

**Struttura completa**:
```python
try:
    operazione_rischiosa()
except TipoSpecifico as e:
    print(f"Errore specifico: {e}")
except (Tipo1, Tipo2) as e:
    print(f"Uno di questi errori: {e}")
except Exception as e:
    print(f"Errore generico: {e}")
else:
    # eseguito SOLO se NON si è verificata eccezione nel try
    print("Tutto ok")
finally:
    # eseguito SEMPRE (con o senza eccezione)
    cleanup()
```

**Eccezioni comuni**:

| Eccezione | Causa |
|-----------|-------|
| `ValueError` | Valore non valido per il tipo |
| `TypeError` | Tipo sbagliato |
| `KeyError` | Chiave assente in dict |
| `IndexError` | Indice fuori range |
| `FileNotFoundError` | File non trovato |
| `ZeroDivisionError` | Divisione per zero |
| `AttributeError` | Attributo non esistente |
| `ImportError` | Modulo non trovato |

**Lanciare eccezione**:
```python
raise ValueError("valore non valido")
raise  # rilancia eccezione corrente (dentro except)
```

**Eccezioni custom**:
```python
class MiaEccezione(Exception):
    def __init__(self, msg, codice):
        super().__init__(msg)
        self.codice = codice

raise MiaEccezione("errore", 42)
```

**Gerarchia**:
```
BaseException
└── Exception
    ├── ValueError
    ├── TypeError
    ├── RuntimeError
    ├── IOError
    └── ...
```

`except Exception` cattura tutto tranne `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`.

> 🎯 Esame: La differenza tra `else` e `finally`, e come creare eccezioni custom.

## Perché importa

Gestione eccezioni robusta è critica in networking, file I/O, database — tutti scenari dove errori sono frequenti.

## Connessioni

- [[file-io]] — I/O su file lancia `FileNotFoundError`, `IOError`
- [[oop]] — le eccezioni sono classi Python
- [[socket]] — la comunicazione di rete lancia eccezioni su connessione fallita

## Fonti

- [[08-file-eccezioni]]

_Aggiornato: 2026-06-04 — ingest iniziale_
