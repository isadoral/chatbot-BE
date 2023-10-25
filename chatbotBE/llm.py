from flask import Flask, request, jsonify
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.retrievers import SVMRetriever
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, PromptTemplate
import os

import os

BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')
DEPLOYMENT_NAME = "api3_2"

knowledgebase = ""
conversation_history = ""
user_question = ""
prompt = ""
GPT_answer = ""
current_conversation = ""

knowledgebase, conversation_history, user_question, prompt, GPT_answer, current_conversation

# Prompt Design 

# funciton to store the user's question

def receive_question():
    data = request.json
    print(data)
    user_question = data.get('prompt')
    return user_question

# function to store the conversation history
def update_conversation_history(user_question, chatbot_response):
    global conversation_history
    # Append user's input
    conversation_history += "User said: " + user_question + "\n\n"
    # Append chatbot's response
    conversation_history += "Makkie responded: " + chatbot_response + "\n\n"
    return conversation_history


def load_database():
    # # Load database
    loader = PyPDFLoader("./Dataset4.pdf")
    # # split into pages
    all_pages = loader.load_and_split()
    # # store as vector database
    # vectorstore = Chroma.from_documents(documents=all_pages, embedding=embeddings)
    print("There are", len(all_pages), "pages sucessfully stored in vector database")
    return all_pages

# def find_pages(all_pages, user_question):
#     # find relevant pages
#     svm_retriever = SVMRetriever.from_documents(all_pages ,embeddings) # setup svm retriever
#     knowledgebase = svm_retriever.get_relevant_documents(user_question) # find relevant pages
#     print("There are ", len(knowledgebase), "relevant pages found")
#     return knowledgebase

def generate_prompt(prompt):
    rag_prompt_custom = PromptTemplate.from_template(prompt)
    return rag_prompt_custom

def model_call(prompt, all_pages, model):
    model(
        [
            HumanMessage(
                content=prompt(user_question, all_pages, conversation_history)
            )
        ]
    )
    response = model(
    [
        HumanMessage(
            content="Translate this sentence from English to French. I love programming."
        )
    ]
    ) 

def generate_prompt_and_call(rag_prompt_custom, all_pages, model):
    rag_chain = (
        {"knowledgebase": all_pages, "user_question": RunnablePassthrough(), "conversation_history": RunnablePassthrough()} 
        | rag_prompt_custom 
        | model
    )
    return rag_chain   


