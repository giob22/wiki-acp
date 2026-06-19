---
tipo: concetto
importanza_esame: alta
prerequisiti: [funzioni]
---

## Definizione

Lo **scope** (ambito) in Python determina la visibilità dei nomi (variabili). Python usa la regola **LEGB**: Local → Enclosing → Global → Built-in. Ogni chiamata di funzione crea un nuovo **frame** (scope locale) indipendente.

## Spiegazione

**Regola LEGB** (ordine di ricerca di un nome):
1. **Local**: scope della funzione corrente
2. **Enclosing**: scope delle funzioni esterne annidate
3. **Global**: scope del modulo
4. **Built-in**: nomi predefiniti Python (`len`, `print`, ...)

```python
x = 10  # global

def outer():
    x = 20  # enclosing per inner
    def inner():
        x = 30  # local di inner
        print(x)  # → 30 (local)
    inner()
    print(x)  # → 20 (enclosing di outer = local di outer)

outer()
print(x)  # → 10 (global)
```

**Esempio complesso con h() dentro g()** (dalle slide):
```python
def g(x):
    def h():
        x = 'abc'  # locale a h — NON modifica x di g
    x = x + 1      # x locale a g (= param + 1)
    print('g: x =', x)  # stampa x di g
    h()             # h modifica il suo x locale; g.x rimane invariato
    return x        # restituisce x di g

x = 3
z = g(x)   # z = 4, global x rimane 3
```

**Keyword `global`**: forza un nome nello scope locale a referenziare quello globale:
```python
x = 10
def f():
    global x
    x = x + 1  # modifica x globale
f()
print(x)  # → 11
```

**Keyword `nonlocal`**: come `global` ma per scope enclosing:
```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x = x + 1
    inner()
    print(x)  # → 11
```

> 🎯 Esame: Il comportamento di `h()` dentro `g()` con variabili locali dallo stesso nome — domanda tipica all'orale.

## Perché importa

Capire lo scope è essenziale per prevedere il comportamento del codice, specie con funzioni annidate e passaggio parametri. Senza questo, comportamenti sorprendenti sembrano bug.

## Connessioni

- [[funzioni]] — ogni chiamata crea un frame/scope locale
- [[passaggio-parametri]] — il passaggio per assegnazione crea un binding locale

## Fonti

- [[04-funzioni]]
- [[07-passaggio-parametri]]

_Aggiornato: 2026-06-04 — ingest iniziale_
