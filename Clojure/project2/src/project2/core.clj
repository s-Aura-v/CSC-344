(ns project2.core
  (:gen-class))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))


(if true
  "By Zeus's hammer!"
  "By Aquaman's trident!")


(if (true false)
  "By Zeus's hammer!"
  "By Aquaman's trident!")

(if (= "hello" "hello")
  "true"
  "false")

;; broken code? Why does it not return Chewbacca as name?
(def name "Chewbacca")
(str "\"Uggllglglglglglglglll\" - " @name)

;; doesn't work at all
(defn error-message
      [severity]
      (str "OH GOD! IT'S A DISASTER! WE'RE "
           (if (= severity :mild)
             "MILDLY INCONVENIENCED!"
             "DOOOOOOOMED!")))

(error-message :mild)
