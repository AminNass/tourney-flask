import datetime

from tourney.classes import Teams as Teams, Members as Members, Events as Events, Tourney as Tourney
from tourney.app import App as AppModule
from tourney.classes.Common import log as log
import os
from pathlib import Path

# Main Class
class Main:

    rootDirectory = Path(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        log(f"Program started at {datetime.datetime.now()}", "SUCCESS")

    def run(self):
        app = AppModule.createApp()
        Main.onInitialize(self, app)

        AppModule.createWindow("Tourney", app)



    def onInitialize(self, app):

        # Load logic here, just pre creating for testing.

        Members.Members.createMember(
            username="Jack223",
            firstname="JJack",
            lastname="Stone"
        )

        Members.Members.createMember(
            username="MikeA",
            firstname="Mike",
            lastname="Afton"
        )

        Members.Members.createMember(
            username="JoeC",
            firstname="Joe",
            lastname="Clark"
        )

        log(f"Dictionary check: {list(Members.Members.getMemberRegistry())}")

        log(Members.Members.getMember(username="JoeC").lastname)

        Teams.Teams.createTeam("Team Falcons")

        Teams.Teams.getTeam(name="Team Falcons").addMember(Members.Members.getMember(username="MikeA"))

        RLCS = Tourney.Tourney.createTourney("RLCS")

        RLCS.addEvent("RLCS Major", Events.Events.createEvent("Major"))


if __name__ == "__main__":
    app = Main()
    app.run()
