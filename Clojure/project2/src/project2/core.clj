(ns project2.core
  (:require [clojure.string :as str])
  (:gen-class))
(defn not-elimination
  "Eliminate double-nots from a function of nots"
  [expr]
  (if
    (and (= 'not (first expr)) (= 'not (first (second expr))))
    ;; If there are two consecutive 'not' expressions, return the inner expression.
    (second (second expr))
    ;; If not, return the original expression.
    (do (if (= 'not (first expr))
          ()
          ;; if false, return expr
          expr))))

;; Tests
(not-elimination '(not a))
(not-elimination '(not (not a)))
(not-elimination '(not (not (and a b))))
(not-elimination '(not (not (not (not c)))))
