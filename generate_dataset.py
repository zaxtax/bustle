from bustle import bustle
from stringdsl import stringdsl
import stringprogs
import itertools
import random
import string

def subexpressions(exp):
    r = []
    r += [exp]
    if type(exp) is tuple or type(exp) is list:
        if exp[0] == "input":
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
    return build_sample(sample, search, dsl, inp)

def build_sample(sample, search, dsl, inp):
    exp = sample[0]
    o = sample[1]
    (pos, neg) = handle_expression(exp, search, dsl, inp)
    return ((inp, pos, o), (inp, neg, o))


typ = ("str", ("str",))
# charset = string.printable[:-6]
charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-+/"


def generate_input(N=3, LB=5, UB=8):
    # TODO: maybe generate more interesting inputs that satisfy constraints
    #   such as index within range
    # numbers?
    # dates?
    # URLs?
    # words?
    inp = []
    for i in [random.randint(LB, UB) for _ in range(N)]:
        inp.append("".join([random.choice(charset) for _ in range(i)]))
    inp = inp + stringprogs.input
    return [inp]


def generate_dataset(dsl=stringdsl):
    data = []
    N = 7
    N_search = 5
    N_selected = 1000
    for i in range(N_search):
        inp = generate_input()
        search = bustle(dsl, typ, inp, ["dummy" for _ in inp[0]], N=N)
        search = [v for i in range(2, N) for v in search[i]["str"]]
        for j in range(N_selected):
            data.append(select_expression(search, dsl, inp))
        #for sample in search:
        #    data.append(build_sample(sample, search, dsl, inp))
    return data
