---
tipo: concetto
importanza_esame: alta
prerequisiti: [scope, tipi-scalari, strutture-dati]
---

## Definizione

In Python i parametri vengono passati **per assegnazione** (call-by-object-reference): la funzione riceve un riferimento all'oggetto — non una copia del valore né un riferimento alla variabile del chiamante. Il comportamento dipende dalla **mutabilità** dell'oggetto.

## Spiegazione

**Oggetti immutabili** (int, float, str, tuple):
- La funzione riceve il riferimento all'oggetto
- Se la funzione fa **rebind** (`x = x + 1`), crea un nuovo oggetto locale
- L'oggetto originale nel chiamante **non cambia**

```python
def fun(x):
    x = x + 1                          # rebind → nuovo oggetto locale
    print("[fun] x ref:", hex(id(x)))  # ref diversa

x = 10
print("[global] x ref:", hex(id(x)))   # ref originale
fun(x)
print("[global] dopo:", x)             # → 10 (invariato)
```

**Oggetti mutabili** (list, dict, set):
- La funzione riceve il riferimento allo stesso oggetto
- **Mutazioni in-place** (`l.extend(...)`, `l.append(...)`) **sono visibili** al chiamante
- **Rebind** (`l = [nuovo]`) crea un oggetto locale → l'originale **non cambia**

```python
def changeme_rebind(l):
    l = [1, 2, 3, 4]  # rebind → oggetto locale, originale invariato

def changeme_no_rebind(l):
    l.extend([5])      # mutazione in-place → visibile al chiamante

mylist = [10, 20, 30]
changeme_rebind(mylist)
print(mylist)      # → [10, 20, 30]  (invariato)
changeme_no_rebind(mylist)
print(mylist)      # → [10, 20, 30, 5]  (modificato!)
```

**Keyword `global`** per modificare scalari globali:
```python
x = 10
def fun():
    global x
    x = x + 1   # ora lavora sulla variabile globale
fun()
print(x)  # → 11
```

> 🎯 Esame: Domanda classica — "cosa stampa questo codice?" con lista passata a funzione che la modifica vs che la ribinda.

## Perché importa

Capire la semantica del passaggio parametri evita bug sottili dove si modifica (o non si modifica) involontariamente un dato del chiamante.

## Connessioni

- [[scope]] — il parametro è un binding locale nel frame della funzione
- [[strutture-dati]] — liste e dizionari sono mutabili
- [[tipi-scalari]] — scalari e stringhe sono immutabili

## Fonti

- [[04-funzioni]]
- [[07-passaggio-parametri]]

_Aggiornato: 2026-06-04 — ingest iniziale_
