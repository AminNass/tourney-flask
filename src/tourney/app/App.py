from flask import Flask, render_template, jsonify, request
import webview
import threading
from tkinter import messagebox
import tkinter as tk

from tourney.classes.Common import log as log, saveAllData as saveAll
from tourney.classes import Members as Members, Teams as Teams, Events as Events, Tourney as Tourney

# Flask

class App:
    def __init__(self, name, loadhtml):
        self.name = "Tourney"
        self.loadhtml = loadhtml
        self.app = Flask(__name__)
        self.appMenus()
        self.appAPI()
        self.window = webview.create_window(self.name, self.app, width=800, height=600, resizable=False)
        self.window.events.closing += self.onClosing
        self.exitMenuOpened = False


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

            return render_template(
                "members.html",
                members=list(Members.Members.getMemberRegistry().values())
            )

        @self.app.route("/teams")
        def teams():
            log(f"Getting ready to load page: teams.html")
            self.changeTitle("Teams")

            teams = list(Teams.Teams.getTeamRegistry().values())
            members = list(Members.Members.getMemberRegistry().values())

            for team in teams:
                # Declaring team member info object.
                log(f"getting member data for team {team}")
                teamMembers = team.members
                team.membersInfo = []
                team.memberCount = len(teamMembers)
                for teamMember in teamMembers:
                    # Appending team member info into each team.
                    log(f"getting member data for team {team.name}, for member {teamMember}")
                    memberInfo = Members.Members.getMember(id=teamMember).getMemberInfo()
                    team.membersInfo.append(memberInfo)

            return render_template(
                "teams.html",
                teams=teams
            )

        @self.app.route("/events")
        def events():
            log(f"Getting ready to load page: events.html")
            self.changeTitle("Events")

            events = list(Events.Events.getTeamRegistry().values())

            return render_template(
                "events.html",
                events=events
            )

        @self.app.route("/tourneys")
        def tourneys():
            log(f"Getting ready to load page: tourney.html")
            self.changeTitle("Tourney")

            tourneys = list(Tourney.Tourney.getTourneyRegistry().values())

            for tourney in tourneys:
                tourney.eventCount = len(tourney.events)

            return render_template(
                "tourney.html",
                tourneys=tourneys
            )

        @self.app.route("/tourney/manager/<tourneyid>")
        def tourneyManager(tourneyid):

            tourney = Tourney.Tourney.getTourney(id=tourneyid)

            if not isinstance(tourney, Tourney.Tourney):
                return tourneys()

            tourney.overallPoints = tourney.getAllTeamPoints()

            return render_template(
                "tourneyManager.html",
                tourney=tourney
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

        @self.app.route("/api/getMemberByID", methods=["GET"])
        def getUserByID():
            data = request.get_json()
            foundMember = Members.Members.getMember(id=data.get("memberID"))
            return jsonify(foundMember.getMemberInfo())

        @self.app.route(f"/api/createTeam", methods=["POST"])
        def createTeam():
            log("Received request to create a new team")

            data = request.get_json()
            name = data.get("name")

            if not name:
                log("Failed to create member: Missing Fields", "ERROR")
                return jsonify({"status": "error", "message": "All fields are required"})

            newTeam = Teams.Teams.createTeam(name)

            if isinstance(newTeam, Teams.Teams):
                return jsonify({"status": "success", "message": f"Member with username: {newTeam.name} has been created."})
            else:
                return jsonify({"status": "error", "message": f"{newTeam}"})

        @self.app.route("/api/editTeam", methods=["POST"])
        def editTeam():
            log("Received request to edit a team")

            data = request.get_json()

            TeamObject = Teams.Teams.getTeam(id=data.get("teamID"))

            newName = data.get("name")

            editedMember = Teams.Teams.changeInformation(TeamObject, newName)

            if isinstance(editedMember, Teams.Teams):
                return jsonify({"status": "success", "message": f"Member with username: {editedMember.name} has been edited."})
            else:
                return jsonify({"status": "error", "message": f"{editedMember}"})

        @self.app.route("/api/deleteTeam", methods=["POST"])
        def deleteTeam():
            log("Received request to delete a team")

            data = request.get_json()

            deletedMember = Teams.Teams.removeTeam(Teams.Teams.getTeam(id=data.get("teamID")))

            if deletedMember:
                return jsonify({"status": "success", "message": f"Team with name: {data.get("name")} has been deleted."})
            else:
                return jsonify({"status": "error", "message": f"Could not find name in registry."})

        @self.app.route("/api/removeTeamMember", methods=["POST"])
        def deleteTeamMember():
            log("Received request to remove a team member")

            data = request.get_json()

            teamID = data.get("teamID")
            memberID = data.get("memberID")

            log(f"{teamID}, {memberID}")

            teamObject = Teams.Teams.getTeam(id=teamID)

            teamObject.removeMember(memberID)

            return jsonify({"status": "success", "message": f"Removed member in team: {teamObject.name}."})

        @self.app.route("/api/addTeamMember", methods=["POST"])
        def addTeamMember():
            log("Received request to add a team member")

            data = request.get_json()

            teamID = data.get("teamID")
            username = data.get("username")

            teamObject = Teams.Teams.getTeam(id=teamID)

            memberObject = Members.Members.getMember(username=username)

            if isinstance(memberObject, Members.Members):
                result = teamObject.addMember(memberObject)
                if result is True: return jsonify({"status": "success", "message": f"Added member ({memberObject.username}) in team: {teamObject.name}."})
                else: return jsonify({"status": "error", "message": f"{result}"})
            else: return jsonify({"status": "error", "message": f"{memberObject}"})

        @self.app.route("/api/saveTeams", methods=["POST"])
        def saveTeams():
            log("Received request to save members.")

            Teams.Teams.saveData()

            return jsonify({"status": "success", "message": f"Saved teams successfully."})

        @self.app.route(f"/api/createEvent", methods=["POST"])
        def createEvent():
            log("Received request to create a new event")

            data = request.get_json()
            name = data.get("name")

            if not name:
                log("Failed to create member: Missing Fields", "ERROR")
                return jsonify({"status": "error", "message": "All fields are required"})

            newEvent = Events.Events.createEvent(name)

            if isinstance(newEvent, Events.Events):
                return jsonify(
                    {"status": "success", "message": f"Member with username: {newEvent.name} has been created."})
            else:
                return jsonify({"status": "error", "message": f"{newEvent}"})

        @self.app.route("/api/editEvent", methods=["POST"])
        def editEvent():
            from tourney.classes.Common import zeroChar as zChar

            log("Received request to edit a event")

            data = request.get_json()

            EventObject = Events.Events.getEvent(id=data.get("eventID"))

            newRankPoints = data.get("rankPoints")

            newName = zChar(data.get("name"))

            EventObject.rankSettings(newRankPoints.keys(), newRankPoints.values(), data.get("allowMultipleRanks"))

            if not newName is None:
                editedMember = Events.Events.changeInformation(EventObject, newName)

                if isinstance(editedMember, Events.Events):

                    return jsonify({"status": "success", "message": f"Member with username: {editedMember.name} has been edited."})
                else:
                    return jsonify({"status": "error", "message": f"{editedMember}"})

            return jsonify({"status": "success", "message": f"Member with name: {EventObject.name} rankSettings has been edited."})


        @self.app.route("/api/deleteEvent", methods=["POST"])
        def deleteEvent():
            log("Received request to delete a event")

            data = request.get_json()

            deletedMember = Events.Events.delEvent(Events.Events.getEvent(id=data.get("eventID")))

            if deletedMember:
                return jsonify({"status": "success", "message": f"Event with name: {data.get("name")} has been deleted."})
            else:
                return jsonify({"status": "error", "message": f"Could not find name in registry."})

        @self.app.route("/api/saveEvents", methods=["POST"])
        def saveEvents():
            log("Received request to save events.")

            Events.Events.saveData()

            return jsonify({"status": "success", "message": f"Saved teams successfully."})

        @self.app.route("/api/changeTourneyEvent", methods=["POST"])
        def changeTourneyEvent():
            log("Received request to change tourney event information/")

            data = request.get_json()

            tourneyID = data.get("tourneyID")
            eventID = data.get("eventID")
            newName = data.get("eventName")

            log(f"{tourneyID}, {eventID}, {newName}")

            tourney = Tourney.Tourney.getTourney(id=tourneyID)

            tourneyEvent = tourney.getEvent(id=eventID)

            result = tourney.changeEvent(newName, tourneyEvent)

            if isinstance(result, Events.Events):
                return jsonify({"status": "success", "message": f"Event with name: {data.get("name")} has been deleted."})

            return jsonify({"status": "error", "message": f"{result}"})

        @self.app.route("/api/changeTourneyEventStatus", methods=["POST"])
        def changeTourneyEventStatus():
            log("Received request to change tourney event status")

            data = request.get_json()
            tourneyID = data.get("tourneyID")
            eventID = data.get("eventID")
            status = data.get("status")

            tourney = Tourney.Tourney.getTourney(id=tourneyID)
            tourneyEvent = tourney.getEvent(id=eventID)

            result = None

            if status == "Start": result = tourneyEvent.startEvent()
            elif status == "End":result = tourneyEvent.endEvent()
            elif status == "Ready":result = tourneyEvent.readyEvent()
            if result == "success":
                log(f"Successfully changed tourney event to {status}", "SUCCESS")
                return jsonify({"status": "success", "message": f"Status has successfully changed to {status}"})

            return jsonify({"status": "error", "message": f"{result}"})

        @self.app.route("/api/getTourneyEventLength", methods=["GET"])
        def getTourneyEventLength():
            log("Received request to get tourney event length")

            tourneyID = request.args.get("tourneyID")
            eventID = request.args.get("eventID")

            tourney = Tourney.Tourney.getTourney(id=tourneyID)
            tourneyEvent = tourney.getEvent(id=eventID)

            result = str(tourneyEvent.eventLength())

            return jsonify({"status": "success", "message": f"{result}"})




    def startWindow(self):
        log(f"Window started successfully", "SUCCESS")
        webview.start()
        log(f"Window closed successfully", "SUCCESS")

    def onClosing(self):

        if self.exitMenuOpened: return False

        log(f"Attempting to close App.")

        self.exitMenuOpened = True

        root = tk.Tk()
        root.withdraw()

        prompt = messagebox.askyesnocancel("Saves Changes", "Do you want to save changes?")
        root.destroy()

        if prompt:
            log("Exiting with saving changes.", "SUCCESS")
            saveAll()
            self.exitMenuOpened = False
            return True
        elif prompt == False:
            log("Exiting without saving changes.", "SUCCESS")
            self.exitMenuOpened = False
            return True
        else:
            log("Exit canceled", "SUCCESS")
            self.exitMenuOpened = False
            return False

    def changeTitle(self, title):

        def executeTitleChange(title):
            self.window.title = f"Tourney - {title}"
            log(f"Changed title to {title}", "SUCCESS")

        threading.Thread(target=executeTitleChange, args=(title,), daemon=True).start()