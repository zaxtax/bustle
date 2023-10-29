from dslparser import printer
from llm_outlines import gen

debug = True
choices = ["A", "B", "C", "D", "E"]
choice_stats = {c:0 for c in choices}

def generateDeltaWeight(dsl, It, Ot, Vt, I, O, V):
    global choice_stats
    prompt = dsl.desc()
    prompt += "\n"
    n = len(O)
    prompt += f"You have to generate a function with input/output as follows on {n} examples:\n"
    prompt += dsl.io_print(I, O)
    expr = printer(dsl, V[0])
    res = V[1]
    outres = O
    prompt += f"Can you guess whether the DSL expression `{expr}` is likely to appear as a sub-expression in a solution in our DSL to the function `f` to synthesize. The expression has the following output on the inputs above: {res}, while the final solution should have the following output: {outres}.\n"
    prompt += "Answer with one of the grades A, B, C, D, E.\n"
    prompt += "A means very likely to appear.\n"
    prompt += "B means somewhat likely to appear.\n"
    prompt += "C means somewhat unlikely to appear.\n"
    prompt += "D means unlikely to appear.\n"
    prompt += "E means very unlikely to appear.\n"
    prompt += "So answer with one of the grades A, B, C, D, E.\n"
    prompt += "Your grade is:"
    if debug:
        print("PROMPT:")
        print(prompt)
    r = gen(prompt, choices)
    if debug:
        print(r)
    choice_stats[r] += 1
    return choices.index(r)

def test():
    from arithdsl import ArithDsl
    from bustle import bustle   
    al = ArithDsl()
    int2 = ("int", ("int",))
    r = bustle(
        al, int2, [[1, 2, 3, 4]], [0, 2, 4, 6], llm=generateDeltaWeight
    )
    print(printer(al, r))
    print(choice_stats)

if __name__ == "__main__":
    print("running tests...")
    test()
    print("done")
