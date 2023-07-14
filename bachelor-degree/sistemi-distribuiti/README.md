
﻿
# CPbank
##### Pagliaroli Chiara 866160 - Piacente Cristian 866020
# README
Questo documento contiene una descrizione riguardante il lavoro svolto, una sezione Frontend e una sezione Backend per spiegare nel dettaglio come abbiamo implementato i requisiti presenti nella traccia e in cui spieghiamo le funzionalità aggiuntive.

## 1. Descrizione

Per produrre l'elaborato, abbiamo utilizzato il linguaggio Go per gestire le richieste Backend (grazie al framework Chi) e per il Frontend gestiamo gli endpoint tramite jQuery e sfruttiamo Bootstrap 5.0 per l'interfaccia grafica. In particolare, per quanto riguarda Go, le dipendenze sono: 
- github.com/go-chi per gestire le richieste HTTP 
- github.com/lib/pq per connetterci al database PostgreSQL 
- github.com/google/uuid per validare UUID v4 

Inoltre usiamo un database PostgreSQL come memoria secondaria.

Come da traccia, nelle richieste Backend è possibile utilizzare sia x-www-form-urlencoded sia JSON. Tutte le risposte sono in formato JSON. 

#### Interpretazioni varie della traccia
Nel momento in cui si effettua uno storno su un'operazione tramite l'endpoint /api/divert, non si potrà più in futuro utlizzare la stessa operazione stornata per effettuare un nuovo storno, né si può stornare lo storno.

## 2. Frontend
Di seguito elencate le funzionalità e alcuni dettagli implementativi del frontend.
### Pagina Home (endpoint /)
La pagina Home è uno degli endpoint previsti dal progetto. Si può cercare un id e visualizzare la tabella delle sue transazioni. Se l'account è attivo ma non ne ha viene visualizzata una tabella vuota; se è inattivo viene mostrato apposito errore. Le richieste per aggiornare la tabella vengono fatte attraverso richieste AJAX.
Cliccando sui titoli delle colonne è possibile riordinare in ordine ascendente o discendente le varie colonne. Per fare ciò viene usato il codice presente al seguente link, https://github.com/tyleruebele/sort-table, opportunamente integrato con nuove classi di sorting per le date nel nostro formato e il formato per il denaro usato nelle tabelle.
Cliccare un id nella tabella diverso da quello su cui è stata fatta la richiesta comporta la richiesta ajax dei dati di quell'account e il conseguente aggiornamento della tabella.

### Pagina Transfer (endpoint /transfer)
La pagina transfer è il secondo degli endpoint richiesti. Qui è possibile fare operazioni tra account attivi con sufficiente bilancio. Tutti gli input sono controllati prima di essere inoltrati e risultato o eventuali errori sono mostrati come alert sotto al box per il trasferimento. 
Se si sono copiati degli id dalla pagina "Accounts" è possibile usare la funzione "Paste Ids" per riempire rapidamente gli id; viene richiesto il permesso al browser e controllato il contenuto della clipboard prima di fare il paste.

### Pagina Divert (endpoint /divert)
La pagina divert serve a stornare un'operazione dato l'id. L'esito o l'eventuale errore vengono mostrati sotto al box.

### Pagina Accounts (endpoint /accounts)
La pagina Accounts permette di navigare agilmente fra i vari accounts nella banca. 
In primis permette di cercare gli account per nome e cognome (tra gli attivi o inattivi, cliccando il pulsante sulla sinistra); se i campi sono lasciati vuoti vengono mostrati tutti gli account.
Cliccando sulle righe è possibile mettere i dati dell'utente nel primo box, per modificarne nome e cognome (a cui poi deve seguire pressione del pulsante "Save" per essere registrato); inoltre il pulsante "Activate" o "Deactivate" permette di attivare gli account inattivi e viceversa.
Nel box sottostante è possibile creare nuovi account fornendo un nome e un cognome.
Inoltre è possibile attivare la funzione "Copy Ids", che permette di copiare due id dalla tabella cliccandoli uno dopo l'altro (appaiono istruzioni a video). Questo permette di velocizzare l'inserimento dei dati nella pagina Transfer.
Sono noti bug minori che a causa della mancanza di tempo non sono stati gestiti (il pulsante in alto a sinistra "Active" o "Inactive" non si aggiorna a dovere se premuto durante un aggiornamento di tabella).

### Pagina Info (endpoint /info)
Pagina di info generali e background del progetto.

