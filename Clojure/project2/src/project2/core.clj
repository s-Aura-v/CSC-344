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
    #{(second and-prop) (nth and-prop 2)}
    "Not an and-statement"
    ))

;;Tests
(and-elimination '(and a b))
(and-elimination '(and (not (not (if a b))) a))

;;modus ponens: from (if X Y) and X, infer Y

(defn modus-ponens
  "Infer x from if (X Y) and X"
  [if-prop]
  (if  (= (second (first if-prop)) (nth if-prop 2))
    ;;if first input is equal to given variable
    #{(second (first if-prop))}
    ;;else if second input is equal to given variable
    (if (= (nth (first if-prop) 2) (nth if-prop 2))
      #{(nth (first if-prop) 2)}
      #{()}
     )))

;;Tests
(modus-ponens '((if A B) and A))
(modus-ponens '((if A B) and B))
(modus-ponens '((if A B) and C))


;;;modus tollens: from (if X Y) and (not Y), infer (not X)

(defn modus-tollens
  "Evaluate (not A) from if (A B) and (not B)"
  [if-prop]
  (if  (= (second (first if-prop)) (last (nth if-prop 2)))
    (set ['not (nth (first if-prop) 2)])
    ;;Remember to check if its even there
    (set ['not (second (first if-prop))])
    )
  )

;;Tests
(modus-tollens '((if A B) and (not A)))
(modus-tollens '((if A B) and (not B)))


;Elim-step

(defn elim-step
  "One step of the elimination inference procedure."
  [prop]
  ;;Not elimination
  (if (and (list? prop) (= 'not (first prop)))
    (not-elimination prop)
    ;;and-elimination
    (if (and (list? prop) (= 'and (first prop)))
      (and-elimination prop)
      ;;if X Y and X infer Y
      (if (and (list? prop) (= 'if (first prop)) (list? (last prop)) ())
        ;; if it's a list, do tollens
        (modus-tollens prop)
        ;;if not, do ponens
        (modus-ponens prop)
        )
      )
    )
  )

;;Tests
(def testF '(and (not (not if (a b))) a))
(elim-step testF)

;;Infer-fwd

(defn fwd-infer
  "Make logical inferences based on propositions"
  [prop known]
  (loop [ prop known]
    if (empty? prop)
    (concat prop )
  )



(empty? '(1 2 3))
(empty? ())


;;Tests
(fwd-infer '(if a b) '#{(not b)})
(fwd-infer 'a '#{(if a b) (if b c)})
(fwd-infer-elim '(and (not (not (if a b))) a) '#{})


