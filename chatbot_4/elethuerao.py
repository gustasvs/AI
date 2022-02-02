from transformers import pipeline
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
#generator("In the name of united states I", do_sample=True, min_length=150)
