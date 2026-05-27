from flask import Flask, render_template, jsonify, request
import webview
import threading

from tourney.classes.Common import log as log
from tourney.classes import Members as Members, Teams as Teams, Events as Events, Tourney as Tourney, Common as Common

# Flask

class App:
    def __init__(self, name, loadhtml):
        self.name = "Tourney"
        self.loadhtml = loadhtml
        self.app = Flask(__name__)
        self.appMenus()
        self.appAPI()
        self.window = webview.create_window(self.name, self.app, width=800, height=600, resizable=False)

        log(f"Created app: {name}, load page set to {loadhtml}.html", "SUCCESS")

    def appMenus(self):

        # Menus

        @self.app.route("/")
        def launch():
            log(f"Getting ready to load page: loading.html")
            return render_template(
                "loading.html",
                loadhtml=self.loadhtml
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
            log(f"Getting ready to load page: members.html")
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

    def appAPI(self):

        @self.app.route(f"/api/createMember", methods=["POST"])
        def createMember():
            log("Received request to create a new member")

            data = request.get_json()
            username = data.get("username")
            firstname = data.get("firstname")
            lastname = data.get("lastname")

            if not username or not firstname or not lastname:
                log("Failed to create member: Missing Fields", "ERROR")
                return jsonify({"status": "error", "message": "All fields are required"})

            newMember = Members.Members.createMember(username, firstname, lastname)

            if isinstance(newMember, Members.Members):
                return jsonify({"status": "success", "message": f"Member with username: {newMember.username} has been created."})
            else:
                return jsonify({"status": "error", "message": f"{newMember}"})

        @self.app.route("/api/editMember", methods=["POST"])
        def editMember():
            log("Received request to edit a member")

            data = request.get_json()

            MemberObject = Members.Members.getMember(id=data.get("memberID"))

            newUsername = data.get("username")
            newFirstname = data.get("firstname")
            newLastname = data.get("lastname")

            editedMember = Members.Members.changeInformation(MemberObject, newUsername, newFirstname, newLastname)

            if isinstance(editedMember, Members.Members):
                return jsonify({"status": "success", "message": f"Member with username: {editedMember.username} has been edited."})
            else:
                return jsonify({"status": "error", "message": f"{editedMember}"})

        log(f"Loaded API", "SUCCESS")

        @self.app.route("/api/deleteMember", methods=["POST"])
        def deleteMember():
            log("Received request to delete a member")

            data = request.get_json()

            deletedMember = Members.Members.removeMember(Members.Members.getMember(id=data.get("memberID")))

            if deletedMember:
                return jsonify({"status": "success", "message": f"Member with username: {data.get("username")} has been deleted."})
            else:
                return jsonify({"status": "error", "message": f"Could not find member in registry."})

        @self.app.route("/api/saveMembers", methods=["POST"])
        def saveMembers():
            log("Received request to save members.")

            Members.Members.saveData()

            return jsonify({"status": "success", "message": f"Saved members successfully."})

    def startWindow(self):
        log(f"Window started successfully", "SUCCESS")
        webview.start()
        log(f"Window closed successfully", "SUCCESS")

    def changeTitle(self, title):

        def executeTitleChange(title):
            self.window.title = f"Tourney - {title}"
            log(f"Changed title to {title}", "SUCCESS")

        threading.Thread(target=executeTitleChange, args=(title,), daemon=True).start()