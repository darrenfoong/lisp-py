(define foldls
  (lambda (f e xs)
    (if
      (equal? xs "")
      e
      (foldls f (f e (head xs)) (tail xs)))
    )
  )
)
