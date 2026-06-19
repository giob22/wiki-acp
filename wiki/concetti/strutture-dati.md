---
tipo: concetto
importanza_esame: alta
prerequisiti: [tipi-scalari, costrutti-controllo]
---

## Definizione

Le principali strutture dati built-in di Python sono **tuple** (immutabile), **lista** (mutabile ordinata), **dizionario** (mapping chiave-valore), e **set** (insieme non ordinato). Tutte supportano comprehension per costruzione compatta.

## Spiegazione

### Tuple

Sequenza **immutabile** — non modificabile dopo la creazione:
```python
t = (1, 2, 3)
t = (42,)       # tupla con un elemento (virgola obbligatoria!)
t = 1, 2, 3     # packing implicito
a, b, c = t     # unpacking
```

### Lista

Sequenza **mutabile** — operazioni principali:
```python
l = [1, 2, 3]
l.append(4)         # aggiunge in coda: [1,2,3,4]
l.extend([5, 6])    # aggiunge più elementi: [1,2,3,4,5,6]
l.insert(0, 0)      # inserisce in posizione: [0,1,2,3,4,5,6]
l.remove(3)         # rimuove prima occorrenza
l.pop()             # rimuove e restituisce ultimo
l.pop(0)            # rimuove e restituisce indice 0
l.sort()            # ordina in-place
sorted(l)           # nuova lista ordinata
len(l)              # lunghezza
l[1:3]              # slicing
```

### Dizionario

Mapping **mutabile** chiave-valore (chiavi devono essere hashable):
```python
d = {"nome": "Alice", "età": 30}
d["nome"]           # → "Alice" (KeyError se assente)
d.get("x", "def")  # → "def" (accesso sicuro)
d["nuovo"] = "v"   # aggiunta/modifica
del d["nome"]       # rimozione
d.keys()            # vista delle chiavi
d.values()          # vista dei valori
d.items()           # vista di coppie (k,v)
"nome" in d         # → True
```
Python 3.7+: mantiene **ordine di inserimento**.

### Set

Insieme non ordinato di elementi unici (hashable):
```python
s = {1, 2, 3}
s = set()           # set vuoto (non {}, che è dict vuoto)
s.add(4)
s.remove(1)
s1 | s2   # unione
s1 & s2   # intersezione
s1 - s2   # differenza
```

### Comprehension

```python
# List comprehension
quadrati = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
quadrati_d = {x: x**2 for x in range(5)}

# Set comprehension
unici = {x % 3 for x in range(10)}
```

> 🎯 Esame: Differenza lista/tupla, accesso sicuro dizionario con `.get()`, comprehension syntax.

## Perché importa

Strutture dati onnipresenti nel corso — usate in networking, threading (Queue), REST (JSON ≈ dict), MongoDB (documenti ≈ dict).

## Connessioni

- [[passaggio-parametri]] — lista/dict mutabili → effetti visibili al chiamante
- [[nosql]] — documenti MongoDB ≈ dizionari Python annidati
- [[rest]] — JSON è rappresentato come dict in Python

## Fonti

- [[06-tuple-liste-dizionari]]

_Aggiornato: 2026-06-04 — ingest iniziale_
