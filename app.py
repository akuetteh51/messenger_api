from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify
import os
import datetime

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'vitacheck.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)



@app.route('/api/user', methods=['POST'])
def user():
    data=request.get_json() 
    name=data["name"]
    # Retrieve the message data from the database
    user=User(name=name)
    db.session.add(user)
    db.session.commit()

    return jsonify({"status":200})

@app.route('/api/message', methods=['POST'])
def message():
    data=request.get_json() 
    text=data["text"]
    sender_id=data["sender_id"]
    receiver_id=data["receiver_id"]
    message = Message(text=text, sender_id=sender_id, recipient_id=receiver_id, chat_id=1)
    db.session.add(message)
    db.session.commit()
    return jsonify({"status":200})

@app.route('/api/messages', methods=['GET'])
def get_messages():
    # Retrieve the message data from the database
   
    messages = Message.query.all()

    # Serialize the message data
    result = [{'sender': message.sender_id, 'recipient': message.recipient_id, 'message': message.message} for message in messages]

    # Return a response
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

