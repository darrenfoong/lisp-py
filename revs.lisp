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
