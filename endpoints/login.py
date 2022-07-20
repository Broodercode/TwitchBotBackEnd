from helpers.db_helpers import run_query
import bcrypt
from flask import request, jsonify
from app import app
import requests
from env import BEARER, CLIENT_ID


@app.post('/login')
def user_login():
    print('app post reached')

    salt = bcrypt.gensalt()
    data = request.json
    email = data.get('email')
    twitch_username = data.get('twitch_username')
    raw_pw = data.get('password')
    password = bcrypt.hashpw(raw_pw.encode(), salt)
    #use database error
    emailCheck = run_query("SELECT email FROM clients WHERE email = ?", [email])

    url = 'https://api.twitch.tv/helix/users?login=' + twitch_username
    headers = {'Authorization': BEARER, 'Client-Id': CLIENT_ID}
    print(email, password, twitch_username, url)
    res = requests.get(url=url, headers=headers).json()
    
    id = res['data'][0]['id']
    print(res['data'][0]['id'])

    if not email or not password or not twitch_username:
        return jsonify('Missing required field'), 422
    elif len(emailCheck) != 0:
        return jsonify('username or email already exists'), 422
    elif len(res['data']) == 0:
        return jsonify('twitch user does not exist')
    else:
        run_query("INSERT INTO clients (email,password,client_id) VALUES(?,?,?)", [email, password, id])
        return jsonify('added successfully')