---
tipo: fonte
titolo: "Python — Passaggio parametri"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, parametri, passaggio-per-assegnazione, mutabile, immutabile, global, rebind]
---

## Sommario

Slide dedicata esclusivamente al passaggio dei parametri in Python (12 pagine). Si chiarisce che Python non usa né "pass-by-value" né "pass-by-reference" nel senso C++, ma **pass-by-assignment** (call-by-object-reference). Il comportamento dipende dalla mutabilità dell'oggetto passato.

## Punti chiave

1. Python non ha passaggio **per valore** né **per riferimento** (in senso C++)
2. **Passaggio per assegnazione**: si passa il riferimento all'oggetto — il parametro è un nuovo binding locale
3. Oggetto **immutabile** (int, float, str, tuple):
   - Rebind locale (`x = x + 1`) crea un nuovo oggetto; l'originale non cambia
   - `id(x)` diverso dentro e fuori la funzione dopo rebind
4. Oggetto **mutabile** (list, dict, set):
   - Mutazioni in-place (`l.extend(...)`) **sono visibili** al chiamante (stesso oggetto)
   - Rebind (`l = [1,2,3]`) crea un nuovo oggetto locale; l'originale **non cambia**
5. Per modificare una variabile immutabile globale dall'interno di una funzione: usare `global x`
6. `global x` fa sì che il nome `x` nella funzione punti all'oggetto globale
7. Senza `global`, assegnare a `x` crea una variabile locale che **oscura** quella globale

## Concetti introdotti

- [[passaggio-parametri]]
- [[scope]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è il passaggio per assegnazione? In cosa differisce da pass-by-value e pass-by-reference?
- Cosa succede se passo una lista a una funzione e la modifico con `.append()`?
- Cosa succede se passo una lista e faccio `l = [nuovo valore]`?
- Come si modifica una variabile globale immutabile da dentro una funzione?
