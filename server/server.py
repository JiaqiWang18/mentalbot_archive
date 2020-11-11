from flask import Flask, request, abort, render_template
from flask_cors import CORS
from .chat import chat

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/chat")
def chat_api():
    key = request.args.get('key')
    inp = request.args.get('input')

    if not key or key != "wfefh4jyt":
        abort(403)
    if not inp or inp == "":
        abort(500)
    return chat('server/trainDataAndModel/model.tflearn','server/trainDataAndModel/data.pickle','server/tags.json',inp)
