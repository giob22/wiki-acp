# Discorso orale — NoSQL e MongoDB

> Export discorsivo da [[nosql]] e [[mongodb]] per l'esposizione orale. Testo da
> leggere/parlare, non schematico. Ordine logico: cos'è un database/DBMS e il suo
> ruolo nel web → relazionali vs non-relazionali (schema, ACID, scalabilità) →
> tipologie NoSQL → MongoDB (gerarchia, documenti, PyMongo) → focus scalabilità
> orizzontale → atomicità sotto concorrenza → (in coda) cosa rispondere se chiedono
> oltre la fonte.
> _Generato: 2026-06-22 — fonte: wiki/concetti/nosql.md, wiki/entità/mongodb.md (PDF 17-NoSQL)_

---

## Apertura (la frase con cui cominciare)

"Nelle web application i dati vivono nel **back-end**, ed è lì che entrano in gioco i database. Un **database** è una collezione di dati organizzati in modo da poter essere acceduti, gestiti e aggiornati facilmente; un **DBMS**, *Database Management System*, è il software che permette di creare, definire e manipolare quel database. Oltre a memorizzare e processare i dati, un DBMS si occupa di **protezione, sicurezza** e soprattutto di mantenere la **consistenza** dei dati quando ci sono utenti multipli che accedono in concorrenza. I database si dividono in due grandi famiglie: **relazionali**, che usano SQL, e **non-relazionali**, i NoSQL. La scelta tra le due dipende dalla natura del dato e dalla funzionalità che serve, e si possono anche usare in combinazione."

## Perché un database nel back-end (il contesto web)

"Conviene dire subito *perché* un database serve in una web app. Primo: dà **persistenza** — i dati sopravvivono al riavvio o al crash del server, non vivono solo nella memoria del processo. Secondo: **riduce il carico sulla memoria centrale**, perché i dati stanno su disco gestiti dal DBMS invece che tutti in RAM. Terzo: serve le richieste dei client che leggono o scrivono dati. In pratica un client fa una richiesta al web server, il web server interroga il database e restituisce il risultato. Tra i DBMS relazionali classici ci sono MySQL, Oracle, SQL Server, PostgreSQL, DB2."

## Relazionali (SQL): schema, chiavi, ACID

"I database **relazionali** si basano su uno **schema**: uno schema è un template che definisce in anticipo la struttura dei dati, e ogni nuova riga deve conformarsi ad esso. Questo rende i dati **prevedibili e facilmente valutabili**. I dati stanno in **tabelle** — chiamate anche **entità** — collegate tra loro da **chiavi**, le *keys*: le chiavi danno accesso rapido a una riga o colonna e mettono in relazione le tabelle. Pensiamo a un `User` collegato ai suoi `Order`, ciascun ordine collegato alle sue righe e ai `Product`: una modifica si propaga in modo predicibile e sistematico.

Il punto qualificante dei relazionali è la **ACID-compliance**, che per un RDBMS è un *must*: **Atomicity, Consistency, Isolation, Durability**. Queste quattro proprietà garantiscono che le transazioni siano affidabili, lasciando pochissimo spazio agli errori."

## Lo svantaggio dei relazionali (che prepara il NoSQL)

"Il rovescio della medaglia è duplice. Da un lato, lo **schema rigido** e i vincoli forti rendono *quasi impossibile* l'uso dei relazionali negli scenari **big data**. Dall'altro, c'è il problema della **scalabilità**: per reggere più carico vorrei distribuire il database su server multipli, ma — testualmente dalla fonte — *gestire le tabelle su differenti server è difficoltoso*. La via pratica diventa allora comprare server più potenti e costosi, cioè scalare **verticalmente**, anziché aggiungere macchine. C'è anche un terzo punto: i vincoli di schema **ostacolano la migrazione** dei dati tra RDBMS diversi, che dovrebbero essere identici per funzionare. Sono esattamente i limiti che i NoSQL nascono per superare."

## Non-relazionali (NoSQL): schema-free, collection e documenti

"I database **non-relazionali** sono più **indulgenti** nella struttura. Invece di tabelle con righe e colonne usano **collections** di categorie diverse — per esempio utenti e ordini — e ogni collection è fatta di **documents**, cioè dati *semi-strutturati*. La caratteristica chiave è che sono **schema-free**: in una stessa collection possono esserci documenti che non seguono lo stesso pattern, i campi si creano *on-the-fly*, e collection diverse non devono necessariamente avere relazioni tra loro.

