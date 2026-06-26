---
tipo: concetto
importanza_esame: bassa
prerequisiti: [tipi-scalari]
---

#flashcards/acp

## Definizione

I costrutti di controllo del flusso in Python sono `if/elif/else`, `while`, `for`. L'**indentazione** è sintattica (obbligatoria), non estetica — sostituisce le parentesi graffe di C/Java.

## Spiegazione

**If/elif/else**:
```python
if condizione1:
    # blocco
elif condizione2:
    # blocco
else:
    # blocco
```
Nessuna parentesi necessaria. Qualsiasi espressione può essere condizione (truthy/falsy).

**While**:
```python
while condizione:
    corpo
```

**For** + `range()`:
```python
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 10, 2):  # 1, 3, 5, 7, 9
    print(i)
```
`range(start, stop, step)` — `stop` escluso.

**Iterazione su sequenze**:
```python
for c in "hello":     # itera carattere per carattere
    print(c)

for item in [1, 2, 3]:  # itera su lista
    print(item)
```

**Break e Continue**:
```python
for i in range(10):
    if i == 5:
        break       # esce dal ciclo
    if i % 2 == 0:
        continue    # salta al prossimo ciclo
```

**Operatore ternario**:
```python
x = "pari" if n % 2 == 0 else "dispari"
```

> 🎯 Esame: L'indentazione obbligatoria e la sintassi di range() con 3 argomenti.

Come funziona range() con 3 argomenti e perché l'indentazione è speciale in Python?
?
range(start, stop, step) genera da start a stop-1 con passo step. L'indentazione è obbligatoria e definisce i blocchi (al posto delle graffe).


## Perché importa

Base del controllo del flusso — prerequisito per tutte le strutture dati e algoritmi del corso.

## Connessioni

- [[strutture-dati]] — for itera su liste, tuple, dizionari
- [[funzioni]] — costrutti usati dentro le funzioni

## Fonti

- [[03-costrutti-controllo]]

_Aggiornato: 2026-06-04 — ingest iniziale_
