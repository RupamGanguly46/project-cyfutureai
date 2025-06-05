from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not api_key or not endpoint:
    raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT environment variables")

# Ensure API keys and endpoint are set
if "AZURE_OPENAI_API_KEY" not in os.environ:
    os.environ["AZURE_OPENAI_API_KEY"] = api_key
os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint 

# Create a summary model (can use same model as chat for now)
def get_summary_model():
    return AzureChatOpenAI(
        model_name="gpt-4o",
        azure_deployment="gpt-4o",  # Or a separate deployment if preferred
        api_version="2024-02-15-preview",
        temperature=0,
        max_tokens=1024
    )

memory = ConversationSummaryBufferMemory(
    llm=get_summary_model(),
    max_token_limit=200
)
