---
tipo: concetto
importanza_esame: media
prerequisiti: [threading, gil, processo-thread]
---

## Definizione

**asyncio** è il modulo Python per la programmazione **asincrona** basata su **event loop** e **coroutine**. Alternativa a threading e multiprocessing per workload I/O-bound: un singolo thread gestisce N operazioni concorrenti tramite sospensione cooperativa, senza bloccarsi.

## Spiegazione

TODO: da espandere — nessuna slide dedicata ancora ingesta per questo argomento.

**Concetti fondamentali**:
- **Event loop**: ciclo che gestisce l'esecuzione delle coroutine e dispatcha eventi I/O
- **Coroutine** (`async def`): funzione che può sospendersi cedendo il controllo all'event loop
- **`await`**: sospende la coroutine corrente; l'event loop esegue altri task nel frattempo
- **Task**: coroutine schedulata per esecuzione concorrente

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)   # I/O simulato — event loop esegue altri task
    return f"data da {url}"

async def main():
    results = await asyncio.gather(fetch("a"), fetch("b"), fetch("c"))
    # le 3 fetch girano "concorrentemente" in ~1s, non 3s
    print(results)

asyncio.run(main())
```

**Confronto con threading e multiprocessing**:

| | threading | multiprocessing | asyncio |
|---|---|---|---|
| GIL | sì (limita CPU-bound) | no (processi separati) | no (single-thread) |
| Adatto a | I/O-bound | CPU-bound | I/O-bound |
| Overhead | medio (context switch OS) | alto (spawn processo) | basso (context switch cooperativo) |
| Modello | preemptive | preemptive | cooperativo |

Il modello **cooperativo** significa che un task cede il controllo esplicitamente con `await` — nessun preemption da parte dell'OS. Vantaggio: nessuna race condition su strutture dati condivise; svantaggio: un task che non fa mai `await` blocca l'intero event loop.

> 🎯 Esame: asyncio è alternativa single-thread a threading per I/O-bound — nessun problema GIL perché single-threaded; richiede `await` esplicito (cooperativo, non preemptive).

## Perché importa

asyncio è il terzo pilastro della concorrenza Python (dopo [[threading]] e [[multiprocessing]]). Citato esplicitamente nel programma del corso (slide 00-introduzione). Usato da FastAPI (web framework) e in operazioni di rete ad alta concorrenza.

## Connessioni

- [[threading]] — alternativa preemptive multi-thread; stessa classe di problemi I/O-bound
- [[multiprocessing]] — alternativa per CPU-bound; processi separati, nessun GIL
- [[gil]] — asyncio aggira il GIL perché single-threaded (un solo thread alla volta)
- [[socket]] — asyncio offre API asincrone per socket (`asyncio.open_connection`)

## Fonti

TODO: nessuna fonte ingesta per asyncio — fonte raw mancante; il concetto è menzionato in [[00-introduzione]]

_Aggiornato: 2026-06-06 — stub creato per riparare link rotto in 00-introduzione; da espandere con ingest dedicato_
