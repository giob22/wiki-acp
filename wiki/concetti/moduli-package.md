---
tipo: concetto
importanza_esame: media
prerequisiti: [funzioni]
---

#flashcards/acp

## Definizione

Un **modulo** Python è un file `.py` che contiene funzioni, classi e variabili riutilizzabili. Un **package** è una directory che contiene un file `__init__.py` e può contenere moduli e sotto-package.

## Spiegazione

**Importare un modulo**:
```python
import math               # accesso: math.sqrt(4)
from math import sqrt     # accesso diretto: sqrt(4)
import numpy as np        # alias: np.array(...)
from os import *          # importa tutto (sconsigliato)
```

**Guard `__name__`**:
```python
if __name__ == "__main__":
    # eseguito solo quando il file è lo script principale
    # NON eseguito quando il modulo è importato
    main()
```

**Meccanismo di ricerca moduli** (ordine):
1. Directory corrente
2. `PYTHONPATH` (variabile d'ambiente)
3. `sys.path` (lista configurabile)
4. Standard library

```python
import sys
print(sys.path)   # mostra percorsi di ricerca
```

**Gestione pacchetti**: `pip install nome-pacchetto` installa da PyPI

**Package**:
```
mio_package/
    __init__.py       # rende la directory un package (può essere vuoto)
    modulo1.py
    modulo2.py
    sotto_pkg/
        __init__.py
        modulo3.py
```

```python
from mio_package import modulo1
from mio_package.sotto_pkg import modulo3
```

**`__all__`** in `__init__.py`: lista di nomi esportati con `from pkg import *`

**Import assoluti** (raccomandati): `from sound.effects import echo`

**Import relativi** (all'interno del package):
```python
from . import echo          # package corrente
from .. import formats      # package padre
from ..filters import eq    # sotto-package fratello
```

**`__path__`**: variabile che controlla dove il package cerca i suoi sottomoduli

> 🎯 Esame: La guard `__name__ == "__main__"` e la struttura dei package.

A cosa serve la guard `if __name__ == "__main__":`?
?
Esegue quel blocco solo quando il file è lanciato direttamente come script, non quando è importato come modulo (__name__ vale '__main__' solo nel primo caso).


## Perché importa

I moduli e package sono il meccanismo di organizzazione del codice Python — base per l'uso di librerie come `grpcio`, `flask`, `pymongo`.

## Connessioni

- [[funzioni]] — i moduli espongono funzioni
- [[oop]] — i moduli espongono classi

## Fonti

- [[05-moduli-package]]

_Aggiornato: 2026-06-04 — ingest iniziale_
