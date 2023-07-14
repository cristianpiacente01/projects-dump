Consegna di Gennaio 2022 - Piacente Cristian 866020
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
	     Regarding the other fields, they are stored as atoms, or [] if not found.

	     
	     For example: ?- uri_parse("scheme://userinfo@host:42/path?query#fragment", URI).
	     		  URI = uri(scheme, userinfo, host, 42, path, query, fragment).

	     We devoloped the parser using a simplified version of RFC 3986 https://datatracker.ietf.org/doc/html/rfc3986.
	     In particular we developed a library in the programming language: SWI-Prolog.
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



HOW TO USE THE PROJECT: Download SWI-Prolog from https://www.swi-prolog.org/Download.html and go to File --> Consult ... (choose uri-parse.pl).
	     	        You can use SWI-Prolog console to input a goal, for example: 
	     	     	     uri_parse("URI to check and eventually split", URI).


Necessary predicates to know: 

1) uri_parse/2: the predicate parses a URI string.

Arguments: +URIString (representation of a URI).
	   -uri(Scheme, Userinfo, Host, Port, Path, Query, Fragment)

2) uri_display/1: the predicate prints on the standard output the given URI compound term fields,
		  or if a URI string is passed then it parses the string and it prints the result's fields.

Arguments: +uri(Scheme, Userinfo, Host, Port, Path, Query, Fragment)
	   or +URIString

Examples:

	?- uri_display("scheme://userinfo@host:42/path?query#fragment"). 
	Rappresentazione URI:
		Scheme: scheme
		Userinfo: userinfo
		Host: host
		Port: 42
		Path: path
		Query: query
		Fragment: fragment
	true.

	?- uri_parse("http://google.com", URI), uri_display(URI).
	Rappresentazione URI:
		Scheme: http
		Userinfo: []
		Host: google.com
		Port: 80
		Path: []
		Query: []
		Fragment: []
	URI = uri(http, [], 'google.com', 80, [], [], []).

3) uri_display/2: the predicate prints on the specified output the given URI compound term fields,
		  or if a URI string is passed then it parses the string and it prints the result's fields.

Arguments: +uri(Scheme, Userinfo, Host, Port, Path, Query, Fragment)
	   or +URIString
	   +Stream

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
	     Per quanto riguarda gli altri campi, vengono salvati come atomi oppure come [] se non trovati.


	     Esempio: ?- uri_parse("scheme://userinfo@host:42/path?query#fragment", URI).
	     	      URI = uri(scheme, userinfo, host, 42, path, query, fragment).

	     Abbiamo sviluppato il parser utilizzando una versione semplificata delle RFC 3986 https://datatracker.ietf.org/doc/html/rfc3986.
	     In particolare abbiamo sviluppato una libreria nel linguaggio di programmazione: SWI-Prolog.
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



COME USARE IL PROGETTO: Scarica SWI-Prolog da https://www.swi-prolog.org/Download.html e vai su File --> Consult ... (scegli uri-parse.pl).
	     	        Puoi utilizzare la console di SWI-Prolog per dare in input un goal, ad esempio: 
	     	     	     uri_parse("URI to check and eventually split", URI).


Predicati da conoscere: 

1) uri_parse/2: il predicato fa il parsing di una stringa di URI.

Argomenti: +URIString (rappresentazione di un URI).
	   -uri(Scheme, Userinfo, Host, Port, Path, Query, Fragment)

2) uri_display/1: il predicato stampa su standard output i campi dell'URI (termine composto),
		  oppure se viene passata una stringa allora fa il parsing e stampa i campi del risultato.

Argomenti: +uri(Scheme, Userinfo, Host, Port, Path, Query, Fragment)
	   oppure +URIString

Esempi:

	?- uri_display("scheme://userinfo@host:42/path?query#fragment"). 
	Rappresentazione URI:
		Scheme: scheme
		Userinfo: userinfo
		Host: host
		Port: 42
		Path: path
		Query: query
		Fragment: fragment
	true.

	?- uri_parse("http://google.com", URI), uri_display(URI).
	Rappresentazione URI:
		Scheme: http
		Userinfo: []
		Host: google.com
		Port: 80
		Path: []
		Query: []
		Fragment: []
	URI = uri(http, [], 'google.com', 80, [], [], []).

3) uri_display/2: il predicato stampa sull'output stream specificato i campi dell'URI (termine composto),
		  oppure se viene passata una stringa allora fa il parsing e stampa i campi del risultato.

Argomenti: +uri(Scheme, Userinfo, Host, Port, Path, Query, Fragment)
	   oppure +URIString
	   +Stream


Licenza: libera

Per informazioni più dettagliate, si controlli il codice sorgente (commentato).