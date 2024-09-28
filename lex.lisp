(define lex
  (lambda (chars)
    (map revs (lexinner "" chars))
  )
)
