---
tipo: concetto
importanza_esame: alta
prerequisiti: [costrutti-controllo, tipi-scalari]
---

#flashcards/acp

## Definizione

Una funzione in Python è un blocco di codice riutilizzabile definito con `def`. In Python le funzioni sono **oggetti di prima classe**: possono essere assegnate a variabili, passate come argomenti e restituite da altre funzioni.

## Spiegazione

**Definizione base**:
```python
def nome(param1, param2, default_param=valore):
    """Docstring — descrive la funzione."""
    corpo
    return risultato  # senza return → restituisce None
```

**Parametri**:
```python
def f(a, b=10, *args, **kwargs):
    pass

f(1)           # a=1, b=10
f(1, 2, 3, 4)  # a=1, b=2, args=(3,4)
f(x=5)         # keyword argument
```

**Docstring**: stringa immediatamente dopo `def`; accessibile via `f.__doc__` e `help(f)`.

**Return**: `return expr` restituisce `expr`. `return` senza espressione (o mancante) → `None`.

**Funzioni come oggetti** (prima classe):
```python
def applica(funzione, valore):
    return funzione(valore)

applica(str.upper, "hello")  # → "HELLO"

# Funzione lambda (anonima)
quadrato = lambda x: x ** 2
```

**Funzioni annidate**:
```python
def outer(x):
    def inner():
        return x * 2  # accede allo scope di outer (enclosing)
    return inner()
```

> 🎯 Esame: Differenza tra parametri positional/keyword, cosa restituisce una funzione senza return, funzioni come first-class objects.

Differenza tra parametri positional e keyword, e cosa restituisce una funzione senza return?
?
I positional si passano per posizione, i keyword per nome (nome=valore). Senza return (o return nudo) la funzione restituisce None. Le funzioni sono first-class objects.


## Perché importa

Le funzioni sono il mattone base dell'astrazione in Python. La loro semantica (scope, passaggio parametri) è fondamentale per capire il comportamento del codice.

## Connessioni

- [[scope]] — ogni chiamata crea un nuovo frame/scope locale
- [[passaggio-parametri]] — come gli argomenti vengono passati alle funzioni
- [[oop]] — i metodi sono funzioni con `self` come primo parametro

## Fonti

- [[04-funzioni]]

_Aggiornato: 2026-06-04 — ingest iniziale_
