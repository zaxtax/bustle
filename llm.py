import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer, TextStreamer

#base_model_name = "mistralai/Mistral-7B-v0.1"
base_model_name = "meta-llama/Llama-2-70b-hf"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    use_auth_token=True
)

tokenizer = AutoTokenizer.from_pretrained(base_model_name)
tokenizer.pad_token = tokenizer.eos_token

model = base_model

streamer = TextStreamer(tokenizer)

def generate(eval_prompt, max_new_tokens=200):
    model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
    
    model.eval()
    
    r = None
    with torch.no_grad():
        r = tokenizer.decode(model.generate(**model_input,
                                            #streamer=streamer,
                                            max_new_tokens=max_new_tokens)[0],
                             skip_special_tokens=True)
    return r

def generateReweight(dsl, w, It, Ot, Vt):
    return w
