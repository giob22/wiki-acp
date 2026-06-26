---
tipo: concetto
importanza_esame: alta
prerequisiti: [oop, ereditarieta]
---

#flashcards/acp

## Definizione

Il **polimorfismo** è la capacità di oggetti di **tipi diversi** di rispondere allo **stesso messaggio** (stessa chiamata di metodo / stessa interfaccia) in modo **specifico per il proprio tipo**. La domanda chiave che distingue i linguaggi è: **come si decide se un oggetto è "idoneo"** a essere usato dove ci si aspetta un certo comportamento?

- **Java → polimorfismo nominale**: l'idoneità è decisa in base alla **classe** dell'oggetto e alle **relazioni di ereditarietà/implementazione dichiarate esplicitamente** (per *nome* del tipo).
- **Python → polimorfismo strutturale (duck typing)**: l'idoneità è decisa in base alla **struttura** dell'oggetto, cioè a *quali metodi/attributi possiede*, indipendentemente dalla sua classe.

## Spiegazione

### Java — polimorfismo nominale

In Java un oggetto è utilizzabile al posto di un tipo `T` **solo se la sua classe dichiara esplicitamente** la relazione: `class Cane extends Animale` oppure `class X implements Interfaccia`. Conta il **nome** del tipo e la gerarchia dichiarata (relazione "is-a" esplicita). La verifica è **statica**: il **compilatore** controlla a compile-time che il tipo dichiarato esponga il metodo invocato.

```java
class Animale { String parla() { return "..."; } }
class Cane extends Animale { String parla() { return "Bau!"; } }   // override

Animale a = new Cane();   // ok: Cane è-un Animale (relazione dichiarata)
a.parla();                // → "Bau!"  (dynamic dispatch sul tipo EFFETTIVo)
```

Forme di polimorfismo in Java:
- **Subtype / override (runtime, "inclusion")**: il metodo virtuale è risolto a **runtime** (*dynamic dispatch*, via vtable) in base al **tipo effettivo** dell'oggetto, non al tipo dichiarato della variabile.
- **Overload (ad-hoc, compile-time)**: stesso nome di metodo, **firme diverse**; risolto a compile-time in base ai tipi degli argomenti.
- **Parametrico (generics)**: `class Box<T> { ... }`.

> ⚠️ Punto cruciale del nominale: se due classi **non imparentate** espongono entrambe un metodo `parla()` con la stessa firma, **non** sono interscambiabili — manca la relazione di ereditarietà/implementazione **dichiarata**. Java rifiuta a compile-time.

### Python — polimorfismo strutturale (duck typing)

Principio del **duck typing**: *"If it walks like a duck and quacks like a duck, it's a duck."* Conta la **struttura** dell'oggetto (i metodi/attributi che possiede), **non** la sua classe né una base comune. La verifica è **dinamica**: il metodo viene cercato **a runtime** (lookup nell'`__dict__` dell'oggetto/della classe lungo l'MRO); se c'è, funziona, altrimenti si solleva `AttributeError` **a runtime**.

```python
class Cane:
    def parla(self): return "Bau!"

class Anatra:                 # NON eredita da Cane né da una base comune
    def parla(self): return "Qua!"

def fai_parlare(x):
    return x.parla()          # non importa il TIPO di x, basta che abbia parla()

fai_parlare(Cane())           # → "Bau!"
fai_parlare(Anatra())         # → "Qua!"   ← polimorfe pur senza alcuna parentela
```

Conseguenze:
- **Non serve una superclasse comune** né implementare un'interfaccia dichiarata: l'interfaccia in Python è **implicita** (un *protocollo* = l'insieme dei metodi attesi).
- L'ereditarietà con override (→ [[ereditarieta]]) è **un caso particolare** di polimorfismo, ma non è la condizione necessaria: in Python lo è la sola presenza dei metodi giusti.
- Strumenti opzionali per **imporre** struttura: `abc.ABC` + `@abstractmethod` (impone che le sottoclassi definiscano certi metodi); `typing.Protocol` (PEP 544) per *structural subtyping* verificabile staticamente dai type checker ("static duck typing").

### Confronto diretto

| | **Java — nominale** | **Python — strutturale (duck typing)** |
|---|---|---|
| Cosa decide l'idoneità | il **nome del tipo** + relazione `extends`/`implements` dichiarata | la **struttura**: i metodi/attributi presenti sull'oggetto |
| Quando si verifica | **compile-time** (tipizzazione statica) | **runtime** (tipizzazione dinamica) |
| Serve una base comune? | **Sì** (gerarchia dichiarata) | **No** (classi non imparentate possono essere polimorfe) |
| Cosa succede se non idoneo | **errore di compilazione** | **`AttributeError` a runtime** |
| Meccanismo di dispatch | *dynamic dispatch* su vtable (per override) | *lookup* dell'attributo a runtime lungo l'MRO |
| Interfacce | esplicite (`interface`) | implicite (protocolli); opzionali `ABC`/`Protocol` |

> 🎯 Esame: *"Come funziona il polimorfismo in Python?"* → **duck typing**, polimorfismo **strutturale e dinamico**: conta cosa l'oggetto *sa fare*, non la sua classe. Contrapporlo al **nominale** di Java, **statico**, basato sulla classe e sulle relazioni di ereditarietà dichiarate. Trade-off: il nominale dà sicurezza a compile-time e contratti espliciti; lo strutturale dà flessibilità e codice più generico, al prezzo di errori spostati a runtime.

Come funziona il polimorfismo in Python e in cosa differisce da Java?
?
Python: duck typing, strutturale e dinamico — conta cosa l'oggetto sa fare, non la classe (errori a runtime). Java: nominale e statico — conta la classe e le relazioni dichiarate (controlli a compile-time).


## Perché importa

È una domanda d'orale ricorrente, sia da sola sia dentro "differenze OOP Python vs Java". Il tema ritorna nel corso:
- **`Thread`**: si fa l'override di `run()` — in Java nominale (sottoclasse di `Thread` o implementazione di `Runnable`, → [[java-threading]]), in Python override del metodo (→ [[threading]]).
- **gRPC**: gli stub generati definiscono un'interfaccia che il servicer implementa — in Java il servicer **implementa** l'interfaccia generata (nominale), in Python eredita dalla classe `...Servicer` ma di fatto conta che esponga i metodi giusti.

## Connessioni

- [[ereditarieta]] — l'override dei metodi è il caso "subtype" del polimorfismo; in Python è un caso particolare del duck typing
- [[oop]] — il polimorfismo è uno dei pilastri dell'OOP (con incapsulamento ed ereditarietà)
- [[java-threading]] — override di `run()` / `Runnable`: polimorfismo nominale in azione
- [[threading]] — l'equivalente Python (override di `run`) sfrutta il duck typing
- [[grpc]] — interfacce generate dagli stub: nominale (Java) vs strutturale (Python)

## Fonti

- [[09-oop]]

_Aggiornato: 2026-06-20 — creazione pagina: polimorfismo nominale (Java) vs strutturale/duck typing (Python), forme (override/overload/generics), confronto statico/dinamico, ABC/Protocol_