I **pro**: la natura schema-free rende facile gestire e memorizzare grandi volumi di dati, e i dati possono essere distribuiti tra nodi diversi — quindi scalano bene orizzontalmente. I **contro**, che sono il prezzo della flessibilità: non posso dare per scontata la presenza di un campo, perché un documento potrebbe non averlo; e non avendo relazioni gestite dal DB, **aggiornare i dati è più complesso**, perché ogni dettaglio va aggiornato separatamente."

## Le tipologie di NoSQL (con esempi)

"I NoSQL non sono un'unica cosa, ma una famiglia. Le tipologie principali sono:
- **Key-Value**: memorizzano coppie chiave→valore, semplicissime; esempi Redis e Amazon DynamoDB. Buone per cache e sessioni.
- **Document Store**: gestiscono un dizionario ampio di tipi e valori, anche **innestati**, e memorizzano i dati come **documenti JSON**; gli esempi famosi sono Couchbase e **MongoDB**.
- **Search Engine**: si distinguono dai document store perché permettono di accedere ai dati tramite semplici **ricerche testuali** full-text; esempi Solr, Splunk, Elasticsearch.
A questi si aggiungono i **graph database** come Neo4j per dati a forte relazione, e gli store a colonne come Cassandra. Per il corso il riferimento è il document store, e in particolare MongoDB."

## MongoDB: cos'è e la gerarchia dei dati

"**MongoDB** è un DBMS **document-oriented** open-source. Memorizza i dati come **documenti JSON-like** — internamente in formato binario **BSON** — raggruppati in collection, ed è schema-free, quindi ogni documento può avere campi diversi.

La gerarchia, dall'alto in basso, è: l'**istanza** MongoDB contiene uno o più **Database**; ogni database contiene delle **Collection**; ogni collection contiene dei **Document**; e ogni documento è fatto di **Field**, cioè coppie nome-valore. Il parallelo col mondo relazionale è utile: la **collection** corrisponde grosso modo a una **tabella**, ma senza schema fisso; il **document** corrisponde a una **riga**, ma è un oggetto JSON che può essere annidato.

Due concetti da nominare: ogni documento ha una primary key nel campo **`_id`**, che MongoDB **autogenera** come ObjectId se non lo fornisco io; e l'**embedded document**, cioè un campo il cui valore è a sua volta un documento — è il modo NoSQL di rappresentare una relazione, al posto del JOIN relazionale, annidando i dati dentro lo stesso documento."

## Come si usa da Python: PyMongo

"Il driver ufficiale per usare MongoDB da Python è **PyMongo**, si installa con `pip install pymongo`. La cosa elegante è che i documenti sono rappresentati direttamente come **dict** Python, perché sono dati in stile JSON. Il flusso tipico: creo un `MongoClient` indicando host e porta — di default `localhost:27017` —, accedo al database con la sintassi a indice `client['mio_db']`, e poi alla collection con `db['utenti']`; sia database che collection vengono creati *on-the-fly* al primo uso. Da lì uso `insert_one`/`insert_many` per scrivere, `find_one` che torna un dict o `None` e `find` che torna un **cursor** iterabile per leggere, e `update_one`/`delete_one` per modificare. Nei filtri uso operatori col prefisso dollaro, per esempio `{'età': {'$gt': 25}}`, e negli update i modificatori come `$set` o `$inc`."

## Il focus richiesto: scalabilità orizzontale

"Vorrei soffermarmi sulla **scalabilità**, perché è uno dei punti su cui le due famiglie divergono di più, e la fonte lo tratta da entrambi i lati.

Dal lato relazionale è uno **svantaggio**: per scalare un RDBMS dovrei distribuirlo su più server, ma — cito — *gestire le tabelle su differenti server è difficoltoso*. Il motivo di fondo è che le tabelle sono legate da chiavi e relazioni, e una query che fa JOIN tra tabelle che stanno su macchine diverse è complicata e lenta. Così, in pratica, i relazionali si scalano **verticalmente**: si compra una macchina più potente, che è costosa e ha comunque un limite.

Dal lato NoSQL è un **pro**: essendo schema-free e senza relazioni obbligatorie tra collection, i dati — cito ancora — *possono essere distribuiti tra differenti nodi per migliorarne l'accessibilità*. Questa è la **scalabilità orizzontale**: invece di una macchina più grossa, aggiungo più macchine. È facile proprio perché i documenti sono **indipendenti**: non dovendo garantire JOIN tra nodi, ogni nodo può servire la sua porzione di dati in modo autonomo.

