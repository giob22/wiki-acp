---
tipo: concetto
importanza_esame: alta
prerequisiti: [oop]
---

## Definizione

L'**ereditarietà** in Python permette a una classe (**figlia**) di estendere un'altra classe (**madre**), ereditandone attributi e metodi. Il **polimorfismo** permette a oggetti di classi diverse di rispondere allo stesso messaggio in modo diverso.

## Spiegazione

**Ereditarietà**:
```python
class Animale:
    def __init__(self, nome):
        self.nome = nome

    def parla(self):
        return "..."

class Cane(Animale):           # Cane eredita da Animale
    def parla(self):           # override del metodo
        return "Bau!"

class Gatto(Animale):
    def __init__(self, nome, indoor):
        super().__init__(nome)  # chiama costruttore della madre
        self.indoor = indoor

    def parla(self):
        return "Miao!"
```

**`super()`**: accede ai metodi della classe madre senza nominarla esplicitamente — raccomandato per manutenibilità.

**Polimorfismo**:
```python
animali = [Cane("Rex"), Gatto("Tom", True)]
for a in animali:
    print(a.parla())   # → "Bau!" poi "Miao!" — stesso messaggio, risposta diversa
```

> 💡 Connessione: qui il polimorfismo passa per l'override e una base comune (`Animale`), ma in Python **non è necessaria una superclasse comune**: per il **duck typing** basta che gli oggetti abbiano il metodo `parla()`. Confronto completo nominale (Java) vs strutturale (Python) → [[polimorfismo]].

**Ereditarietà multipla** (Python supporta, usare con cautela):
```python
class C(A, B):
    pass
```
MRO (Method Resolution Order) risolve i conflitti — `C.__mro__` mostra l'ordine.

**Classi astratte** (con `abc`):
```python
from abc import ABC, abstractmethod

class Forma(ABC):
    @abstractmethod
    def area(self):
        pass

class Cerchio(Forma):
    def area(self):
        return 3.14 * self.r ** 2
```

**Controlli tipo**:
```python
isinstance(cane, Animale)  # → True (eredita da Animale)
isinstance(cane, Gatto)    # → False
issubclass(Cane, Animale)  # → True
```

> 🎯 Esame: Uso di `super()`, polimorfismo con lista di oggetti, cosa sono le classi astratte.

## Perché importa

Ereditarietà usata nel corso per: sottoclassare `Thread`, creare eccezioni custom, estendere le classi gRPC servicer.

## Connessioni

- [[oop]] — ereditarietà è un pilastro dell'OOP
- [[threading]] — `Thread` si sottoclassa per creare thread personalizzati
- [[eccezioni]] — eccezioni custom ereditano da `Exception`

## Fonti

- [[09-oop]]

_Aggiornato: 2026-06-04 — ingest iniziale_
