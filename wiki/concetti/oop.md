---
tipo: concetto
importanza_esame: alta
prerequisiti: [funzioni, strutture-dati]
---

#flashcards/acp

## Definizione

La **programmazione orientata agli oggetti (OOP)** in Python si basa su classi e oggetti. Una **classe** è un template; un **oggetto** è un'istanza della classe. Python supporta incapsulamento, ereditarietà e polimorfismo.

## Spiegazione

**Definizione classe**:
```python
class Persona:
    specie = "Homo sapiens"  # attributo di CLASSE — condiviso tra istanze

    def __init__(self, nome, età):  # costruttore
        self.nome = nome            # attributo di ISTANZA
        self.età = età

    def __str__(self):              # rappresentazione stringa
        return f"Persona({self.nome}, {self.età})"

    def saluta(self):               # metodo d'istanza
        return f"Ciao, sono {self.nome}"
```

**`self`**: riferimento all'istanza corrente — primo parametro di ogni metodo d'istanza.

**Creazione e uso**:
```python
p = Persona("Alice", 30)  # chiama __init__
print(p.nome)             # → "Alice"
print(p)                  # → chiama __str__
print(Persona.specie)     # attributo di classe
```

**Metodi speciali (dunder)**:
```python
__init__(self, ...)    # costruttore
__str__(self)          # print(obj)
__repr__(self)         # debug repr
__del__(self)          # distruttore (chiamato dal GC)
__eq__(self, other)    # obj1 == obj2
__lt__(self, other)    # obj1 < obj2
__add__(self, other)   # obj1 + obj2
__len__(self)          # len(obj)
```

**Incapsulamento** (per convenzione):
```python
self._attributo    # privato per convenzione (non forzato)
self.__attributo   # name mangling → _Classe__attributo
```

**`isinstance(obj, Classe)`** — verifica tipo a runtime.

> 🎯 Esame: Differenza attributo di classe vs istanza, ruolo di `self`, metodi dunder.

Differenza tra attributo di classe e di istanza, e ruolo di self?
?
Attributo di classe: condiviso tra le istanze. Di istanza: proprio di ogni oggetto (self.x). self è il riferimento all'istanza corrente, primo parametro dei metodi.


## Perché importa

Tutta la libreria standard Python è OOP. Flask, gRPC, threading, PyMongo — tutte le API del corso usano classi.

## Connessioni

- [[ereditarieta]] — estensione delle classi in Python
- [[polimorfismo]] — pilastro dell'OOP: duck typing (Python, strutturale) vs nominale (Java)
- [[eccezioni]] — le eccezioni sono classi che ereditano da `Exception`
- [[threading]] — `Thread` è una classe da sottoclassare

## Fonti

- [[09-oop]]

_Aggiornato: 2026-06-04 — ingest iniziale_