Il collegamento concettuale che chiuderei così: la **rinuncia alle relazioni** gestite dal database — che è lo svantaggio NoSQL dell'aggiornamento più complesso — è esattamente ciò che **abilita** la distribuzione su nodi. Flessibilità di schema e distribuibilità sono due facce della stessa scelta di design."

## Il trade-off di scelta: RDBMS vs DBMS non relazionale (sintesi)

"In sintesi, la scelta tra un **RDBMS** e un **DBMS non relazionale** è un trade-off tra **consistenza e struttura** da un lato e **flessibilità e scalabilità** dall'altro. Scelgo un **relazionale** quando i dati sono **strutturati e fortemente relazionati**, lo schema è stabile, e mi servono **garanzie ACID** e transazioni affidabili — il prezzo è uno schema rigido e una scalabilità solo **verticale**, costosa. Scelgo un **NoSQL** quando ho **grandi volumi**, dati **eterogenei o semi-strutturati** e schema che evolve, e mi serve **scalabilità orizzontale** facile su più nodi — il prezzo è la rinuncia a parte delle garanzie ACID e a relazioni gestite dal DB, con aggiornamenti più complessi. In una frase: *i relazionali ottimizzano consistenza e integrità, i NoSQL ottimizzano scala e flessibilità* — e infatti spesso si usano **insieme**, ciascuno per la porzione di dati a cui si adatta meglio."

## Un buon punto tecnico: atomicità sotto concorrenza

"Se voglio mostrare profondità su MongoDB, il tema migliore è la **concorrenza**. Se faccio una `find_one` e poi una `update_one` separate, apro una **race condition** — il classico TOCTOU, *time-of-check-to-time-of-use*: tra la lettura e la scrittura un altro client può modificare il documento, e la mia scrittura sovrascrive perdendo quel cambiamento. È lo stesso problema delle race condition tra thread. La soluzione di MongoDB è la famiglia `find_one_and_update` / `find_one_and_replace` / `find_one_and_delete`, che esegue lettura e scrittura come **un'unica operazione atomica lato server**, con lock a livello di documento. Il principio è lo stesso di un `Lock` nel threading, ma invece di sincronizzare nel client **demando l'atomicità al DBMS**, che la implementa nello storage engine. Il pattern classico è il contatore atomico con `$inc` e `upsert`."

## In coda — se chiedono oltre la fonte (CAP, BASE, sharding, replica)

> ⚠️ Questa sezione è **conoscenza esterna**: il PDF del corso si ferma alla
> "distribuzione dei dati su differenti nodi" e **non** nomina sharding, replica,
> eventual consistency, CAP o BASE. Se il professore le chiede, dichiararle come
> nozioni standard, non come contenuto della slide.

"Se mi chiedono *come* avviene concretamente la distribuzione su nodi, i termini standard sono due. Lo **sharding** è il partizionamento orizzontale: i documenti di una collection vengono suddivisi tra più nodi (gli *shard*) in base a una chiave, così ogni nodo ne tiene solo una porzione — è ciò che dà la scalabilità in scrittura e in volume. La **replica** (in MongoDB i *replica set*) è invece la copia ridondante degli stessi dati su più nodi, per **disponibilità** e tolleranza ai guasti: se un nodo cade, una replica continua a servire i dati.

Da qui nasce il tema della **consistenza distribuita**. Il **teorema CAP** dice che in un sistema distribuito, in presenza di partizioni di rete, non si possono garantire insieme consistenza forte e disponibilità: bisogna scegliere. Molti NoSQL privilegiano la disponibilità e accettano la **eventual consistency**, cioè le repliche convergono allo stesso valore *col tempo*, non istantaneamente. È il senso dell'acronimo **BASE** — *Basically Available, Soft state, Eventual consistency* — contrapposto ad **ACID**: i relazionali garantiscono consistenza forte e transazioni, i NoSQL rilassano queste garanzie in cambio di scalabilità e disponibilità. Questo è anche il motivo per cui, nella tabella di confronto, alla riga ACID dei NoSQL metto 'garanzie rilassate'."

## Promemoria — domande frequenti su questa parte

- Differenza tra database **relazionale e NoSQL** (schema, ACID, scalabilità).
- Cosa sono le proprietà **ACID** e perché i relazionali le garantiscono.
- Cos'è **MongoDB**: gerarchia Database → Collection → Document → Field.
- Cos'è il campo **`_id`** e come viene generato.
- **Tipologie** di NoSQL con un esempio ciascuna.
- Perché i NoSQL **scalano orizzontalmente** e i relazionali no.
- (Se approfondiscono) perché `find_one`+`update_one` separati sono sbagliati e come `find_one_and_update` risolve.
