---
tipo: fonte
titolo: "Python — OOP"
data_ingest: 2026-06-04
formato: slide-pdf
argomenti: [python, oop, classe, oggetto, ereditarietà, polimorfismo, encapsulation, dunder]
---

## Sommario

Slide sulla programmazione orientata agli oggetti in Python. Si descrive la definizione di classi, il costruttore `__init__`, il parametro `self`, attributi di istanza vs di classe, metodi speciali (dunder), ereditarietà, polimorfismo e incapsulamento tramite convenzione (underscore).

## Punti chiave

1. **Classe** = template per creare oggetti; **oggetto** = istanza della classe
2. Definizione: `class NomeClasse:` (corpo indentato)
3. **`__init__(self, ...)`** — costruttore; chiamato automaticamente alla creazione
4. **`self`** — riferimento all'istanza corrente; primo parametro di ogni metodo d'istanza
5. **Attributi di istanza** — definiti in `__init__` con `self.attr = val`
6. **Attributi di classe** — definiti nel corpo della classe; condivisi tra tutte le istanze
7. Metodi **speciali (dunder)**:
   - `__init__` — costruttore
   - `__str__` — rappresentazione stringa per `print()`
   - `__repr__` — rappresentazione per debug
   - `__del__` — distruttore (invocato dal GC)
   - `__eq__`, `__lt__`, `__add__`, ... — operator overloading
8. **Ereditarietà**: `class Figlia(Madre):` — eredita attributi e metodi
   - `super().__init__(...)` — chiama il costruttore della classe madre
9. **Polimorfismo**: stessa interfaccia, comportamento diverso a seconda del tipo reale
10. **Incapsulamento**: convenzione `_attr` (privato per convenzione), `__attr` (name mangling)
11. `isinstance(obj, Classe)` — verifica il tipo a runtime

## Concetti introdotti

- [[oop]]
- [[ereditarieta]]

## Domande aperte

- Nessuna

## Domande da esame

- Cos'è `self`? Perché è necessario?
- Differenza tra attributo di classe e attributo di istanza
- Come si implementa l'ereditarietà in Python?
- Cosa fa `super()`?
- Cosa sono i metodi dunder? Esempi
- Come si implementa il polimorfismo in Python?
