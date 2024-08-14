from flask import Flask, request, jsonify
import openai
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

##loading my environment variables
from dotenv import load_dotenv 
load_dotenv()
##

app = Flask(__name__)
CORS(app)

## SQL LITE db things
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatterbox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

## End SQL db things

## loading the API key through an ENV file 
openai.api_key = os.getenv('OPEN_AI_API_KEY')

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