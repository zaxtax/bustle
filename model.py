import torch
import torch.nn as nn
import torch.nn.functional as F

# The neural guide takes the input and output, and an intermediary value,
# and predicts whether the intermediary value is part of the solution.
#
# We use a simple Multi-Layer Perceptron.
class Rater(nn.Module):
    def __init__(self, input_dim):
        super().__init__()

        self.input_fc = nn.Linear(input_dim, 250)
        self.hidden_fc = nn.Linear(250, 100)
        self.output_fc = nn.Linear(100, 1)
        self.output_prob = nn.Sigmoid()

    def forward(self, x):
        batch_size = x.shape[0]
        x = x.view(batch_size, -1)
        h_1 = F.relu(self.input_fc(x))
        h_2 = F.relu(self.hidden_fc(h_1))
        y_pred = self.output_fc(h_2)
        y_prob = self.output_prob(y_pred)
        return y_prob
