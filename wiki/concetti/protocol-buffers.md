---
tipo: concetto
importanza_esame: alta
prerequisiti: [rpc]
---

## Definizione

**Protocol Buffers (protobuf)** è il meccanismo open-source di Google per serializzare dati strutturati. Usa una **rappresentazione binaria** (non testuale come JSON/XML), è fortemente tipizzato, e serve da IDL per gRPC.

## Spiegazione

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
- **`package`**: evita conflitti di nome; in Python **ignorato** (moduli organizzati per filesystem); in Java **non ignorato** — determina il package generato (sovrascrivibile con `option java_package`)
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
- [[rpc]] — il file `.proto` è l'IDL di gRPC
- [[rest]] — confronto: REST usa JSON (testuale) vs gRPC usa protobuf (binario)

## Fonti

- [[14-python-rpc-grpc]]

_Aggiornato: 2026-06-04 — ingest iniziale_
