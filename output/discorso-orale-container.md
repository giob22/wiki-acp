# Discorso orale — Virtualizzazione e Container

> Export discorsivo da [[virtualizzazione-container]], [[linux-namespaces]],
> [[cgroups]], [[docker]], [[docker-compose]], [[docker-swarm]] e [[kubernetes]]
> per l'esposizione orale. Testo da leggere/parlare, non schematico. Ordine logico:
> problema delle VM → da dove nasce l'overhead (trap-and-emulate, ring) → la
> soluzione container (kernel condiviso, "processo esteso") → i due pilastri
> (namespaces = isolamento, cgroups = risorse) → Docker (immagini a layer/OverlayFS,
> Dockerfile, under the hood) → orchestrazione (Compose → Swarm → Kubernetes) →
> il trade-off prestazioni↔isolamento → (in coda) cosa rispondere se chiedono oltre.
> _Generato: 2026-06-26 — fonte: PDF 03-service-deployment-containers + appunti._

---

## Apertura (la frase con cui cominciare)

"Il tema dei container nasce da una domanda molto concreta: quando devo *deployare* un'applicazione — penso ai servizi che abbiamo costruito nel corso, un server Flask, un server gRPC, MongoDB, ActiveMQ — come faccio a eseguirla in modo **portabile, riproducibile e indipendente dall'ambiente** della macchina su cui gira? La risposta classica era la **macchina virtuale**; la risposta moderna è il **container**. E la differenza tra le due non è un dettaglio implementativo: è una scelta su *quanto* virtualizzare. Per questo conviene partire dal problema delle VM, capire da dove viene il loro costo, e arrivare al container come forma di **virtualizzazione leggera**."

## Il problema delle macchine virtuali

"Una macchina virtuale virtualizza **l'intero hardware**: ogni VM contiene un **sistema operativo guest completo**, gestito da un componente chiamato **hypervisor**. Questo dà un isolamento molto forte, ma ha un prezzo su quattro fronti. Primo, **overhead prestazionale** dovuto all'hypervisor e all'OS guest. Secondo, **alto consumo di memoria e storage**, perché ogni VM si porta dietro il proprio sistema operativo. Terzo, **avvio lento**, nell'ordine dei minuti. Quarto, **costi di licenza e manutenzione** del guest OS.

Sugli hypervisor vale la pena fare una distinzione: un hypervisor **Type-1**, detto *bare-metal*, gira direttamente sull'hardware — VMware ESXi, Xen, Hyper-V; un **Type-2**, detto *hosted*, gira come applicazione sopra un sistema operativo host — VirtualBox, VMware Workstation. Lo stack VM tipico, dal basso, è: risorse fisiche → kernel/OS host → hypervisor → guest OS → applicazione e librerie.

A questo punto la domanda chiave da porsi a voce alta è: *è davvero necessario virtualizzare tutto l'hardware?* È da questa domanda che nascono i container."

## Da dove nasce l'overhead: trap-and-emulate e i ring

"Vale la pena spiegare *perché* le VM costano, perché è il cuore della differenza coi container. Non tutte le operazioni del guest pagano lo stesso prezzo: quelle costose sono le **istruzioni privilegiate o sensitive**. Sulle CPU x86 esistono dei **livelli di privilegio**, chiamati *ring*: il **ring 0** è riservato al kernel, il **ring 3** al codice utente. Certe istruzioni — accesso diretto all'hardware, modifica della memoria fisica, configurazione delle interruzioni — sono eseguibili **solo in ring 0**.

Ora, in una VM il guest OS *crede* di girare in ring 0, ma in realtà l'hypervisor lo ha 'declassato'. Così, a ogni istruzione privilegiata, la CPU genera una **trap** verso l'hypervisor, che la **intercetta, emula o traduce**, e poi restituisce il controllo. Questo meccanismo si chiama **trap-and-emulate** ed è esattamente la sorgente dell'overhead della virtualizzazione pesante: le system call del guest non vanno direttamente all'hardware, passano per uno strato di indirezione.

E qui sta il punto: **nei container questo meccanismo non esiste**. Il processo containerizzato esegue le proprie system call **direttamente sul kernel host**, che le esegue normalmente, limitandosi ad applicare le restrizioni di namespace e cgroups. È la 'nessun overhead dovuto al livello di hypervisor' che si legge nelle slide."

## La soluzione container: kernel condiviso e "processo esteso"

