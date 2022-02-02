# https://huggingface.co/microsoft/DialoGPT-large?

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large").to("cuda")

chat_step = 0
last_answer = ""
previous_answers = []
while True:
    question = input("\n--> ")
    if question == "" or question == None:
        continue
    if question == "delete":
        chat_step = 0
        continue
    
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(question + tokenizer.eos_token, return_tensors='pt').to("cuda")

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(
        bot_input_ids, max_length=200,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=1,
        top_k=100, top_p=0.7,
        temperature=0.8).to("cuda")

    # pretty print last ouput tokens from bot
    answer = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    if (answer in previous_answers):
        chat_step = 0
        previous_answers = []
        print ("me not smart")
    else:     
        chat_step += 1
        print(answer)
        previous_answers.append(answer)
