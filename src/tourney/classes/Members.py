
from tourney.classes.Common import uniqueIDGenerator, saveDataDirectory as saveDir, log as log, removeWhitespace as remWs, isInCharLimit as limCheck, zeroChar as zChar, timeNow as now
import json

class Members:

    registry = {}
    nameCharLimit = 25
    saveDirectory = saveDir() / "Members"

    def __init__(self, identifier=None, username=None, firstname=None, lastname=None):
        """
        Init class for members. It allows for creating an instance of members class
        It shouldn't be used for creating members as it wouldn't be saved to the registry.
        :param identifier:
        :param username:
        :param firstname:
        :param lastname:
        """
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

        self.id = identifier

        # NOTES:
        # I should not call this class directly and always use its functions.
        # Otherwise, it will just create an object and not update the registry.

    # Save Data

    @classmethod
    def saveData(cls, autoSave=False):
        """
        This function saves data to the machines local user directory.
        :param autoSave:
        """
        # Check if directory exists
        cls.saveDirectory.mkdir(parents=True, exist_ok=True)

        # Define file that the members will be saved in.
        if autoSave:
            file = cls.saveDirectory / f"(autoSave) Members-{now()}.json"
        else:
            log("Attempting to save data for members", "INFO")
            file = cls.saveDirectory / "members.json"

        # Declare a dictionary to hold all members
        membersData = {}

        # Loop through the registry and add them to the dictionary.
        for user in cls.registry.values():
            # Using user.id as the unique key
            membersData[user.id] = {
                "Username": user.username,
                "Firstname": user.firstname,
                "Lastname": user.lastname
            }

        # Write the dictionary into the json file.
        with open(file, "w") as f:
            json.dump(membersData, f, indent=4)

        log(f"File at {file} has been saved", "SUCCESS")

    @classmethod
    def loadData(cls):
        """
        This function loads all member data into the registry.
        :return:
        """
        file = cls.saveDirectory / "members.json"

        # Check if file exists
        if not file.exists():
            log("No saved member data found.", "INFO")
            return

        # Open the json and load it
        with open(file, "r") as f:
            membersData = json.load(f)

        # Declared to record the failed loading attempts.
        failLoads = 0

        # Loop through the dictionary
        # userID is the key, MembersData is the value in the dictionary.
        for userID, memberInfo in membersData.items():
            try:
                # Recreate member objects.
                loadedMember = cls(
                    identifier=userID,
                    username=memberInfo["Username"],
                    firstname=memberInfo["Firstname"],
                    lastname=memberInfo["Lastname"]
                )

                # Add it to the dictionary.
                cls.registry[loadedMember.id] = loadedMember
                log(f"Member '{loadedMember.username}' loaded.", "SUCCESS")

            except KeyError as e:
                failLoads = failLoads + 1
                log(f"Failed to load user {userID} due to missing field: {e}", "ERROR")

        log(f"Successfully loaded {len(cls.registry)} / {len(cls.registry) + failLoads} members.", "SUCCESS")

    #
    # Class Methods
    #

    # Class method that creates a member.
    @classmethod
    def createMember(cls, username, firstname, lastname):
        """
        This function creates a member. This is then saved in the registry.
        This function will always return the new member object with creation is successful.
        If not successful, it will return an error message as a string.
        :param username:
        :param firstname:
        :param lastname:
        :return:
        """

        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the username argument.
            if ob.username.lower() == username.lower():
                log(f"The Username: {username} already exists.", "ERROR")
                return "Username already exists."

        lim = cls.nameCharLimit

        if not limCheck(username, lim) or not limCheck(firstname, lim) or not limCheck(lastname, lim):
            log(f"Cannot create {username}, user, firstname or lastname is more than {lim} characters.", "ERROR")
            return f"All names must be below {lim} characters."

        # Generates a unqiue ID.
        unqiueId = uniqueIDGenerator(registry=cls.registry, prefix="USER")

        # Then it creates a new object of itself (cls) and puts in the arguments.
        # Added " ".join(text.split()) to remove white space and extra spaces.
        newMember = cls(identifier=unqiueId, username=remWs(username), firstname=remWs(firstname), lastname=remWs(lastname))

        # Adds the member to the registry.
        cls.registry[unqiueId] = newMember
        log(f"Member '{username}' created.", "SUCCESS")
        # Returns the new member to né used in the main class.
        return newMember

    # class method to remove a member.
    @classmethod
    def removeMember(cls, ob):
        """
        This function removes a member from the registry.
        When successful it will return True, if not successful then it will return an error message as a string.\n
        * This function handles removal of members from teams.
        :param ob:
        :return:
        """
        def removeMemberFromTeams(memberID):
            from tourney.classes import Teams as Teams

            log("Attempting to remove member from teams.")

            teams = list(Teams.Teams.getTeamRegistry().values())

            for team in teams:
                for teamMemberID in team.members:
                    if teamMemberID == memberID:
                        log(f"Found Member in team: {team.name}", "SUCCESS")
                        team.members.remove(memberID)



        # It pops out the ID from the registry. The pop() function returns return when successful.
        removedUser = cls.registry.pop(ob.id, None)

        # Checks if it was successfully popped out. If False then username is not in the registry
        if removedUser:
            log(f"Member: {ob.username} removed", "SUCCESS")

            removeMemberFromTeams(ob.id)

            return True
        else:
            log(f"Member: {ob.username} not found", "ERROR")
            return "Member not found"

    # class method to change member information
    @classmethod
    def changeInformation(cls, ob, newUsername=None, newFirstName=None, newLastname=None):
        # Setting arguements to variable
        username = zChar(newUsername)
        firstname = zChar(newFirstName)
        lastname = zChar(newLastname)

        lim = cls.nameCharLimit

        if not limCheck(newUsername, lim) or not limCheck(newFirstName, lim) or not limCheck(newLastname, lim):
            log(f"Cannot edit {ob.username}, user, firstname or lastname is more than {cls.nameCharLimit} characters.", "ERROR")
            return f"All names entered must be below {cls.nameCharLimit} characters."

        # Keeps data that hasn't been changed.
        if username is None: username = ob.username
        else:
            for nob in cls.registry.values():
                # Checking for every value (Which is an object) in the registry is the same as the username argument.
                if nob.username.lower() == username.lower():
                    log(f"The Username: {newUsername} already exists.", "ERROR")
                    return "Username already exists."


        if firstname is None: firstname = ob.firstname
        if lastname is None: lastname = ob.lastname

        # Create a new object of itself:
        # Makes sure that the identifier stays the same by taking it from the original object.
        # Then updates the username, firstname and lastname.
        newMember = cls(identifier=ob.id, username=username, firstname=firstname, lastname=lastname)

        # Updates the registry, using the id.
        cls.registry[ob.id] = newMember
        # Returns the new updated object.
        return newMember

    # Class method that returns object from username
    @classmethod
    def getMember(cls, id=None, username=None):
        # This gives 2 options for getting the object of the member.

        # Runs when there is something other than None in the ID arguement.
        if not id == None:
            # Loops through every value in the member registry.
            for ido in cls.registry.values():
                # Compares the id found in the object with the ID arguement.
                if ido.id == id:
                    # Return the value in the registry (Which is the object).
                    return ido
        # Runs when id is none and username is something other than None.
        elif not username == None:
            for ob in cls.registry.values():
            # Checking for every value (Which is an object) in the regisry is the same as the username arugement.
                if ob.username.lower() == username.lower():
                    # Returns when found the name.
                    log(f"User found: {username}", "SUCCESS")
                    return ob
        else:
            # Returns nothing when both arguments are None.
            log(f"No arguments was entered", "ERROR")
            return "No member arguments were entered."
            
        # Returns None when no Member is found in the registry with the ID or Username.
        log(f"No member was found using the Username:, {username} or the ID:, {id}", "ERROR")
        return f"No member with the username: {username} or the ID:, {id} was found."

    @classmethod
    def getMemberRegistry(cls):
        # Returns the entire registry
        return cls.registry

    # App functions

    @classmethod
    def formatData(cls):
        data = [[],[],[],[]]

        IDsList = list(cls.registry.keys())

        # Append to data list

        for ID in IDsList:
            memberData = cls.getMember(id=ID)

            data[0].append(memberData.id)
            data[1].append(memberData.username)
            data[2].append(memberData.firstname)
            data[3].append(memberData.lastname)

        rowData = list(zip(*data))
        log(f"Successfully formatted data:\n {rowData}", "SUCCESS")
        return rowData
    #
    # Object Functions
    #

    # Function to get the member info
    def getMemberInfo(self):
        # Returns the username, firstname and lastname.
        return [self.id, self.username, self.firstname, self.lastname]