"Un container **non è una macchina virtuale** nel senso tradizionale. Tre cose lo definiscono: **non c'è emulazione** di dispositivi fisici; **condivide direttamente il kernel host**; usa due astrazioni native del kernel Linux — i **namespaces** per l'isolamento e i **cgroups** per la gestione delle risorse.

Il concetto da interiorizzare e da dire chiaramente all'orale è questo: *dal punto di vista del kernel, un container è un normale processo Linux* — o un gruppo di processi — *a cui però il kernel 'mente' su ciò che lo circonda*. Il processo crede di avere il proprio filesystem, la propria rete, il proprio elenco di processi; in realtà sta solo vedendo una **vista ristretta** delle risorse dell'host. Per questo lo possiamo definire un **processo esteso**: un processo normale, arricchito di una vista privata delle risorse — i namespace — e di limiti sul consumo — i cgroups. E la 'virtualizzazione leggera' si definisce esattamente così: una virtualizzazione che **riusa le astrazioni già offerte dal kernel** invece di costruirne di nuove via software.

Da questo discende una conseguenza fondamentale: **tutti i container su un host condividono lo stesso kernel**. Quindi non posso eseguire un container Windows su un kernel Linux — mentre con una VM sì, perché la VM si porta dietro il proprio OS. È il motivo per cui Docker Desktop su Mac e Windows, sotto il cofano, nasconde una **piccola VM Linux**.

I numeri rendono l'idea: un container si avvia in **circa 2 secondi**, contro i circa 2 minuti di una VM e i 5-10 minuti del bare metal; e sullo stesso server fisico ci stanno **100-1000 container** contro 10-100 VM."

## Primo pilastro: i namespaces (isolamento della visibilità)

"Il primo pilastro è dato dai **Linux Namespaces**. Un namespace è un **dominio di denominazione** per un certo tipo di risorsa: i processi nello stesso namespace condividono la stessa vista di quella risorsa, processi in namespace diversi ne hanno viste **completamente isolate**. I tipi principali sono sei o sette: **mnt** (mount, il filesystem), **pid** (lo spazio dei PID), **net** (lo stack di rete), **ipc** (la IPC System V), **uts** (hostname), **user** (UID/GID), e **cgroup**.

Un punto fine ma importante: i namespace **si ereditano, non si 'hanno'**. Un normale processo lanciato da terminale non ha un namespace 'suo': con una `fork()` ordinaria il figlio **eredita** i namespace del padre, e risalendo fino a init, PID 1, tutti i processi normali vivono negli stessi **namespace 'root'**, che esistono dall'avvio e contengono tutte le risorse globali. Un namespace **nuovo** nasce **solo** passando i flag `CLONE_NEWxxx` alla system call `clone()` o a `unshare()` — ed è esattamente ciò che fa Docker all'avvio di un container. La formula da ricordare: *i namespace non sono una proprietà intrinseca del processo, ma un contesto che si eredita*.

Le tre system call da citare sono: **`clone()`**, che crea un nuovo processo *e* un nuovo namespace; **`unshare()`**, che non crea un processo ma stacca il processo corrente in un nuovo namespace; **`setns()`**, che fa fare a un processo il *join* di un namespace già esistente. Vale la pena aggiungere che `docker exec` — quando entro in un container in esecuzione con una shell — sotto sotto è un **`nsenter`** che usa `setns()` per entrare nei namespace di quel container.

Due esempi rendono tutto concreto. Il **PID namespace**: dentro il container il processo principale si vede come **PID 1**, ma il kernel host lo conosce con un PID reale diverso. L'isolamento è **unidirezionale**: l'host vede tutti i processi dei container, un container non vede quelli dell'host. E c'è un risvolto pratico: in Unix il PID 1 è *init*, ha responsabilità speciali — raccoglie gli zombie e gestisce i segnali in modo particolare — per cui se l'applicazione diventa PID 1 e non gestisce `SIGTERM`, un `docker stop` aspetta il timeout e poi manda `SIGKILL`; da qui l'opzione `docker run --init` che inserisce un piccolo init (`tini`).

