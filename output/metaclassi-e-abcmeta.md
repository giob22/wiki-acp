# Metaclassi e `ABCMeta` in Python

> Export didattico. Argomento ancorato alla slide `01_PYTHON_09-Python_OOP`.
>
> ⚠️ **Livello di copertura del corso:** la slide tratta le metaclassi in modo *leggerissimo* — le nomina solo per spiegare `ABCMeta`. Le sezioni marcate **⚠️ oltre la slide** sono approfondimento: utili per capire *davvero*, ma all'esame il professore si ferma a «Python usa le metaclassi per definire il tipo di una classe → da lì nasce `ABCMeta`».
>
> Nota sul nome: nel materiale si chiama **`ABCMeta`** (la metaclasse) con la classe ausiliaria **`ABC`**. Non esiste "MetaABC".

---

## 1. Punto di partenza: in Python tutto è un oggetto (slide)

Anche le **classi** sono oggetti. La slide lo dimostra con `type()`:

```python
>>> c = Coordinate(3, 4)
>>> print(type(c))
<class '__main__.Coordinate'>   # il tipo dell'istanza c è la classe Coordinate

>>> print(type(Coordinate))
<class 'type'>                  # il tipo della classe Coordinate è... type
```

La catena dei tipi:

```
istanza   →   classe      →   metaclasse
   c          Coordinate         type
```

- `c` è un'istanza di `Coordinate` → `type(c)` è `Coordinate`
- `Coordinate` è un'istanza di `type` → `type(Coordinate)` è `type`

Quindi una **classe è essa stessa un oggetto**, e l'oggetto da cui è "istanziata" è la sua **metaclasse**. La metaclasse di default in Python è **`type`**.

---

## 2. Cos'è una metaclasse (definizione)

Definizione testuale della slide:

> *"Python usa delle metaclassi per definire il tipo di una classe. Una metaclasse è una classe che consente ad altre classi di essere istanziate come oggetto della metaclasse stessa."*

In una frase:

> **Se la classe è lo stampo delle istanze, la metaclasse è lo stampo delle classi.**

Una **metaclasse** governa **come una classe viene creata**, non come si comporta un'istanza. Quando scrivi `class Coordinate: ...`, Python non "esegue" solo il blocco: **chiama la metaclasse** per costruire l'oggetto-classe e lo assegna al nome `Coordinate`.

| Livello | Oggetto | Stampato da | Quando agisce |
|---|---|---|---|
| Istanza | `c` | la classe `Coordinate` | a ogni `Coordinate(...)` |
| Classe | `Coordinate` | la metaclasse `type` | una volta, alla definizione della classe |

---

## 3. Come `type` costruisce le classi (⚠️ oltre la slide)

`type` ha una **doppia natura**:

- con **un** argomento → ritorna il tipo di un oggetto: `type(c)`
- con **tre** argomenti → **crea una classe** a runtime

Queste due definizioni sono equivalenti:

```python
# forma normale (zucchero sintattico)
class Coordinate:
    pianeta = "Terra"
    def saluta(self): return "ciao"

# forma esplicita tramite la metaclasse
Coordinate = type(
    "Coordinate",                       # name  → nome della classe
    (),                                  # bases → tuple delle classi base (ereditarietà)
    {                                    # namespace → attributi e metodi
        "pianeta": "Terra",
        "saluta": lambda self: "ciao",
    },
)
```

La parola chiave `class` è **zucchero sintattico** su `type(name, bases, namespace)`.
È letteralmente questo che la slide intende con «Python usa le metaclassi per definire il tipo di una classe».

---

## 4. Scrivere una metaclasse propria (⚠️ oltre la slide)

Si deriva da `type` e si indica con `metaclass=`:

```python
class MiaMeta(type):
    def __new__(mcs, name, bases, namespace):
        # mcs = la metaclasse; gira UNA volta per OGNI classe creata con questa metaclasse
        namespace["creata_da"] = "MiaMeta"
        return super().__new__(mcs, name, bases, namespace)

class Foo(metaclass=MiaMeta):
    pass

print(Foo.creata_da)   # "MiaMeta"
```

Metodi chiave della metaclasse:

- **`__new__`** — costruisce e ritorna l'oggetto-classe (può ispezionare/modificare metodi e attributi *prima* che la classe esista).
- **`__init__`** — inizializza la classe appena creata.

> 💡 La metaclasse interviene **alla definizione della classe** (una volta sola), non a ogni creazione di istanza. È il momento giusto per imporre vincoli strutturali su *come le classi sono scritte*: validare le sottoclassi, registrarle automaticamente, oppure **impedire l'istanziazione** se mancano certi metodi. Quest'ultimo è esattamente ciò che fa il modulo `abc`.

