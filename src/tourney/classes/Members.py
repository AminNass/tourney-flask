from tourney.classes import Common as Common
from tourney.classes.Common import log as log
from tourney import Main as Main
import json
from pathlib import Path

class Members:

    registry = {}
    saveDirectory = Main.Main.rootDirectory / "saveData" / "members"

    def __init__(self, master=None, identifier=None, username=None, firstname=None, lastname=None):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

        self.id = identifier

        # NOTES:
        # I should not call this class directly and always use its functions.
        # Otherwise, it will just create an object and not update the registry.

    # Save Data

    @classmethod
    def saveData(cls):
        # Getting root directory
        cls.saveDirectory.mkdir(parents=True, exist_ok=True) 

        for user in cls.registry.values():
            memberData = {
                "_comment": "Changing the id WILL break things.",
                "ID": user.id,
                "Username": user.username,
                "Firstname": user.firstname,
                "Lastname": user.lastname
            }

            # Creates filename
            fileName = f"({user.id}) {user.username}.json"
            with open(cls.saveDirectory / fileName, "w") as f:
                json.dump(memberData, f, indent=4)

            log(f"{fileName} SAVED", "SUCCESS")

    @classmethod
    def loadData(cls):
        # Define the directory path
        saveDirectory = Path(Main.Main.rootDirectory) / "saveData" / "members"

        # Check if the directory exists to avoid errors.
        if not saveDirectory.exists():
            log("No save data directory found.", "ERROR")
            return

        # Loop through every .json file in the folder
        for filePath in saveDirectory.glob("*.json"):
            try:
                with open(filePath, "r") as f:
                    data = json.load(f)

                # Reconstruct the member object
                loadedMember = cls(
                    identifier=data["ID"],
                    username=data["Username"],
                    firstname=data["Firstname"],
                    lastname=data["Lastname"]
                )

                # 5. Add it back into the registry dictionary
                cls.registry[loadedMember.id] = loadedMember
            
                log(f"Loaded member: {loadedMember.username}", "SUCCESS")
            
            except Exception as e:
                log(f"Failed to load {filePath.name}: {e}", "ERROR")
    
    #
    # Class Methods
    #

    # Class method that creates a member.
    @classmethod
    def createMember(cls, username, firstname, lastname):

        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the username arugement.
            if ob.username == username:
                log(f"The Username: {username} already exists.", "ERROR")
                return None

        # Generates a unqiue ID.
        unqiueId = Common.uniqueIDGenerator(registry=cls.registry, prefix="USER")
        
        # Then it creates a new object of itself (cls) and puts in the arguements.
        newMember = cls(master=cls, identifier=unqiueId, username=username, firstname=firstname, lastname=lastname)

        # Adds the member to the registry.
        cls.registry[unqiueId] = newMember
        log(f"Member '{username}' created.", "SUCCESS")
        # Returns the new member to né used in the main class.
        return newMember

    # class method to remove a member.
    @classmethod
    def removeMember(cls, ob):
        # It pops out the ID from the registry. The pop() function returns return when sucessfull.
        removedUser = cls.registry.pop(ob.id, None)

        # Checks if it was sucessfully popped out. If False then username is not in the registry
        if removedUser:
            log(f"Member: {ob.username} removed", "SUCCESS")
            return True
        else:
            log(f"Member: {ob.username} not found", "ERROR")
            return False

    # class method to change member information
    @classmethod
    def changeInformation(cls, ob, newUsername=None, newFirstName=None, newLastname=None):
        # Setting arguements to variables
        username = newUsername
        firstname = newFirstName
        lastname = newLastname

        # Keeps data that hasnt been changed.
        if newUsername == None: username = ob.username
        if newFirstName == None: firstname = ob.firstname
        if newLastname == None: lastname = ob.lastname

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
                if ob.username == username:
                    # Returns when found the name.
                    log(f"User found: {username}", "SUCCESS")
                    return ob
        else:
            # Returns nothing when both arguments are None.
            log(f"No arguements was entered", "ERROR")
            return None
            
        # Returns None when no Member is found in the registry with the ID or Username.
        log(f"No member was found using the Username:, {username} or the ID:, {id}", "ERROR")
        return None

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