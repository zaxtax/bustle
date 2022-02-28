## BEGIN DSL ##

Ops = ['add', 'mul', 'neg', 'lt', 'if']
Types = ['int', 'bool']

def execute(op, args):
    if op == 'add':
        return args[0] + args[1]
    elif op == 'mul':
        return args[0] * args[1]
    elif op == 'neg':
        return -args[0]
    elif op == 'lt':
        return args[0] < args[1]
    elif op == 'if':
        return args[1] if args[0] else args[2]
    else:
        assert False

def types(op):
    if op in ['neg']:
        return ('int', ('int',))
    elif op in ['add', 'mul']:
        return ('int', ('int', 'int'))
    elif op in ['lt']:
        return ('bool', ('int', 'int'))
    elif op in ['if']:
        return ('int', ('bool', 'int', 'int'))
    else:
        assert False

## END DSL ##

def arity(op):
    return len(argtypes(op))

def argtypes(op):
    _, ts = types(op)
    return ts

def returntype(op):
    t, _ = types(op)
    return t

def executeV(op, args):
    arg_exps = [e for e,x in args]
    arg_vals = [x for e,x in args]
    x = []
    for op_args in zip(*arg_vals):
        a = execute(op, op_args)
        x = x + [a]
    e = (op, arg_exps)
    return (e, x)

def all_args(n, ts, E, w):
    if n==1:
        r = [[a] for a in E[w][ts[0]]]
    else:
        r = [[a] + b for w1 in range(1, w-n+2) for b in all_args(n-1, ts[1:], E, w-w1) for a in E[w1][ts[0]]]
    return r

def all_args_for(op, E, w):
    return all_args(arity(op), argtypes(op), E, w)

def sameV(V1, V2):
    return V1[1] == V2[1]

def sameO(V, O):
    return V[1] == O

def containsV(V, E, t):
    for En in E.values():
        for X in En[t]:
            if sameV(V,X):
                return True
    return False

def expression(X):
    return X[0]

def extractConstants(I, O):
    cs = [1]
    return [('int', (c,[c for _ in range(len(O))])) for c in cs]

def empty_e(ts):
    En = {}
    for t in ts:
        En[t] = []
    return En

def inputVs(I, It):
    return [(It[i], (('input', i), I[i])) for i in range(len(I))]

def initialVs(I, O, It, Ot):
    E1 = empty_e(Types)
    for (t, v) in extractConstants(I, O) + inputVs(I, It):
        E1[t] = E1[t] + [v]
    return E1

# The Bustle Synthesis Algorithm (without ML for now)
# Input: Input-output examples (I,O)
# Output: A program P consistent with the examples (I, O)
# Auxiliary Data:
#   supported operations Ops
#   supported types Types
#   type signature typeSig
def bustle(I, O, typeSig):
    Ot, It = typeSig
    E = {}
    E[1] = initialVs(I, O, It, Ot)

    # edge cases (not in paper)
    for V in E[1][Ot]:
        if sameO(V, O):
            return expression(V)

    for w in range(2, 5):
        E[w] = empty_e(Types)
        for op in Ops:
            t = returntype(op)
            for args in all_args_for(op, E, w-1):
                V = executeV(op, args)
                if not containsV(V, E, t):
                    E[w][t] = E[w][t] + [V]
                if t == Ot and sameO(V, O):
                    return expression(V)
    return E # for debugging

def test():
    int2 = ('int', ('int',))
    assert 1 == bustle([[1, 2, 3]], [1, 1, 1], int2)
    assert ('input', 0) == bustle([[1, 2, 3]], [1, 2, 3], int2)
    assert ('add', [('input', 0), 1]) == bustle([[1, 2, 3]], [2, 3, 4], int2)
    assert ('neg', [('input', 0)]) == bustle([[1, 2, 3]], [-1, -2, -3], int2)
    assert ('add', [('input', 0), ('neg', [1])]) == bustle([[1, 2, 3]], [0, 1, 2], int2)
