# Lisp interpreter in Python

## Running

```
python -m main
lisp-py> load fac
lisp-py> (fac 10)
3628800
lisp-py> load seq
lisp-py> (seq 5)
(5 4 3 2 1)
lisp-py> load map
lisp-py> (map fac (seq 5))
(120 24 6 2 1)
lisp-py> load foldl
lisp-py> load foldr
lisp-py> (define add (lambda (a b) (+ a b)))
lisp-py> (foldl add 0 (map fac (seq 5)))
15
lisp-py> (foldr add 0 (map fac (seq 5)))
15
lisp-py> load mapf
lisp-py> (mapf fac (seq 5))
(120 24 6 2 1)
```

## Notes

Code adapted from http://norvig.com/lispy.html
