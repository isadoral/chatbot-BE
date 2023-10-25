from flask import Flask, jsonify, request
from chatbotBE.llm import receive_question
from langchain.llms import AzureOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI

app = Flask(__name__)
import os
from dotenv import load_dotenv

load_dotenv()

import os

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://<your-endpoint.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "your AzureOpenAI key"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')
DEPLOYMENT_NAME = "api3_2"
OPENAI_API_VERSION = "2023-05-15"
OPEN_API_TYPE = "azure"

from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

model = AzureChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_version="2023-07-01-preview",
    deployment_name=DEPLOYMENT_NAME,
    openai_api_key=API_KEY,
    openai_api_type="azure",
)


@app.route("/question")
def hello_world():
    response = model(
    [
        HumanMessage(
            content="Translate this sentence from English to French. I love programming."
        )
    ]
    )  
    print(response)
    return "Hello, World!"


@app.route('/question_chat', methods=['POST'])
def question_chat():
    receive_question()

@app.route('/demo', methods=['POST'])
def demo():
    print(request)
    data = request.json
    print(data)
    return jsonify(title="agile", messages=["hello world"])
