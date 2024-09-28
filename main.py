import operator as op

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)


class String(str):
    pass


QUOTE = '"'


def lex(chars: str) -> list[str]:
    "Convert a string of characters into a list of tokens."
    # without support for strings, the implementation is easy:
    # return chars.replace("(", " ( ").replace(")", " ) ").split()
    tokens = []
    chars_split = chars.split(QUOTE)
    for i in range(0, len(chars_split)):
        if i % 2 == 0:  # not in a string
            tokens += chars_split[i].replace("(", " ( ").replace(")", " ) ").split()
        else:  # in a string
            tokens.append(f"{QUOTE}{chars_split[i]}{QUOTE}")

    return tokens


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


def eval(x, env=standard_env()):
    "Evaluate an expression in an environment."
    if isinstance(x, String):  # string
        return x
    elif isinstance(x, Symbol):  # variable reference
        return env.find(x)
    elif isinstance(x, List) and len(x) == 0:  # empty list
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
        if len(args) == 0:  # allow passing of func symbols as variables
            return x
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
