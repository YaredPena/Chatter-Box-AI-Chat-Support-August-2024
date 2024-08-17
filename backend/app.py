from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import getpass
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
import random

##loading my environment variables (openai key)
from dotenv import load_dotenv 
load_dotenv()

## loading the API key through an ENV file 
openai_api_key = os.getenv('OPENAI_API_KEY')
chat_history = [] #stores chat history              note- it might be better to use a dictionary to hold user and ai responses as a pair. might have to change the function
random_complaints=["Why does the app crash every time I try to view a thread? 🤦‍♂️ #FixYourApp", "Why does X keep recommending tweets from people I don't follow? Not interested, thanks. 😒", "When did 'chronological timeline' become a distant memory? I miss seeing tweets in order. #RIP", "I swear the new font makes everything harder to read. Why change what's not broken? 🥴", "Does anyone else’s notifications just... disappear? Like, where did they go? #GlitchCity"]
query=random.choice(random_complaints) #get some random complaint from generated complaints.

def run_query(query, chat_history, openai_api_key):
    load_dotenv()
    persist_directory = 'db'

    db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))  # access db
    retriever = db.as_retriever(search_kwargs={"k": 3})  # kwargs determines how many docs it uses

    llm = OpenAI(api_key=openai_api_key, max_tokens=1500, temperature=.8)  # LLM setup

    # Perform similarity search
    search_results = retriever.get_relevant_documents(query)

    # Extract texts from the retrieved documents
    context = "\n".join([doc.page_content for doc in search_results])

    # Store the query in the chat history first
    chat_history.append(HumanMessage(content=query))
    
    # Combine the context with the role and query
    full_query = f"You are a digital support assistant. Please use the following context to format your response:\n{context}\nQuery:\n{query}"
    
    # Get response from LLM
    llm_response = llm(full_query)

    # Store the LLM response in the chat history
    chat_history.append(AIMessage(content=llm_response))

    return llm_response  # Return the LLM response



app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message':"Welcome to the Chatter-Box Assistant Chat AI"})

@app.route('/api/chat', methods=['POST'])
def api_query():
    if not request.is_json:
        return jsonify({'error': 'Request data must be JSON'}), 400

    data = request.get_json()
    print("Received data:", data)  # Debugging line

    query = data.get('message')
    if not query:
        return jsonify({'error': 'No message provided'}), 400

    response = run_query(query, [], os.getenv('OPENAI_API_KEY'))
    
    return jsonify({'reply': response})
if __name__ == '__main__':
    app.run(debug=True, port=5000)