---

## 5. `ABCMeta` e `ABC` — il punto del corso (slide)

Il modulo `abc` fornisce l'infrastruttura per le **Abstract Base Class (ABC)** e si appoggia proprio alle metaclassi.

- **`ABCMeta`** — la **metaclasse** vera e propria. Una classe la cui metaclasse è `ABCMeta` (o derivata):
  1. **non può essere istanziata** finché restano metodi astratti non sovrascritti;
  2. gestisce la registrazione delle sottoclassi virtuali (`.register()`).
- **`ABC`** — **classe ausiliaria** comoda che ha già `ABCMeta` come metaclasse. Serve solo a evitare la sintassi `metaclass=`.

Le due forme sono equivalenti:

```python
# forma con la metaclasse (esplicita)
from abc import ABCMeta, abstractmethod
class Animal(metaclass=ABCMeta):
    @abstractmethod
    def doAction(self): pass

# forma con la classe helper (quella della slide)
from abc import ABC, abstractmethod
class Animal(ABC):          # ABC "deriva" ABCMeta → stesso effetto
    @abstractmethod
    def doAction(self): pass
```

### `@abstractmethod`

Il decoratore marca un metodo come astratto. Citazione testuale della slide:

> *"L'uso di questo decoratore richiede che la metaclasse della classe sia `ABCMeta` o che derivi da essa (e.g., `ABC` deriva `ABCMeta`). Una classe che ha una metaclasse derivata da `ABCMeta` non può essere istanziata a meno che tutti i suoi metodi astratti [...] non vengano sovrascritti."*

Meccanismo concreto: è **`ABCMeta` (la metaclasse) che, al momento dell'istanziazione, controlla se restano metodi astratti** e in caso solleva l'eccezione. Senza la metaclasse, `@abstractmethod` sarebbe un decoratore inerte.

```python
class Animal(ABC):
    @abstractmethod
    def doAction(self): pass

class Human(Animal):
    def doAction(self): print("I can walk and run")

a = Animal()
# TypeError: Can't instantiate abstract class Animal with abstract method doAction

R = Human()      # OK: doAction sovrascritto
R.doAction()     # "I can walk and run"
```

La differenza la fa **solo** `@abstractmethod` (esempio della slide):

| Codice | Istanziabile? |
|---|---|
| `def doAction(self): pass` (senza decoratore) | **Sì**, nessuna eccezione |
| `@abstractmethod def doAction(self): pass` | **No**, `TypeError` |

---

## 6. Sintesi della catena logica

```
tutto è oggetto
    └─ anche le classi sono oggetti       (type(Coordinate) == type)
        └─ la classe della classe = metaclasse
            └─ metaclasse di default = type        (crea le classi: type(name, bases, ns))
                └─ metaclasse specializzata = ABCMeta
                    └─ controlla i metodi astratti all'istanziazione
                        └─ @abstractmethod li marca
                            └─ ABC = scorciatoia che eredita ABCMeta
```

---

## 7. Per l'esame

> 🎯 **Esame:** il filo logico richiesto è **classe astratta → modulo `abc` → metaclasse `ABCMeta` → `@abstractmethod`**. Punto da non sbagliare: l'impossibilità di istanziare una classe astratta **non** è magia del decoratore, è la **metaclasse `ABCMeta`** che fa il controllo. `ABC` è solo una scorciatoia che eredita quella metaclasse.

> 🎯 **Esame:** sapere spiegare `type(Coordinate)` → `type`, cioè che le classi sono oggetti e la loro classe è la metaclasse.

> 💡 **Connessione (`polimorfismo`):** le ABC sono lo strumento Python per imporre un'interfaccia *nominale* (devi ereditare e implementare), in contrapposizione al **duck typing** strutturale e a `typing.Protocol`. ABC = "interfacce formali"; duck typing = "interfacce informali" (entrambe nominate nella slide OOP).

---

## Fonti

- Slide raw: `01_PYTHON_09-Python_OOP` (sezione "Classi Astratte e Interfacce", "il modulo abc", `type()`).
- Pagine wiki correlate: `[[ereditarieta]]` (classi astratte con `abc`), `[[polimorfismo]]` (ABC vs Protocol vs duck typing), `[[oop]]`.

_Generato: 2026-06-26 — export didattico metaclassi + ABCMeta su richiesta. Sezioni 3-4 marcate come approfondimento oltre la slide._
