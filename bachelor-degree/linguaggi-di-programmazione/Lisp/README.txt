Consegna di Gennaio 2022 - Piacente Cristian 866020
V1.1: Lisp commenting convention.
DATE: 15/01/22
TITLE: URI-parser

Universita' degli Studi di Milano - Bicocca

Course Programming Languages

Project members:
Cavaleri Matteo 875050
Piacente Cristian 866020
Tombolini Simone 869564


DESCRIPTION: This project has the aim of parsing a given string (if a valid URI) 
	     creating an internal structure and decomposing the URI into 7 fields:

	     	1 Scheme
	     	2 Userinfo
	     	3 Host
	     	4 Port
	     	5 Path
	     	6 Query
	     	7 Fragment
	     
	     The port is saved as an integer unlike the other fields; if not found then it's set to 80.
	     Regarding the other fields, they are stored as strings, or NIL if not found.

	     
	     For example: (uri-parse "scheme://userinfo@host:42/path?query#fragment")
	     		  #S(URI-STRUCTURE :SCHEME "scheme" :USERINFO "userinfo" :HOST "host" :PORT 42 :PATH "path" :QUERY "query" :FRAGMENT "fragment")

	     We devoloped the parser using a simplified version of RFC 3986 https://datatracker.ietf.org/doc/html/rfc3986.
	     In particular we developed a library in the programming language: Common Lisp.
	     Before parsing, we convert all Space occurrences (ASCII 32nd character) to "%20".

	     In relation to the 7 fields specified above, some of them are required
	     (for example, if a URI doesn't contain a valid scheme we know it's not valid).

	     Some schemes are considered special, because they have their own grammar rules.

	     For example, "zos" is a special scheme in which the field "path" is required with its own rule
	     (only if '/' is found after the eventual authority).
	     This special zos restriction doesn't count for the other schemes,
	     since in general path is optional.

	     For instance,
	     	"zos:/" is not a valid URI (because there are 0 characters in the path)
	     	"zos:" is a valid URI (because there's no '/' after the (missing) authority)
	     	"zos:/special(path)" is a valid URI.

	     The other accepted special schemes are
	     	- "mailto"
	     	- "news"
	     	- "tel" or "fax".



HOW TO USE THE PROJECT: Download LispWorks from http://www.lispworks.com/index.html and go to File --> Compile and Load... (choose uri-parse.lisp).
	     	        You can use the listener to input Common Lisp code, for example: 
	     	     	     (uri-parse "URI to check and eventually split")


Necessary functions to know: 

1) uri-parse: the function parses a URI string.

Parameter: string (representation of a URI).

Returns:     uri-structure (a struct with the fields specified in the project description)
	     or NIL (if the argument is not a string or a valid URI).

2) uri-display: the function prints the given uri-structure's fields 
	        on the standard output if only an argument is passed, otherwise on the specified output stream.

Parameters: uri-structure (first arg, it represents the URI which you want to display).
	    &optional stream (second arg: output stream used for printing).

Returns:    T
	    or NIL (if the first argument isn't a uri-structure or the second is neither NIL nor a stream).


3) Here are the 7 functions which get a uri-structure and return a specific field value:

uri-scheme:	uri-structure --> string

uri-userinfo:   uri-structure --> string

uri-host:	uri-structure --> string

uri-port:	uri-structure --> integer

uri-path:	uri-structure --> string

uri-query:	uri-structure --> string

uri-fragment:	uri-structure --> string


License: completely free license

If you want further information, please check the commented source code.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

DATA: 15/01/2022
TITOLO: URI-parser

Universita' degli Studi di Milano - Bicocca

Corso di Linguaggi di Programmazione

Membri del progetto:
Cavaleri Matteo 875050 
Piacente Cristian 866020
Tombolini Simone 869564


DESCRIZIONE: il progetto ha lo scopo di parsare di una stringa data in input (se è un URI valido)
	     creando una struttura interna e scomponendo l'URI in 7 campi:

	     	1 Scheme
	     	2 Userinfo
	     	3 Host
	     	4 Port
	     	5 Path
	     	6 Query
	     	7 Fragment
	     
	     La porta viene memorizzata come un intero a differenza degli altri campi; se non è presente allora diventa 80.
	     Per quanto riguarda gli altri campi, vengono salvati come stringhe oppure come NIL se non trovati.


	     Esempio: (uri-parse "scheme://userinfo@host:42/path?query#fragment")
	     	      #S(URI-STRUCTURE :SCHEME "scheme" :USERINFO "userinfo" :HOST "host" :PORT 42 :PATH "path" :QUERY "query" :FRAGMENT "fragment")

	     Abbiamo sviluppato il parser utilizzando una versione semplificata delle RFC 3986 https://datatracker.ietf.org/doc/html/rfc3986.
	     In particolare abbiamo sviluppato una libreria nel linguaggio di programmazione: Common Lisp.
	     Prima di fare il parsing, tutte le occorrenze del carattere spazio (32esimo carattere ASCII) vengono sostituite con la stringa "%20".

	     Riguardo ai 7 campi specificati sopra, alcuni di essi sono obbligatori
	     (per esempio, se un URI non contiene uno scheme valido allora l'URI non è valido).

	     Alcuni scheme sono considerati speciali, perché hanno proprie regole della grammatica.

	     Per esempio, "zos" è uno scheme speciale in cui il campo "path" è obbligatorio con la sua regola di produzione
	     (solo se '/' è trovato dopo l'eventuale authority).
	     Questa limitazione di zos non conta per gli altri scheme,
	     dato che il path è opzionale in generale.

	     Ad esempio:
	     	"zos:/" non è valido (non ci sono caratteri dopo '/')
	     	"zos:" è valido (path non è obbligatorio poiché non c'è '/')
	     	"zos:/special(path)" è valido.

	     Gli altri scheme speciali accettati sono
	     	- "mailto"
	     	- "news"
	     	- "tel" o "fax".



COME USARE IL PROGETTO: Scarica LispWorks da http://www.lispworks.com/index.html e vai su File --> Compile and Load... (scegli uri-parse.lisp).
	     	        Puoi utilizzare il listener per scrivere codice in Common Lisp, ad esempio: 
	     	     	     (uri-parse "URI da parsare")


Funzioni da conoscere: 

1) uri-parse: fa il parsing di una URI string.

Parametro: string (rappresentazione di un URI).

Restituisce: uri-structure (una struct con i campi elencati nella descrizione del progetto)
	     oppure NIL (se l'argomento non è una stringa o se non è un URI valido).

2) uri-display: la funzione stampa i campi della uri-structure passata come argomento 
	        su standard output se è presente solo un argomento, altrimenti sull'output stream specificato.

Parametri: uri-structure (primo arg, rappresenta l'URI che si desidera visualizzare).
	   &optional stream (secondo arg: output stream usata per la stampa).

Restituisce:     T
		 oppure NIL (se il primo argomento non è una uri-structure oppure il secondo né NIL né uno stream).

3) Di seguito le 7 funzioni che ricevono in ingresso una uri-structure e restituiscono un specifico valore di un campo:

uri-scheme:	uri-structure --> string

uri-userinfo:   uri-structure --> string

uri-host:	uri-structure --> string

uri-port:	uri-structure --> integer

uri-path:	uri-structure --> string

uri-query:	uri-structure --> string

uri-fragment:	uri-structure --> string


Licenza: libera

Per informazioni più dettagliate, si controlli il codice sorgente (commentato).