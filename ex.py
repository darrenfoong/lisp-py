import operator as op


class Symbol(str):
    pass


String = str
Number = (int, float)
Atom = (Symbol, String, Number)
List = list
Exp = (Atom, List)


QUOTE = '"'


def lex(chars: str) -> list[str]:
    "Convert a string of characters into a list of tokens."
    # Exercise 3: handle strings with spaces
    # Example: (tail "hello world")
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def parse(tokens: list[str]) -> Exp:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(parse(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol or string."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            if token.startswith(QUOTE) and token.endswith(QUOTE):
                return String(token[1:-1])
            else:
                return Symbol(token)


class Env(dict):
    "An environment: a dict of {'var': val} pairs, with an outer Env."

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        "Find var in the innermost Env where it appears."
        if var in self:
            return self[var]
        else:
            # Exercise 2: raise a RuntimeError if variable does not exist
            # Example: (what)
            return self.outer.find(var)


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return eval(self.body, Env(self.params, args, self.env))


def standard_env() -> Env:
    env = Env()
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
            "append": op.add,
            "begin": lambda *x: x[-1],
            "head": lambda x: x[0],  # originally car
            "tail": lambda x: x[1:],  # originally cdr
            "cons": lambda x, y: [x] + y,
            "list": lambda *x: List(x),
            "number": atom,  # abused to cast strings to numbers
        }
    )
    return env


global_env = standard_env()


def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):  # variable reference
        return env.find(x)
    elif isinstance(x, String):  # string
        return x
    # Exercise 1: handle empty lists
    # Example: (tail ())
    elif not isinstance(x, List):  # constant
        return x
    op, *args = x  # otherwise a list
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


def repl(prompt="lisp-py-ex> "):
    "A prompt-read-eval-print loop."
    while True:
        try:
            input_str = input(prompt)

            if input_str.startswith("load"):
                input_str_split = input_str.split(" ")
                if len(input_str_split) < 2:
                    print("error: load requires a file path")
                    continue
                for i in range(1, len(input_str_split)):
                    with open(f"{input_str_split[i]}.lisp", "r") as f:
                        blocks = f.read().split("---")
                        for block in blocks:
                            val = eval(parse(lex(block)))
                            if val is not None:
                                print(scheme_str(val))
            else:
                val = eval(parse(lex(input_str)))
                if val is not None:
                    print(scheme_str(val))
        except KeyboardInterrupt:
            print("\nBye")
            return
        except Exception as e:
            print(e)


def scheme_str(exp) -> str:
    "Convert a Python object back into a Scheme-readable string."
    if isinstance(exp, List):
        return "(" + " ".join(map(scheme_str, exp)) + ")"
    elif isinstance(exp, String):
        return f'"{exp}"'
    else:
        return str(exp)


if __name__ == "__main__":
    repl()
