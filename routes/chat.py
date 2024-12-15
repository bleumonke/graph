from flask import Blueprint, jsonify

chat = Blueprint('chat', __name__)

@chat.route('/', methods=['GET'])
def chat_check():
    return jsonify({'message': 'chat is working!'}), 200