(define foldl
  (lambda (f e xs)
    (if
      (equal? xs ())
      e
      (foldl f (f e (head xs)) (tail xs)))
    )
  )
)
