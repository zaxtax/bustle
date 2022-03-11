import torch
from torch.nn import BCELoss
from tqdm import tqdm

from model import Rater
from generate_dataset import generate_dataset
from stringdsl import stringdsl
from stringprops import llProps
from bustle import propertySignature, propertySignatureSize
It = ('str',)
Ot = 'str'
dsl = stringdsl
dataset = generate_dataset()

def initialModel(key):
    (It, Ot, Vt) = key
    return Rater(
        propertySignatureSize(It, Ot, llProps) +
        propertySignatureSize(Vt, Ot, llProps)
    )
    
Ms = {}
loss = BCELoss()

for epoch in tqdm(range(10)):
    Ts = {}
    for sample in dataset:
        pos, neg = sample

        for (ex, valence) in ((pos, 1), (neg, -1)):
            (I, V, O) = pos
            Vt = dsl.inferType(V[0])

            key = (It, Ot, Vt)
            M = Ms.get(key)
            if M is None:
                M = initialModel(key)
                Ms[key] = M
                optimizer = torch.optim.Adam(M.parameters(), lr=0.001)
            train_losses = Ts.get(key, [])
            M.train()

            optimizer.zero_grad()
    
            s1 = propertySignature(I, It, O, Ot, llProps)
            s2 = propertySignature(V, Vt, O, Ot, llProps)
            s = torch.cat([s1, s2])

            outputs = M(s)
            loss_v = loss(outputs, torch.tensor([1.0*valence]))
            loss_v.backward()
            optimizer.step()
            train_losses.append(loss_v.item())
    print('loss', train_losses)