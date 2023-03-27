import time

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# checkpoint = "gpt2"
checkpoint = "/root/fuzzopt/data/train_model/distilgpt2_finetune/checkpoint-640000"
# checkpoint = "Salesforce/codegen-350M-mono"
model = AutoModelForCausalLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

text = "function ("
start = time.time()

generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer, device=0)
allGeneration = generator(text, num_return_sequences=1, max_length=512,
                          pad_token_id=tokenizer.eos_token_id)
print(allGeneration)
print("完成：", time.time() - start)

# completion = model.generate(**tokenizer(text, return_tensors="pt"))
#
# print(tokenizer.decode(completion[0]))

# from datasets import load_dataset
#
# ds = load_dataset("codeparrot/github-code", streaming=True, split="train",languages=["javascript"])
# print(next(iter(ds)))