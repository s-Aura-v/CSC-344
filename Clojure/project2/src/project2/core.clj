(ns project2.core
  (:require [clojure.string :as str])
  (:gen-class))


;;How to do not not elimination
;;1. If 2<= nots, remove 2 nots and return the remaining value
;;2. if 1 not, then return empty string

;(defn isItNot?
;  "Determine if value is not"
;  )
(defn not-count
  "Count how many times a word appears"
  [string]
  (count (re-seq #"not" string)))

(defn not-elimination
  "Take a function and clarify its double negatives"
  [not-expr]
  (if (str/includes? [not-expr] "not" )
       "Has not"
       "Not has not"
    ))

(not-elimination "(not (not x))")
(not-count "(not (not x))")
(not-count `(not (not x)))


(if (str/includes? "(not x)" "not" )
  "Has not"
  "Does not have not")


