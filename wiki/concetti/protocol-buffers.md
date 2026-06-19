---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc]
---

## Definizione

**Protocol Buffers (protobuf)** è il meccanismo open-source ormai maturo di Google per serializzare dati strutturati. Usa una **rappresentazione binaria** (non testuale come JSON/XML), è **fortemente tipizzato**, e in gRPC svolge un doppio ruolo: **IDL** per definire l'interfaccia del servizio (genera stub client e classi server astratte) e **formato di interscambio** dei messaggi (payload piccoli). È basato sul classico **modello Proxy-Skeleton** (stub e server).

## Spiegazione

### Dati strutturati come messaggi

In protobuf i tipi di dato sono strutturati come **messaggi**. Un **messaggio** è un piccolo record logico di informazioni contenente una serie di coppie **nome-valore** chiamate **campi**. Ogni campo ha un **numero univoco** (*field tag*), usato per identificarlo nel **formato binario** del messaggio — questo è ciò che rende il formato compatto e indipendente dai nomi.

**Struttura file `.proto`**:
```protobuf
syntax = "proto3";                    // versione del linguaggio

package nome.package;                 // namespace (ignorato in Python; non ignorato in Java)

// Definizione del servizio (per gRPC)
service NomeServizio {
    rpc NomeMetodo (TipoRequest) returns (TipoResponse);
}

// Definizione messaggio
message Student {
    string student_id = 1;  // field tag: identifica il campo nel binario
    string first_name = 2;
    string last_name = 3;
    string address = 4;
    bool   is_joined = 5;
}
```

**Elementi chiave**:
- **`syntax = "proto3"`**: versione del linguaggio protobuf
- **`package`**: evita conflitti di nome tra i tipi di messaggi di un protocollo; in Python **ignorato** (moduli organizzati per filesystem) ma comunque **fortemente raccomandato** — altrimenti si rischiano conflitti di denominazione nei descrittori e il `.proto` diventa non portabile verso altri linguaggi; in Java **non ignorato** — determina il package generato (sovrascrivibile con `option java_package`)
- **`message`**: tipo di dato strutturato; equivalente a una classe
- **Campo**: coppia `tipo nome = tag`
- **Field tag**: numero univoco che identifica il campo nel **formato binario** — non cambiarlo mai dopo il deploy
- **Tipi**: `string`, `int32`, `int64`, `float`, `bool`, `bytes`, messaggi annidati, `repeated` (array)

**Esempio gRPC completo (ProductInfo.proto)**:
```protobuf
syntax = "proto3";
package ecommerce;

service ProductInfo {
    rpc addProduct(Product) returns (ProductID);
    rpc getProduct(ProductID) returns (Product);
}

message Product {
    string id = 1;
    string name = 2;
    string description = 3;
}

message ProductID {
    string value = 1;
}
```

**Vantaggi su JSON/XML**:
- **Binario**: più compatto (3-10x meno spazio)
- **Più veloce** da serializzare/deserializzare
- **Schema enforcement**: i tipi sono verificati
- **Backward compatibility**: i field tag permettono evoluzione del schema

**Svantaggi**:
- Non leggibile dall'uomo (debug più difficile)
- Richiede compilazione del file `.proto`

> 🎯 Esame: Struttura di un file `.proto` (syntax, package, service, message, field tag), perché i tag sono importanti.

## Perché importa

protobuf è il formato di serializzazione di gRPC — capirlo è necessario per definire servizi e messaggi correttamente.

## Connessioni

- [[grpc]] — usa protobuf come IDL e formato di serializzazione
- [[rpc]] — il file `.proto` è l'IDL di gRPC; protobuf è un approccio di **external data representation** (come CDR, XDR, Java serialization, XML)
- [[rest]] — confronto: REST usa JSON (testuale) vs gRPC usa protobuf (binario)
- [[middleware]] — il marshalling con formato esterno concordato è una proprietà generale dei middleware

## Fonti

- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-19 — estensione MODULO 2 (slide 14): doppio ruolo (IDL + interscambio), modello Proxy-Skeleton, messaggi come record di campi nome-valore numerati, package raccomandato anche se ignorato in Python_
