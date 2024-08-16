from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import getpass
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from langchain_community.chains import *
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader

##loading my environment variables
from dotenv import load_dotenv 
load_dotenv()
##

app = Flask(__name__)
CORS(app)

persist_directory= 'db'  
raw_documents = CSVLoader(file_path='backend\data\out.csv').load() #load pdf files from data folder
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  #load data into 1000 bit chunks
documents = text_splitter.split_documents(raw_documents) #split the text 
db = Chroma.from_documents(documents, OpenAIEmbeddings(),persist_directory=persist_directory) #here we initialize the database. this is only to be run once. 
os.environ['OPENAI_API_KEY'] = 

db = Chroma.from_documents(documents, OpenAIEmbeddings())

## loading the API key through an ENV file 
openai_api_key = os.getenv('OPEN_AI_API_KEY')

@app.route('/')
def home():
    return "Welcome to the Chatter-Box Assistant Chat AI"

@app.route('/api/chat', methods =['POST'])
def chat():
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

## make a request to the API
    response = openai.Completion.create(
        engine="gpt-3.5",
        prompt=message,
        max_tokens=150
    )

## grab the response
    reply = response.choices[0].text.strip()
    return jsonify({'reply': reply})

## populate db tables --> Sqlite
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


## switch api for the openAI -> Assistant API later ask for help with that.
## import os for env files.

##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:chatterbox.db' <-- this was wrong

##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db' <-- relative paths
##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////chatterbox.db' <-- absolute paths

## need to create sqlite db.