---
tipo: concetto
importanza_esame: alta
prerequisiti: [processo-thread, linux-namespaces, cgroups]
---

#flashcards/acp

## Definizione

Un **container** è un'unità di esecuzione leggera e portatile che isola un'applicazione con le sue dipendenze, sfruttando le primitive del kernel host (namespaces e cgroups) invece di emulare hardware e sistema operativo come fanno le Virtual Machine.

## Spiegazione

### Il problema delle Virtual Machine

Le VM tradizionali virtualizzano l'hardware intero: ogni VM include un sistema operativo guest completo gestito da un hypervisor. Questo introduce:
- **Overhead prestazionale** dovuto a hypervisor e OS guest
- **Elevato consumo di memoria e storage** (ogni VM porta il proprio OS)
- **Avvio lento** (ordine dei minuti)
- **Costi di licenza e manutenzione** del guest OS

La domanda chiave è: è davvero necessario virtualizzare tutta l'hardware?

**Hypervisor Type-1 vs Type-2**: un hypervisor **Type-1** (*bare-metal*) gira direttamente sull'hardware (VMware ESXi, Xen, Hyper-V); un **Type-2** (*hosted*) gira come applicazione sopra un OS host (VirtualBox, VMware Workstation). Lo stack VM del corso è disegnato come Type-2: risorse fisiche → Host Kernel/OS → Hypervisor → Guest OS → App/Libs.

**Perché le VM hanno overhead — trap-and-emulate**: non tutte le operazioni del guest pagano lo stesso costo; quelle costose sono le **istruzioni privilegiate/sensitive**. Su x86 la CPU ha **livelli di privilegio** (*ring*): il **ring 0** è riservato al kernel, il **ring 3** al codice utente. Alcune istruzioni (accesso all'hardware, modifica memoria fisica, configurazione interruzioni) sono eseguibili **solo in ring 0**. In una VM il guest OS *crede* di girare in ring 0, ma l'hypervisor lo ha "declassato": a ogni istruzione privilegiata la CPU genera una **trap** verso l'hypervisor, che **intercetta, emula o traduce** l'operazione e restituisce il controllo. Questo meccanismo (**trap-and-emulate**) è il cuore dell'overhead. Nei container **non esiste**: il processo containerizzato esegue le proprie system call **direttamente sul kernel host**, che le esegue normalmente limitandosi ad applicare le restrizioni di namespace e cgroups (è la "nessun overhead dovuto al livello di hypervisor" della slide).

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

### Il container come "processo esteso"

Concetto chiave da interiorizzare: dal punto di vista del kernel, **un container è un normale processo (o gruppo di processi) Linux**, a cui però il kernel "mente" su ciò che lo circonda. Il processo crede di avere il proprio filesystem, la propria rete, il proprio elenco di processi — ma è solo una **vista ristretta** delle risorse dell'host. Possiamo quindi identificarlo come un **processo esteso**: un processo normale arricchito di una vista privata delle risorse ([[linux-namespaces]]) e di limiti sul consumo ([[cgroups]]). La **virtualizzazione leggera** è definibile come una virtualizzazione in cui si **riusano le astrazioni già offerte dal kernel** invece di costruirne di nuove via software. Conseguenza fondamentale: **tutti i container su un host condividono lo stesso kernel** → non si può eseguire un container Windows su un kernel Linux (mentre con una VM sì, perché la VM porta con sé il proprio OS). Per questo Docker Desktop su Mac/Windows nasconde sotto una **VM Linux leggera**.

### Il rovescio della medaglia: l'isolamento

I container **non sono veramente isolati** come le VM: il kernel host condiviso è un **single point of failure** e un'unica superficie d'attacco — un bug o una vulnerabilità del kernel compromette potenzialmente *tutti* i container, e un crash del kernel li abbatte tutti insieme. Anche le VM non sono perfettamente isolate (esistono attacchi di *privilege escalation* e di **VM escape**), ma gli hypervisor sono progettati apposta per l'isolamento, con una superficie d'attacco molto più piccola di un kernel general-purpose → sono più affidabili sul piano della sicurezza. È il **trade-off fondamentale prestazioni ↔ isolamento**: la virtualizzazione leggera guadagna prestazioni proprio togliendo lo strato di indirezione (l'hypervisor) che però dava l'isolamento. Questo spiega l'esistenza di runtime "ibridi" come **gVisor** (kernel in user-space) e **Kata** (micro-VM leggera) che reintroducono un po' di indirezione per recuperare isolamento (→ [[kubernetes]], OCI).

> 💡 Filosofia operativa: i container sono **effimeri e usa-e-getta** — *cattle, not pets* (bestiame, non animali domestici): se un container ha problemi non lo si "cura", lo si distrugge e se ne crea uno nuovo. Lo stato persistente va quindi fuori dal container (volumi, DB).

## Perché importa

Comprendere i container è fondamentale per capire il deployment moderno di servizi. Tutto il corso culmina nel poter deployare applicazioni (Flask, gRPC, MongoDB) in modo portabile e scalabile, indipendentemente dall'ambiente sottostante.

> 🎯 Esame: La domanda "differenza tra container e VM" è quasi certamente presente. Risposta chiave: no emulazione hardware, no Guest OS, usa namespaces + cgroups del kernel host.

Differenza fondamentale tra container e VM?
?
Il container non emula hardware e non ha Guest OS: condivide il kernel host e usa namespaces (isolamento) + cgroups (risorse). La VM virtualizza l'hardware con hypervisor + OS guest completo.


## Connessioni

- [[linux-namespaces]] — meccanismo kernel per l'isolamento
- [[cgroups]] — meccanismo kernel per la gestione delle risorse
- [[docker]] — principale implementazione di container
- [[docker-swarm]] — orchestrazione cluster di container
- [[kubernetes]] — orchestratore alternativo più avanzato

## Fonti

- [[03-service-deployment-containers]]

_Aggiornato: 2026-06-12 — ingest iniziale_
_Aggiornato: 2026-06-19 — MODULO 4 (slide 03 + appunti): hypervisor Type-1/Type-2, trap-and-emulate/ring 0-3/istruzioni sensitive (origine overhead VM), container come "processo esteso" + condivisione kernel, trade-off prestazioni↔isolamento (single point of failure/VM escape/gVisor-Kata), cattle-not-pets_
