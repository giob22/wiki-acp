---
tipo: fonte
titolo: "Python — Tuple, Liste, Dizionari"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, tuple, lista, dizionario, set, comprehension, strutture-dati]
---

## Sommario

Slide sulle principali strutture dati Python (20+ pagine). Si trattano tuple (immutabili), liste (mutabili, con operazioni CRUD), dizionari (mapping chiave-valore), set, e le list/dict comprehension come costrutti idiomatici pythoniani.

## Punti chiave

1. **Tuple**: sequenza immutabile — `(1, 2, 3)`. Non modificabile dopo la creazione. Usate per dati eterogenei correlati
2. **Liste**: sequenza mutabile — `[1, 2, 3]`
   - `append(x)` — aggiunge in coda
   - `extend([x,y])` — aggiunge più elementi
   - `insert(i, x)` — inserisce in posizione
   - `remove(x)` — rimuove prima occorrenza
   - `pop(i)` — rimuove e restituisce elemento
   - `sort()` / `sorted()` — ordinamento in-place / nuova lista
   - `len()`, `index()`, `count()`
3. **Dizionari**: mapping `{chiave: valore}` — chiavi devono essere hashable (immutabili)
   - `d[k]` — accesso; `KeyError` se chiave assente
   - `d.get(k, default)` — accesso sicuro
   - `d.keys()`, `d.values()`, `d.items()`
   - `k in d` — test appartenenza
   - Dal Python 3.7+ i dizionari mantengono l'ordine di inserimento
4. **Set**: insieme non ordinato di elementi unici — `{1, 2, 3}` o `set()`
   - Operazioni: `|` (unione), `&` (intersezione), `-` (differenza)
5. **List comprehension**: `[expr for x in iterable if condizione]`
6. **Dict comprehension**: `{k: v for k, v in items}`
7. Tutte le strutture supportano **slicing** (tranne dict e set)

## Concetti introdotti

- [[strutture-dati]]

## Domande aperte

- Nessuna

## Domande da esame

- Differenza tra lista e tupla
- Come si crea un dizionario? Come si accede a un valore inesistente senza eccezione?
- Sintassi di una list comprehension
- Quando usare un set invece di una lista?
