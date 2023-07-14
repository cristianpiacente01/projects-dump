;;;; Consegna di Gennaio 2022 - Piacente Cristian 866020
;;;; Parser di uri con grammatica semplificata
;;;; 15/01/22 Universita' degli Studi di Milano - Bicocca
;;;; Corso di Linguaggi di Programmazione
;;;; Componenti del gruppo:
;;;;
;;;; Cavaleri Matteo 875050
;;;; Piacente Cristian 866020
;;;; Tombolini Simone 869564

;;; definisco una struttura chiamata uri-structure con 7 campi

(defstruct uri-structure scheme userinfo host port path query fragment)

;;; funzione che restituisce il valore del campo scheme della struttura
;;; passata come argomento

(defun uri-scheme (structure)
  (uri-structure-scheme structure))

;;; analogamente in basso per gli altri campi

(defun uri-userinfo (structure)
  (uri-structure-userinfo structure))

(defun uri-host (structure)
  (uri-structure-host structure))

(defun uri-port (structure)
  (uri-structure-port structure))

(defun uri-path (structure)
  (uri-structure-path structure))

(defun uri-query (structure)
  (uri-structure-query structure))

(defun uri-fragment (structure)
  (uri-structure-fragment structure))

;;; funzione aggiuntiva per vedere se list e' una lista non nulla
;;; riga 42

(defun not-empty-list (list)
  (and (listp list) (not (null list))))

