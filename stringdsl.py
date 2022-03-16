from dsl import Dsl


def StringDsl(supportExtraConstants=False):
    # note: because we don't support overloading, we name
    # SubstituteI instead of overloading Substitute, and
    # FindI instead of overloading Find`
    Ops = [
        "Concatenate",
        "Left",
        "Right",
        "Mid",
        "Replace",
        "Trim",
        "Repeat",
        "Substitute",
        "SubstituteI",
        "To_Text",
        "Lower",
        "Upper",
        "Proper",
        "If",
        "Add",
        "Minus",
        "Divide",
        "Find",
        "FindI",
        "Len",
        "Exact",
        "Equals",
        "GT",
        "GE",
        "IsNumber",
        "Value",
    ]
    Types = ["str", "int", "bool"]

    def execute(op, x):
        if op == "Concatenate":
            return x[0] + x[1]
        elif op == "Left":
            return x[0][: x[1]]
        elif op == "Right":
            return x[0][len(x[0]) - x[1] :]
        elif op == "Mid":
            return x[0][x[1] : x[1] + x[2]]
        elif op == "Replace":
            a = x[0]
            start = x[1]
            length = x[2]
            r = x[3]
            ret = a[:start] + r + a[start + length :]
            return ret
        elif op == "Trim":
            return x[0].strip()
        elif op == "Repeat":
            return x[0] * x[1]
        elif op == "Substitute":
            return x[0].replace(x[1], x[2])
        elif op == "SubstituteI":
            return x[0].replace(x[1], x[2], x[3])
        elif op == "To_Text":
            return str(x[0])
        elif op == "Lower":
            return x[0].lower()
        elif op == "Upper":
            return x[0].upper()
        elif op == "Proper":
            return x[0].title()
        elif op == "If":
            return x[1] if x[0] else x[2]
        elif op == "Add":
            return x[0] + x[1]
        elif op == "Minus":
            return x[0] - x[1]
        elif op == "Divide":
            return x[0] // x[1]
        elif op == "Find":
            return x[1].find(x[0])
        elif op == "FindI":
            return x[1].find(x[0], x[2])
        elif op == "Len":
            return len(x[0])
        elif op == "Exact":
            return x[0] == x[1]
        elif op == "Equals":
            return x[0] == x[1]
        elif op == "GT":
            return x[0] > x[1]
        elif op == "GE":
            return x[0] >= x[1]
        elif op == "IsNumber":
            return x[0].isnumeric()
        elif op == "Value":
            return int(x[0])
        else:
            assert False

    def types(op):
        s = "str"
        i = "int"
        b = "bool"

        if op == "Concatenate":
            return (s, (s, s))
        elif op in ["Left", "Right"]:
            return (s, (s, i))
        elif op == "Mid":
            return (s, (s, i, i))
        elif op == "Replace":
            return (s, (s, i, i, s))
        elif op == "Trim":
            return (s, (s,))
        elif op == "Repeat":
            return (s, (s, i))
        elif op == "Substitute":
            return (s, (s, s, s))
        elif op == "SubstituteI":
            return (s, (s, s, s, i))
        elif op == "To_Text":
            return (s, (i,))
        elif op in ["Lower", "Upper", "Proper"]:
            return (s, (s,))
        elif op == "If":
            return (s, (b, s, s))
        elif op in ["Add", "Minus", "Divide"]:
            return (i, (i, i))
        elif op == "Find":
            return (i, (s, s))
        elif op == "FindI":
            return (i, (s, s, i))
        elif op == "Len":
            return (i, (s,))
        elif op == "Exact":
            return (b, (s, s))
        elif op in ["Equals", "GT", "GE"]:
            return (b, (i, i))
        elif op == "IsNumber":
            return (b, (s,))
        elif op == "Value":
            return (i, (s,))
        else:
            assert False, "op %s is undefined in types" % op

    def constantVs(N, t, cs):
        return [(t, (c, [c for _ in range(N)])) for c in cs]

    def extractConstants(I, O, It, Ot):
        extraConstants = []
        if supportExtraConstants:
            extraConstants = [
                ",", ".", "!", "?", "(", ")", "|", "[", "]", "<", ">",
                "{", "}", "-", "+", "_", "/", "$", "#", ":",";", "@","%", "O"
            ]
        N = len(O)
        intVs = constantVs(N, "int", [0, 1, 2, 3, 99])
        strVs = constantVs(
            N,
            "str",
            [
                " ", ""
            ] + extraConstants
        )
        # TODO: string constants extracted from I/O examples
        return intVs + strVs

    def inferType(v):
        if type(v) is str:
            return "str"
        elif type(v) is int:
            return "int"
        elif type(v) is bool:
            return "bool"
        else:
            assert False

    return Dsl(Ops, Types, execute, types, extractConstants, inferType)


stringdsl = StringDsl()


def test():
    from bustle import bustle, propertySignatureSize
    from stringprops import llProps
    from model import Rater, loadModel
    import torch

    str2 = ("str", ("str",))
    str3 = ("str", ("str", "str"))

    sl = StringDsl()
    slx = StringDsl(True)
    MsInit = {
        (("str",), "str", "str"): Rater(
            2 * propertySignatureSize(("str",), "str", llProps)
        )
    }
    MsTrained = loadModel()

    for (desc, sl, llProps, Ms) in [
            ('no ML', sl, None, None),
            ('init ML', sl, llProps, MsInit),
            ('trained ML', sl, llProps, MsTrained),
            ('trained ML, extended DSL', slx, llProps, MsTrained)
            ]:
        print(desc)

        assert ("Left", [("input", 0), 1]) == bustle(
            sl, str2, [["hello", "world"]], ["h", "w"], llProps, Ms
        )
        assert ("Right", [("input", 0), 1]) == bustle(
            sl, str2, [["hello", "world"]], ["o", "d"], llProps, Ms
        )
        assert ("Concatenate", [("input", 0), ("input", 1)]) == bustle(
            sl, str3,
            [["hello", "world"], ["you", "domination"]],
            ["helloyou", "worlddomination"],
            llProps, Ms
        )
        assert (
            "Concatenate", [("input", 0), ("Concatenate", [" ", ("input", 1)])],
        ) == bustle(
            sl, str3,
            [["hello", "world"], ["you", "domination"]],
            ["hello you", "world domination"],
            llProps, Ms
        )
        assert (
            bustle(
                sl, str2,
                [["hello", "world", "domination", "yes"]], ["ho", "wd", "dn", "ys"],
                llProps, Ms
            ) in  [
                ("Concatenate", [("Left", [("input", 0), 1]), ("Right", [("input", 0), 1])]),
                ('Replace', [('input', 0), 1, ('Minus', [0, 2]), ''])
            ])

if __name__ == "__main__":
    print("running tests...")
    test()
    print("done")
