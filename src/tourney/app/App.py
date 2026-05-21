from flask import Flask, render_template

import webview
import threading

from tourney.classes.Members import Members as Members
from tourney.classes.Teams import Teams as Teams
from tourney.classes.Events import Events as Events
from tourney.classes.Tourney import Tourney as Tourney

# Flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def start_flask():
    # Run Flask on a specific port
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    webview.create_window("Tourney", "http://127.0.0.1:5000")
    webview.start()