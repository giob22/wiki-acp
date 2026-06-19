---
tipo: concetto
importanza_esame: media
prerequisiti: [interprete-python]
---

## Definizione

I tipi scalari di Python sono tipi di dato che rappresentano un singolo valore atomico: `int`, `float`, `bool`, `NoneType`. In Python **tutto è un oggetto**, inclusi i valori scalari.

## Spiegazione

**Tipi scalari**:

| Tipo | Esempio | Note |
|------|---------|------|
| `int` | `42`, `-7`, `0` | Precisione arbitraria (no overflow) |
| `float` | `3.14`, `-0.5` | Doppia precisione IEEE 754 |
| `bool` | `True`, `False` | Sottotipo di `int` (`True == 1`) |
| `NoneType` | `None` | Unico valore del tipo; usato per "assenza di valore" |

**Type casting** (conversione esplicita):
```python
int("42")       # → 42
float(3)        # → 3.0
str(42)         # → "42"
bool(0)         # → False (falsy: 0, None, "", [], {})
```

**Operatori aritmetici**:
```python
7 / 2   # → 3.5   (divisione reale)
7 // 2  # → 3     (divisione intera, floor)
7 % 2   # → 1     (modulo)
2 ** 8  # → 256   (potenza)
```

**Operatori di confronto**: `==`, `!=`, `<`, `>`, `<=`, `>=` → restituiscono `bool`

**Operatori logici**: `and`, `or`, `not` — cortocircuito (short-circuit evaluation)

> 🎯 Esame: La differenza tra `/` e `//`, e capire i valori "falsy" sono domande tipiche.

## Perché importa

La distinzione mutabile/immutabile (tutti gli scalari sono immutabili) è fondamentale per capire il passaggio parametri.

## Connessioni

- [[stringhe]] — tipo non-scalare immutabile con comportamento simile
- [[passaggio-parametri]] — scalari immutabili → rebind locale non modifica il chiamante

## Fonti

- [[02-tipi-scalari-stringhe]]

_Aggiornato: 2026-06-04 — ingest iniziale_
