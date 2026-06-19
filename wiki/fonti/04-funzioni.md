---
tipo: fonte
titolo: "Python — Funzioni"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, funzioni, scope, docstring, higher-order, passaggio-parametri, global]
---

## Sommario

Slide sulle funzioni Python (27 pagine). Si trattano definizione, parametri, docstring, il modello di scope (frame/environment), il valore di ritorno, le funzioni come oggetti di prima classe, le funzioni annidate, e il passaggio dei parametri (per assegnazione). Pagine 21-27 approfondiscono scope complesso e passaggio per oggetti mutabili/immutabili.

## Punti chiave

1. Definizione: `def nome(params):` — corpo indentato
2. **Docstring**: stringa immediatamente dopo `def`, accessibile via `help()` e `__doc__`
3. Ogni chiamata crea un nuovo **frame** (scope locale) nello stack
4. **Scope rules** (LEGB): Local → Enclosing → Global → Built-in
5. `return` restituisce un valore; senza `return` (o `return` nudo) → `None`
6. Funzioni sono **oggetti di prima classe**: passabili come argomenti, assegnabili a variabili
7. Funzioni **annidate**: `h` definita dentro `g` ha accesso allo scope di `g` (enclosing)
8. **Passaggio per assegnazione** (call-by-object-reference):
   - Se oggetto **immutabile** (int, str, tuple): rebind locale non modifica il chiamante
   - Se oggetto **mutabile** (list, dict): mutazione in-place visibile al chiamante; rebind no
9. `global x` nello scope locale forza la funzione a lavorare sulla variabile globale
10. Esempio scope complesso: `g(x)` che chiama `h()` internamente — ogni scope ha la propria `x`

## Concetti introdotti

- [[funzioni]]
- [[scope]]
- [[passaggio-parametri]]

## Domande aperte

- Nessuna — materiale esaustivo

## Domande da esame

- Cos'è il passaggio per assegnazione in Python?
- Differenza tra oggetto mutabile e immutabile nel passaggio parametri
- Come funziona lo scope LEGB?
- Cosa stampa il seguente codice? (scope annidato con `h()` dentro `g()`)
- Quando serve la keyword `global`?
