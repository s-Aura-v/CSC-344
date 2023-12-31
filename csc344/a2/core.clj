(ns project2.core
  (:require [clojure.string :as str])
  (:gen-class))

;; Not Elimination
(defn not-elimination
  "Eliminate double-nots from a function of nots"
  [expr]
  (if (and (= 'not (first expr))
           (list? (second expr)) (= 'not (first (second expr))))
    ;; check if there are 2 nots
    #{(second (second expr))}
    ;; if not, check if there is not is present at all
    (if (= 'not (first expr))
      ;;return nothing if there is a not
      #{}
      ;;return the expression if there are no nots
      #{(first expr)})))

;; Tests
(not-elimination '(a))
(not-elimination '(not a))
(not-elimination '(not (not a)))
(not-elimination '(not (not (and a b))))
(not-elimination '(not (not (not (not c)))))

;; and-elimination
(defn and-elimination
  "Return a vector of {a,b} if A and B"
  [and-prop]
  (if (= 'and (first and-prop))
    #{(second and-prop) (nth and-prop 2)}
    "Not an and-statement"))

;; Tests
(and-elimination '(and a b))
(and-elimination '(and (not (not (if a b))) a))

;; modus ponens2 from (if X Y) and X, infer Y
(defn modus-ponens2
  "Infer x from if (X Y) and X"
  [if-prop kb]
  (if (not (symbol? if-prop))
    ;;true
    (if (= (second if-prop) (first kb))
      #{(nth if-prop 2)}
      #{(nth if-prop 1)})
    ;;false
    (if (= if-prop (second kb))
      #{(nth kb 2)}
      #{(nth kb 1)})))

;; Tests
(modus-ponens2 '(if A B) '#{A})
(modus-ponens2 '(if a b) '#{a})
(modus-ponens2 '(if A B) '#{B})
;; Backwards tests
(modus-ponens2 'a '(if a b))
(modus-ponens2 'b '(if b c))

;; modus tollens: from (if X Y) and (not Y), infer (not X)
(defn modus-tollens
  "Evaluate (not A) from if (A B) and (not B)"
  [if-prop kb]
  (if (= (second if-prop) (second (first kb)))
    (set [(list 'not (nth if-prop 2))])
    (set [(list 'not (second if-prop))])))

;; Tests
(modus-tollens '(if A B) '#{(not A)})
(modus-tollens '(if A B) '#{(not B)})

;; Relevant-kb for modus-ponens2
(defn relevant-kb
  "Do the required relevant-kb"
  [ant kb]
  (for [prop kb :when (and (seq? prop) (= (second prop) ant))] prop))
;; tests
(relevant-kb 'b '#{(if a b) (if b c)})
(relevant-kb 'a '#{(if a b) (if b c)})

;; Elim-step
(defn elim-step1
  "One step of the elimination inference procedure."
  [prop kb]
  ;; Not elimination
  (if (not (symbol? prop)) ;; if prop is a not symbol
    ;; if true
    (if (and (list? prop) (= 'not (first prop)))
      (clojure.set/union kb (not-elimination prop))
      ;; and-elimination
      (if (and (list? prop) (= 'and (first prop)))
        (clojure.set/union kb (and-elimination prop))
        ;; if X Y and X infer Y
        (if (and (list? prop) (= 'if (first prop)) (list? (first kb)))
          ;; if it has a not, do tollens
          (clojure.set/union kb (modus-tollens prop kb))
          ;; if not, do ponens
          (clojure.set/union kb (modus-ponens2 prop kb)))))
    ;; if false
    (clojure.set/union
     (modus-ponens2 prop (first (relevant-kb prop kb)))
     (modus-ponens2 'b (first (relevant-kb 'b kb))))))

;; Infer fwd
(defn fwd-infer
  "Make logical inferences based on propositions"
  [prop known]
  (loop [current-prop #{prop}
         current-known known]
    (if (empty? current-prop)
      current-known
      (let [new-known (elim-step1 (first current-prop) current-known)]
        (recur (rest current-prop)
               (if (not (empty? known))
                 (clojure.set/union current-prop current-known new-known)
                 (clojure.set/union (elim-step1 prop known)
                                    (elim-step1 (second prop) '#{})
                                    #{prop}
                                    (elim-step1 (second (second (second prop))) #{(last prop)}))))))))

(last '(and (not (not (if a b))) a))

;; Tests
(fwd-infer '(if a b) '#{(not b)})
;; #{(if a b) (not a) (not b)}
(fwd-infer 'a '#{(if a b) (if b c)})
;; {(if a b) a c (if b c) b}
(fwd-infer '(and (not (not (if a b))) a) '#{})
;; #{(if a b) (not (not (if a b))) a (and (not (not (if a b))) a) b}


