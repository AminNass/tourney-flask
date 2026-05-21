from tourney.classes import Teams as Teams, Members as Members, Events as Events, Tourney as Tourney
from tourney.app import App as AppModule
import os
from pathlib import Path

# Main Class
class Main:

    rootDirectory = Path(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        print("Running...")

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

        print(f"Dictionary check: {list(Members.Members.getMemberRegistry())}")

        print(Members.Members.getMember(username="JoeC").lastname)

        Teams.Teams.createTeam("Team Falcons")

        Teams.Teams.getTeam(name="Team Falcons").addMember(Members.Members.getMember(username="MikeA"))

        RLCS = Tourney.Tourney.createTourney("RLCS")

        RLCS.addEvent("RLCS Major", Events.Events.createEvent("Major"))


if __name__ == "__main__":
    app = Main()
    app.run()
