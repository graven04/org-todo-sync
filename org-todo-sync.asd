;;;; org-todo-sync.asd

(defsystem "org-todo-sync"
  :description "Describe org-todo-sync here"
  :author "Rajesh Gaire"
  :license  "Specify license here"
;;  :depends-on ()
  :components  ((:module "src"
            :components
	    ((:file "package")
	     (:file "org-todo-sync")
	     )))
  :serial t
)
