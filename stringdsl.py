from bustle import Dsl, bustle, propertySignatureSize

def StringDsl():
    # note: because we don't support overloading, we name
    # SubstituteI instead of overloading Substitute, and
    # FindI instead of overloading Find`
    Ops = ['Concat', 'Left', 'Right', 'Substr',
           'Replace', 'Trim', 'Repeat', 'Substitute',
           'SubstituteI', 'ToText', 'LowerCase', 'UpperCase',
           'ProperCase', 'If',
           'Plus', 'Minus',
           'Find', 'FindI', 'Len',
           'Equals', 'GreaterThan', 'GreaterThanOrEqualTo'
           ]
    Types = ['str', 'int', 'bool']

    def execute(op, x):
        if op == 'Concat':
            return x[0] + x[1]
        elif op == 'Left':
            return x[0][:x[1]]
        elif op == 'Right':
            return x[0][len(x[0])-x[1]:]
        elif op == 'Substr':
            return x[0][x[1]:x[2]]
        elif op == 'Replace':
            assert False, "todo"
        elif op == 'Trim':
            return x[0].strip()
        elif op == 'Repeat':
            return x[0]*x[1]
        elif op == 'Substitute':
            assert False, "todo"
        elif op == 'SubstituteI':
            assert False, "todo"
        elif op == 'ToText':
            return str(x[0])
        elif op == 'LowerCase':
            return x[0].lower()
        elif op == 'UpperCase':
            return x[0].Upper()
        elif op == 'ProperCase':
            assert False, "todo"
        elif op == 'If':
            return x[1] if x[0] else x[2]
        elif op == 'Plus':
            return x[0] + x[1]
        elif op == 'Minus':
            return x[0] - x[1]
        elif op == 'Find':
            assert False, "todo"
        elif op == 'FindI':
            assert False, "todo"
        elif op == 'Len':
            return len(x[0])
        elif op == 'Equals':
            return x[0]==x[1]
        elif op == 'GreaterThan':
            return x[0]>x[1]
        elif op == 'GreaterThanOrEqualTo':
            return x[0]>=x[1]
        else:
            assert False

    def types(op):
        s = 'str'
        i = 'int'
        b = 'bool'

        if op == 'Concat':
            return (s, (s, s))
        elif op in ['Left', 'Right']:
            return (s, (s, i))
        elif op == 'Substr':
            return (s, (s, i, i))
        elif op == 'Replace':
            return (s, (s, i, i, s))
        elif op == 'Trim':
            return  (s, (s,))
        elif op == 'Repeat':
            return (s, (s, i))
        elif op == 'Substitute':
            return (s, (s, s, s))
        elif op == 'SubstituteI':
            return (s, (s, s, s, i))
        elif op == 'ToText':
            return (s, (i,))
        elif op in ['LowerCase', 'UpperCase', 'ProperCase']:
            return (s, (s,))
        elif op == 'If':
            return (s, (b, s, s))
        elif op in ['Plus', 'Minus']:
            return (i, (i, i))
        elif op == 'Find':
            return (i, (s, s))
        elif op == 'FindI':
            return (i, (s, s, i))
        elif op == 'Len':
            return (i, (s,))
        elif op in ['Equals', 'GreaterThan', 'GreaterThanOrEqualTo']:
            return (b, (s, s))
        else:
            assert False, 'op %s is undefined in types' % op

    def constantVs(N, t, cs):
        return [(t, (c,[c for _ in range(N)])) for c in cs]

    def extractConstants(I, O, It, Ot):
        N = len(O)
        intVs = constantVs(N, 'int', [0, 1, 2, 3, 99])
        strVs = constantVs(N, 'str', [
            " "
            # TODO: that many constants seem to cause hanging
            #       will the ML help include them?
            #"", " ", ",", ".", "!", "?", "(", ")", "|", "[", "]", "<", ">",
            #"{", "}", "-", "+", "_", "/", "$", "#", ":",";", "@","%", "O"
        ])
        # TODO: string constants extracted from I/O examples
        return intVs + strVs

    return Dsl(Ops, Types, execute, types, extractConstants)

def test():
    from stringprops import llProps
    from model import Rater
    sl = StringDsl()
    Ms = {(('str',), 'str', 'str'): Rater(
        2*propertySignatureSize(('str',), 'str', llProps)
    )}
    str2 = ('str', ('str',))
    str3 = ('str', ('str','str'))
    assert ('Left', [('input', 0), 1]) == bustle(sl, str2, [["hello", "world"]], ["h", "w"], llProps, Ms)
    assert ('Right', [('input', 0), 1]) == bustle(sl, str2, [["hello", "world"]], ["o", "d"], llProps, Ms)
    assert ('Concat', [('input', 0), ('input', 1)]) == bustle(sl, str3, [["hello", "world"], ["you", "domination"]], ["helloyou", "worlddomination"])
    assert ('Concat', [('input', 0), ('Concat', [' ', ('input', 1)])]) == bustle(sl, str3, [["hello", "world"], ["you", "domination"]], ["hello you", "world domination"], llProps, Ms)
    assert ('Concat', [('Left', [('input', 0), 1]), ('Right', [('input', 0), 1])]) == bustle(sl, str2, [["hello", "world"]], ["ho", "wd"])

if __name__ == '__main__':
    print('running tests...')
    test()
    print('done')
