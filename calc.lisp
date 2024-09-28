(define lexinner
  (lambda (token chars)
    (if
      (equal? chars "")
      (list token)
      (if
        (equal? (head chars) " ")
        (cons token (lexinner "" (tail chars)))
        (lexinner (append (head chars) token) (tail chars))
      )
    )
  )
)
---
(define lex
  (lambda (chars)
    (map revs (lexinner "" chars))
  )
)
