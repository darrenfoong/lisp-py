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
