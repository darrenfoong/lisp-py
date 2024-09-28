(define len
  (lambda (xs)
    (if
      (equal? xs ())
      0
      (+ 1 (len (tail xs)))
    )
  )
)
---
(define fac
  (lambda (n)
    (if
      (<= n 1)
      1
      (* n (fac (- n 1)))
    )
  )
)
---
(define fib
  (lambda (n)
    (if
      (< n 2)
      1
      (+ (fib (- n 1)) (fib (- n 2)))
    )
  )
)
---
(define seq
   (lambda (n)
     (if
       (equal? n 0)
       ()
       (cons n (seq (- n 1)))
     )
   )
)
