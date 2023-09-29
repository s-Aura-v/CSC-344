(ns project2.core
  (:require [clojure.string :as str])
  (:gen-class))
(defn not-elimination
  "Eliminate double-nots from a function of nots"
  [expr]
  (if
    (and  (list? expr) (= 'not (first expr))
          (list? (second expr)) (= 'not (first (second expr))))
    ;; check if there are 2 nots
    (second (second expr))
    ;; if not, check if there is not is present at all
    (if (= 'not (first expr))
      ;;return nothing if there is a not
      ()
      ;;return the expression if there are no nots
      expr)
    ))

;; Tests
(not-elimination '(a))
(not-elimination '(not a))
(not-elimination '(not (not a)))
(not-elimination '(not (not (and a b))))
(not-elimination '(not (not (not (not c)))))