Il **network namespace**: ogni container ottiene una **propria istanza dello stack TCP/IP** — non si duplica il codice dello stack, che è uno solo nel kernel, ma si replicano per namespace tutte le strutture dati: interfacce, tabelle di routing, ARP, regole iptables e soprattutto lo **spazio delle porte**. Conseguenza che fa sempre effetto all'orale: **due container possono entrambi fare bind sulla porta 5001 senza conflitto**, perché ciascuno la apre nel proprio stack; il conflitto nasce solo quando voglio pubblicarle entrambe sulla **stessa porta dell'host**, che vive nel root namespace ed è unica. La comunicazione tra namespace passa per **coppie veth** — come un cavo virtuale — collegate a un **Linux bridge**, che in Docker di default si chiama `docker0`, e l'uscita verso l'esterno passa per **NAT**."

## Secondo pilastro: i cgroups (gestione delle risorse)

"Il secondo pilastro sono i **cgroups**, *Control Groups*: un sottosistema del kernel — nato in Google nel 2006-2007 — che fornisce un framework per **limitare, contabilizzare e monitorare le risorse** assegnate a **gruppi** di processi.

La distinzione con i namespace è la frase chiave da dire: i **namespace** isolano la **visibilità** delle risorse, e lo fanno **per singolo processo**; i **cgroups** limitano il **consumo** delle risorse, e lo fanno **per gruppo** di processi. Sono complementari, ed entrambi necessari per realizzare un container.

Docker crea un cgroup dedicato per ogni container e vi associa il processo principale, così posso limitare la RAM con `--memory 512m`, la CPU con `--cpus 0.5`, la banda di I/O su disco, e monitorare il consumo reale. I moduli da conoscerne almeno tre o quattro: `memory` per la memoria, `cpu` e `cpuset` per la CPU e l'assegnazione di core specifici, `blkio` per l'I/O su disco, `net_prio` per la priorità di rete, `devices` per consentire o negare l'accesso ai dispositivi, `freezer` per sospendere e riprendere i task. I cgroup si presentano come un **filesystem virtuale** sotto `/sys/fs/cgroup`: creare un gruppo significa creare una directory, imporre un limite significa scrivere in un file.

Un dettaglio che fa la differenza all'orale: i cgroups limitano **anche risorse che non sono hardware**. L'esempio canonico è il controller **`pids`**, che impedisce a un gruppo di creare nuovi processi oltre un limite. Il razionale è che il PID e la struttura dati associata nel kernel sono una risorsa finita, banale da esaurire; l'applicazione pratica è la difesa contro la **fork bomb** — un processo che si duplica all'infinito: senza un limite sui PID, un container compromesso potrebbe saturare la tabella dei processi e bloccare l'intero host *pur restando dentro i limiti di CPU e RAM*. Docker lo espone con `--pids-limit`. Morale: i cgroups non rispondono solo a 'quanta CPU o RAM consumi', ma più in generale a 'quanti oggetti del kernel un gruppo di processi può allocare'. E se un container sfora la memoria, interviene l'**OOM killer** — è il motivo per cui un container 'muore' quando supera la RAM assegnata."

## Docker: cos'è e l'immagine a layer

"Arrivati ai due pilastri, **Docker** è il motore che li mette insieme rendendoli usabili. È scritto in Go, nasce nel 2010 come dotCloud e diventa Docker nel 2013. Una precisazione storica che conviene fare: **Docker non ha inventato i container** — esistevano già `chroot`, le jail di FreeBSD, le Zone di Solaris, e soprattutto **LXC** su Linux. L'innovazione di Docker è stata l'**esperienza d'uso**: il formato di immagine a layer, il Dockerfile, il registry pubblico — ha reso i container *facili*.

Il concetto centrale è l'**immagine**. Un'immagine Docker **non è** un disco virtuale né un filesystem tradizionale: è uno **Union File System**, in pratica **OverlayFS**, organizzato a **layer**. Ogni layer è **read-only**, identificato da un hash SHA256; al momento del `run` si aggiunge in cima un sottile layer **read-write**, il *thin R/W layer*, specifico per quell'istanza di container. Il vantaggio enorme è che più container basati sulla stessa immagine **condividono gli stessi layer read-only**, e hanno solo il proprio thin layer separato.

