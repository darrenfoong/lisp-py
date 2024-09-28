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
---
(define parse
  (lambda (tokens)
    (list
      (head (tail tokens))
      (number (head tokens))
      (number (head (rev tokens)))
    )
  )
)
---
(define eval
  (lambda (exp)
    (if (equal? (head exp) "+")
      (+ (head (tail exp)) (head (rev exp)))
      (if (equal? (head exp) "-")
        (- (head (tail exp)) (head (rev exp)))
        (if (equal? (head exp) "*")
          (* (head (tail exp)) (head (rev exp)))
          (if (equal? (head exp) "/")
            (/ (head (tail exp)) (head (rev exp)))
            ("oops")
          )
        )
      )
    )
  )
)
---
(define calc
  (lambda (input_str)
    (eval
      (parse
        (lex input_str)
      )
    )
  )
)
