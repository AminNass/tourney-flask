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

        Teams.Teams.loadData()

        Events.Events.loadData()

        Tourney.Tourney.loadData()

        self.appModule.startWindow()




if __name__ == "__main__":
    app = Main()
    app.run()
