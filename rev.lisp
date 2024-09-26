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
