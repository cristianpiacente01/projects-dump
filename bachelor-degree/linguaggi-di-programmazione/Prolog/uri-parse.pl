/* Consegna di Gennaio 2022 - Piacente Cristian 866020
Parser di uri con grammatica semplificata
15/01/22 Universita' degli Studi di Milano - Bicocca
Corso di Linguaggi di Programmazione

Componenti del gruppo:

Cavaleri Matteo 875050
Piacente Cristian 866020
Tombolini Simone 869564
*/

digit --> [D], { atom(D), atom_number(D, Digit), between(0, 9, Digit) }.
/* quando converto con string_chars a lista di caratteri, 
non ho numeri ma atomi: un digit valido 
puo' essere ad esempio ['1'],
converto '1' in number e controllo che sia tra 0 e 9 */


identificatore_host --> [H | T], { subtract([H | T],
					    [., /, ?, #, @, :],
					    [H | T])
				 }.

/* identificatore_host non ammette i caratteri . / ? # @ :
sottraggo dalla lista [Head | Tail] quei caratteri, 
se ottengo la stessa lista [Head | Tail] significa 
che i caratteri non ammessi non sono presenti,
inoltre definendo la lista come [Head | Tail] sappiamo che
e' presente almeno un elemento, cioe' Head, mentre Tail puo' essere [] */


identificatore --> [H | T], { subtract([H | T],
				       [/, ?, #, @, :],
				       [H | T])
			    }.

/* stesso discorso per identificatore ma qui il punto e' ammesso */


fragment --> [_ | _].
% 42
% fragment non ha caratteri non ammessi e ovviamente ha almeno un carattere


query --> [H | T], { subtract([H | T], [#], [H | T]) }.

% l'unico carattere non ammesso in query e' #


optional_path --> []. % caso base: 0 volte

optional_path --> [/], identificatore, optional_path.

% ['/' identificatore]*


path --> identificatore, optional_path.

% per costruire il path, spezzo in identificatore e parte opzionale



% inizio definizione grammatica per il path speciale nello schema zos


% predicati aggiuntivi

is_alphanum_list([]) :- !.

is_alphanum_list([X]) :-
    !, % un solo elemento
    char_type(X, alnum).

is_alphanum_list([H | T]) :-
    % piu' di un elemento
    is_alphanum_list([H]),
    is_alphanum_list(T).

% possibili elementi di id44 (non in ordine)
is_id44_element(['.']) :- !.
is_id44_element([X]) :- is_alphanum_list([X]).


contains_id44_elements([X]) :-
    !,
    is_id44_element([X]).

contains_id44_elements([H | T]) :-
    is_id44_element([H]),
    contains_id44_elements(T).

is_id44_tail([]) :- !.

is_id44_tail([X]) :-
    !,
    is_alphanum_list([X]).

is_id44_tail([H | T]) :-
    last(T, Element),
    is_alphanum_list([Element]),
    remove_last_element([H | T], NewList), % definito piu' in basso
    contains_id44_elements(NewList).

% qui continuano le regole DCG

opt_id8 --> [].

opt_id8 --> ['('], [H | T], [')'], { length([H | T], X),
				     between(1, 8, X),
				     char_type(H, alpha),
				     % carattere alfabetico
				     is_alphanum_list(T)
				     /* caratteri alfanumerici */
				   }.

id44 --> [H | T], { length([H | T], X),
		    between(1, 44, X),
		    char_type(H, alpha),
		    is_id44_tail(T)
		    /* predicato speciale per id44 */
		  }.



path_zos --> id44, opt_id8. % path speciale zos



port --> digit. % caso base: 1 digit

port --> digit, port.

% una porta e' la concatenazione di piu' digit


byte --> [AtomX], [AtomY], [AtomZ],
	 { phrase('digit', [AtomX]),
	   phrase('digit', [AtomY]),
	   phrase('digit', [AtomZ]),
	   atom_number(AtomX, X),
	   atom_number(AtomY, Y),
	   atom_number(AtomZ, Z),
	   Num is X * 100 + Y * 10 + Z,
	   between(0, 255, Num)
	 }.

% per controllare l'IP spezzo in 4 byte e controllo singolarmente i byte


indirizzo_IP --> byte, [.],
		 byte, [.],
		 byte, [.],
		 byte.

% IP = concatenazione di 4 byte separati dal punto


optional_id_host --> [].

optional_id_host --> [.], identificatore_host, optional_id_host.

% ['.' identificatore_host]*


host --> indirizzo_IP.

host --> identificatore_host, optional_id_host.

/* in realta' se la prima regola fallisce entra nella seconda
rendendo inutili i controlli sui byte */


userinfo --> identificatore.

% self-explanatory


authority --> [/], [/], host.

authority --> [/], [/], userinfo, [@], host.

authority --> [/], [/], host, [:], port.

authority --> [/], [/], userinfo, [@], host, [:], port.

/* i 4 casi che puo' avere authority,
poiche' l'unica parte obbligatoria e' host (dopo '//') */



check_lowercase([H | T], Check) :-
    /* predicato che controlla se una lista di caratteri
convertita in lowercase e' uguale a Check */
    !,
    string_chars(Str, [H | T]),
    string_lower(Str, Check).

check_lowercase(Str, Check) :-
    % versione alternativa usata in check_special/2 dove ho un atomo
    string_lower(Str, Check).

sp_scheme_zos --> [H | T], { check_lowercase([H | T], "zos") }.

sp_scheme_mailto --> [H | T], { check_lowercase([H | T], "mailto") }.

sp_scheme_news --> [H | T], { check_lowercase([H | T], "news") }.

sp_scheme_telfax --> [H | T], { check_lowercase([H | T], "tel") }.

sp_scheme_telfax --> [H | T], { check_lowercase([H | T], "fax") }.

/* definizione degli schemi speciali, composti da scheme ben precisi 
e che hanno una grammatica diversa dal normale */


scheme --> identificatore.

% self-explanatory


% campi opzionali che rimangono

opt_authority --> [].

opt_authority --> authority.

first_opt --> [].

first_opt --> path.

second_opt --> [].

second_opt --> [?], query.


third_opt --> [].

third_opt --> [#], fragment.


big_opt --> [].

big_opt --> [/],
	    first_opt,
	    second_opt,
	    third_opt.

zos_big_opt --> [].

% come big_opt per URI1 pero' con path di zos

zos_big_opt --> [/],
		path_zos,
		second_opt,
		third_opt.


/* per gestire i campi opzionali,
spezzo in parti piu' piccole opzionali e poi le concateno */



mailto_opt --> [].

mailto_opt --> userinfo.

mailto_opt --> userinfo, [@], host.


news_opt --> [].

news_opt --> host.


telfax_opt --> [].

telfax_opt --> userinfo.



% uri con scheme mailto

uri --> sp_scheme_mailto,
	[:],
	!, % cut, non fare backtracking con altre regole
	mailto_opt.


% uri con scheme news

uri --> sp_scheme_news,
	[:],
	!,
	news_opt.

% uri con scheme tel o fax

uri --> sp_scheme_telfax,
	[:],
	!,
	telfax_opt.

% uri con scheme zos

uri --> sp_scheme_zos,
	[:],
	!,
	opt_authority,
	zos_big_opt.

% URI1

uri --> scheme,
	[:],
	opt_authority,
	big_opt.

/* qui termina la definizione della grammatica con le DCG
e inizia la parte del parsing che si basa sui delimitatori */

/* delimiter/2 definisce i caratteri 
che delimitano gli elementi della grammatica */

delimiter('scheme', ':').
delimiter('scheme', '/').
delimiter('userinfo', '@').
delimiter('host', ':').
delimiter('host', '/').
delimiter('port', '/').
delimiter('path', '?').
delimiter('path', '#').
delimiter('query', '#').

% delimiter/1 dice che quell'elemento puo' non avere delimitatore

:- dynamic delimiter/1. % usato dinamicamente per userinfo in scheme speciali

delimiter('host').
delimiter('port').
delimiter('path').
delimiter('query').
delimiter('fragment').

/* keep_delimiter/1 dice che voglio tenere il delimiter nella SubList
(la SubList sarebbe la sottolista di caratteri 
successiva all'elemento trovato) 
tengo l'eventuale delimiter di path (cioe' ?) e di query (cioe' #)
altrimenti poi query e fragment si confondono facilmente */

keep_delimiter('path').
keep_delimiter('query').

/* get_default_result/2 dice
che risultato dare in caso di elemento non trovato */

get_default_result('port', 80) :- !.
get_default_result(_, []).

/* check_authority/2 mi serve per capire se c'e' un host 
(obbligatorio in caso di authority)
e se ci possono essere eventuali userinfo e port,
il secondo argomento vale 1 
se si trova l'authority (che in realta' inizia con '//')
nella SubList passata come primo argomento, 
0 altrimenti */

check_authority([:, /, / | _], 1) :- !.
check_authority(_, 0).

/* fix_rest/3 viene utilizzato per rimuovere i delimitatori 
in testa nella SubList,
se c'e' un fatto di keep_delimiter il risultato e' la lista di partenza */

fix_rest(Element, [H | T], [H | T]) :-
    delimiter(Element, H), % delimiter in testa
    keep_delimiter(Element), % ... ma voglio tenerlo
    !.

fix_rest('scheme', [':', '/', '/' | T], T) :- !.

fix_rest('scheme', [':', '/' | T], T) :- !.

fix_rest('scheme', [':' | T], T) :- !.

% ho dovuto esplicitare tutti i casi di scheme perche'
% ho tolto la ricorsione nella definizione di fix_rest in basso

fix_rest(Element, [H | T], T) :-
    delimiter(Element, H), % delimiter in testa e non voglio tenerlo
    !.

fix_rest(_, SubList, SubList).

% caso base, non ho delimiter in testa, ho finito

fix_port(Atom, Result) :-
    atom(Atom),
    !,
    atom_number(Atom, Result).

fix_port(80, 80). % caso di default, non devo fare nulla

/* predicato che mi converte l'eventuale port da atom a number,
questo perche' guardando l'esempio 80 e' un numero e non un atomo,
se fosse stato un atomo ci sarebbe scritto '80' */

% qui utilizzo un predicato helper per ottenere un elemento della grammatica

/* get_element_helper/5 ha come argomenti:
- una lista di caratteri che corrisponde 
alla SubList della precedente chiamata,
o a tutta la lista iniziale se stiamo cercando 
lo scheme dato che e' il primo elemento 
- l'elemento della grammatica da cercare
- un accumulatore che tiene i caratteri validi trovati finora
- il risultato vero e proprio, cioe' un atomo 
(o un numero se stiamo cercando port)
- SubList, la sottolista dei caratteri successivi a ElementRes
*/

/* caso critico: nell'host se ho un punto skippo il punto
altrimenti una stringa che termina col punto non e' un valido host */

get_element_helper(Chars, 'host', ElementList, ElementRes, SubList) :-
    last(ElementList, '.'),
    remove_last_element(ElementList, OldElemList),
    phrase('host', OldElemList),
    /* se ho un punto alla fine dell'accumulatore, 
lo tolgo e mi assicuro che quello prima sia valido */
    append(ElementList, [RestH | _], Chars),
    /* trovo una lista con RestH come head (il prossimo carattere) 
tale che concatenando l'accumulatore con essa si ha la lista di tutti
i caratteri */
    append(ElementList, [RestH], NewElemList),
    /* il nuovo accumulatore sara' quello precedente con 
alla fine il prossimo carattere, cioe' RestH, che metto in una lista
per poter fare l'append */
    !, /* arrivati qui si sa che il punto non era l'ultimo carattere
altrimenti non ci sarebbe un RestH e fallirebbe, metto il cut perche'
siamo sicuri che sia questo il caso e non bisogna fare backtracking */
    get_element_helper(Chars, 'host', NewElemList, ElementRes, SubList).
/* chiamata con il nuovo accumulatore, in pratica e' stato gestito
 il punto skippandolo, perche' senno' phrase('host', ElementList)
fallirebbe, con ElementList = lista con punto alla fine */

% stesso ragionamento per path con lo slash

get_element_helper(Chars, 'path', ElementList, ElementRes, SubList) :-
    last(ElementList, '/'),
    remove_last_element(ElementList, OldElemList),
    phrase('path', OldElemList),
    append(ElementList, [RestH | _], Chars),
    append(ElementList, [RestH], NewElemList),
    !,
    get_element_helper(Chars, 'path', NewElemList, ElementRes, SubList).

% caso ricorsivo

get_element_helper(Chars, Element, ElementList, ElementRes, SubList) :-
    phrase(Element, ElementList), % mi assicuro che sia tutto valido
    append(ElementList, [RestH | _], Chars),
    % mi assicuro che esista almeno un carattere rimanente da controllare
    append(ElementList, [RestH], NewElemList),
    % trovo il nuovo accumulatore
    !, % cut, non fare backtracking perche' e' questo il caso
    get_element_helper(Chars, Element, NewElemList, ElementRes, SubList).
% chiamata ricorsiva col nuovo accumulatore

% un caso base: posso non avere un delimiter ed e' tutto valido

% (non c'e' altro da controllare altrimenti sarei nel caso di prima)

get_element_helper(Chars, Element, ElementList, ElementRes, SubList) :-
    delimiter(Element), % Element puo' non avere un delimiter
    phrase(Element, ElementList), % mi assicuro che sia tutto valido
    !, 
    append(ElementList, SubList, Chars), % trovo la SubList rimanente
    atomic_list_concat(ElementList, ElementRes). % converto la lista a atomo

% un altro caso base: devo togliere l'ultimo carattere (cioe' un delimiter)

get_element_helper(Chars, Element, ElementList, ElementRes, SubList) :-
    delimiter(Element, Delimiter), % trovo i delimiter di Element
    last(ElementList, Delimiter), % l'ultimo elemento e' un delimiter
    remove_last_element(ElementList, ActualElemList),
    % lo tolgo, ottenendo ActualElemList = lista senza delimiter alla fine
    phrase(Element, ActualElemList),
    % mi assicuro che tutto quello prima sia valido
    !,
    append(ActualElemList, SubList, Chars), % trovo la SubList
    atomic_list_concat(ActualElemList, ElementRes). % converto in atomo

/* ultimo caso base: non trovo un delimiter (obbligatorio) ed e' tutto valido
oppure non trovo l'elemento */

get_element_helper(Chars, Element, _, ElementRes, Chars) :-
    get_default_result(Element, ElementRes).
/* SubList diventa tutto Chars 
e ElementRes = risultato di default in base all'Element,
quindi 80 per port e lista vuota per gli altri Element */

/* il predicato helper termina qui, ora c'e' il predicato
get_helper che utilizza l'helper, quindi 
non ha l'accumulatore tra gli argomenti*/

/* ma prima di get_element/4, definisco get_element/6 solo per scheme 
per capire se saltare path e eventuali userinfo e port oppure no,
e il sesto argomento per supportare le sintassi speciali,
gli argomenti sono:
- Chars: lista di tutti i caratteri da considerare
- Element: nome dell'elemento della grammatica da cercare
- ElementRes: risultato trovato
(atomo o lista vuota, tranne per port dove e' sempre un numero)
- SubList: sottolista da considerare successivamente, segue l'elemento trovato
- UserinfoHostPort: argomento in piu' rispetto a get_element/4,
vale 1 se check_authority ha successo, 0 se non viene trovato l'authority 
- Spec: 0 se non e' uno scheme speciale, 1 se tel o fax, 
2 se news, 3 se mailto (zos viene gestito direttamente con le DCG) */

get_element([H | T], 'scheme', ElementRes, SubList, UserinfoHostPort, Spec) :-
    /* mi serve spezzare la lista Chars in Head e Tail perche' all'inizio
l'accumulatore diventa la lista con il primo carattere 
cioe' la lista con Head */
    get_element_helper([H | T], 'scheme', [H], ElementRes, TempSubList),
    /* da notare che non si ottiene subito SubList 
ma un'altra lista che chiamo TempSubList, perche' poi si andra' a utilizzare
fix_rest per eventualmente rimuovere i delimiter in testa, 
se non li voglio tenere */
    check_authority(TempSubList, UserinfoHostPort),
    /* ma prima di usare fix_rest, uso check_authority per vedere 
se e' presente l'authority, perche' se rimuovo subito i delimiter 
non ho piu' il modo di vedere subito se c'e' un authority */
    check_special(ElementRes, Spec), % check per scheme speciali
    fix_rest('scheme', TempSubList, SubList). % ora tolgo i delimiter

/* check_special/2 viene definito piu' in basso,
dopo get_userinfo_host_port */




% ora c'e' get_element/4 (e anche quelli particolari per query e fragment)

% casi in cui ho ancora il delimiter, a causa di keep_delimiter

get_element_q(['?' | T], 'query', ElementRes, SubList) :-
    % predicato particolare per evitare la ricorsione su se' stesso
    !,
    get_element(T, 'query', ElementRes, SubList).

get_element_q(List, 'query', ElementRes, SubList) :-
    % non c'e' query
    get_element(List, 'query', ElementRes, SubList).

get_element_f(['#' | T], 'fragment', ElementRes, SubList) :-
    % stesso ragionamento per fragment
    !,
    get_element(T, 'fragment', ElementRes, SubList).

get_element_f(List, 'fragment', ElementRes, SubList) :-
    % non c'e' fragment
    get_element(List, 'fragment', ElementRes, SubList).

% se ho la lista vuota come lista di caratteri ho finito

get_element([], Element, ElementRes, []) :-
    !,
    get_default_result(Element, ElementRes).

% se ho port come elemento devo convertire da atomo a numero con fix_port

get_element([H | T], 'port', ElementRes, SubList) :-
    !,
    get_element_helper([H | T], 'port', [H], TempRes, TempSubList),
    fix_port(TempRes, ElementRes),
    fix_rest('port', TempSubList, SubList).

% altrimenti tengo un atomo come risultato

get_element([H | T], Element, ElementRes, SubList) :-
    get_element_helper([H | T], Element, [H], ElementRes, TempSubList),
    fix_rest(Element, TempSubList, SubList).

/* qui inizia il predicato helper (con accumulatore CurrentList) 
di remove_last_element, utilizzato per rimuovere l'ultimo carattere 
se e' un delimiter */

/* gli argomenti di remove_last_element_helper/3 sono:
- la lista iniziale
- un accumulatore CurrentList
- la lista finale NewList senza l'ultimo elemento della lista */

% caso ricorsivo: lista con almeno due elementi

remove_last_element_helper([H1, H2 | T], CurrentList, NewList) :-
    !, % ho almeno due elementi, non fare backtracking
    append(CurrentList, [H1], NewCurrentList),
    /* dato che ho almeno due elementi, di sicuro il primo lo devo tenere
quindi lo metto alla fine dell'accumulatore e poi chiamo ricorsivamente
dal secondo elemento in poi */
    remove_last_element_helper([H2 | T], NewCurrentList, NewList).

% caso base: ho solo un elemento, il risultato e' l'accumulatore stesso

remove_last_element_helper([_], CurrentList, CurrentList).


/* predicato remove_last_element/2 che richiama il predicato helper
usando come accumulatore una lista vuota */

remove_last_element(List, NewList) :-
    remove_last_element_helper(List, [], NewList).

/* ora il predicato get_userinfo_host_port/6 per gestire userinfo, host e port
argomenti:
- flag che vale 1 oppure 0 in base al risultato di check_authority 
utilizzato in precedenza, 
1 se e' presente un authority, 0 altrimenti
- Chars: lista di tutti i caratteri
- Userinfo: eventuale userinfo oppure []
- Host: host trovato
- Port: eventuale port, oppure 80
- SubList: sottolista da utilizzare successivamente per gli altri elementi */

get_userinfo_host_port(1, Chars, Userinfo, Host, Port, SubList) :-
    !, % se ho 1 prendo userinfo, host e port sfruttando get_element/4
    get_element(Chars, 'userinfo', Userinfo, Chars2),
    get_element(Chars2, 'host', Host, Chars3),
    get_element(Chars3, 'port', Port, SubList).

get_userinfo_host_port(_, Chars, [], [], 80, Chars).
/* se non ho 1 ma 0 oppure qualsiasi altra cosa come flag, 
non c'e' un authority quindi Userinfo = [], Host = [], Port = 80
e la sottolista da considerare successivamente e' quella iniziale
cioe' tengo tutti i caratteri */

/* check_special/2 prende un atomo (scheme) 
e il secondo argomento e':
3 se ElementRes e' mailto
2 se news
1 se tel o fax
0 altrimenti (scheme non speciale)
(il controllo e' case insensitive) */ 
check_special(ElementRes, 3) :-
    check_lowercase(ElementRes, "mailto"),
    !.

check_special(ElementRes, 2) :-
    check_lowercase(ElementRes, "news"),
    !.

check_special(ElementRes, 1) :-
    check_lowercase(ElementRes, "tel"),
    !.

check_special(ElementRes, 1) :-
    check_lowercase(ElementRes, "fax"),
    !.

% zos viene gestito direttamente con le DCG

check_special(_, 0).

/* predicato speciale che usa quello normale se non si ha uno scheme speciale
gli argomenti sono:
- un numero che identifica il tipo di scheme (da check_special)
- CheckUHP (risultato di check_authority, inutile se lo scheme e' speciale)
- Chars, lista di caratteri da considerare
- Userinfo
- Host
- Port
- SubList, che dev'essere la lista vuota se siamo in uno scheme speciale,
perche' dopo userinfo e host non c'e' altro */
spec_userinfo_host_port(0, CheckUHP, Chars, Userinfo, Host, Port, SubList) :-
    !, % scheme normale
    get_userinfo_host_port(CheckUHP, Chars, Userinfo, Host, Port, SubList).

spec_userinfo_host_port(1, _, Chars, Userinfo, [], 80, []) :-
    !, % tel o fax
    assert(delimiter('userinfo')), % life hack
    get_element(Chars, 'userinfo', Userinfo, []),
    retract(delimiter('userinfo')). % per non fare casini

spec_userinfo_host_port(2, _, Chars, [], Host, 80, []) :-
    !, % news
    get_element(Chars, 'host', Host, []).

spec_userinfo_host_port(3, _, Chars, Userinfo, Host, 80, []) :-
    !, % mailto
    assert(delimiter('userinfo')),
    get_element(Chars, 'userinfo', Userinfo, Chars2),
    retract(delimiter('userinfo')),
    get_element(Chars2, 'host', Host, []).





/* ora un predicato che da un uri con i suoi campi 
mi fornisce una stringa che lo rappresenta,
viene utilizzato in uri_display/2 */

% uri_to_string/2, gli argomenti sono l'uri e la stringa in output

uri_to_string(uri(Scheme,
		  Userinfo,
		  Host,
		  Port,
		  Path,
		  Query,
		  Fragment), ResultString) :-

    swritef(ResultString, 'Rappresentazione URI:
\tScheme: %w
\tUserinfo: %w
\tHost: %w
\tPort: %w
\tPath: %w
\tQuery: %w
\tFragment: %w', [Scheme,
		  Userinfo,
		  Host,
		  Port,
		  Path,
		  Query,
		  Fragment]).



/* predicati aggiuntivi per la successiva conversione
da URIString con spazi a URIString con %20 */

% chars_replace/5 con accumulatore come quarto argomento

chars_replace(Chars, SubChars, _, Acc, NewChars) :-
    length(Chars, X),
    length(SubChars, Y),
    X < Y,
    % Chars e' piu' breve di SubChars quindi non posso trovare SubChars
    !,
    append(Acc, Chars, NewChars).

chars_replace(Chars, Chars, NewSubChars, Acc, NewChars) :-
    !,
    % se come SubChars ho Chars stesso
    append(Acc, NewSubChars, NewChars).

% casi ricorsivi

chars_replace(Chars, SubChars, NewSubChars, Acc, NewChars) :-
    append(SubChars, Rest, Chars), % trovati all'inizio
    !,
    append(Acc, NewSubChars, NewAcc),
    chars_replace(Rest, SubChars, NewSubChars, NewAcc, NewChars).

chars_replace([H | T], SubChars, NewSubChars, Acc, NewChars) :-
    % SubChars non trovato per ora, metto nell'accumulatore l'head e continuo
    append(Acc, [H], NewAcc),
    chars_replace(T, SubChars, NewSubChars, NewAcc, NewChars).


% string_replace/4 che usa chars_replace con accumulatore []

string_replace(String, Substr, NewSubstr, NewString) :-
    string_chars(String, Chars),
    string_chars(Substr, SubChars),
    string_chars(NewSubstr, NewSubChars),
    chars_replace(Chars, SubChars, NewSubChars, [], NewChars),
    string_chars(NewString, NewChars).


% implementazione di uri_parse/2

uri_parse(OldURIString, uri(Scheme,
			    Userinfo,
			    Host,
			    Port,
			    Path,
			    Query,
			    Fragment)) :-

    string_replace(OldURIString, " ", "%20", URIString), % conversione

    string_chars(URIString, Chars), % da stringa a lista di caratteri

    phrase('uri', Chars), % controllo che l'uri sia valido

    !, /* per le dcg (nelle dcg non posso mettere i cut dato che 
fermerebbero la ricerca dei match al primo carattere valido),
altrimenti uri_parse da' anche false come risultato */

    % e qui viene scomposto Chars nei vari elementi
    
    get_element(Chars, 'scheme', Scheme, Chars2, UHP, Spec),

    % Spec = special, per gli scheme speciali
    
    % UHP sta per Userinfo Host Port

    spec_userinfo_host_port(Spec, UHP, Chars2, Userinfo, Host, Port, Chars3),

    get_element(Chars3, 'path', Path, Chars4),

    get_element_q(Chars4, 'query', Query, Chars5),

    /* get_element_q viene usato solo per query 
per togliere il ? senza ricorsione
altrimenti avrei problemi per uri del tipo 
"http://42/?????" perche' continua
ricorsivamente a togliere il ? */

    get_element_f(Chars5, 'fragment', Fragment, []).
% stessa cosa per fragment

% dopo aver cercato fragment devo per forza avere la lista vuota come SubList


% per convertire gli spazi nei campi:

fix_spaces_in_atom([], []) :- !.

fix_spaces_in_atom(Atom, NewAtom) :-
    string_replace(Atom, " ", "%20", NewString),
    atom_string(NewAtom, NewString).

% uri_display/2

uri_display(uri(OldScheme,
		OldUserinfo,
		OldHost,
		Port,
		OldPath,
		OldQuery,
		OldFragment), Stream) :-

    !,

    fix_spaces_in_atom(OldScheme, Scheme),

    fix_spaces_in_atom(OldUserinfo, Userinfo),

    fix_spaces_in_atom(OldHost, Host),

    fix_spaces_in_atom(OldPath, Path),

    fix_spaces_in_atom(OldQuery, Query),

    fix_spaces_in_atom(OldFragment, Fragment),
    
    uri_to_string(uri(Scheme,
		      Userinfo,
		      Host,
		      Port,
		      Path,
		      Query,
		      Fragment), OutputStr), % conversione da uri a stringa

    current_output(OldStream), % mi salvo lo stream

    set_output(Stream), % cambio lo stream con quello dell'argomento

    writeln(OutputStr), % salvo nel buffer la stringa

    flush_output(Stream), % scrivo nello stream quello che c'e' nel buffer

    set_output(OldStream). % reimposto lo stream precedente


% uri_display/2 non richiesto che prende un URIString al posto di un uri

/* a differenza dell'altro, se l'uri (URIString) non e' valido 
non viene stampato niente perche' uri_parse fallisce */

uri_display(URIString, Stream) :-
    /* a questo punto so che URIString non e' un uri del tipo uri(Scheme, ...)
    per il cut messo sopra */
    uri_parse(URIString, URI),
    uri_display(URI, Stream).

% uri_display/1

uri_display(uri(Scheme,
		Userinfo,
		Host,
		Port,
		Path,
		Query,
		Fragment)) :-
    !,

    current_output(Stream),
    
    uri_display(uri(Scheme,
		    Userinfo,
		    Host,
		    Port,
		    Path,
		    Query,
		    Fragment), Stream).

% uri_display/1 non richiesto che prende un URIString al posto di un uri

/* a differenza dell'altro, se l'uri (URIString) non e' valido 
non viene stampato niente perche' uri_parse fallisce */

uri_display(URIString) :-
    uri_parse(URIString, URI),
    uri_display(URI).
