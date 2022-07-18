from flask import Flask

#uuid is for session tokens

app = Flask(__name__)
from endpoints import login, bot, streamStatus