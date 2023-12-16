(ns project2.core
  (:gen-class)
  ;(:use [set])
  (:require [clojure.set :as set]))

;---=== PART ONE ===---


;not-elimination method
(defn not-elimination [input]
  (if (= (first input) 'not)
    (let [sub-list (second input)]
      (if (list? sub-list)
        (if (= (first sub-list) 'not)
          (set [(second sub-list)])
          #{})
        #{}
        )
      )
    #{}
    )
  )


;and-elimination method
(defn and-elimination [proposition]
  (if (and (= (first proposition) 'and) (>= (count proposition) 3))
    (let [rest-prop (rest proposition)]
      #{rest-prop}
      )
    )
  )
;modus-ponens method
(defn modus-ponens1 [proposition kb]                        ;kb -> knowlegde base (what we know)
  ;from (if X Y) and X, infer Y
  ;Examples 1 and 3
  ; (println (first (rest proposition)))
  ;    (println kb)
  (if (= (first proposition) 'if)
    (if (= (second proposition) (first kb))
      ;(println (last proposition))
      (let [result (last proposition)]
        ;(println result)
        #{result}
        )
      )
    )
  )


(defn modus-ponens2 [proposition kb]
  ;from Y, infer (if X Y) and X
  ;Example 2
  (let [relevant-prop kb]
    ;(println relevant-prop)
    (let [relevant-kb proposition]
      ;(println relevant-kb)
      ;(println (first (first relevant-prop)))
      (if (= (first (first relevant-prop)) 'if)
        ;(println (second (first relevant-prop)))
        (if (= (second (first relevant-prop)) relevant-kb)
          ;(println (last (first relevant-prop)))
          (let [result (last (first relevant-prop))]
            ;(println result)
            #{result}
            )
          )
        )
      )


    )
  )

;modus-tollens method
(defn modus-tollens [proposition kb]                        ;modus tollens: from (if X Y) and (not Y), infer (not X)
  ;(println (first proposition))
  ;(println (second (first kb)))
  ;(println (second (rest proposition)))
  ;(println (conj (list (second proposition)) 'not))
  (if (= (first proposition) 'if)
    (if (= (second (first kb)) (second (rest proposition)))
      #{(conj (list (second proposition)) 'not)}
      )
    )
  )


;---=== Part 1 tests ===---
(def a (modus-ponens2 'a '#{(if a b) (if b c)}))   ; --> #{b}
(def b (modus-ponens1 '(if b c) '#{b}))     ; --> #{c}
(def c (and-elimination '(and a b)))     ; --> #{(a b)}
(def d (not-elimination '(not (not a))))   ; --> #{a}
(modus-tollens '(if a b) '#{(not b)})   ;--> #{not a}


;---=== PART TWO ===---


(defn elim-step [proposition kb]
  (let [new-stuff #{}]
    (cond
      (symbol? proposition)  ;'a '#{((if a b) (if b c))}

      (if (= (first (second kb)) proposition)     ;'a '#{((if a b) (if b c))}
        (= (first (first kb)) 'if)
        (let [newly-known (first (first kb))]
          (print "Because: ") (println (first (first kb)))
          (let [newly-known (conj newly-known proposition)]
            (print "And: ") (println proposition)
            ;(println (first proposition))
            ;(println (first kb))
            ;(println (modus-ponens2 (first proposition) (first kb)))
            (let [result (first (modus-ponens2 proposition (first kb)))]
              (print "I derived: ") (println result)
              (let [newly-known (conj newly-known result)]
                (println "By modus ponens")
                (print "=>") (println #{newly-known}) (println "")
                (set/union (list new-stuff) (list newly-known))
                newly-known
                )
              )
            )
          )
        )

      ;;modus tollens
      (and (= (first proposition) 'if) (= (first (first kb)) 'not) (set? kb))  ;'(if a b) '#{(not b)}
      (if (and (= (first proposition) 'if) (= (first (first kb)) 'not) (set? kb))
        (let [newly-known (list proposition)]
          (println "proposition")
          (print "Because: ") (println proposition)
          (let [newly-known (set/union newly-known kb)]
            (print "And: ") (println (flatten (into () kb)))
            (let [result (modus-tollens proposition kb)]
              (print "I derived: ") (println (flatten (into () result)))
              (let [newly-known (set/union newly-known result)]
                (println "By modus tollens")
                (print "=>") (println (into #{} newly-known)) (println "")
                (into #{} (set/union (new-stuff newly-known)))
                )
              )
            )
          )
        )

      ;not elimination
      (= (first proposition) 'not)
      (let [newly-known (list proposition)]
        (print "Because: ") (print proposition) (println "")
        (let [result (first (not-elimination proposition))]
          (print "I derived: ") (print result) (println "")
          (println "By not-elimination")
          (let [newly-known (set/union newly-known (list result))]
            (print "=>") (println #{newly-known}) (println "")
            (set/union new-stuff newly-known)
            )
          )
        )
      ;;and elimination
      (= (first proposition) 'and)
      (let [newly-known (list proposition)]
        (print "Because: ") (print proposition) (println "")
        (let [result (first (and-elimination proposition))]
          (let [last-part (last result)]
            (let [newly-known (conj newly-known last-part)]
              (conj newly-known last-part)
              (let [first-part (drop-last result)]
                (let [newly-known (set/union newly-known first-part)]
                  (set/union newly-known first-part)
                  (print "I derived: ") (print first-part) (println "")
                  (print "And: ") (print last-part) (println "")
                  (println "By and-elimination")
                  (print "=>") (println #{newly-known}) (println "")
                  (set/union new-stuff newly-known)
                  )
                )
              )
            )
          )
        )
      ;;modus-ponens
      (= (first proposition) 'if)   ;'(if a b) '#{a}
      (if (= (second proposition) (first kb))
        (let [newly-known (list proposition)]
          (print "Because: ") (println proposition)
          (let [newly-known (conj newly-known (first kb))]
            (print "And: ") (println (first kb))
            (let [result (first (modus-ponens1 proposition kb))]
              (print "I derived: ") (println result)
              (let [newly-known (conj newly-known result)]
                (println "By modus ponens")
                (print "=>") (println #{newly-known}) (println "")
                (set/union (list new-stuff) (list newly-known))
                newly-known
                )
              )
            )
          )
        )
      )
    )
  )


;---=== Part 2 tests ===---
;(println "")(println "---=== Elim Step Tests ===---")(println "")
;(println "Modus ponens 2")(println "")
;(def f (elim-step 'a '#{((if a b) (if b c))}))             ; --> #{b}
;(println "")(println "Modus ponens 1")(println "")
;(def g (elim-step '(if b c) '#{b}))                        ; --> #{c}
;(println "")(println "And Elimination")(println "")
;(def h (elim-step '(and (not (not (if a b))) a) '#{}))     ; --> #{(a b)}
;(println "")(println "Not Elimination")(println "")
;(def i (elim-step '(not (not a)) '#{}))                    ; --> #{a}
(println "")(println "Modus tollens")(println "")
(elim-step '(if a b) '#{(not b)})                 ;--> #{not a}


;---=== PART THREE ===---



