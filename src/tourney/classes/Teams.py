from tourney.classes import Members as Members, Common as Common
from tourney.classes.Common import log as log

class Teams:

    registry = {}

    def __init__(self, master=None, identifier=None, name=None):
        self.name = name
        self.id = identifier

        self.members = []

    #
    # Class Functions
    #

    @classmethod
    def createTeam(cls, name, type=None):

        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name == name:
                log(f"The Team name: {name} already exists.", "ERROR")
                return None

        prefix = "TEAM"

        if type == "I": prefix = "I.TEAM"

        # Generates a unqiue ID.
        unqiueId = Common.uniqueIDGenerator(registry=cls.registry, prefix=prefix)
        # creates a new team as an object.
        newTeam = cls(master=cls, identifier=unqiueId, name=name)
        if type == "I":
            del newTeam.members
            newTeam.member = None

        # Adds new team to registry.
        cls.registry[unqiueId] = newTeam
        log(f"Team '{name}' created.", "SUCCESS")
        # Returns the new team to be used in the main class.
        return newTeam

    @classmethod
    def removeTeam(cls, ob):
        # It pops out the ID from the registry. The pop() function returns return when sucessfull.
        removedTeam = cls.registry.pop(ob.id, None)

        # Checks if it was sucessfully popped out. If False then team is not in the registry
        if removedTeam:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return False


    @classmethod
    def getTeam(cls, id=None, name=None):

        # This gives 2 options for getting the object of the team.

        # Runs when there is something other than None in the ID arguement.
        if not id == None:
            # Loops through every value in the team registry.
            for ido in cls.registry.values():
                # Compares the id found in the object with the ID arguement.
                if ido.id == id:
                    # Return the value in the registry (Which is the object).
                    return ido
        # Runs when id is none and name is something other than None.
        elif not name == None:
            for ob in cls.registry.values():
            # Checking for every value (Which is a object) in the regisry is the same as the name arugement.
                if ob.name == name:
                    # Returns when found the name.
                    return ob
        else:
            # Returns nothing when both arugments are None.
            log(f"No arguements was entered", "ERROR")
            return None
            
        # Returns None when no team is found in the registry with the ID or Username.
        log(f"No team was found with the name: {name} or the ID: {id}", "ERROR")
        return None


    @classmethod
    def getTeamRegistry(cls):
        return cls.registry

    #
    # Object Functions
    #

    def addMember(self, *args):
        # *ARGS: This is a list of Members, the code works find if you just put one.

        # Loops for every member in this team
        for i in self.members:
            # Loops through every Member ID
            for j in args:
                if i == j.id:
                    log(f"{j}, is already a member of {i}", "ERROR")
                    return None
        
        for i in args:
            self.members.append(i.id)
        log(f"Member(s) has been added.", "SUCCESS")
        return None
    
    def removeMember(self, *args):
        
        for i in args:
            for j in range(len(self.members) - 1):
                if i == self.members[j]:
                    self.members.pop(j)
                    continue
                log(f"{i.username} cannot be found in members: Skipping", "ERROR")
        log(f"Member(s) has been removed.", "SUCCESS")
        return

    def getMembers(self):
        foundMembers = []
        # Get Member registry
        memberRegistry = Members.Members.getMemberRegistry()

        # Loop through every member inside of this team.
        for mId in self.members:
            # Check if the Ids in member registry.
            if mId in memberRegistry:
                # When found Id, get the value using the mId.
                memberObject = memberRegistry[mId]
                foundMembers.append(memberObject)
            else:
                log(f"Id not found in Member registry: {mId} not found.")

        # Returns a list of Member objects.
        return foundMembers