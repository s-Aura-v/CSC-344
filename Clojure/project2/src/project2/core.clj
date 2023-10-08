(ns project2.core
  (:require [clojure.string :as str])
  (:gen-class))

;;Not Elimination

(defn not-elimination
  "Eliminate double-nots from a function of nots"
  [expr]
  (if
    (and (= 'not (first expr))
         (list? (second expr)) (= 'not (first (second expr))))
    ;; check if there are 2 nots
    #{(second (second expr))}
    ;; if not, check if there is not is present at all
    (if (= 'not (first expr))
      ;;return nothing if there is a not
      #{()}
      ;;return the expression if there are no nots
      #{expr})
    ))

;; Tests
(not-elimination '(a))
(not-elimination '(not a))
(not-elimination '(not (not a)))
(not-elimination '(not (not (and a b))))
(not-elimination '(not (not (not (not c)))))


;;and-elimination

(defn and-elimination
  "Return a vector of {a,b} if A and B"
  [and-prop]
  (if (= 'and (first and-prop))
    #{(list (second and-prop) (nth and-prop 2))}
    "Not an and-statement"
    ))

;;Tests
(and-elimination '(and a b))
(and-elimination '(and (not (not (if a b))) a))

;;modus ponens: from (if X Y) and X, infer Y


(defn modus-ponens
  "Infer x from if (X Y) and X"
  [if-prop kb]
  (let [if-prop-list (first (seq if-prop))
        kb-list (first (seq kb))]
    (if (= (first kb-list) (second if-prop-list))
      #{(list (nth if-prop-list 1))}
      #{(list (nth if-prop-list 2))})))

;;Tests
(modus-ponens '#{(if A B)} '#{(A)})
(modus-ponens '#{(if A B)} '#{(B)})


;;modus tollens: from (if X Y) and (not Y), infer (not X)

(defn modus-tollens
  "Evaluate (not A) from if (A B) and (not B)"
  [if-prop kb]
  (if (= (second if-prop) (second (first kb)))
    (set [(list 'not (nth if-prop 2))])
    (set [(list 'not (second if-prop))])
    ))

;;Tests
(modus-tollens '(if A B) '#{(not A)})
(modus-tollens '(if A B) '#{(not B)})


;Elim-step

(defn elim-step
  "One step of the elimination inference procedure."
  [prop kb]
  ;;Not elimination
  (if (and (list? prop) (= 'not (first prop)))
    (not-elimination prop)
    ;;and-elimination
    (if (and (list? prop) (= 'and (first prop)))
      (and-elimination prop)
      ;;if X Y and X infer Y
      (if (and (list? prop) (= 'if (first prop)) (= 'not (first (first kb))) ())
        ;; if it has a not, do tollens
        (modus-tollens prop kb)
        ;;if not, do ponens
        (modus-ponens prop kb)
        )
      )
    )
  )

;;Tests
(elim-step '(not (not (and a b))) #{})
(elim-step '(and (not (not (if a b))) a) #{})
(elim-step '#{(if A B)} '#{(A)})
(elim-step '(if A B) '#{(not A)})

;;Infer fwd
(defn fwd-infer
  "Make logical inferences based on propositions"
  [prop known]
  (loop [prop prop
         known known]
    (if (empty? prop)
      known
      (let [new-known (elim-step (first prop) known)]
        (recur (rest prop) (clojure.set/union known new-known))))))


;;Tests
(fwd-infer '#{(if a b)} '#{(not b)})
;;#{(if a b) (not a) (not b)}
(fwd-infer '#{(and (not (not (if a b))) a)} '#{})
;; #{(if a b) (not (not (if a b))) a (and (not (not (if a b))) a) b}
