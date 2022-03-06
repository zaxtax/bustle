import torch
from stringprops import props_str, props_int, props_str2str, props_int2str

from model import Rater

def ArithDsl():
    Ops = ["add", "mul", "div", "neg", "lt", "if"]
    Types = ["int", "bool"]

    def execute(op, args):
        if op == "add":
            return args[0] + args[1]
        elif op == "mul":
            return args[0] * args[1]
        elif op == "div":
            return args[0] / args[1]
        elif op == "neg":
            return -args[0]
        elif op == "lt":
            return args[0] < args[1]
        elif op == "if":
            return args[1] if args[0] else args[2]
        else:
            assert False

    def types(op):
        if op in ["neg"]:
            return ("int", ("int",))
        elif op in ["add", "mul", "div"]:
            return ("int", ("int", "int"))
        elif op in ["lt"]:
            return ("bool", ("int", "int"))
        elif op in ["if"]:
            return ("int", ("bool", "int", "int"))
        else:
            assert False

    def extractConstants(I, O, It, Ot):
        cs = [0, 1]
        return [("int", (c, [c for _ in range(len(O))])) for c in cs]

    return Dsl(Ops, Types, execute, types, extractConstants)


class Dsl:
    def __init__(self, Ops, Types, execute, types, extractConstants):
        self.Ops = Ops
        self.Types = Types
        self.execute = execute
        self.types = types
        self.extractConstants = extractConstants

    def arity(self, op):
        return len(self.argtypes(op))

    def argtypes(self, op):
        _, ts = self.types(op)
        return ts

    def returntype(self, op):
        t, _ = self.types(op)
        return t


def executeV(dsl, op, args):
    arg_exps = [e for e, x in args]
    arg_vals = [x for e, x in args]
    x = []
    for op_args in zip(*arg_vals):
        a = dsl.execute(op, op_args)
        x = x + [a]
    e = (op, arg_exps)
    return (e, x)


def all_args(n, ts, E, w):
    if n == 1:
        r = [[a] for a in E[w][ts[0]]]
    else:
        r = [
            [a] + b
            for w1 in range(1, w - n + 2)
            for b in all_args(n - 1, ts[1:], E, w - w1)
            for a in E[w1][ts[0]]
        ]
    return r


def all_args_for(dsl, op, E, w):
    return all_args(dsl.arity(op), dsl.argtypes(op), E, w)


def sameV(V1, V2):
    return V1[1] == V2[1]


def sameO(V, O):
    return V[1] == O


def containsV(V, E, t):
    for En in E.values():
        for X in En[t]:
            if sameV(V, X):
                return True
    return False


def value(V):
    return V[1]


def expression(X):
    return X[0]


def empty_e(ts):
    En = {}
    for t in ts:
        En[t] = []
    return En


def inputVs(I, It):
    return [(It[i], (("input", i), I[i])) for i in range(len(I))]


def initialVs(dsl, I, O, It, Ot):
    E1 = empty_e(dsl.Types)
    for (t, v) in dsl.extractConstants(I, O, It, Ot) + inputVs(I, It):
        E1[t] = E1[t] + [v]
    return E1


# The Bustle Synthesis Algorithm (without ML for now)
# Input: Input-output examples (I,O)
# Output: A program P consistent with the examples (I, O)
# Auxiliary Data:
#   a DSL with supported operations
#   type signature typeSig
#   property list of typed lists of functions llProps
#   models Ms, a dictionary keyed by types of (input, output, intermediary)
def bustle(dsl, typeSig, I, O, llProps=None, Ms=None):
    Ot, It = typeSig
    E = {}
    E[1] = initialVs(dsl, I, O, It, Ot)

    # edge cases (not in paper)
    for V in E[1][Ot]:
        if sameO(V, O):
            return expression(V)

    s_io = propertySignature(I, It, O, Ot, llProps)

    for w in range(2, 10):
        E[w] = empty_e(dsl.Types)
        for op in dsl.Ops:
            t = dsl.returntype(op)
            for args in all_args_for(dsl, op, E, w - 1):
                try:
                    V = executeV(dsl, op, args)
                    Vt = dsl.types(op)[0]
                except:
                    # ignore expressions that cause errors
                    continue
                if not containsV(V, E, t):
                    wp = w
                    s_vo = propertySignature([value(V)], [Vt], O, Ot, llProps)
                    wp = reweightWithModel(Ms, It, Ot, Vt, s_io, s_vo, w)
                    addE(dsl, E, wp, t, V)
                if t == Ot and sameO(V, O):
                    return expression(V)
    return E  # for debugging

