(define map
  (lambda (f xs)
    (if
      (= xs ())
      ()
      (cons (f (head xs)) (map f (tail xs)))
    )
  )
)
---
(define foldl
  (lambda (f e xs)
    (if
      (= xs ())
      e
      (foldl f (f e (head xs)) (tail xs)))
    )
  )
)
---
(define foldr
  (lambda (f e xs)
    (if
      (= xs ())
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
      (= xs "")
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
