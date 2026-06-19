---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, linux-namespaces, cgroups]
---

## Definizione

Un **container** è un'unità di esecuzione leggera e portatile che isola un'applicazione con le sue dipendenze, sfruttando le primitive del kernel host (namespaces e cgroups) invece di emulare hardware e sistema operativo come fanno le Virtual Machine.

## Spiegazione

### Il problema delle Virtual Machine

Le VM tradizionali virtualizzano l'hardware intero: ogni VM include un sistema operativo guest completo gestito da un hypervisor (Type-1 o Type-2). Questo introduce:
- **Overhead prestazionale** dovuto a hypervisor e OS guest
- **Elevato consumo di memoria e storage** (ogni VM porta il proprio OS)
- **Avvio lento** (ordine dei minuti)
- **Costi di licenza e manutenzione** del guest OS

La domanda chiave è: è davvero necessario virtualizzare tutta l'hardware?

### La soluzione container

Un container **non è una macchina virtuale** nel senso tradizionale:
- **Non c'è emulazione** di dispositivi fisici
- Condivide il **kernel host** direttamente
- Usa le astrazioni native del kernel: [[linux-namespaces]] per l'isolamento, [[cgroups]] per la gestione delle risorse

Questo consente:
- Avvio in **~2 secondi** (vs ~2 minuti VM vs ~5-10 minuti bare metal)
- Deploy in secondi
- Scaling guidato da policy
- Footprint ridotto: **100-1000 container** vs 10-100 VM sullo stesso server fisico

### Confronto prestazionale

| Aspetto | Bare Metal | VM | Container |
|---|---|---|---|
| Boot time | ~5-10 min | ~2 min | ~2 sec |
| Deploy | Settimane | Minuti | Secondi |
| Complessità deploy | HW + OS + Runtime + App | OS + Runtime + App | Runtime + App |
| Investimento | Server dedicato | VM dedicata | Pay per runtime |
| Scaling | Mesi | Ore | Secondi |

### Stack architetturale a confronto

```
Container:  [ App/Libs ]
            [ Container management libraries ]
            [ Host Kernel ]
            [ CPU | Storage | Memory | Network ]

VM:         [ App/Libs ]
            [ Guest OS ]
            [ Hypervisor (Type-2) ]
            [ Host Kernel/OS ]
            [ CPU | Storage | Memory | Network ]
```

La differenza fondamentale: il container **non ha Guest OS né Hypervisor**. Comunica direttamente col kernel host tramite namespaces e cgroups.

## Perché importa

Comprendere i container è fondamentale per capire il deployment moderno di servizi. Tutto il corso culmina nel poter deployare applicazioni (Flask, gRPC, MongoDB) in modo portabile e scalabile, indipendentemente dall'ambiente sottostante.

> 🎯 Esame: La domanda "differenza tra container e VM" è quasi certamente presente. Risposta chiave: no emulazione hardware, no Guest OS, usa namespaces + cgroups del kernel host.

## Connessioni

- [[linux-namespaces]] — meccanismo kernel per l'isolamento
- [[cgroups]] — meccanismo kernel per la gestione delle risorse
- [[docker]] — principale implementazione di container
- [[docker-swarm]] — orchestrazione cluster di container
- [[kubernetes]] — orchestratore alternativo più avanzato

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