def addE(dsl, E, w, t, V):
    if w not in E:
        E[w] = empty_e(dsl.Types)
    E[w][t] = E[w][t] + [V]


def evaluateProperty(I, prop):
    all_false = -1
    all_true = 1
    mixed = 0

    tests = torch.tensor([prop(*i) for i in I])
    if torch.all(tests):
        return all_true
    elif torch.all(tests == False):
        return all_false
    else:
        return mixed

def propertySignatureSize(It, Ot, llProps):
    size = 0
    # FIXME: Only handle single input for now
    It = It[0]
    for typs, props in llProps:
        if len(typs) == 1:
            if typs[0] == It:
                size += len(props)
            if typs[0] == Ot:
                size += len(props)
        elif len(typs) == 2:
            if typs[0] == It and typs[1] == Ot:
                size += len(props)
    return size

def propertySignature(I, It, O, Ot, llProps):
    propSig = []
    if llProps is None:
        return None

    # FIXME: Only handle single input for now
    I = I[0]
    It = It[0]

    for typs, props in llProps:
        if len(typs) == 1:
            if typs[0] == It:
                _I = [[i] for i in I]
                for p in props:
                    sig = evaluateProperty(_I, p)
                    propSig.append(sig)
            if typs[0] == Ot:
                _O = [[o] for o in O]
                for p in props:
                    sig = evaluateProperty(_O, p)
                    propSig.append(sig)
        elif len(typs) == 2:
            if typs[0] == It and typs[1] == Ot:
                for p in props:
                    sig = evaluateProperty(zip(I, O), p)
                    propSig.append(sig)
    return torch.tensor(propSig).float()

def discrete_prediction(w, p):
    if p < 0.1:
        d = 0
    elif p < 0.2:
        d = 1
    elif p < 0.3:
        d = 2
    elif p < 0.4:
        d = 3
    elif p < 0.6:
        d = 4
    else:
        d = 5
    return w + 5 - d

def reweightWithModel(Ms, It, Ot, Vt, s_io, s_vo, w):
    if Ms is None or s_io is None or s_vo is None:
        return w + 5

    wp = w
    if Ms:
        key = (It, Ot, Vt)
        M = Ms.get(key)
        if M is not None:
            c = torch.cat([s_io, s_vo])
            wp = discrete_prediction(w, M(c))
        # else:
        #     assert False, "missing model for "+str(key)

    return wp  # TODO


def test():
    al = ArithDsl()
    llProps = [props_str, props_int, props_str2str, props_int2str]
    llProps = [
        (("int",), [lambda inp: inp % 2 == 0]),
        (("bool",), [lambda b: b]),
        (
            ("int", "int"),
            [lambda inp, oup: inp - oup > 0, lambda inp, oup: abs(inp - oup) <= 1],
        ),
        (("bool", "int"), [lambda b, oup: (oup % 2 == 0) == b]),
    ]
    Ms = {(('int',), 'int', 'int'): Rater(
        2*propertySignatureSize(('int',), 'int', llProps)
    )}

    int2 = ("int", ("int",))
    int3 = ("int", ("int", "int"))
    assert 1 == bustle(al, int2, [[1, 2, 3]], [1, 1, 1], llProps, Ms)
    assert ("input", 0) == bustle(al, int2, [[1, 2, 3]], [1, 2, 3], llProps, Ms)
    assert ("add", [("input", 0), 1]) == bustle(
        al, int2, [[1, 2, 3]], [2, 3, 4], llProps, Ms
    )
    assert ("neg", [("input", 0)]) == bustle(
        al, int2, [[1, 2, 3]], [-1, -2, -3], llProps, Ms
    )
    assert ("add", [("input", 0), ("neg", [1])]) == bustle(
        al, int2, [[1, 2, 3]], [0, 1, 2], llProps, Ms
    )
    assert ("if", [("lt", [("input", 0), ("input", 1)]), 1, 0]) == bustle(
        al, int3, [[1, 2, 3], [3, 1, 2]], [1, 0, 0]
    )


if __name__ == "__main__":
    print("running tests...")
    test()
    print("done")