;;; T se la lunghezza di list e
;;; la lunghezza della lista differenza
;;; tra list e la lista con i caratteri non ammessi
;;; rimane uguale (non posso controllare se le liste sono uguali perche'
;;; la funzione set-difference le tratta come set, quindi non conta l'ordine)

(defun check-illegal-chars (list illegal)
  (cond ((and (not-empty-list list) (not-empty-list illegal))
	 (eql (length list) (length (set-difference list illegal))))))


;;; in basso funzioni che controllano se una lista di caratteri
;;; viene riconosciuto correttamente come un certo elemento della grammatica

(defun check-identificatore (list)
  (check-illegal-chars list '(#\/ #\? #\# #\@ #\:)))

;;; le funzioni check che prendono anche la struttura settano direttamente
;;; il campo trovato se valido, in modo che dopo aver controllato tutto
;;; l'uri la struttura sia gia' stata riempita senza dover fare altro

;;; le funzioni prive di commento sono autoesplicative

(defun check-scheme (list u-struct)
  (and (check-identificatore list)
       (setf (uri-structure-scheme u-struct)
	     (chars-list-to-string list))
       T))

(defun check-userinfo (list u-struct)
  (and (check-identificatore list)
       (setf (uri-structure-userinfo u-struct)
	     (chars-list-to-string list))
       T))

(defun check-query (list u-struct)
  (and (check-illegal-chars list '(#\#))
       (setf (uri-structure-query u-struct)
	     (chars-list-to-string list))
       T))

(defun check-fragment (list u-struct)
  (and (not-empty-list list)
       (setf (uri-structure-fragment u-struct)
	     (chars-list-to-string list))
       T))

(defun check-identificatore-host (list)
  (check-illegal-chars list '(#\. #\/ #\? #\# #\@ #\:)))

(defun check-digit (list)
  (and (listp list)
       (eql 1 (length list))
       (integerp (digit-char-p (car list)))))

;;; per controllare port, ricorsivamente, metto come
;;; caso base quando ho list di lunghezza di 1
;;; e richiamo la check-digit (che prende proprio
;;; una lista di un solo carattere numerico)
;;; mentre il caso ricorsivo controlla
;;; se il car (dentro una cons-cell) e' un digit
;;; e viene eseguita la cdr-recursion

(defun check-port (list u-struct)
  (cond ((and (listp list) (eql 1 (length list)))
	 (and (check-digit list)
	      (setf (uri-structure-port u-struct)
		    (parse-integer
		     (chars-list-to-string list)))
	      T))
	((not-empty-list list)
	 (and (check-digit (cons (car list) NIL))
	      (check-port (cdr list) u-struct)
	      (setf (uri-structure-port u-struct)
		    (parse-integer
		     (chars-list-to-string list)))
	      T))))

;;; check-path-found viene usata nell'helper (funzione con accumulatore)
;;; di check-path quando trova /

(defun check-path-found (before after u-struct)
  ;; before = lista di caratteri prima di /
  ;; after = lista di caratteri dopo /
  (and (check-identificatore before)
       (check-path after u-struct)
       (setf (uri-structure-path u-struct)
	     (chars-list-to-string
	      (append before
		      '(#\/)
		      after)))
       T))

;;; helper della funzione check-path, current-list e' l'accumulatore

(defun check-path-helper (list u-struct current-list)
  (cond ((eql (car (last current-list)) #\/) ; / trovato
	 (check-path-found (butlast current-list)
			   (subseq list (length current-list))
			   u-struct))
	((< (length current-list) (length list)) ; caso ricorsivo
	 ;; nella chiamata ricorsiva prendo l'n-esimo carattere
	 ;; (n = lunghezza accumulatore corrente, in questo
	 ;; modo prende il successivo carattere poiche' gli
	 ;; indici partono da 0)
	 ;; e lo inserisco nell'accumulatore della prossima chiamata
	 (check-path-helper list
			    u-struct
			    (append current-list
				    (cons (nth
					   (length current-list)
					   list)
					  NIL))))))

(defun check-path (list u-struct)
  (cond ((check-identificatore list)
	 ;; caso in cui ho solo un identificatore
	 (and (setf (uri-structure-path u-struct)
		    (chars-list-to-string list))
	      T))
	;; richiamo l'helper con accumulatore iniziale lista vuota (NIL)
	((not-empty-list list) (check-path-helper list u-struct
						  NIL))))

;;; check-byte mi serve per controllare l'IP in seguito

(defun check-byte (list)
  (and (listp list)
       (eql 3 (length list))
       (check-digit (cons (first list) NIL))
       (check-digit (cons (second list) NIL))
       (check-digit (cons (third list) NIL))
       (let
	   ((first-digit (digit-char-p (first list)))
	    (second-digit (digit-char-p (second list)))
	    (third-digit (digit-char-p (third list))))
	 (<=
	  (+
	   (* first-digit 100)
	   (* second-digit 10)
	   third-digit)
	  255)))) ; il valore non deve superare 255

;;; controlla se list e' un IP valido (come sempre, lista di
;;; caratteri)

(defun check-IP (list)
  (and (listp list)
       (eql 15 (length list))
       (eql (nth 3 list) #\.)
       (eql (nth 7 list) #\.)
       (eql (nth 11 list) #\.)
       (check-byte (subseq list 0 3))
       (check-byte (subseq list 4 7))
       (check-byte (subseq list 8 11))
       (check-byte (subseq list 12))))

;;; check-host-found e' l'analogo di check-path-found pero' per host

(defun check-host-found (before after u-struct)
  ;; before = lista di caratteri prima di .
  ;; after = lista di caratteri dopo .
  (and (check-identificatore-host before)
       (check-host after u-struct T)
       (setf (uri-structure-host u-struct)
	     (chars-list-to-string
	      (append before
		      '(#\.)
		      after)))
       T))

(defun check-host-helper (list u-struct current-list)
  (cond ((eql (car (last current-list)) #\.)
	 (check-host-found (butlast current-list)
			   (subseq list (length current-list))
			   u-struct))
	((< (length current-list) (length list))
	 (check-host-helper list
			    u-struct
			    (append current-list
				    (cons (nth
					   (length current-list)
					   list)
					  NIL))))))

;;; ho messo un parametro opzionale "no-ip" perche' in questo modo,
;;; di default (ho NIL) viene controllato anche che sia un IP valido,
;;; tuttavia quando richiamo check-host-found gli passo T come terzo
;;; argomento cosi' Common Lisp evita un controllo inutile in check-host
;;; dato che la regola di produzione di IP
;;; non limita il tipo di host accettato

(defun check-host (list u-struct &optional no-ip)
  (cond ((and (not no-ip) (check-IP list))
	 (and (setf (uri-structure-host u-struct)
		    (chars-list-to-string
		     list))
	      T))
	((check-identificatore-host list)
	 (and (setf (uri-structure-host u-struct)
		    (chars-list-to-string
		     list))
	      T))
	((not-empty-list list) (check-host-helper list u-struct NIL))))

;;; qua invece ci sono alcune funzioni che "consumano",
;;; dalla (sotto)lista passata come argomento,
;;; un particolare elemento della grammatica
;;; poiche' la logica che viene usata per controllare se un uri e' valido,
;;; alla fine, e' che riesco a consumare tutti gli elementi presenti
;;; ed avere NIL come sottolista finale

(defun consume-userinfo-helper (list u-struct acc)
  (cond ((eql (length list) (length acc)) list)
	;; se non trovo userinfo non tolgo niente, restituisco list stessa
	((and (eql (car (last acc)) #\@)
	      (check-userinfo (butlast acc) u-struct))
	 ;; delimitatore @ trovato e tutto quello prima e' un userinfo
	 (subseq list (length acc)))
	;; "consumo" restituendo la sottolista successiva a @
	(T (consume-userinfo-helper ; caso ricorsivo
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-host-helper (list u-struct acc)
  ;; caso specifico dentro authority
  ;; devo avere : come delimitatore perche' dev'esserci port in questo caso
  (cond ((eql (length list) (length acc)) NIL) ; non trovo port
	((and (eql (car (last acc)) #\:)
	      (check-host (butlast acc) u-struct))
	 (subseq list (length acc)))
	(T (consume-host-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-userinfo (list u-struct)
  (consume-userinfo-helper list u-struct NIL))

(defun consume-host (list u-struct)
  (consume-host-helper list u-struct NIL))

;;; altro check, per l'authority

(defun check-authority (list u-struct)
  (and (listp list)
       (>= (length list) 3)
       (eql (first list) (second list))
       (eql (first list) #\/)
       (let
	   ((sublist (consume-userinfo (subseq list 2) u-struct)))
	 (cond ((check-host sublist u-struct) T) ; niente port
	       ((not-empty-list sublist)
		(let
		    ((new-sublist (consume-host sublist u-struct)))
		  (and (not-empty-list new-sublist)
		       (check-port new-sublist u-struct))))))))

(defun consume-scheme-helper (list u-struct acc)
  ;; : come delimitatore
  (cond ((and (eql (car (last acc)) #\:)
	      (check-scheme (butlast acc) u-struct))
	 (subseq list (length acc)))
	((eql (length list) (length acc)) list) ; scheme non trovato
	(T (consume-scheme-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-scheme (list u-struct)
  (consume-scheme-helper list u-struct NIL))

(defun consume-authority-helper (list u-struct acc)
  ;; / come delimitatore perche' so da check-uri che
  ;; non sono nel caso in cui c'e' solo authority
  (cond ((and (eql (car (last acc)) #\/)
	      (check-authority (butlast acc) u-struct))
	 (subseq list (- (length acc) 1))) ; tengo / per dopo
	((eql (length list) (length acc)) list) ; authority non trovato
	(T (consume-authority-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))


(defun consume-authority (list u-struct)
  (consume-authority-helper list u-struct NIL))

(defun consume-path-helper (list u-struct acc)
  ;; delimitatori possibili: ? oppure # (perche' da consume-p-q-f so che
  ;; dev'esserci qualcosa dopo)
  (cond ((and
	  (or (eql (car (last acc)) #\?)
	      (eql (car (last acc)) #\#))
	  (check-path (butlast acc) u-struct))
	 (subseq list (- (length acc) 1))) ; tengo il delimitatore
	((eql (length list) (length acc)) list) ; path non trovato
	(T (consume-path-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-path (list u-struct)
  (consume-path-helper list u-struct NIL))

(defun consume-query-helper (list u-struct acc)
  ;; o nessun delimitatore o #
  (cond ((and (eql (car (last acc)) #\#)
	      (check-query (butlast acc) u-struct))
	 (subseq list (- (length acc) 1))) ; tengo # per dopo
	((and (eql (length list) (length acc))
	      (check-query list u-struct))
	 NIL) ; tutto valido, nessun delimitatore
	((eql (length list) (length acc)) list) ; query non trovato
	(T (consume-query-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-query (list u-struct)
  (cond ((not (eql (car list) #\?)) list) ; ho finito, non ho query
	((>= (length list) 2)
	 (consume-query-helper (cdr list) u-struct NIL))
	(T list))) ; lunghezza < 2

(defun consume-fragment-helper (list u-struct acc) 
  ;; nessun delimitatore
  (cond ((and (eql (length list) (length acc))
	      (check-fragment list u-struct))
	 NIL) ; ok
	((eql (length list) (length acc)) list) ; fragment non trovato
	(T (consume-fragment-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-fragment (list u-struct)
  (cond ((not (eql (car list) #\#)) list) ; ho finito, non ho fragment
	((>= (length list) 2)
	 (consume-fragment-helper (cdr list) u-struct NIL))
	(T list))) ; lunghezza < 2

;;; consume-p-q-f se riesce a consumare tutto restituisce NIL
;;; altrimenti qualcosa che rimane che non e' corretto

(defun consume-p-q-f (list u-struct)
  ;; ho lo / perche' l'ho tenuto dopo consume-authority 
  (cond ((not (eql (car list) #\/)) list) ; non ho / quindi non valido
	((eql (length list) 1) NIL) ; ho finito, ho solo / che e' valido
	(T (let
	       ((sublist (cdr list))) ; per togliere /
	     (cond ((check-path sublist u-struct) NIL)
		   ;; ho solo path, ho finito
		   ((and (eql (car sublist) #\?)
			 (check-query (cdr sublist) u-struct))
		    NIL) ; stesso per query
		   ((and (eql (car sublist) #\#)
			 (check-fragment (cdr sublist) u-struct))
		    NIL) ; ... e per fragment
		   (T (consume-fragment
		       (consume-query
			(consume-path sublist u-struct)
			u-struct)
		       u-struct)))))))

;;; funzioni aggiuntive per controllare lo scheme speciale zos

(defun valid-id44-chars (list)
  ;; controllo sui caratteri interni (estremi esclusi)
  ;; perche' gli estremi sono controllati in check-id44
  (and (listp list)
       (cond ((null list) T) ; caso base
	     (T ; caso ricorsivo
	      (and
	       (or (alphanumericp (car list))
		   (eql (car list) #\.))
	       (valid-id44-chars (cdr list)))))))

(defun valid-id8-chars (list)
  ;; controllo sui caratteri dal secondo in poi perche'
  ;; il primo e' gia' stato controllato in check-id8
  ;; ma in realta' avrei potuto ricontrollare anche il primo
  ;; (inutile perche'
  ;; tutti i caratteri alpha sono anche alphanumeric)
  (and (listp list)
       (cond ((null list) T)
	     (T
	      (and
	       (alphanumericp (car list))
	       (valid-id8-chars (cdr list)))))))

;;; il controllo finale (solo caratteri alfanumerici e punti)
;;; in check-id44 esclude gli estremi perche' vengono
;;; gia' controllati prima

(defun check-id44 (list)
  (and (listp list)
       (>= (length list) 1)
       (<= (length list) 44)
       (alpha-char-p (car list)) ; inizia con un carattere alfabetico
       (alphanumericp (car (last list))) ; non termina con '.'
       (cond ((eql (length list) 1) T) ; gia' controllato
	     (T
	      (valid-id44-chars (subseq list 1 (- (length list) 1)))))))

(defun consume-id44-helper (list acc)
  (cond ((check-id44 list) NIL) ; ho finito, valido
	((and (eql (car (last acc)) #\()
	      (check-id44 (butlast acc))) ; trovato il delimitatore (
	 (subseq list (- (length acc) 1))) ; lo tengo
	((eql (length list) (length acc)) list) ; non trovato
	(T (consume-id44-helper ; caso ricorsivo
	    list
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))


(defun consume-id44 (list)
  (consume-id44-helper list NIL))

;;; in check-id8 alla fine avrei potuto ricontrollare anche il primo
;;; ma e' inutile avendo gia' fatto il controllo che sia alpha

(defun check-id8 (list)
  (and (listp list)
       (>= (length list) 1)
       (<= (length list) 8)
       (alpha-char-p (car list))
       (valid-id8-chars (subseq list 1))))

(defun check-zos-path (list u-struct)
  ;; id44 ['(' id8 ')']
  ;; id44 = (caratteri alfanumerici o '.')+
  ;; id8 = (caratteri alfanumerici)+
  ;; lunghezza di id44 tra 1 e 44, id8 tra 1 e 8
  ;; entrambi iniziano con un carattere alfabetico
  ;; id44 non termina con '.'
  (and (listp list)
       (>= (length list) 1)
       (let
	   ((sublist (consume-id44 list)))
	 (cond ((eql (length list) (length sublist))
		NIL) ; id44 non trovato
	       ((null sublist)
		(and (setf (uri-structure-path u-struct)
			   (chars-list-to-string list))
		     T)) ; solo id44, valido
	       (T
		(and (>= (length sublist) 3) ; '(' id8 ')'
		     (eql (car sublist) #\()
		     (eql (car (last sublist)) #\))
		     (check-id8
		      (subseq sublist 1 (- (length sublist) 1)))
		     (setf (uri-structure-path u-struct)
			   (chars-list-to-string list))
		     T))))))

(defun consume-zos-path-helper (list u-struct acc)
  ;; delimitatori possibili: ? oppure #
  (cond ((and
	  (or (eql (car (last acc)) #\?)
	      (eql (car (last acc)) #\#))
	  (check-zos-path (butlast acc) u-struct))
	 (subseq list (- (length acc) 1))) ; tengo il delimitatore
	((eql (length list) (length acc)) list) ; path non trovato
	(T (consume-zos-path-helper
	    list
	    u-struct
	    (append acc
		    (cons (nth
			   (length acc)
			   list)
			  NIL))))))

(defun consume-zos-path (list u-struct)
  (consume-zos-path-helper list u-struct NIL))


(defun consume-zos-p-q-f (list u-struct)
  (cond ((not (eql (car list) #\/)) list) ; non ho /
	(T (let
	       ((sublist (cdr list))) ; tolgo /
	     (cond ((check-zos-path sublist u-struct) NIL)
		   ;; solo zos_path, ho finito
		   (T (let
			  ((new-sublist (consume-zos-path sublist u-struct)))
			(cond ((eql (length sublist) (length new-sublist))
			       list) ; zos_path non trovato, non valido
			      ((and (eql (car new-sublist) #\?)
				    (check-query (cdr new-sublist)
						 u-struct))
			       NIL) ; solo query dopo zos_path, finito
			      ((and (eql (car new-sublist) #\#)
				    (check-fragment (cdr new-sublist)
						    u-struct))
			       NIL) ; stesso per fragment
			      (T (consume-fragment
				  (consume-query
				   new-sublist u-struct)
				  u-struct))))))))))

;;; funzione che converte una lista in stringa

(defun chars-list-to-string (list)
  (cond ((< (length list) 1) "")
	(T
	 (concatenate 'string (string (car list))
		      (chars-list-to-string (rest list))))))

;;; funzione che restituisce lo scheme (se trovato, come stringa)

(defun get-scheme (list u-struct)
  (cond ((and (listp list)
	      (>= (length list) 2))
	 (let* ; binding sequenziali
	     ((rest (consume-scheme list u-struct))
	      (scheme-length (- (length list) (+ 1 (length rest)))))
	   (cond ((< scheme-length 1) NIL)
		 (T (chars-list-to-string (subseq list 0 scheme-length))))))))

;;; funzione che prende lo scheme e gli associa un numero

(defun scheme-to-num (scheme)
  (cond ((equalp scheme "") -1)
	((equalp scheme "mailto") 1)
	((equalp scheme "news") 2)
	((or (equalp scheme "tel") (equalp scheme "fax")) 3)
	((equalp scheme "zos") 4)
	(T 0)))

;;; funzione che trova lo scheme con get-scheme e poi restituisce la
;;; rispettiva associazione numerica, spiegata in basso

(defun get-scheme-type (list u-struct)
  ;; -1 = scheme non trovato
  ;; 0 = URI1
  ;; 1 = mailto
  ;; 2 = news
  ;; 3 = tel o fax
  ;; 4 = zos
  (let
      ((scheme (get-scheme list u-struct)))
    (scheme-to-num scheme)))

;;; funzione che controlla un uri con scheme speciale

(defun check-uri-special (list u-struct scheme-type)
  (let
      ((sublist (consume-scheme list u-struct)))
    (cond ((null sublist) T) ; uri con solo scheme, valido
	  ((eql scheme-type 1) ; mailto:[userinfo[@host]]
	   (cond ((check-userinfo sublist u-struct) T) ; mailto:userinfo
		 (T ; mailto:userinfo@host
		  (check-host
		   (consume-userinfo sublist u-struct)
		   u-struct))))
	  ((eql scheme-type 2) ; news:[host]
	   (check-host sublist u-struct)) ; news:host
	  ((eql scheme-type 3) ; tel:[userinfo] (o fax, uguali)
	   (check-userinfo sublist u-struct)) ; tel:userinfo
	  ((eql scheme-type 4)
	   ;; stesso ragionamento di URI1 ma con il path di zos
	   (cond ((check-authority sublist u-struct) T)
		 ;; zos con solo authority, valido
		 (T (let
			((new-sublist (consume-authority sublist u-struct)))
		      ;; new-sublist con / e path_zos almeno
		      (null (consume-zos-p-q-f new-sublist u-struct)))))))))


;;; funzione che controlla un uri di tipo URI1
;;; restituisce T se e solo se la sottolista rimanente alla fine e'
;;; NIL. La chiamata finale (consume-p-q-f) e' per path query fragment

(defun check-uri (list u-struct)
  (and (listp list)
       (>= (length list) 2)
       (let
	   ((scheme-type (get-scheme-type list u-struct)))
	 (cond ((< scheme-type 0) NIL) ; scheme non trovato
	       ((> scheme-type 0) (check-uri-special
				   list
				   u-struct
				   scheme-type))
	       (T ; = 0 quindi URI1
		(let
		    ((sublist (consume-scheme list u-struct)))
		  ;; a questo punto lo scheme c'e' per forza
		  ;; altrimenti scheme-type darebbe -1
		  (cond ((null sublist) T) ; uri con solo scheme, valido.
			((check-authority sublist u-struct) T)
			;; uri con scheme e authority, ok
			(T (let
			       ((new-sublist (consume-authority
					      sublist
					      u-struct)))
			     ;; new-sublist e' con / iniziale
			     (null (consume-p-q-f
				    new-sublist
				    u-struct)))))))))))


;;; funzione che sostituisce tutte le occorrenze di " " con "%20"

(defun replace-space (uristring)
  (cond ((equal "" uristring) "") ; caso base
	((eql (car (coerce uristring 'list)) #\ ) ; oppure #\Space
	 (concatenate 'string
		      "%20"
		      (replace-space (subseq uristring 1))))
	(T ; non ho lo spazio come primo carattere
	 (concatenate 'string
		      (subseq uristring 0 1)
		      (replace-space
		       (subseq uristring 1))))))

;;; funzione richiesta che prende un URIString
;;; e restituisce una uri-structure riempita, altrimenti NIL

(defun uri-parse (uristring)
  (cond ((stringp uristring)
	 (let
	     ((chars (coerce (replace-space uristring) 'list))
	      (u-struct (make-uri-structure :port 80)))
	   ;; struttura con gli altri 6 campi inizialmente messi a NIL
	   ;; ma i 7 campi vengono settati correttamente
	   ;; da check-uri (che a sua volta controlla e setta ogni elemento)
	   (cond ((check-uri chars u-struct) u-struct)))))) ; uri valido


;;; funzione usata da uri-display perche'
;;; nella stampa concateno stringhe, ma port e' un integer quindi
;;; necessita di una conversione con write-to-string,
;;; mentre se ho gia' una stringa restituisco la stringa stessa
;;; e se ho un campo NIL restituisco "NIL"

(defun fix-field (field)
  (cond ((integerp field)
	 (write-to-string field))
	((stringp field) field)
	((null field) "NIL")))

;;; funzione richiesta che prende un uri-structure e (opzionale) uno stream
;;; se lo stream e' NIL verra' stampato su *standard-output*
;;; a differenza della versione Prolog, non vengono rimpiazzati gli spazi
;;; all'interno della struttura gia' riempita perche'
;;; viene dato per scontato che venga creata da uri-parse.

(defun uri-display (structure &optional stream)
  (cond ((and (uri-structure-p structure)
	      ;; controllo che structure sia un uri-structure
	      ;; usando uri-structure-p
	      (or (streamp stream)
		  ;; controllo che stream sia uno stream oppure NIL
		  (null stream)))
	 (let* ; variabili convertite in stringa
	     ((scheme (fix-field
		       (uri-scheme structure)))
	      (userinfo (fix-field
			 (uri-userinfo structure)))
	      (host (fix-field
		     (uri-host structure)))
	      (port (fix-field
		     (uri-port structure)))
	      (path (fix-field
		     (uri-path structure)))
	      (query (fix-field
		      (uri-query structure)))
	      (fragment (fix-field
			 (uri-fragment structure)))
	      (out (concatenate 'string ; output che viene stampato
				"Scheme:        " scheme
				(string #\Newline)
				"Userinfo:      " userinfo
				(string #\Newline)
				"Host:          " host
				(string #\Newline)
				"Port:          " port
				(string #\Newline)
				"Path:          " path
				(string #\Newline)
				"Query:         " query
				(string #\Newline)
				"Fragment:      " fragment)))
	   (and (write-line out stream)
		(or (finish-output stream) ; finish-output sarebbe la flush
		    T))))))
