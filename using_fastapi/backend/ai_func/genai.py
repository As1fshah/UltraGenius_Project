from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash',
                             api_key= os.getenv('GOOGLE_API_KEY'),
                             temperature= 0.7)


def start_conversation(user_query: str, context : str):

    prompt = f"""
    Please answer the following question based on the provided context. Make sure to include all relevant details from the context in your response. 
    If the information is not available, kindly state: "I am unable to find the required details, please provide more information."

    Context:
    {context}

    Question:
    {user_query}

    Answer:
    """
    return llm.invoke(prompt).content


