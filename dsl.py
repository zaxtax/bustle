def makeOpCache(Ops):
    cache = {}
    for op in Ops:
        cache[op.lower()] = op
    return cache

class Dsl:
    def __init__(self, Ops, Types, execute, types, extractConstants):
        self.Ops = Ops
        self.Types = Types
        self.execute = execute
        self.types = types
        self.extractConstants = extractConstants

        self.opCache = makeOpCache(Ops)

    def eval(self, x, inp):
        if type(x) is tuple or type(x) is list:
            if x[0] == 'input':
                return inp[x[1]]
            else:
                return self.execute(x[0], [self.eval(e, inp) for e in x[1]])
        else:
            return x

    def evalIO(self, exp, inps):
        return [self.eval(exp, inp) for inp in zip(*inps)]
    
    def isOp(self, token):
        return token.lower() in self.opCache

    def toOp(self, token):
        return self.opCache[token.lower()]

    def arity(self, op):
        return len(self.argtypes(op))

    def argtypes(self, op):
        _, ts = self.types(op)
        return ts

    def returntype(self, op):
        t, _ = self.types(op)
        return t

def test():
    from arithdsl import ArithDsl
    al = ArithDsl()
    assert 2 == al.eval(("add", [("input", 0), 1]), [1])
    assert [2,3,4] == al.evalIO(("add", [("input", 0), 1]), [[1,2,3]])
