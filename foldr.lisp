(define foldr
  (lambda (f e xs)
    (if
      (equal? xs ())
      e
      (f (head xs) (foldr f e (tail xs)))
    )
  )
)
