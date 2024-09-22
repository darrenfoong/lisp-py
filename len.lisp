(define len
  (lambda (xs)
    (if
      (equal? xs ())
      0
      (+ 1 (len (tail xs)))
    )
  )
)
