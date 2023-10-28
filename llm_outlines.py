import outlines.text.generate.sample as sample
import outlines.text.generate as generate
import outlines.models as models
import torch

#base_model_name = "mistralai/Mistral-7B-v0.1"
base_model_name = "meta-llama/Llama-2-13b-hf"
model = models.transformers(base_model_name, device="cuda")

def gen(prompt, choices):
    return gen_greedy(prompt, choices)

def gen_greedy(prompt, choices):
    return generate.choice(model, choices, sampler=sample.greedy)(prompt)