Conviene spiegare come funziona l'overlay, perché è elegante. Tre tipi di layer: i **lowerdir**, i layer inferiori read-only, che nel caso Docker sono i layer dell'immagine; l'**upperdir**, l'unico layer superiore read-write, cioè il thin layer del container; e il **merged**, la vista fusa risultante, ciò che il processo vede come proprio filesystem — il *rootfs*. Le tre regole, con l'analogia dei lucidi trasparenti sovrapposti guardati dall'alto: in **lettura** si cerca dall'alto verso il basso e vince il primo trovato, quindi l'upperdir 'copre' i lowerdir; in **scrittura** su un file che sta in un layer read-only interviene il **copy-on-write**, cioè il file viene prima copiato nell'upperdir e poi modificato, lasciando intatto l'originale — ed è per questo che più container possono condividere lo stesso layer immagine senza interferenze; in **cancellazione** di un file di un lowerdir, non potendolo rimuovere davvero, si crea un **whiteout file** nell'upperdir, un marcatore che lo maschera. Da queste regole discende tutto: condivisione efficiente, immagini immutabili, container effimero — distruggerlo butta solo l'upperdir — e avvio quasi istantaneo, perché basta montare un overlay sui lowerdir esistenti più un upperdir vuoto."

## Il Dockerfile e Docker under the hood

"Il **Dockerfile** è la ricetta che costruisce l'immagine, layer per layer. Le direttive principali: **`FROM`** parte da un'immagine base, **`WORKDIR`** imposta la directory di lavoro, **`COPY`** copia file dall'host, **`RUN`** esegue comandi a build-time creando un nuovo layer, **`ENTRYPOINT`** specifica l'eseguibile fisso lanciato all'avvio, **`CMD`** gli argomenti di default, **`EXPOSE`** documenta le porte in ascolto.

Due punti che chiedono spesso. Primo, **ENTRYPOINT vs CMD**: il comando effettivo è la **concatenazione** dei due — `ENTRYPOINT ["python3"]` più `CMD ["app.py"]` significa 'esegui sempre python3, con app.py come script di default'. Se passo un argomento a `docker run immagine altro.py`, questo **sostituisce CMD** ma non l'ENTRYPOINT — per cambiare l'ENTRYPOINT serve il flag esplicito `--entrypoint`. E attenzione: **`EXPOSE` è solo documentazione**, non apre nessuna porta verso l'host; la pubblicazione vera avviene con `-p host:container` al run. Secondo punto, la **cache dei layer**: ogni istruzione che modifica il filesystem crea un layer, e Docker riusa i layer in cache se istruzione e file non sono cambiati. Per questo, nell'esempio Flask, si copia *prima* `requirements.txt` e si fa `pip install`, e *solo dopo* si copia il codice: se modifico solo il codice, la cache delle dipendenze resta valida e il rebuild è quasi istantaneo. L'ordine delle istruzioni non è estetico, è ottimizzazione.

Mettendo insieme i pezzi — 'Docker under the hood' — ecco come nasce un container: il container ottiene il proprio **rootfs** montando in overlay i layer dell'immagine, e il kernel passa al nuovo root con **`pivot_root`** — il filesystem dell'host risulta così isolato, grazie al **mount namespace**; viene aggiunto il layer **copy-on-write**; gli pseudo-filesystem `/proc`, `/sys`, `/dev` vengono montati privatamente — `/proc` richiede un nuovo **PID namespace**; i file di configurazione come `hostname` e `resolv.conf`, che non possono stare in un'immagine generica, vengono **bind-mountati**; e i **volumi**, che sono cartelle regolari dell'host bind-mountate nel container, permettono ai dati di **sopravvivere** al singolo container ed essere condivisi. Quest'ultimo punto si lega alla filosofia operativa: i container sono **effimeri e usa-e-getta** — *cattle, not pets*, bestiame non animali domestici: se un container ha problemi non lo si cura, lo si distrugge e se ne crea uno nuovo; lo stato persistente va fuori, in volumi o database."

## Orchestrazione: da Compose a Swarm

"Finora ho parlato di un container per volta. Ma un'applicazione reale è **multi-container** — pensiamo a Flask più MongoDB. Qui entra **Docker Compose**: uno strumento che descrive l'intero stack in un file YAML, il `compose.yaml`, con una sezione `services` dove per ogni servizio dico se fare il build da Dockerfile o usare un'immagine dal registry, quali porte pubblicare nel formato `host:container`, quali volumi montare, quali variabili d'ambiente, e i collegamenti di rete. Con un solo comando, `docker compose up`, costruisco e avvio tutto; con `docker compose down` distruggo tutto. Risolve il problema di dover buildare, avviare e collegare manualmente ogni container.

Quando però voglio **scalare su più macchine** e avere **alta disponibilità**, serve un **orchestratore**. Il primo è **Docker Swarm**, integrato nel Docker Engine. In uno swarm i nodi hanno due ruoli: i **manager**, che gestiscono il join dei nodi, mantengono lo stato globale del cluster e orchestrano i deploy — e tra loro eleggono un **leader**; e i **worker**, che ricevono ed eseguono i **task** assegnati. Un nodo può essere insieme manager e worker.

