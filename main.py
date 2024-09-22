import math
import operator as op

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)


def tokenize(chars: str) -> list:
    "Convert a string of characters into a list of tokens."
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def parse(program: str) -> Exp:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list) -> Exp:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


class Env(dict):
    "An environment: a dict of {'var': val} pairs, with an outer Env."

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.params, args, self.env))


def standard_env() -> Env:
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "apply": lambda proc, args: proc(*args),
            "begin": lambda *x: x[-1],
            "head": lambda x: x[0], # originally car
            "tail": lambda x: x[1:], # originally cdr
            "cons": lambda x, y: [x] + y,
            "eq?": op.is_,
            "expt": pow,
            "equal?": op.eq,
            "length": len,
            "list": lambda *x: List(x),
            "list?": lambda x: isinstance(x, List),
            "map": map,
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, Number),
            "print": print,
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
        }
    )
    return env


global_env = standard_env()


def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):  # variable reference
        return env.find(x)[x]
    elif isinstance(x, List) and len(x) == 0: # empty list
        return x
    elif not isinstance(x, List):  # constant
        return x
    op, *args = x
    if op == "if":  # conditional
        (test, conseq, alt) = args
        exp = conseq if eval(test, env) else alt
        return eval(exp, env)
    elif op == "define":  # definition
        (symbol, exp) = args
        env[symbol] = eval(exp, env)
    elif op == "lambda":  # procedure
        (params, body) = args
        return Procedure(params, body, env)
    else:  # procedure call
        proc = eval(op, env)
        vals = [eval(arg, env) for arg in args]
        return proc(*vals)


def repl(prompt="lisp-py> "):
    "A prompt-read-eval-print loop."
    while True:
        try:
            input_str = input(prompt)

            if input_str.startswith("load"):
                input_str_split = input_str.split(" ")
                if len(input_str_split) != 2:
                    print("error: load requires a file path")
                    continue
                with open(f"{input_str_split[1]}.lisp", "r") as f:
                    input_str = f.read()

            val = eval(parse(input_str))
            if val is not None:
                print(schemestr(val))
        except KeyboardInterrupt:
            print("\nBye")
            return
        except Exception as e:
            print(e)


def schemestr(exp):
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, List):
        return "(" + " ".join(map(schemestr, exp)) + ")"
    else:
        return str(exp)


if __name__ == "__main__":
    repl()
