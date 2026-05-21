

from tourney.classes import Teams as Teams, Members as Members
import os
from pathlib import Path


class Main:

    rootDirectory = Path(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self):
        print("Running...")
    
    def main(self):
        print("Hello World")

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

if __name__ == "__main__":
    app = Main()
    app.main()