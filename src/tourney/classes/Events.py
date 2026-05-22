from tourney.classes import Common as Common
from tourney.classes.Common import log as log
import datetime

class Events:
    
    registry = {}

    def __init__(self, master=None, identifier=None, name=None):
        self.id = identifier

        self.name = name

        self.points = {}
        self.rankPoints = {}
        self.addMultipleRanks = False

        self.status = None
        self.startTime = None
        self.endTime = None

    @classmethod
    def createEvent(cls, name):

        for ob in cls.registry.values():
        # Checking for every value (Which is a object) in the regisry is the same as the name arugement.
            if ob.name == name:
                log(f"The name: {name} already exists.", "ERROR")
                return None
            
        unqiueId = Common.uniqueIDGenerator(registry=cls.registry, prefix="EVENT")

        newEvent = cls(master=cls, identifier=unqiueId, name=name)
        newEvent.status = "Ready"

        cls.registry[unqiueId] = newEvent
        log(f"Team '{name}' created.")

        return newEvent
    
    @classmethod
    def delEvent(cls, ob):
        # It pops out the ID from the registry. The pop() function returns true when successful.
        deletedEvents = cls.registry.pop(ob.id, None)

        # Checks if it was sucessfully popped out. If False then team is not in the registry
        if deletedEvents:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return False
    
    @classmethod
    def getEvent(cls, id=None, name=None):

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
            log("No arguements was entered", "ERROR")
            return None
            
        # Returns None when no event is found in the registry with the ID or Username.
        log(f"No event was found with the name: {name} or the ID: {id}", "ERROR")
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
            startDateTime = datetime.datetime.now()
            log(f"{self.name} Event has started: {startDateTime}", "SUCCESS")
            self.startTime = startDateTime
            self.status = "Started"
            return

        log(f"{self.name} Event is not ready yet", "ERROR")
        return
    
    def endEvent(self):
        if self.status == "Started":
            endDateTime = datetime.datetime.now()
            log(f"{self.name} Event has ended: {endDateTime}", "SUCCESS")
            self.endTime = endDateTime
            self.status = "Ended"
            return
        
        log(f"{self.name} Event has not started.", "ERROR")
        return
    
    def readyEvent(self):
        if self.status == "Ended":
            self.points = {}
            self.status = "Ready"
            log(f"{self.name} Event is ready.", "SUCCESS")
            return
        elif self.status == "Started":
            log(f"{self.name} Event cannot be ready when it has already started.", "ERROR")
            return
        
        log(f"{self.name} Event is already ready.", "ERROR")
        return
    
    def eventLength(self):
        if self.status == "Started": return datetime.datetime.now() - self.startTime
            
        if self.status == "Ended": return self.startTime - self.endTime

        if self.status == "Ready":
            log(f"{self.name} Event cannot have a length when ready.", "ERROR")
            return

    def rankSettings(self, ranks, points):

        # Set removes duplicates. The application will check already. This is a fail-safe.
        setRanks = set(ranks)

        for rank in setRanks:
            self.rankPoints[rank] = points
        return

    def addTeam(self, team):

        if team in self.points:
            log(f"Team: {team} is already in this event", "ERROR")
            return

        self.points[team] = 0
        return

    def removeTeam(self, team):
        result = self.points.pop(team)
        if result == None:
            log(f"{team} Team not found", "ERROR")
        else:
            log(f"Team found: {team}", "SUCCESS")
        return

    def addRank(self, team, rank):

        if team not in self.points:
            log(f"Team: {team} is not in this event", "ERROR")
            return
        elif not self.addMultipleRanks:
            if self.rankPoints[team] > 0:
                log(f"Team: {team} already gained a rank in this event", "ERROR")

        points = self.rankPoints[rank] + self.points[team]
        self.points[team] = points
        log(f"Rank gained: {rank} points gained: {points}", "SUCCESS")
        return

    def removeRank(self, team, rank):

        if team not in self.points:
            log(f"Team: {team} is not in this event", "ERROR")
            return

        points = self.points[team] - self.rankPoints[rank]
        self.points[team] = points
        log(f"Rank removed: {rank} points removed: {points}")
        return

    #debug

