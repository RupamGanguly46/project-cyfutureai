from langchain_openai import AzureChatOpenAI
from langchain.chains import ConversationChain
from chat_memory import memory
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file variables

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not api_key or not endpoint:
    raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT environment variables")

# Ensure API keys and endpoint are set
if "AZURE_OPENAI_API_KEY" not in os.environ:
    os.environ["AZURE_OPENAI_API_KEY"] = api_key
os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint

# Create the Azure Chat LLM
llm = AzureChatOpenAI(
    model_name="gpt-4o",
    azure_deployment="gpt-4o",  # Your deployment name
    api_version="2024-02-15-preview",
    temperature=0.7,
    max_tokens=1000
)

# Chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# def get_response(user_input: str):
#     return conversation.predict(input=user_input)

def get_response(user_input: str, sentiment: str = None):
    prompt = user_input
    if sentiment:
        prompt = f"[User sentiment: {sentiment}]\n{user_input}"
    return conversation.predict(input=prompt)
