from llm_outlines import gen

def generateDeltaWeight(dsl, It, Ot, Vt, I, O, V):
    prompt = dsl.desc()
    prompt += "\n"
    n = len(O)
    prompt += f"You have to generate a function f with input/output as follows on {n} examples:\n"
    for i in range(0, n):
        ins = [repr(x[i]) for x in I]
        out = repr(O[i])
        prompt += f"{i}. f({','.join(ins)}) = {out}\n"
    expr = V[0]
    res = V[1]
    prompt += f"Can you guess whether the DSL expression {expr} is likely to appear to as a sub-expression in a solution to the function f to synthesize. The expression has the following output on the inputs above: {res}. Answer with one of the grades A, B, C, D, E.\n"
    prompt += "A means very likely to appear.\n"
    prompt += "E means very unlikely to appear.\n"
    prompt += "Your grade is:"
    print("PROMPT:")
    print(prompt)
    choices = ["A", "B", "C", "D", "E"]
    r = gen(prompt, choices)
    print(r)
    return choices.index(r)

def test():
    from arithdsl import ArithDsl
    from bustle import bustle   
    al = ArithDsl()
    int2 = ("int", ("int",))
    print(bustle(
        al, int2, [[1, 2, 3, 4]], [0, 2, 4, 6], llm=generateDeltaWeight
    ))

if __name__ == "__main__":
    print("running tests...")
    test()
    print("done")

    
    
    
