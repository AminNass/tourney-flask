import datetime

from tourney.classes import Teams as Teams, Members as Members, Events as Events, Tourney as Tourney
from tourney.app.App import App as AppModule
from tourney.classes.Common import log as log, getDataDirectory as dataDir

# Main Class
class Main:

    rootDirectory = dataDir()
    saveDirectory = rootDirectory / "saveData"


    def __init__(self):
        self.appModule = AppModule("Tourney", "home")

    def run(self):
        log(f"Starting app: {datetime.datetime.now()}", "SUCCESS")
        self.onInitialize()

    def onInitialize(self):

        # Load logic here, just pre creating for testing.

        Members.Members.loadData()

        log(f"Dictionary check: {list(Members.Members.getMemberRegistry())}")

        log(Members.Members.getMember(username="JoeC").lastname)

        Teams.Teams.createTeam("Team Falcons")

        Teams.Teams.getTeam(name="Team Falcons").addMember(Members.Members.getMember(username="MikeAhhh"))

        RLCS = Tourney.Tourney.createTourney("RLCS")

        RLCS.addEvent("RLCS Major", Events.Events.createEvent("Major"))

        log(Members.Members.formatData())

        self.appModule.startWindow()




if __name__ == "__main__":
    app = Main()
    app.run()
