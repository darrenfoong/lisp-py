(define fac
  (lambda (n)
    (if
      (<= n 1)
      1
      (* n (fac (- n 1)))
    )
  )
)
