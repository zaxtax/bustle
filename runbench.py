from dslparser import parse, printer
from stringdsl import StringDsl
from bustle import bustle, propertySignatureSize
import stringprogs
from stringprops import llProps
from model import Rater, loadModel
import torch

from absl import app
from absl import flags
from absl import logging

def main(_):
    sl = stringdsl
    I = stringprogs.all_inputs(1)
    #I = [["1", "2.0", "hello", "-1", "-1.0", "-", "hello-you"]]
    Ms = loadModel()
    
    str2 = ("str", ("str",))
    
    for prog in stringprogs.stringprogs[1:]:
        ast = parse(sl, prog)
        if sl.numInputs(ast)>1:
            continue
        O = sl.evalIO(ast, I)
        print('bench', prog)
        ast_found = bustle(sl, str2, I, O, llProps, Ms, print_stats=True)
        prog_found = printer(sl, ast_found)
        print(prog_found)

if __name__ == '__main__':
    app.run(main)
