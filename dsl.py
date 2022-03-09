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
