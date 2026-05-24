import threading

from flask import Flask, render_template

import webview
from tourney.classes.Common import log as log
from tourney.classes import Members as Members, Teams as Teams, Events as Events, Tourney as Tourney, Common as Common

# Flask

class App:
    def __init__(self, name, loadhtml):
        self.name = "Tourney"
        self.loadhtml = loadhtml
        self.app = Flask(__name__)
        self.appMenus()
        self.window = webview.create_window(self.name, self.app, width=800, height=600, resizable=False)

        log(f"Created app: {name}, load page set to {loadhtml}.html", "SUCCESS")

    def appMenus(self):

        @self.app.route("/")
        def launch():
            log(f"Getting ready to load page: loading.html")
            return render_template(
                "loading.html",
                loadhtml="home"
            )

        @self.app.route("/home")
        def home():
            log(f"Getting ready to load page: home.html")
            self.changeTitle("Home")

            memberList = list(Members.Members.getMemberRegistry())
            return render_template(
                "home.html",
                members=memberList
            )

        @self.app.route("/members")
        def members():
            log(f"Getting ready to load page: home.html")
            self.changeTitle("Members")

            #memberData = Members.Members.formatData()

            return render_template(
                "members.html",
                members=list(Members.Members.getMemberRegistry().values())
            )

        @self.app.route("/about")
        def about():
            log(f"Getting ready to load page: about.html")
            self.changeTitle("About")

            return render_template(
                "about.html"
            )

        log(f"Loaded all menus", "SUCCESS")

    def startWindow(self):
        webview.start()
        log(f"Window started.", "SUCCESS")

    def changeTitle(self, title):

        def executeTitleChange(title):
            self.window.title = f"Tourney - {title}"
            log(f"Changed title to {title}", "SUCCESS")

        threading.Thread(target=executeTitleChange, args=(title,), daemon=True).start()