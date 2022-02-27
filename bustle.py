Ops = ['add', 'mul', 'neg']

def execute(op, args):
    if op == 'add':
        return args[0] + args[1]
    elif op == 'mul':
        return args[0] * args[1]
    elif op == 'neg':
        return -args[0]
    else:
        assert False

def arity(op):
    if op in ['neg']:
        return 1
    elif op in ['add', 'mul']:
        return 2
    else:
        assert False

def executeV(op, args):
    arg_exps = [e for e,x in args]
    arg_vals = [x for e,x in args]
    x = []
    for op_args in zip(*arg_vals):
        a = execute(op, op_args)
        x = x + [a]
    e = (op, arg_exps)
    return (e, x)

def all_args_for(op, E, w):
    n = arity(op)
    # TODO: do this generally
    if n==1:
        for a1 in E[w]:
            yield (a1,)
    elif n==2:
        for w1 in range(1, w):
            w2 = w - w1
            for a1 in E[w1]:
                for a2 in E[w2]:
                    yield (a1, a2)
    else:
        assert False, "not implemented"

def sameV(V1, V2):
    return V1[1] == V2[1]

def sameO(V, O):
    return V[1] == O

def containsV(V, E):
    for ws in E.values():
        for X in ws:
            if sameV(V,X):
                return True
    return False

def expression(X):
    return X[0]

def extractConstants(I, O):
    cs = [1]
    return [(c,[c for _ in range(len(O))]) for c in cs]

def inputVs(I):
    return [(('input', i), I[i]) for i in range(len(I))]

# The Bustle Synthesis Algorithm (without ML for now)
# Input: Input-output examples (I,O)
# Output: A program P consistent with the examples (I, O)
# Auxiliary Data:
#   supported operations Ops
def bustle(I, O):
    E = {}
    C = extractConstants(I, O)
    E[1] = inputVs(I) + C

    # edge cases (not in paper)
    for V in E[1]:
        if sameO(V, O):
            return expression(V)

    for w in range(2, 5):
        E[w] = []
        for op in Ops:
            for args in all_args_for(op, E, w-1):
                V = executeV(op, args)
                if not containsV(V, E):
                    E[w] = E[w] + [V]
                if sameO(V, O):
                    return expression(V)
    return E # for debugging

def test():
    assert 1 == bustle([[1, 2, 3]], [1, 1, 1])
    assert ('input', 0) == bustle([[1, 2, 3]], [1, 2, 3])
    assert ('add', [('input', 0), 1]) == bustle([[1, 2, 3]], [2, 3, 4])
    assert ('neg', [('input', 0)]) == bustle([[1, 2, 3]], [-1, -2, -3])
    assert ('add', [('input', 0), ('neg', [1])]) == bustle([[1, 2, 3]], [0, 1, 2])
