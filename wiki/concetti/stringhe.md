---
tipo: concetto
importanza_esame: media
prerequisiti: [tipi-scalari]
---

#flashcards/acp

## Definizione

Le stringhe in Python (`str`) sono sequenze **immutabili** di caratteri Unicode. Ogni operazione su una stringa produce un **nuovo oggetto** — la stringa originale non viene mai modificata.

## Spiegazione

**Creazione**: `"testo"`, `'testo'`, `"""multiriga"""`

**Indicizzazione**:
```python
s = "hello"
s[0]   # 'h'   (primo)
s[-1]  # 'o'   (ultimo)
s[-2]  # 'l'
```

**Slicing** — `s[start:stop:step]` (stop **escluso**):
```python
s = "abcdef"
s[1:4]    # "bcd"
s[::2]    # "ace"  (ogni 2 caratteri)
s[::-1]   # "fedcba"  (invertita)
s[2:]     # "cdef"
s[:3]     # "abc"
```

**Metodi principali**:
```python
s.upper()         # → "HELLO"
s.lower()         # → "hello"
s.strip()         # rimuove spazi inizio/fine
s.split(sep)      # → lista di parti
sep.join(lista)   # unisce lista con sep
s.replace(a, b)   # sostituisce a con b
s.startswith(p)   # → bool
s.find(sub)       # → indice o -1
len(s)            # lunghezza
```

**Iterazione pythonica**:
```python
for c in "hello":
    print(c)
```

**Immutabilità**: `s[0] = 'H'` → `TypeError`

**f-string** (Python 3.6+): `f"Valore: {variabile}"` — interpolazione diretta

> 🎯 Esame: Il slicing con step negativo e il concetto di immutabilità sono domande tipiche.

Come funziona lo slicing con step negativo e l'immutabilità delle stringhe?
?
s[::-1] inverte la stringa (step -1). Le stringhe sono immutabili: ogni operazione che 'modifica' crea una nuova stringa.


## Perché importa

L'immutabilità spiega perché `s = s + "x"` crea un nuovo oggetto e non modifica quello originale — rilevante per il passaggio parametri.

## Connessioni

- [[tipi-scalari]] — le stringhe sono immutabili come gli scalari
- [[passaggio-parametri]] — str è immutabile → rebind locale non modifica il chiamante
- [[strutture-dati]] — tuple, liste, dict sono strutture dati correlate

## Fonti

- [[02-tipi-scalari-stringhe]]
- [[03-costrutti-controllo]]

_Aggiornato: 2026-06-04 — ingest iniziale_
