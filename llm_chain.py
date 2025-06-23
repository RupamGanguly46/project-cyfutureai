# from langchain_openai import AzureChatOpenAI
# from langchain.chains import ConversationChain
# from chat_memory import memory
# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load .env file variables

# api_key = os.getenv("AZURE_OPENAI_API_KEY")
# endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# if not api_key or not endpoint:
#     raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT environment variables")

# # Ensure API keys and endpoint are set
# if "AZURE_OPENAI_API_KEY" not in os.environ:
#     os.environ["AZURE_OPENAI_API_KEY"] = api_key
# os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint

# # Create the Azure Chat LLM
# llm = AzureChatOpenAI(
#     model_name="gpt-4o",
#     azure_deployment="gpt-4o",  # Your deployment name
#     api_version="2024-02-15-preview",
#     temperature=0.7,
#     max_tokens=1000
# )

# # Chain with memory
# conversation = ConversationChain(
#     llm=llm,
#     memory=memory,
#     verbose=True
# )

# # def get_response(user_input: str):
# #     return conversation.predict(input=user_input)


# def get_response(user_input: str, sentiment: str = None):
#     prompt = user_input
#     if sentiment:
#         prompt = f"[User sentiment: {sentiment}]\n{user_input}"
#     return conversation.predict(input=prompt)

from langchain_openai import AzureChatOpenAI
# from langchain.prompts import PromptTemplate
from chat_memory import memory
from rag_store import retrieve_context
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not api_key or not endpoint:
    raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")

llm = AzureChatOpenAI(
    model_name="gpt-4o",
    azure_deployment="gpt-4o",
    api_version="2024-02-15-preview",
    temperature=0.3,
    max_tokens=1000
)

system_prompt = """
You are an AI-powered Customer Care Assistant working in a professional customer support environment.
Your responses must always reflect a clear, helpful, respectful, and emotionally intelligent tone, 
similar to a well-trained human customer care representative.

-------------------------------
🎯 ROLE AND SCOPE
-------------------------------
- You are NOT a general-purpose AI.
- ONLY assist with customer support topics related to company services, accounts, or processes.
- If a question is unrelated (e.g., math, facts, code), politely say you're here only for customer support and refer them to a human if needed.

-------------------------------
📜 COMMUNICATION STYLE
-------------------------------
- Use warm, human, empathetic language — but remain professional.
- Be concise and clear — avoid overexplaining.
- Always maintain a welcoming and respectful tone.
- Use short paragraphs and easy-to-read structure.

✅ Sample starters:
- “Sure, I’d be happy to help you with that.”
- “Thanks for reaching out. Here’s what I can tell you…”
- “Let me guide you through that.”
- “I understand this may be frustrating. I’ll do my best to assist you.”

-------------------------------
🤝 TONE & EMPATHY
-------------------------------
- Reflect the user's emotions with calm, human understanding.
- Never sound robotic.
- If a user is angry, be patient, acknowledge the frustration, and aim to resolve.

-------------------------------
🧭 RESPONSE RULES
-------------------------------
1. Stay focused on relevant customer care topics.
2. Never answer off-topic or general queries.
3. Be brief, warm, and informative.
4. Always respond in the same language as the user's message, when possible.
5. Don’t guess — if unsure, say:
   “I’m afraid I don’t have access to that information right now.”

-------------------------------
📚 KNOWLEDGE USE
-------------------------------
- You may reference external customer support documentation.
- Do not hallucinate or invent answers.
- You may use the provided "Relevant Knowledge" to answer the user's question as accurately as possible.

-------------------------------
🚫 DO NOT:
-------------------------------
- Respond to general knowledge, jokes, or trivia.
- Give legal/medical/financial advice.
- Use emojis, memes, or slang.
- Overshare or sound like a chatbot.

-------------------------------
🧠 EXAMPLES
-------------------------------
Q: “I’m having trouble logging in.”
A: “Of course. I’d be happy to help. Could you please share the exact error message you’re seeing?”

Q: “Can you explain what GPT-4 is?”
A: “I’m here to assist only with customer support questions. For general topics, I recommend reaching out to an appropriate source.”

Q: “You guys are terrible!”
A: “I truly understand how frustrating that must be, and I sincerely apologize for the inconvenience. Let’s work together to get this sorted.”

-------------------------------
SUMMARY
-------------------------------
- Be a calm, confident, professional support agent.
- Focus on solving customer problems.
- Be empathetic, but stay on-topic and formal.
- Do not pretend to be a general AI — you're a specialized support assistant.
- Mirror the language used by the customer for better comfort and clarity.

"""

template = """
Relevant Knowledge:
{context}

Conversation Summary:
{history}

User: {input}

Assistant:"""

# prompt = PromptTemplate(
#     input_variables = ["history", "input"],
#     template = system_prompt + "\nConversation Summary:\n{history}\n\nUser: {input}\nAssistant:"
# )

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_message = SystemMessagePromptTemplate.from_template(system_prompt)
human_message = HumanMessagePromptTemplate.from_template("{input}")

chat_prompt = ChatPromptTemplate.from_messages([
    system_message,
    HumanMessagePromptTemplate.from_template("Context:\n{context}\n\nConversation Summary:\n{history}\n\nUser: {input}")
])


def get_response(user_input: str, sentiment: str = None):
    full_input = f"[User sentiment: {sentiment}]\n{user_input}" if sentiment else user_input

    # Get the current summary from memory
    summary = memory.load_memory_variables({}).get("history", "")

    # Retrieve relevant context from RAG store
    context = retrieve_context(user_input)

    # Format the final prompt
    # prompt_text = prompt.format(input=full_input, history=summary)
    prompt_text = chat_prompt.format(input=full_input, history=summary, context=context)

    # Get LLM response
    response = llm.invoke(prompt_text)

    # Update memory with the new interaction
    memory.save_context(
        {"input": user_input},
        {"output": response.content}
    )

    return response.content
