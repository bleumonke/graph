from langchain_mistralai.chat_models import ChatMistralAI

def mistral(model:str):
    return ChatMistralAI(
        model_name=model, 
        mistral_api_key="qIEDZnzrAEhky54SrQWwztBYv4XKgL9Q",
        temperature=0.0, 
        top_p=1.0,
        top_k=1)