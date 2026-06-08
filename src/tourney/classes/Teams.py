import json
from typing import Self

import tourney.classes.Members
from tourney.classes.Common import uniqueIDGenerator, saveDataDirectory as saveDir, log as log, removeWhitespace as remWs, isInCharLimit as limCheck, zeroChar as zChar, timeNow as now


class Teams:
    registry = {}
    saveDirectory = saveDir() / "Teams"
    nameCharLimit = 25

    def __init__(self,
                 identifier: str | None = None,
                 name: str | None = None,
                 members: str | None = None
                 ):
        """
        Init class for Teams. Allows object creation for teams.
        This should not be used to create new teams as it won't appear in the registry.
        :param identifier:
        :param name:
        :param members:
        """
        self.name = name
        self.id = identifier

        if members is None: members = []
        self.members = members

    # Save Data

    @classmethod
    def saveData(cls, autoSave=False):
        """
        Function for saving Teams data to the local user save directory.
        :param autoSave:
        """
        cls.saveDirectory.mkdir(parents=True, exist_ok=True)

        if autoSave:
            file = cls.saveDirectory / f"(autoSave) Teams-{now()}.json"
        else:
            log("Attempting to save data for teams.", "INFO")
            file = cls.saveDirectory / "Teams.json"

        teamsData = {}

        for team in cls.registry.values():

            # Conditionally save based on whether it is an individual team or standard team
            if hasattr(team, 'members'):
                teamsData[team.id] = {
                    "name": team.name,
                    "members": team.members
                }
            else:
                teamsData[team.id] = {
                    "name": team.name,
                    "member": team.member
                }

        with open(file, "w") as f:
            json.dump(teamsData, f, indent=4)

    @classmethod
    def loadData(cls):
        """
        This loads data from the local user save directory.
        :return:
        """
        file = cls.saveDirectory / "Teams.json"

        if not file.exists():
            log("No Teams data found.", "INFO")
            return

        with open(file, "r") as f:
            teamsData = json.load(f)

        # Declared to record the failed loading attempts.
        failLoads = 0

        for teamID, teamInfo in teamsData.items():
            try:
                # Check the dictionary keys to determine how to recreate the object
                if "members" in teamInfo:
                    loadedTeam = cls(
                        identifier=teamID,
                        name=teamInfo["name"],
                        members=teamInfo["members"]
                    )
                else:
                    loadedTeam = cls(
                        identifier=teamID,
                        name=teamInfo["name"]
                    )
                    del loadedTeam.members
                    loadedTeam.member = teamInfo.get("member")

                cls.registry[loadedTeam.id] = loadedTeam
                log(f"Team '{loadedTeam.name}' loaded.", "SUCCESS")

            except KeyError as e:
                failLoads = failLoads + 1
                log(f"({failLoads}) Failed to load user {teamID} due to missing field: {e}", "ERROR")

            log(f"Successfully loaded {len(cls.registry)} / {len(cls.registry) + failLoads} teams.", "SUCCESS")

    #
    # Class Functions
    #

    @classmethod
    def createTeam(cls, name: str, type: str | None = None) -> str | Self:
        """
        This method creates a member, handles name lengths, whitespace and duplicate names.\n
        * Changing the type to 'I' removes 'members' variable and creates 'member' variable.
        :param name:
        :param type:
        :return:
        """
        for ob in cls.registry.values():
            # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name.lower() == remWs(name.lower()):
                log(f"The Team name: {name} already exists.", "ERROR")
                return "Name already exists."

        prefix = "TEAM"

        if type == "I": prefix = "I.TEAM"

        lim = cls.nameCharLimit

        if not limCheck(name, lim):
            log(f"Cannot create [{prefix}: {name}], name is more than {lim} characters.", "ERROR")
            return f"Name must be below {lim} characters."

        # Generates a unique ID.
        uniqueId = uniqueIDGenerator(registry=cls.registry, prefix=prefix)
        # creates a new team as an object.
        newTeam = cls(identifier=uniqueId, name=remWs(name))
        if type == "I":
            del newTeam.members
            newTeam.member = None

        # Adds new team to registry.
        cls.registry[uniqueId] = newTeam
        log(f"Team '{name}' created.", "SUCCESS")
        # Returns the new team to be used in the main class.
        return newTeam

    @classmethod
    def removeTeam(cls, ob: Self) -> bool | str:
        """
        This removes team from registry.
        :param ob:
        :return:
        """
        # It pops out the ID from the registry. The pop() function returns return when successful.
        removedTeam = cls.registry.pop(ob.id, None)

        # Checks if it was sucessfully popped out. If False then team is not in the registry
        if removedTeam:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return f"Team {ob.name} not found"

    @classmethod
    def changeInformation(cls, ob: Self, newName: str | None = None) -> Self | str:
        """
        This changes information for a Team.
        :param ob:
        :param newName:
        :return:
        """
        # Setting arguments to variable
        name = zChar(newName)

        if name is None:
            name = ob.name
            return "You did not enter any name."

        lim = cls.nameCharLimit

        if not limCheck(newName, lim):
            log(f"Cannot edit {ob.name}, name is more than {cls.nameCharLimit} characters.",
                "ERROR")
            return f"The name entered must be below {cls.nameCharLimit} characters."

        for nob in cls.registry.values():
            # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if nob.name.lower() == name.lower():
                log(f"The Username: {newName} already exists.", "ERROR")
                return "Username already exists."

        # Update name
        editedTeam = cls.getTeam(id=ob.id)
        editedTeam.name = name

        # Updates the registry, using the id.
        # cls.registry[ob.id] = newTeam
        # Returns the new updated object.
        return editedTeam

    @classmethod
    def getTeam(cls, id: str | None = None, name: str | None = None) -> Self | str:
        """
        This method gets and returns the team object from the registry
        :param id:
        :param name:
        :return:
        """
        # This gives 2 options for getting the object of the team.

        # Runs when there is something other than None in the ID argument.
        if not id is None:
            # Loops through every value in the team registry.
            for ido in cls.registry.values():
                # Compares the id found in the object with the ID argument.
                if ido.id == id:
                    # Return the value in the registry (Which is the object).
                    return ido
        # Runs when id is none and name is something other than None.
        elif not name is None:
            for ob in cls.registry.values():
                # Checking for every value (Which is a object) in the registry is the same as the name argument.
                if ob.name == name:
                    # Returns when found the name.
                    return ob
        else:
            # Returns nothing when both arguments are None.
            log(f"No arguments was entered", "ERROR")
            return "No arguments was entered."

        # Returns None when no team is found in the registry with the ID or Username.
        log(f"No team was found with the name: {name} or the ID: {id}", "ERROR")
        return f"No team was found with the name: {name} or the ID: {id}"

    @classmethod
    def getTeamRegistry(cls) -> dict[str, Self]:
        """
        Returns team registry.
        :return:
        """
        return cls.registry

    #
    # Object Functions
    #

    def addMember(self, *args: tourney.classes.Members.Members) -> bool | str:
        """
        This method adds members the team. You can pass multiple members at once.\n
        * If your adding a member to an individual team it will replace the original Member.
        :param args:
        :return:
        """
        # *ARGS: This is a list of Members, the code works find if you just put one.

        # Loops for every member in this team
        if hasattr(self, 'members'):
            for i in self.members:
                # Loops through every Member ID
                for j in args:
                    if i == j.id:
                        log(f"{j.username}, is already a member of {self.name}", "ERROR")
                        return f"The member {j.username} is already a member of this team."

            for i in args:
                self.members.append(i.id)
            log(f"Member(s) has been added.", "SUCCESS")
        else:
            self.member = args[0].id
            log(f"Member has been added.", "SUCCESS")
        return True

    # This function expects ids.
    # I made it like java for loop.
    def removeMember(self, *args: tourney.classes.Members.Members) -> bool:
        """
        This function removes from the team and supports multiple members.\n
        * This method doesn't throw an error (skips member) when a Member is not in the team.
        :param args:
        :return:
        """
        if hasattr(self, 'members'):
            for i in args:
                for j in range(len(self.members)):
                    log(f"{j}, {i}: {len(self.members)}.")
                    if i == self.members[j]:
                        self.members.pop(j)
                        log(f"REMOVED: {i} {j}: {len(self.members)}", "SUCCESS")
                        break
                    log(f"{i} cannot be found in members: Skipping", "ERROR")
            log(f"Member(s) has been removed.", "SUCCESS")
        else:
            self.member = None
            log(f"Member has been removed.", "SUCCESS")

        return True

    def getMembers(self) -> list[tourney.classes.Members.Members] | tourney.classes.Members.Members | None:
        """
        Returns all members in the team.
        :return:
        """
        from tourney.classes import Members as Members

        foundMembers = []

        # Get Member registry
        memberRegistry = Members.Members.getMemberRegistry()

        if hasattr(self, 'members'):

            # Loop through every member inside of this team.
            for mId in self.members:
                # Check if the Ids in member registry.
                if mId in memberRegistry:
                    # When found I'd, get the value using the mId.
                    memberObject = memberRegistry[mId]
                    foundMembers.append(memberObject)
                else:
                    log(f"Id not found in Member registry: {mId} not found.")
        else:
            if self.member in memberRegistry:
                foundMembers = memberRegistry[self.member]
            else:
                log(f"Id not found in Member registry: {self.member} not found.")
                return None

        # Returns a list of Member objects.
        return foundMembers