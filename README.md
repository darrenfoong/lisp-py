# Lisp interpreter in Python

## Running

```
python -m main
lisp-py> load fac seq map foldl foldr mapf
lisp-py> (fac 10)
3628800
lisp-py> (seq 5)
(5 4 3 2 1)
lisp-py> (map fac (seq 5))
(120 24 6 2 1)
lisp-py> (foldl + 0 (map fac (seq 5)))
15
lisp-py> (foldr + 0 (map fac (seq 5)))
15
lisp-py> (mapf fac (seq 5))
(120 24 6 2 1)
```

## Notes

Code adapted from http://norvig.com/lispy.html
