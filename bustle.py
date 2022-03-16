import torch

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
        r = [[a] for a in getE(E, w, ts[0])]
    else:
        r = [
            [a] + b
            for w1 in range(1, w - n + 2)
            for b in all_args(n - 1, ts[1:], E, w - w1)
            for a in getE(E, w1, ts[0])
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


def getE(E, w, t):
    return E.get(w, {}).get(t, [])


def set_empty_e_if_none(dsl, E, w):
    if w not in E:
        E[w] = empty_e(dsl.Types)


def inputVs(I, It):
    return [(It[i], (("input", i), I[i])) for i in range(len(I))]


def initialVs(dsl, I, O, It, Ot):
    return dsl.extractConstants(I, O, It, Ot) + inputVs(I, It)


# The Bustle Synthesis Algorithm (without ML for now)
# Input: Input-output examples (I,O)
# Output: A program P consistent with the examples (I, O)
# Auxiliary Data:
#   a DSL with supported operations
#   type signature typeSig
#   property list of typed lists of functions llProps
#   models Ms, a dictionary keyed by types of (input, output, intermediary)
def bustle(dsl, typeSig, I, O, llProps=None, Ms=None, N=100):
    Ot, It = typeSig
    s_io = propertySignature(I, It, O, Ot, llProps)

    E = {}
    for (Vt, V) in initialVs(dsl, I, O, It, Ot):
        w = 1
        r = ret_addV(E, w, It, Ot, Vt, s_io, V, O, llProps, Ms, dsl)
        if r is not None:
            return r

    for w in range(2, N):
        set_empty_e_if_none(dsl, E, w)
        for op in dsl.Ops:
            Vt = dsl.returntype(op)
            for args in all_args_for(dsl, op, E, w - 1):
                try:
                    V = executeV(dsl, op, args)
                except:
                    # ignore expressions that cause errors
                    continue
                r = ret_addV(E, w, It, Ot, Vt, s_io, V, O, llProps, Ms, dsl)
                if r is not None:
                    return r

    return E  # for debugging


def ret_addV(E, w, It, Ot, Vt, s_io, V, O, llProps, Ms, dsl):
    if Vt == Ot and sameO(V, O):
        return expression(V)
    if not containsV(V, E, Vt):
        wp = w
        s_vo = propertySignature((value(V),), (Vt,), O, Ot, llProps)
        wp = reweightWithModel(Ms, It, Ot, Vt, s_io, s_vo, w)
        addE(dsl, E, wp, Vt, V)
    return None


def addE(dsl, E, w, t, V):
    set_empty_e_if_none(dsl, E, w)
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


def propertySignatureSize(Its, Ot, llProps):
    size = 0

    for It in Its:
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


def propertySignature(Is, Its, O, Ot, llProps):
    propSig = []
    if llProps is None:
        return None

    for (I, It) in zip(Is, Its):
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
    if Ms is None:
        return w
    if s_io is None or s_vo is None:
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

    return wp


def test():
    from arithdsl import ArithDsl
    from model import Rater, loadModel

    al = ArithDsl()
    llProps = [
        (("int",), [lambda inp: inp % 2 == 0]),
        (("bool",), [lambda b: b]),
        (
            ("int", "int"),
            [lambda inp, oup: inp - oup > 0, lambda inp, oup: abs(inp - oup) <= 1],
        ),
        (("bool", "int"), [lambda b, oup: (oup % 2 == 0) == b]),
    ]
    Ms = {
        (("int",), "int", "int"): Rater(
            2 * propertySignatureSize(("int",), "int", llProps)
        )
    }
    #Ms = loadModel()
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
        al, int3, [[1, 2, 3], [3, 1, 2]], [1, 0, 0], llProps
    )


if __name__ == "__main__":
    print("running tests...")
    test()
    print("done")
