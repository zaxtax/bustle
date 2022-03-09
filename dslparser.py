import tokenize
import io

def tokens(inp):
    ts = tokenize.generate_tokens(io.StringIO(inp).readline)
    return [x[1] for x in ts if x[1]!='']
    
def parset(dsl, ts):
    if ts[0] in dsl.Ops:
        op = ts[0]
        ts = ts[1:]
        assert ts[0] == '('
        ts = ts[1:]
        (returntype, argtypes) = dsl.types(op)
        n = len(argtypes)
        args = []
        for i in range(n):
            (arg, ts) = parset(dsl, ts)
            args.append(arg)
            if i!=n-1:
                assert ts[0] == ','
                ts = ts[1:]
        assert ts[0] == ')'
        ts = ts[1:]
        return ((op, args), ts)
    elif ts[0].startswith("x"):
        x = ts[0]
        try:
            r = int(x[1:])
        except ValueError:
            assert False, "expected an input (x followed by number), not %s" % x
        return (("input", r), ts[1:])
    else:
        try:
            r = int(ts[0])
            return (r, ts[1:])
        except ValueError:
            assert False, "unexpected token "+ts[0]

def parse(dsl, inp):
    (exp, ts) = parset(dsl, tokens(inp))
    assert ts == []
    return exp

def printer(dsl, x):
    if type(x) is tuple or type(x) is list:
        if x[0] == 'input':
            return 'x'+str(x[1])
        else:
            return x[0]+"("+", ".join([printer(dsl, arg) for arg in x[1]])+")"
    else:
        return str(x)

def test():
    from bustle import ArithDsl
    al = ArithDsl()
    assert ("add", [("input", 0), 1]) == parse(al, "add(x0, 1)")
    assert ("if", [("lt", [("input", 0), ("input", 1)]), 1, 0]) == parse(al, "if(lt(x0, x1), 1, 0)")
    assert "add(x0, 1)" == printer(al, ("add", [("input", 0), 1]))
    assert "if(lt(x0, x1), 1, 0)" == printer(al, ("if", [("lt", [("input", 0), ("input", 1)]), 1, 0]))
