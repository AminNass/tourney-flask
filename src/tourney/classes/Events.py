import json

from tourney.classes.Common import uniqueIDGenerator, log as log, saveDataDirectory as saveDir, removeWhitespace as remWs, isInCharLimit as limCheck, timeNow as now, zeroChar as zChar
import datetime

class Events:
    
    registry = {}
    nameCharLimit = 30
    saveDirectory = saveDir() / "Events"

    def __init__(self, identifier, name,
                 points=None, rankPoints=None,
                 allowMultipleRanks=False,
                 status=None, startTime=None, endTime=None):

        self.id = identifier
        self.name = name

        self.points = points
        self.rankPoints = rankPoints
        self.allowMultipleRanks = allowMultipleRanks

        self.status = status
        self.startTime = startTime
        self.endTime = endTime

        if points is None: self.points = {}
        if rankPoints is None: self.rankPoints = {}

    @classmethod
    def saveData(cls, autoSave=False):

        cls.saveDirectory.mkdir(parents=True, exist_ok=True)

        if autoSave:
            file = cls.saveDirectory / f"(autoSave) Events-{now()}.json"
        else:
            log("Attempting to save data for members", "INFO")
            file = cls.saveDirectory / "Events.json"

        eventsData = {}

        for event in cls.registry.values():

            startTimeStr = event.startTime.isoformat() if event.startTime else None
            endTimeStr = event.endTime.isoformat() if event.endTime else None

            eventsData[event.id] = {
                "name": event.name,
                "points": event.points,
                "rankPoints": event.rankPoints,
                "allowMultipleRanks": event.allowMultipleRanks,
                "status": event.status,
                "startTime": startTimeStr,
                "endTime": endTimeStr,
            }

        with open(file, "w") as f:
            json.dump(eventsData, f, indent=4)

        log(f"File at {file} has been saved", "SUCCESS")

    @classmethod
    def loadData(cls):

        file = cls.saveDirectory / "Events.json"

        if not file.exists():
            log("No save event data found")
            return

        with open(file, "r") as f:
            eventsData = json.load(f)

        failLoads = 0

        for eventID, eventInfo in eventsData.items():
            try:
                startTime = None
                endTime = None

                if eventInfo["startTime"]: startTime = datetime.datetime.fromisoformat(eventInfo["startTime"])
                if eventInfo["endTime"]: endTime = datetime.datetime.fromisoformat(eventInfo["endTime"])

                loadedEvent = cls(
                    identifier=eventID,
                    name=eventInfo["name"],
                    points=eventInfo["points"],
                    rankPoints=eventInfo["rankPoints"],
                    allowMultipleRanks=eventInfo["allowMultipleRanks"],
                    status=eventInfo["status"],
                    startTime=startTime,
                    endTime=endTime
                )

                cls.registry[loadedEvent.id] = loadedEvent
                log(f"Loaded event {loadedEvent.id}", "SUCCESS")

            except Exception as e:
                failLoads = failLoads + 1
                log(f"Failed to load event {eventID}: {e}", "ERROR")

            log(f"Successfully loaded {len(cls.registry)} / {len(cls.registry) + failLoads} events.", "SUCCESS")


    @classmethod
    def createEvent(cls, name):

        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name.lower() == remWs(name.lower()):
                log(f"The name: {name} already exists.", "ERROR")
                return "Name already exists."

        lim = cls.nameCharLimit

        if not limCheck(name, lim):
            log(f"Cannot create {name}, name is more than {lim} characters.", "ERROR")
            return f"Name must be below {lim} characters."

        unqiueId = uniqueIDGenerator(registry=cls.registry, prefix="EVENT")

        newEvent = cls(identifier=unqiueId, name=remWs(name))
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
    def changeInformation(cls, ob, newName=None):
        # Setting arguements to variable
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

        # This changes the information in the object already.
        editedEvent = cls.getEvent(id=ob.id)
        editedEvent.name = name

        # Returns the new updated object.
        return editedEvent
    
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
            # Checking for every value (Which is an object) in the regisry is the same as the name arugement.
                if ob.name == name:
                    # Returns when found the name.
                    return ob
        else:
            # Returns nothing when both arugments are None.
            log("No arguments was entered", "ERROR")
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
            startDateTime = datetime.datetime.now().replace(microsecond=0)
            log(f"{self.name} Event has started: {startDateTime}", "SUCCESS")
            self.startTime = startDateTime
            self.status = "Started"
            return "success"

        log(f"{self.name} Event is not ready yet", "ERROR")
        return "Event not ready yet"
    
    def endEvent(self):
        if self.status == "Started":
            endDateTime = datetime.datetime.now().replace(microsecond=0)
            log(f"{self.name} Event has ended: {endDateTime}", "SUCCESS")
            self.endTime = endDateTime
            self.status = "Ended"
            return "success"
        
        log(f"{self.name} Event has not started.", "ERROR")
        return "Event not started yet"
    
    def readyEvent(self):
        if self.status == "Ended" or self.status is None:
            self.points = {}
            self.status = "Ready"
            self.startTime = None
            self.endTime = None
            log(f"{self.name} Event is ready.", "SUCCESS")
            return "success"
        elif self.status == "Started":
            log(f"{self.name} Event cannot be ready when it has already started.", "ERROR")
            return "Event cannot be ready when it has already started."
        
        log(f"{self.name} Event is already ready.", "ERROR")
        return "Event is already ready yet"
    
    def eventLength(self):
        if self.status == "Started": return datetime.datetime.now().replace(microsecond=0) - self.startTime
            
        if self.status == "Ended": return self.endTime - self.startTime

        if self.status == "Ready":
            log(f"{self.name} Event cannot have a length when ready.", "ERROR")
        return None

    def rankSettings(self, ranks, points, allowMultipleRanks=None):

        self.rankPoints.clear()

        for rank, point in zip(ranks, points):
            self.rankPoints[rank] = point

        if not allowMultipleRanks is None: self.allowMultipleRanks = allowMultipleRanks

    def addTeam(self, team):

        if team.id in self.points:
            log(f"Team: {team} is already in this event", "ERROR")
            return f"{team.name} is already in this event"

        self.points[team.id] = 0
        return True

    def removeTeam(self, team):
        result = self.points.pop(team.id)
        if result is None:
            log(f"{team.name} Team not found", "ERROR")
            return f"{team.name} not found"
        else:
            log(f"Team found: {team}", "SUCCESS")
        return True

    def isTeamInEvent(self, team):
        return team.id in self.points.keys()

    def addRank(self, team, rank):

        if team.id not in self.points:
            log(f"Team: {team.name} is not in this event", "ERROR")
            return f"{team.name} is not in this event"
        elif not self.allowMultipleRanks:
            if team.id in self.points.keys():
                if self.points[team.id] > 0:
                    log(f"Team: {team.name} already gained a rank in this event", "ERROR")
                    return f"Team: {team.name} already gained a rank in this event (AllowMultipleRanks is set to False!)."

        points = self.rankPoints[rank] + self.points[team.id]
        self.points[team.id] = points
        log(f"Rank gained: {rank} points gained: {points}", "SUCCESS")
        return True

    def resetPoints(self, team):
        if team.id not in self.points:
            return "Team not in this event"
        self.points[team.id] = 0
        return True

    def removeRank(self, team, rank):

        if team.id not in self.points:
            log(f"Team: {team.name} is not in this event", "ERROR")
            return

        points = self.points[team.id] - self.rankPoints[rank]
        self.points[team.id] = points
        log(f"Rank removed: {rank} points removed: {points}")
        return

    def getAllTeamPoints(self):
        return self.points

    def getTeamPoints(self, team):

        if team.id not in self.points.keys(): return 0

        return self.points[team]

