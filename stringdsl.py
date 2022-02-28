from bustle import Dsl, bustle

def StringDsl():
    # note: because we don't support overloading, we name
    # substituteI instead of overloading substitute
    # findI instead of overloading find
    Ops = ['concat', 'left', 'right', 'substr',
           'replace', 'trim', 'repeat', 'substitute',
           'substituteI', 'toText', 'lowerCase', 'upperCase',
           'properCase', 'if',
           'plus', 'minus',
           'find', 'findI', 'len',
           'equals', 'greaterThan', 'greaterThanOrEqualTo']
    Types = ['str', 'int', 'bool']

    def execute(op, x):
        if op == 'concat':
            return x[0] + x[1]
        elif op == 'left':
            return x[0][:x[1]]
        elif op == 'right':
            return x[0][len(x[0])-x[1]:]
        elif op == 'substr':
            return x[0][x[1]:x[2]]
        elif op == 'replace':
            assert False, "todo"
        elif op == 'trim':
            return x[0].strip()
        elif op == 'repeat':
            return x[0]*x[1]
        elif op == 'substitute':
            assert False, "todo"
        elif op == 'substituteI':
            assert False, "todo"
        elif op == 'toText':
            return str(x[0])
        elif op == 'lowerCase':
            return x[0].lower()
        elif op == 'upperCase':
            return x[0].upper()
        elif op == 'properCase':
            assert False, "todo"
        elif op == 'if':
            return x[1] if x[0] else x[2]
        elif op == 'plus':
            return x[0] + x[1]
        elif op == 'minus':
            return x[0] - x[1]
        elif op == 'find':
            assert False, "todo"
        elif op == 'findI':
            assert False, "todo"
        elif op == 'len':
            return len(x[0])
        elif op == 'equals':
            return x[0]==x[1]
        elif op == 'greaterThan':
            return x[0]>x[1]
        elif op == 'greaterThanOrEqualTo':
            return x[0]>=x[1]
        else:
            assert False

    def types(op):
        s = 'str'
        i = 'int'
        b = 'bool'

        if op == 'concat':
            return (s, (s, s))
        elif op in ['left', 'right']:
            return (s, (s, i))
        elif op == 'substr':
            return (s, (s, i, i))
        elif op == 'replace':
            return (s, (s, i, i, s))
        elif op == 'trim':
            return  (s, (s,))
        elif op == 'repeat':
            return (s, (s, i))
        elif op == 'substitute':
            return (s, (s, s, s))
        elif op == 'substituteI':
            return (s, (s, s, s, i))
        elif op == 'toText':
            return (s, (i,))
        elif op in ['lowerCase', 'upperCase', 'properCase']:
            return (s, (s,))
        elif op == 'if':
            return (s, (b, s, s))
        elif op in ['plus', 'minus']:
            return (i, (i, i))
        elif op == 'find':
            return (i, (s, s))
        elif op == 'findI':
            return (i, (s, s, i))
        elif op == 'len':
            return (i, (s,))
        elif op in ['equals', 'greaterThan', 'greaterThanOrEqualTo']:
            return (b, (s, s))
        else:
            assert False, 'op %s is undefined in types' % op

    def constantVs(N, t, cs):
        return [(t, (c,[c for _ in range(N)])) for c in cs]

    def extractConstants(I, O, It, Ot):
        N = len(O)
        intVs = constantVs(N, 'int', [0, 1, 2, 3, 99])
        strVs = constantVs(N, 'str', [
            "", " ", ",", ".", "!", "?", "(", ")", "|", "[", "]", "<", ">",
            "{", "}", "-", "+", "_", "/", "$", "#", ":",";", "@","%", "O"
        ])
        # TODO: string constants extracted from I/O examples
        return intVs + strVs

    return Dsl(Ops, Types, execute, types, extractConstants)

def test():
    sl = StringDsl()
    str2 = ('str', ('str',))
    assert ('left', [('input', 0), 1]) == bustle(sl, str2, [["hello", "world"]], ["h", "w"])
    assert ('right', [('input', 0), 1]) == bustle(sl, str2, [["hello", "world"]], ["o", "d"])
    # this spec seems to hang
    # bustle(sl, str2, [["hello", "world"]], ["ho", "wd"])

if __name__ == '__main__':
    print('running tests...')
    test()
    print('done')