## 3. Backend
Di seguito alcuni esempi di risposta per gli endpoint richiesti da implementare e successivamente i nuovi endpoint introdotti.
Per quanto riguarda gli errori, viene impostato un opportuno codice di stato HTTP e nel JSON del body della risposta è presente un messaggio associato alla chiave content.
La chiave content viene utilizzata anche quando si deve mostrare solo un risultato di tipo primitivo, come in POST /api/account che deve restituire solo l'id dell'account creato. Quest'ultimo si distingue dagli errori per il fatto che il codice utilizzato è 200.

### 3.1 Esempi
### /api/account
#### GET

    {
		"f1ce67e29ea3914cac7a": {
			"balance": "$10.00",
			"name": "John",
			"surname": "Doe"
		},
		"88ee3cedc3168543716f": {
			"balance": "$0.00",
			"name": "Jane",
			"surname": "Doe"
		}
	}

#### POST
(nel body della richiesta name, surname)

    {
        "content": "88861bf6c650287e39f0"
    }


#### DELETE
(parametro URL id)

    {
        "content": "Success!"
    }
In realtà l'account non viene eliminato dal database ma viene settato un flag che permette di rendere l'account inattivo (è possibile renderlo di nuovo attivo con un endpoint aggiuntivo descritto alla fine)
    
### /api/account/{accountId}

#### GET
(oltre a settare un header di risposta X-Sistema-Bancario con nome;cognome)

    {
        "balance": "$0.00",
        "name": "Jane",
        "operations": [
            [
                "6e71f4da-98d1-4d3e-a924-8213f7c7cfd9",
                {
                    "amount": "$0.00",
                    "date": "2022-06-23T22:53:59.533012Z",
                    "idRecipient": null,
                    "idSender": "88ee3cedc3168543716f",
                    "recipientIsActive": null,
                    "senderIsActive": true,
                    "type": 1
                }
            ]
        ],
        "surname": "Doe"
    }
    
Come scritto anche nel file ISTRUZIONI, per quanto riguarda il tipo di un'operazione abbiamo utilizzato 0 = trasferimento di denaro, 1 = deposito, 2 = prelievo, 3 = storno, 4 = operazione stornata (un'operazione non può essere stornata più volte).

#### POST
(nel body della richiesta amount)

    {
	    "balance": "$0.00",
	    "id": "6e71f4da-98d1-4d3e-a924-8213f7c7cfd9"
	}

#### PUT
(nel body della richiesta name, surname)

    {
        "content": "Success!"
    }

#### PATCH
(nel body della richiesta name oppure surname)

    {
        "content": "Success!"
    }

#### HEAD
Come GET ma senza body di risposta.


### /api/transfer
#### POST
(nel body della richiesta from, to, amount)

    {
        "balanceRecipient": "$0.00",
        "balanceSender": "$0.00",
        "id": "f6f373c0-4187-4ae7-9c1c-bdae987c5ec2"
    }

### /api/divert
#### POST
(nel body della richiesta id)

    {
        "balanceRecipient": "$0.00",
        "balanceSender": "$0.00",
        "id": "b4d266f3-b733-43a8-8020-e23faedacedd"
    }

### 3.2 Endpoint aggiuntivi
Per quanto riguarda la parte backend, abbiamo aggiunto gli endpoint /api/inactive e /api/inactive/{accountId} per gestire gli account "eliminati" (ossia resi inattivi).
Di seguito una breve descrizione (con esempi di risposta) per gli endpoint backend extra implementati:

### /api/inactive 
**GET**: restituisce la lista di tutti gli account inattivi ("eliminati" con DELETE /api/account) nel sistema.

    {
        "88861bf6c650287e39f0": {
            "balance": "$0.00",
            "name": "Mario",
            "surname": "Rossi"
        }
    }

**DELETE**: rimuove l'account specificato dal parametro URL id dagli account inattivi, rendendolo di nuovo attivo.

    {
        "content": "Success!"
    }

### /api/inactive/{accountId}
**GET**: come /api/account/{accountId} però per un account inattivo, restituisce nome, cognome nonché il saldo con un elenco di tutte le transazioni che coinvolgono l'account identificato da accountId, in ordine cronologico ascendente. Inoltre, introduce un header di risposta con chiave X-Sistema-Bancario. Il valore dell'header è nome;cognome. 

    {
        "balance": "$0.00",
        "name": "Mario",
        "operations": null,
        "surname": "Rossi"
    }

**HEAD**: analogamente, restituisce nome e cognome del proprietario in un header di risposta con chiave X-Sistema-Bancario. Il valore dell'header è in formato nome;cognome.
<br>Come GET ma senza body di risposta.

