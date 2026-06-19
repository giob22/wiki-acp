# Svolgimenti — prove simulate

Una sottocartella per ogni prova svolta.

## Struttura

```
svolgimenti/
├── [ANNO]-[SESSIONE]-sim-01/
│   ├── prova.md          ← prova generata da Claude
│   └── soluzione.md      ← tuo svolgimento
├── [ANNO]-[SESSIONE]-sim-02/
│   └── ...
```

## Workflow

1. `genera prove` → Claude crea `prova.md` in una nuova cartella
2. Svolgi e scrivi la tua risposta in `soluzione.md`
3. `valuta svolgimento [cartella]` → Claude corregge e assegna voto

## Comando valutazione

```
valuta svolgimento svolgimenti/[nome-cartella]
```

Claude legge `prova.md` + `soluzione.md` e produce:
- voto per domanda
- errori concettuali
- punti persi e perché
- suggerimenti di studio
