(ns project2.core
  (:require [clojure.string :as str])
  (:gen-class))


;;How to do not not elimination
;;1. If 2<= nots, remove 2 nots and return the remaining value
;;2. if 1 not, then return empty string

;(defn isItNot?
;  "Determine if value is not"
;  )

;;Tests
(def string '(not (not (not (x)))))
(first string)
(last string)
(next string)
(first (next string))
(reduce 'not string)
(first (reduce 'not string))
(reduce 'not string)

(defn not-elimination
  "Eliminate double-nots from a function of nots "
  [expr]
  (if (and (= 'not (first expr)) (= 'not (first (reduce 'not expr))))
    ;;if there are more than two not expressions
    (reduce 'not (reduce 'not expr))
    ;; Add to true an expression that results in the values after the first string
    ()
    ;; Add to false an null expression
    ))

(defn not-elimination2
  "Eliminate double-nots from a function of nots "
  [expr]
  (if (and (= 'not (first string)) (= 'not (first (reduce 'not string))))
    ;;if there are more than two not expressions
    (reduce 'not (reduce 'not string))
    ;; Add to true an expression that results in the values after the first string
    {}
    ;; Add to false an null expression
  ))

(defn not-elimination3
  "Eliminate double-nots from a function of nots"
  [expr]
  (if
    (and (= 'not (first expr)) (= 'not (first (second expr))))
    ;; If there are two consecutive 'not' expressions, return the inner expression.
    (second (second expr))

    ()
    ;; If not, return the original expression.
    expr))


;; Tests
(not-elimination string)
(not-elimination '(not x))
(not-elimination '(a))
(not-elimination3 '(not (not a)))
(not-elimination3 '(not (not (and a b))))
(not-elimination3 '(not (not (not (not c)))))


(if (str/includes? "(not x)" "not" )
  "Has not"
  "Does not have not")


