# Lisp interpreter in Python

## Running

```
python -m main
lisp-py> (+ 1 1)
2
lisp-py> (begin (define a 2) (define b 3) (* a b))
6
lisp-py> (define xs (list 1 2 3))
lisp-py> (head xs)
1
lisp-py> (tail xs)
(2 3)
lisp-py> load examples
lisp-py> (len (list 1 2 3))
3
lisp-py> (fac 5)
120
lisp-py> (fib 5)
8
lisp-py> (seq 5)
(5 4 3 2 1)
lisp-py> load utils
lisp-py> (map fac (seq 5))
(120 24 6 2 1)
lisp-py> (foldl + 0 (map fac (seq 5)))
153
lisp-py> (foldr + 0 (map fac (seq 5)))
153
lisp-py> (mapf fac (seq 5))
(120 24 6 2 1)
lisp-py> (rev (seq 5))
(1 2 3 4 5)
lisp-py> (revs "hello")
olleh
lisp-py> load calc
lisp-py> (calc "1 + 1")
2
lisp-py> (calc "1 - 1")
0
lisp-py> (calc "4 * 2")
8
lisp-py> (calc "4 / 2")
2.0
```

## Notes

Code adapted from http://norvig.com/lispy.html