Il concetto cardine è lo **stato desiderato**: per un servizio dichiaro quante repliche voglio, quali porte, quali vincoli; e Swarm lavora costantemente per **reconciliation**, cioè confronta di continuo lo stato reale con quello dichiarato e agisce per riallinearli. L'unità atomica di scheduling è il **task**, che implementa un container; una volta assegnato a un nodo, un task **non migra** — se il nodo cade, non viene spostato, ne viene **creato uno nuovo** altrove finché non si torna al numero di repliche richiesto.

Sulla **tolleranza ai guasti** c'è una distinzione che è proprio una trappola d'esame: ci sono **due tipi di guasto gestiti in modo diverso**. Il guasto dei **manager** è gestito dal **quorum** dell'algoritmo di consenso **Raft**: una scrittura sullo stato è accettata solo se è d'accordo la **maggioranza** dei manager, cioè (N/2)+1, e si tollerano (N-1)/2 fallimenti — per questo i manager si tengono in numero **dispari**, 3, 5, 7, e la maggioranza serve a evitare lo **split-brain**. Se si perde il quorum, il cluster non può più orchestrare, ma i container già in esecuzione **continuano a girare**: si ferma il 'cervello', non il piano dati. Il guasto dei **worker**, invece, è gestito dal **reschedule**: i worker non votano nulla, e quando uno cade i manager rilevano che mancano repliche e **ripianificano** i task sui nodi superstiti. In una frase: il quorum protegge la sopravvivenza del **controllo** del cluster, il reschedule protegge la sopravvivenza dei **servizi**.

Vale la pena chiudere col **load balancing**: con `docker service create --replicas 3 --publish 5001:5001` le richieste vengono bilanciate tra le repliche grazie all'**ingress routing mesh** — la porta pubblicata è aperta su *tutti* i nodi dello swarm, e qualunque nodo riceva la richiesta la inoltra, via IPVS, a una replica qualsiasi anche su un altro nodo. E gli aggiornamenti sono **rolling update**: si aggiornano le repliche un po' alla volta, così il servizio resta disponibile, con **rollback** automatico in caso di problemi."

## Kubernetes (a livello introduttivo)

"Sopra Swarm c'è **Kubernetes**, K8s, lo standard de facto in produzione: open source, scritto in Go, basato sul sistema interno di Google chiamato **Borg**. Promuove l'architettura a **microservizi** — l'applicazione scomposta in servizi piccoli e indipendenti — per scalabilità e affidabilità superiori. L'architettura ha un **Control Plane**, che mantiene lo stato del cluster — con **etcd** come store distribuito chiave-valore, il **kube-apiserver** come punto di comunicazione centrale, il **controller-manager** che mantiene lo stato desiderato e lo **scheduler** che decide su quale nodo mettere i nuovi Pod — e i **Node**, ognuno con il **kubelet** come agente, un **container runtime** e i **Pod**, che sono l'unità minima di deploy: uno o più container che condividono rete e storage.

Un punto elegante da citare è la **Container Runtime Interface, la CRI**: Kubernetes non dipende da un singolo runtime, ma parla con qualsiasi runtime compatibile attraverso un'interfaccia **gRPC** standardizzata — sotto la CRI ci sono containerd, CRI-O, e sotto ancora lo standard **OCI**, Open Container Initiative, con runtime come **runc**, e quelli 'ibridi' **gVisor** e **Kata** che reintroducono un po' di isolamento. C'è una bella simmetria col corso: **Docker usa gRPC internamente**, tra daemon e containerd, e **Kubernetes usa gRPC via la CRI** — stesso protocollo, nato anch'esso in Google. Per il corso basta conoscere Kubernetes a questo livello alto: il focus pratico resta Docker e Docker Swarm."

## Il trade-off finale: prestazioni contro isolamento

"Conviene chiudere con la riflessione che lega tutto, perché è quasi sempre la domanda 'cattiva' che fa capire se hai capito davvero. I container guadagnano prestazioni proprio **togliendo** lo strato di indirezione — l'hypervisor — che però dava l'isolamento. Quindi i container **non sono isolati come le VM**: il kernel host condiviso è un **single point of failure** e un'unica superficie d'attacco — un bug o una vulnerabilità del kernel compromette potenzialmente *tutti* i container, e un crash del kernel li abbatte insieme. Le VM non sono perfette neanche loro — esistono attacchi di *VM escape* — ma l'hypervisor è progettato apposta per l'isolamento, con una superficie d'attacco molto più piccola di un kernel general-purpose.

