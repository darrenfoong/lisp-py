(define map
  (lambda (f xs)
    (if
      (equal? xs ())
      ()
      (cons (f (car xs)) (map f (cdr xs)))
    )
  )
)
