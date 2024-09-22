(define seq
   (lambda (n)
     (if
       (equal? n 0)
       ()
       (cons n (seq (- n 1)))
     )
   )
)
