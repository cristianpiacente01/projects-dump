# CPbank
##### Pagliaroli Chiara 866160 - Piacente Cristian 866020
# Istruzioni per eseguire l'elaborato
Ci sono due modalità per poter eseguire e testare l'elaborato, in locale (con installazione da parte dell'utente di tutte le dipendenze) o online (dove basta collegarsi al sito indicato).

 ### 1. In locale
 Per produrre l'elaborato è stata utilizzata l'architettura Windows x64.
 In particolare è stato testato sia su Windows 10 Home build 19044.1766 sia su Windows 11 Pro build 22000.675, entrambi versione 21H2.
#### 1.1  Prerequisiti
I prerequisiti minimi per l'esecuzione in locale sono:

 - **Go**: scaricare l'installer per la versione **go1.18.3 windows/amd64** al seguente link: https://go.dev/dl/go1.18.3.windows-amd64.msi
> Nessuna nota aggiuntiva per quanto riguarda l'installazione di Go.
 - **PostgreSQL**: scaricare l'installer per la versione **14.4** di PostgreSQL per Windows x86-64 al seguente link: https://www.enterprisedb.com/postgresql-tutorial-resources-training?uuid=db55e32d-e9f0-4d7c-9aef-b17d01210704
 >Invece, per PostgreSQL in fase di installazione verranno chiesti i componenti da installare: consigliamo di selezionare **PostgreSQL Server**, **pgAdmin 4** e **Command Line Tools**, in quanto il secondo è molto utile per gestire e lavorare con database PostgreSQL mediante un'interfaccia grafica.
<u>Per quanto riguarda le credenziali per connettersi al database, è possibile scegliere credenziali diverse da quanto consigliato qui in basso, ma in questo caso occorrerà modificare il file **conf.ini** presente nella cartella di progetto.</u>
Riprendendo gli step necessari, una volta selezionati i componenti verrà richiesta una password per il superuser postgres: noi abbiamo scelto **root**.
Scelta la password, si deve selezionare la porta, si consiglia la porta **5432**.
Per quanto riguarda la lingua usata dal database cluster, si può scegliere il locale **English, United States** così da avere $ come valuta utilizzata dal campo MONEY.
A questo punto è possibile procedere con l'installazione.
#### 1.2  Configurazione per il progetto
##### 1.2.1 Configurazione di Go
Installato Go, occorre lavorare all'interno della **directory cpbank** sul Prompt dei comandi/Windows PowerShell.
Inizializzare la cartella di progetto con il seguente comando:

    go mod init cpbank
<br>
Una volta inizializzata la cartella per il modulo cpbank, il seguente comando troverà e installerà le dipendenze necessarie per eseguire il codice:

    go mod tidy
<br>
A questo punto è necessario fare la build del progetto con

    go build cpbank
e finalmente verrà creato un eseguibile cpbank.exe, che è possibile eseguire da riga di comando oppure, in alternativa, si può far interpretare il file **main.go** da Go con il comando

    go run main.go

<br>
Entrambe le modalità permettono di eseguire l'applicazione.


<br>

##### 1.2.2 Configurazione di PostgreSQL
Il programma Go in locale ha bisogno di connettersi a un database PostgreSQL per funzionare correttamente.
Avendo installato i componenti PostgreSQL dal punto 1.1, utilizzeremo **pgAdmin 4** per configurare il database.
Per accedere a pgAdmin verrà richiesto di inserire la password scelta in precedenza.
Sulla schermata di sinistra dovrebbe comparire la scritta Servers (nel panel Browser): espandendo Servers, si vedrà PostgreSQL 14, fare click destro &#8594; Create &#8594; Database &#8594; scrivere **sd** (anche questo parametro è possibile sceglierlo a piacimento grazie al file conf.ini ma sconsigliato) all'interno del campo "Database" &#8594; cliccare su Save.

