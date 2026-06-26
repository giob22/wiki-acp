---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread]
---

#flashcards/acp

## Definizione

**Concorrenza** e **parallelismo** sono due tecniche per aumentare le prestazioni di un sistema di calcolo, spesso confuse ma distinte:
- **Concorrenza** — più attività la cui esecuzione **si sovrappone nel tempo**; si sfruttano i *tempi morti* del processore. Non richiede più CPU.
- **Parallelismo** — più attività eseguite **realmente nello stesso istante** su unità di calcolo distinte (CPU/core multipli).

> 🎯 Esame: **concorrenza non significa parallelismo**. Due processi sono concorrenti (su monoprocessore) se la prima operazione di uno comincia prima dell'ultima dell'altro; il parallelismo richiede hardware con più CPU.

Differenza tra concorrenza e parallelismo?
?
Concorrenza = esecuzioni che si sovrappongono nel tempo (anche su 1 CPU, time-slicing). Parallelismo = esecuzioni nello stesso istante su CPU/core distinti. La concorrenza non richiede più CPU.


## Spiegazione

**Forme di concorrenza**:
- **Multitasking** — capacità di eseguire più *processi* contemporaneamente
- **Multithreading** — più *flussi di controllo leggeri* nello stesso processo

**Forme di parallelismo**:
- **Implicito** — *Instruction-Level Parallelism* (ILP): parallelismo intrinseco delle istruzioni (architetture pipelined)
- **Esplicito** — architetture parallele (sistemi multiprocessore o *n-core*)

Le quattro combinazioni: *non concorrente non parallelo* (sequenziale), *concorrente non parallelo* (1 core, time-slicing), *non concorrente parallelo* (task distinti su core distinti), *concorrente e parallelo*.

### Speed-up e legge di Amdahl

Lo scopo di concorrenza/parallelismo è la **velocizzazione** (*speed-up*):

$$S = \frac{T_1}{T_P}$$

dove `T₁` è il tempo di esecuzione sequenziale (monoprocessore) e `T_P` il tempo su N processori. A parte casi particolari lo speed-up è **meno che lineare** rispetto al numero di CPU, perché esiste sempre una parte non parallelizzabile (sincronizzazione, inizializzazione comune).

**Legge di Amdahl** — sia `f` la frazione **sequenziale** del tempo e `(1−f)` quella **parallelizzabile**:

$$S = \frac{1}{f + \frac{1-f}{n}}$$

| Condizione | Risultato | Interpretazione |
|---|---|---|
| f = 0 | S = n | speed-up ideale, 100% parallelizzabile |
| f > 0 | S < n | speed-up limitato dal codice sequenziale |
| n → ∞ | S_max = 1/f | **limite teorico di Amdahl** |

> 🎯 Esame: la legge di Amdahl mostra che **anche poca frazione sequenziale limita drasticamente** lo speed-up. Esempio classico: compilare 3 file (3+2+1 s) e linkare (1 s) = 7 s su 1 CPU; su 3 CPU si compila in parallelo (max 3 s) + link 1 s = 4 s → speed-up 7/4 = **1.75**, pur usando il triplo dei processori.

Cosa afferma la legge di Amdahl?
?
S = 1/(f + (1-f)/n) con f frazione sequenziale. Anche una piccola f limita drasticamente lo speed-up; per n→∞, S_max = 1/f.


### Limiti del multithreading

- L'uso indiscriminato di thread **aumenta l'overhead** di scheduling e context-switch (più thread = più context-switch = meno tempo utile)
- Il tempo concorrente è compromesso dai **punti di sincronizzazione** (accesso in mutua esclusione a risorse condivise)
- Il multithreading è vantaggioso quando: il tempo di esecuzione di ciascun thread è **molto superiore** al tempo di context-switch, e l'esecuzione non è troppo vincolata da punti di sincronizzazione

### Tipi di processi e interazioni

- **Processi indipendenti** — l'esecuzione dell'uno non è influenzata dall'altro (proprietà di **riproducibilità**)
- **Processi interagenti** — l'esecuzione dell'uno è influenzata dall'altro; l'effetto dipende dalla **velocità relativa** → comportamento **non riproducibile**

Tipologie di interazione:
- **Competizione** — per l'uso di risorse comuni non condivisibili simultaneamente → richiede **mutua esclusione** (sincronizzazione *indiretta/implicita*)
- **Cooperazione** — per svolgere un'attività comune scambiando informazioni → **comunicazione**; le operazioni seguono una sequenza prefissata (sincronizzazione *diretta/esplicita*, es. produttore/consumatore)
- **Interferenza** — situazione erronea dovuta a competizione per uso non autorizzato di risorse o a soluzione errata di problemi di competizione/cooperazione; si manifesta in modo **non deterministico**

## Perché importa

È il quadro teorico che giustifica tutta la concorrenza del corso: spiega perché il [[gil]] limita il threading Python a "concorrenza senza parallelismo", e perché per il CPU-bound serve [[multiprocessing]] (parallelismo reale, comunque limitato da Amdahl).

## Connessioni

- [[processo-thread]] — multitasking vs multithreading
- [[gil]] — il threading Python dà concorrenza ma non parallelismo
- [[multiprocessing]] — parallelismo reale, soggetto al limite di Amdahl
- [[semaforo]] — strumento per i problemi di competizione (mutua esclusione)
- [[produttore-consumatore]] — problema tipico di cooperazione

## Fonti

- [[10-programmazione-concorrente-richiami]]
- [[11-python-concurrency]]

_Aggiornato: 2026-06-19 — pagina creata da slide 10 (concorrenza vs parallelismo, speed-up, legge di Amdahl, limiti multithreading, processi indipendenti/interagenti, competizione/cooperazione/interferenza)_
