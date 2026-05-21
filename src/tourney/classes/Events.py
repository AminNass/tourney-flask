from tourney.classes import Common as Common
import datetime

class Events:
    
    registry = {}

    def __init__(self, master=None, identifier=None, name=None):
        self.id = identifier

        self.name = name

        self.points = {}

    @classmethod
    def createEvent(cls, name):

        for ob in cls.registry.values():
        # Checking for every value (Which is a object) in the regisry is the same as the name arugement.
            if ob.name == name:
                print("The name:", name, "already exists.")
                return None
            
        unqiueId = Common.uniqueIDGenerator(registry=cls.registry, prefix="EVENT")

        newEvent = cls(master=cls, identifier=unqiueId, name=name)
        newEvent.status = "Ready"

        cls.registry[unqiueId] = newEvent
        print(f"Team '{name}' created.")

        return newEvent
    
    @classmethod
    def delEvent(cls, ob):
        # It pops out the ID from the registry. The pop() function returns true when sucessfull.
        deletedEvents = cls.registry.pop(ob.id, None)

        # Checks if it was sucessfully popped out. If False then team is not in the registry
        if deletedEvents:
            print("Team:", ob.name, "removed")
            return True
        else:
            print("Team:", ob.name, "not found")
            return False
    
    @classmethod
    def getTeam(cls, id=None, name=None):

        # This gives 2 options for getting the object of the event.

        # Runs when there is something other than None in the ID arguement.
        if not id == None:
            # Loops through every value in the event registry.
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
            print("No arguements was entered")
            return None
            
        # Returns None when no event is found in the registry with the ID or Username.
        print("No event was found with the name:", name, "or the ID:", id)
        return None
    
    @classmethod
    def getTeamRegistry(cls):
        # Return the entire team registry
        return cls.registry
    
    #
    #  Object Methods
    #

    def startEvent(self):

        if self.status == "Ready":
            startDateTime = datetime
            print(self.name,"Event has started:", startDateTime)
            self.startTime = startDateTime
            self.status = "Started"

            print(self.name, "Event is not ready yet")
            return    

        print()
        return
    
    def endEvent(self):
        if self.status == "Started":
            endDateTime = datetime
            print(self.name,"Event has ended:", endDateTime)
            self.endTime = endDateTime
            self.status = "Ended"
            return
        
        print(self.name, "Event has not started.")
        return
    
    def readyEvent(self):
        if self.status == "Ended":
            self.points = {}
            self.status = "Ready"
            print(self.name, "Event is ready.")
            return
        elif self.status == "Started":
            print(self.name, "Event cannot be ready when it has already started.")
            return
        
        print(self.name, "Event is already ready.")
        return
    
    def eventLength(self):
        if self.status == "Started": return datetime - self.startTime
            
        if self.status == "Ended": return self.startTime - self.endTime

        if self.status == "Ready":
            print(self.name, "Event cannot have a length when ready.")
            return