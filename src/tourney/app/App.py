from flask import Flask, render_template

import webview

from tourney.classes import Members as Members, Teams as Teams, Events as Events, Tourney as Tourney, Common as Common

# Flask
def createApp():
    app = Flask(__name__)

    @app.route("/")
    @app.route("/home")
    def home():

        memberList = list(Members.Members.getMemberRegistry())
        return render_template(
            "home.html",
            members=memberList
        )

    return app

def createWindow(name, app):
    webview.create_window(name, app)
    webview.start()