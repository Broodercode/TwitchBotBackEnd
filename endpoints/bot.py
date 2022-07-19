from helpers.db_helpers import run_query
from flask import request
from app import app
from env import BEARER, CLIENT_ID


headers = {'Authorization': BEARER, 'Client-Id': CLIENT_ID}

@app.post('/api/bot')
def bot_post():
    print('bot post reached')
    
    #message information
    data = request.json
    msg_id = data.get('msg_id')
    content = data.get('content')
    user_id = data.get('user_id')
    room_id = data.get('room_id')
    created_at = data.get('created_at')
    user_handle = data.get('user_handle')
    message_data = [msg_id, content, user_id, room_id, created_at, user_handle]
    

    run_query("INSERT INTO messages (message_id, content, user_id, room_id, created_at, user_handle) VALUES(?,?,?,?,?,?)", message_data)
    return 'success'