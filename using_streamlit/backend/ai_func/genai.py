from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import os 
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash',
                             api_key= os.getenv('GOOGLE_API_KEY'),
                             temperature= 0.7)


def get_conversation_chain():

    prompt_template = """
    Please answer the following question based on the provided context. Make sure to include all relevant details from the context in your response. 
    If the information is not available, kindly state: "I am unable to find the required details, please provide more information."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)

    return chain


