# 下载模型
from transformers import AutoTokenizer, AutoModelForCausalLM

# model_name = "gpt2"
# model_name = "distilgpt2"
# model_name = "gpt2-medium"
# model_name = "Salesforce/codegen-350M-mono"
model_name = "Salesforce/codegen-350M-multi"
model_name = "Salesforce/codegen-2B-multi"
# model_name = "codeparrot/codeparrot"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

model_path = "/root/fuzzopt/data/train_model/"
tokenizer.save_pretrained(model_path + model_name)
model.save_pretrained(model_path + model_name)
