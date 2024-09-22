(define map
  (lambda (f xs)
    (if
      (equal? xs ())
      ()
      (cons (f (head xs)) (map f (tail xs)))
    )
  )
)
