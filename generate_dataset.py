from bustle import bustle
from stringdsl import stringdsl
import itertools
import random

def subexpressions(exp):
    r = []
    r += [exp]
    if type(exp) is tuple or type(exp) is list:
        if exp[0] == 'input':
            return r
        r.extend(itertools.chain(*(subexpressions(s) for s in exp[1])))
    return r

def handle_expression(exp, search, dsl, inp):
    es = subexpressions(exp)
    pos_exp = random.choice(es)
    pos = dsl.evalIO(pos_exp, inp)
    neg = random.choice(search)
    while neg[0] in es:
        neg = random.choice(search)
    return (pos, neg[1])

def select_expression(search, dsl, inp):
    sample = random.choice(search)
    exp = sample[0]
    o = sample[1]
    (pos, neg) =  handle_expression(exp, search, dsl, inp)
    return ((inp,pos,o), (inp, neg, o))

typ = ('str', ('str',))

def generate_input():
    return [["hello", "world"]]

def generate_dataset(dsl=stringdsl):
    data = []
    N = 5
    N_search = 10
    N_selected = 10
    for i in range(N_search):
        inp = generate_input()
        search = bustle(dsl, typ, inp, ["dummy" for _ in inp], N=N)
        search = [v for i in range(2, N) for v in search[i]['str']]
        for j in range(N_selected):
            data.append(select_expression(search, dsl, inp))
    return data

