(define map
  (lambda (f xs)
    (if
      (equal? xs ())
      ()
      (cons (f (head xs)) (map f (tail xs)))
    )
  )
)
---
(define foldl
  (lambda (f e xs)
    (if
      (equal? xs ())
      e
      (foldl f (f e (head xs)) (tail xs)))
    )
  )
)
---
(define foldr
  (lambda (f e xs)
    (if
      (equal? xs ())
      e
      (f (head xs) (foldr f e (tail xs)))
    )
  )
)
---
(define mapf
  (lambda (f xs)
    (foldr
      (lambda (x e)
        (cons (f x) e)
      )
      ()
      xs
    )
  )
)
---
(define rev
  (lambda (xs)
    (foldl
      (lambda (e x)
        (cons x e)
      )
      ()
      xs
    )
  )
)
---
(define foldls
  (lambda (f e xs)
    (if
      (equal? xs "")
      e
      (foldls f (f e (head xs)) (tail xs)))
    )
  )
)
---
(define revs
  (lambda (xs)
    (foldls
      (lambda (e x)
        (append x e)
      )
      ""
      xs
    )
  )
)
