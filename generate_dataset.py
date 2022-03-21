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


def handle_expression(exp, all_search, search, dsl, inp):
    es = subexpressions(exp)
    pos_exp = random.choice(es)
    pos = dsl.evalIO(pos_exp, inp)
    neg = random.choice(all_search)
    while neg[0] in es:
        neg = random.choice(all_search)
    return (pos, neg[1])


def select_expression(all_search, search, dsl, inp):
    sample = random.choice(search)
    return build_sample(sample, all_search, search, dsl, inp)

def build_sample(sample, all_search, search, dsl, inp):
    exp = sample[0]
    o = sample[1]
    (pos, neg) = handle_expression(exp, all_search, search, dsl, inp)
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

def run_bustle(dsl, typ, inp, N):
    all_search = bustle(dsl, typ, inp, ["dummy" for _ in inp[0]], N=N, print_stats=True)
    search = [v for i in range(2, N) for v in all_search[i]["str"]]
    search_bool = [v for i in range(2, N) for v in all_search[i]["bool"]]
    search_int = [v for i in range(2, N) for v in all_search[i]["int"]]
    all_search = search + search_bool + search_int
    return search, all_search


def generate_dataset():
    return generate_dataset_cheat()


def generate_dataset_cheat():
    from dslparser import parse
    dsl = stringdsl
    progs = [parse(dsl,prog) for prog in stringprogs.stringprogs]
    progs1 = [prog for prog in progs if dsl.numInputs(prog) == 1]
    exps = list(itertools.chain(*(subexpressions(prog) for prog in progs1)))

    N = 7
    N_search = 5
    N_selected = 1000
    data = []
    for i in range(N_search):
        inp = [stringprogs.input]
        print('')
        print('BUSTLE')
        search, all_search = run_bustle(dsl, typ, inp, N)
        samples = [(e, dsl.evalIO(e, inp)) for e in exps]
        samples = [(e,o) for (e,o) in samples if type(o[0]) is str]
        print('')
        print('SAMPLES')
        for sample in samples:
            print('.', end='', flush=True)
            for i in range(N_selected):
                data.append(build_sample(sample, all_search, search, dsl, inp))
        #for j in range(N_selected):
        #    data.append(select_expression(search, dsl, inp))
    random.shuffle(data)
    return data


def generate_dataset_old(dsl=stringdsl):
    data = []
    N = 7
    N_search = 5
    N_selected = 1000
    for i in range(N_search):
        inp = generate_input()
        search, all_search = run_bustle(dsl, typ, inp, N)
        for j in range(N_selected):
            data.append(select_expression(all_search, search, dsl, inp))
        #for sample in search:
        #    data.append(build_sample(sample, all_search, dsl, inp))
    return data