> Nel caso dia un errore perché esiste già, tasto destro su Servers &#8594; Refresh, poi espandere Servers, PostgreSQL 14 e Databases &#8594; individuare il database sd, poi click destro &#8594; Delete/Drop così verrà eseguito il DROP DATABASE.

A questo punto avremo un database sd vuoto: fare un click su sd &#8594; andare sulla barra blu di pgAdmin (in alto, vicino il titolo della finestra) &#8594; Tools &#8594; Query Tool e si aprirà una schermata dove è possibile scrivere query SQL.
Scrivere il seguente codice:

    CREATE EXTENSION pgcrypto;
    CREATE TABLE Accounts (
	    id CHAR(20) PRIMARY KEY,
	    name VARCHAR(30) NOT NULL,
	    surname VARCHAR(30) NOT NULL,
	    balance MONEY DEFAULT 0,
	    active BOOLEAN DEFAULT 't'
	);
	CREATE TABLE AccountingOperations (
		id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
		type SMALLINT NOT NULL,
		idSender CHAR(20) NOT NULL,
		idRecipient CHAR(20),
		amount MONEY,
		date TIMESTAMP NOT NULL DEFAULT NOW(),
		FOREIGN KEY(idSender) REFERENCES Accounts(id),
		FOREIGN KEY(idRecipient) REFERENCES Accounts(id)
	);
e premere F5 per eseguire le query.

> Le query riportate in alto permettono di creare la struttura delle due tabelle utilizzate nel database sd.
> &Egrave; necessaria l'estensione pgcrypto (prima riga) per utilizzare la funzione gen_random_uuid, che genera un UUID v4.
> La prima tabella Accounts contiene i dati del proprietario del conto, tra cui l'id da 20 cifre esadecimali che viene utilizzato come chiave primaria, il nome, il cognome, il saldo disponibile e un flag che mi dice se l'account è attivo oppure inattivo (risulta inattivo se è stata fatta una richiesta HTTP con verbo DELETE).
> La seconda tabella AccountingOperations contiene le informazioni su ciascuna operazione, cioè l'id UUID v4 generato da PostgreSQL, poi un campo che mi dice il tipo dell'operazione (0 = trasferimento di denaro, 1 = deposito, 2 = prelievo, 3 = storno, 4 = operazione stornata poiché un'operazione non può essere stornata più volte, vedi README), l'id del mittente (chiave esterna), l'id del destinatario (chiave esterna, ma risulta NULL nel momento in cui l'operazione è un deposito o un prelievo), l'ammontare senza segno e un timestamp per avere la data (e l'orario) in cui è stata effettuata l'operazione.

A questo punto le istruzioni per eseguire in locale il progetto sono concluse.

 ### 2. Online
 Come alternativa per eseguire e testare l'elaborato, è sufficiente collegarsi a https://cpbank.herokuapp.com; attraverso il servizio Heroku difatti abbiamo fatto il deploy della cartella di GitHub contente il progetto. Heroku offre un "dyno" (una piccola unità dove poter eseguire codice) con sistema operativo Ubuntu 22.04, dove viene eseguito il file main.go (le richieste vengono gestite esattamente come se fosse un computer in locale a riceverle, non c'è alcuna semplificazione da parte di Heroku); in contemporanea mette a disposizione un database PostgreSQL il cui link è salvato all'interno del dyno sotto la variabile d'ambiente "DATABASE_URL". Ogni settimana questo link viene aggiornato in automatico da Heroku, senza perdita di dati; tuttavia questo può comportare una temporanea indisponibilità (10 minuti circa) del database. Il sito sarà online, ma darà errori per le query verso il database. 
Utilizzando questa modalità quindi non vi sono istruzioni particolari da fornire, in quanto è possibile utilizzare gli endpoint sia backend sia frontend senza alcuna configurazione da parte dell'utente. Inoltre è possibile utilizzare servizi di terze parti per effettuare le richieste dato l'uso del meccanismo CORS.