Questo è il **trade-off fondamentale: prestazioni contro isolamento**. La virtualizzazione leggera vince in velocità e densità proprio perché rinuncia all'indirezione che proteggeva. Ed è anche il motivo per cui esistono runtime ibridi come **gVisor** — un kernel in user-space — e **Kata** — una micro-VM leggera: cercano di reintrodurre un po' di indirezione per recuperare isolamento senza perdere troppo in leggerezza. Saper articolare questo trade-off è la chiave di tutta la parte sui container."

## Chiusura (la frase con cui finire)

"Quindi, riassumendo il filo: si parte dalla VM, che virtualizza tutto l'hardware e paga in overhead — per via del trap-and-emulate sulle istruzioni privilegiate; si arriva al container come **processo esteso** che condivide il kernel host e riusa due astrazioni native — i **namespaces** per isolare la *visibilità* delle risorse, i **cgroups** per limitarne il *consumo*; **Docker** rende tutto questo usabile con le immagini a layer e il Dockerfile; **Compose** orchestra lo stack multi-container, **Swarm** e **Kubernetes** lo scalano su cluster mantenendo lo stato desiderato. E sotto a tutto resta un'unica tensione di fondo: la leggerezza dei container è il rovescio del loro isolamento più debole."

## Oltre la fonte — cosa rispondere se chiedono di più

Se l'esaminatore spinge oltre quanto trattato a lezione, questi sono i ganci da citare come **conoscenza esterna**, senza spacciarli per contenuto delle slide:

- **cgroups v1 vs v2**: v1 ha gerarchie separate per controller (quella descritta dalle slide), v2 ha una gerarchia unificata, default nelle distro moderne.
- **Sicurezza container oltre namespace/cgroups**: **seccomp** (filtra le system call ammesse), **SELinux/AppArmor** (Mandatory Access Control), **capabilities** Linux (frammentano i privilegi di root). Compaiono nel diagramma OCI di [[kubernetes]] ma non sono approfonditi.
- **OCI image spec vs runtime spec**: lo standard che disaccoppia 'com'è fatta un'immagine' da 'come si avvia un container', e che permette di sostituire il runtime senza toccare Kubernetes.
- **Differenza containerd vs runc**: containerd è il *container manager* di alto livello (ciclo di vita), runc è il *container runtime* di basso livello (esegue materialmente la creazione parlando col kernel, poi termina); tra loro lo *shim* disaccoppia il container dal daemon, così si può riavviare il daemon senza uccidere i container.
- Se chiedono di **stato persistente e database in cluster**: ribadire *cattle not pets*, lo stato fuori dal container (volumi, DB), e che replicare un servizio **stateful** come un broker ActiveMQ o un DB non è banale come replicare uno stateless — serve storage condiviso/cluster (→ [[mom]], [[mongodb]]).

---

## Promemoria — le domande container più probabili (da [[risposte-domande]] §5)

- Differenza container vs VM → no emulazione HW, no guest OS, kernel host + namespaces + cgroups.
- Perché i container sono più veloci → processo esteso, niente trap-and-emulate, boot ≈ fork.
- Cos'è un namespace di rete / mnt → isola stack TCP/IP per container / albero dei mount.
- Differenza namespace vs cgroups → visibilità per-processo vs consumo per-gruppo.
- Cgroups limitano anche risorse non-hardware → `pids` contro la fork bomb.
- File system a layer / dove si scrivono le modifiche → OverlayFS, thin R/W layer (upperdir), copy-on-write/whiteout.
- ENTRYPOINT vs CMD, EXPOSE solo documentazione, cache dei layer.
- Replicare un servizio / ruoli dei nodi / stato desiderato → Swarm, manager/worker, quorum Raft vs reschedule.
- Svantaggi della virtualizzazione lato system call → trap-and-emulate (assente nei container).
- Trade-off prestazioni ↔ isolamento → kernel condiviso = single point of failure; gVisor/Kata.

_Generato: 2026-06-26 — fonte: wiki/concetti/{virtualizzazione-container,linux-namespaces,cgroups}.md, wiki/entità/{docker,docker-compose,docker-swarm,kubernetes}.md (PDF 03-service-deployment-containers + appunti)._
