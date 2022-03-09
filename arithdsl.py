from dsl import Dsl

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
