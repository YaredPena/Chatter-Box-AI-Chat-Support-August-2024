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
##
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

    llm = OpenAI(api_key=openai_api_key, max_tokens=1500, temperature=.3)  # api key self explanatory. max_tokens provides how long of a response 
    # we get from the llm (do note the llm has a cap of 4097.) and temperature provides a scale form 0.0 to 1.0 of how much freedom 
    # the llm should take in its response (how closely it should adhere to docs vs how freely)

    # Perform similarity search
    search_results = retriever.get_relevant_documents(query)

    # Extract texts from the retrieved documents
    context = "\n".join([doc.page_content for doc in search_results])
    
    # Combine the context with the query
    full_query = f"{context}\n\n{query}"
    
    # Get response from LLM
    llm_response = llm(full_query)

    # Store the interaction in chat history
    chat_history.append((HumanMessage(content=query), AIMessage(content=llm_response))) #this stores the pair of the human question and the ai response. 
    
    return llm_response #returns a string response



app = Flask(__name__)
CORS(app)
#home page route, dont think we need other routes for now.
@app.route('/')
def home():
    return "Welcome to the Chatter-Box Assistant Chat AI"




#note for jay, the only data we would need to send to frontend is just the response and 

if __name__ == '__main__':
    app.run(debug=True)


## switch api for the openAI -> Assistant API later ask for help with that.
## import os for env files.

##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:chatterbox.db' <-- this was wrong

##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db' <-- relative paths
##app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////chatterbox.db' <-- absolute paths

## need to create sqlite db.