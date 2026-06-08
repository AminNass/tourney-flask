import json
from typing import Any, Self

import tourney.classes.Teams
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
        """
        Class init code to create an event object. Shouldn't be used to create an Event.\n
        * These arguments must be present for data loading (loadData() just creates an Event Object with these arguments).
        :param identifier: 
        :param name: 
        :param points: 
        :param rankPoints: 
        :param allowMultipleRanks: 
        :param status: 
        :param startTime: 
        :param endTime: 
        """
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
        """
        Function to save data to local save directory.
        :param autoSave: 
        """
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
        """
        Function to load data from local save directory.
        :return: 
        """
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
    def createEvent(cls, name: str) -> Self | str:
        """
        This function creates a new event and adds it to the registry.
        :rtype: str | Self
        """
        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name.lower() == remWs(name.lower()):
                log(f"The name: {name} already exists.", "ERROR")
                return "Name already exists."

        lim = cls.nameCharLimit

        if not limCheck(name, lim):
            log(f"Cannot create {name}, name is more than {lim} characters.", "ERROR")
            return f"Name must be below {lim} characters."

        uniqueId = uniqueIDGenerator(registry=cls.registry, prefix="EVENT")

        newEvent = cls(identifier=uniqueId, name=remWs(name))
        newEvent.status = "Ready"

        cls.registry[uniqueId] = newEvent
        log(f"Team '{name}' created.")

        return newEvent
    
    @classmethod
    def delEvent(cls, ob: Self) -> bool | str:
        """
        This function delete and Event from the registry.
        :param ob: 
        :return: 
        """
        # It pops out the ID from the registry. The pop() function returns true when successful.
        deletedEvents = cls.registry.pop(ob.id, None)

        # Checks if it was successfully popped out. If False then team is not in the registry
        if deletedEvents:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return f"{ob.name} not found"

    @classmethod
    def changeInformation(cls, ob: Self, newName: str | None = None):
        """
        This function changes information in an event.
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

        # This changes the information in the object already.
        editedEvent = cls.getEvent(id=ob.id)
        editedEvent.name = name

        # Returns the new updated object.
        return editedEvent
    
    @classmethod
    def getEvent(cls, id: str | None = None, name: str | None = None) -> Self | str:
        """
        This function get and returns the event using the id or name.
        :param id: 
        :param name: 
        :return: 
        """
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
            return "No arguments was entered"
            
        # Returns None when no event is found in the registry with the ID or Username.
        log(f"No event was found with the name: {name} or the ID: {id}", "ERROR")
        return f"No event was found with the name: {name} or the ID: {id}"
    
    @classmethod
    def getTeamRegistry(cls) -> dict[str, Self]:
        """
        Returns the Team Registry.
        :return: 
        """
        # Return the entire team registry
        return cls.registry
    
    #
    #  Object Methods
    #

    def startEvent(self) -> str:
        """
        This function starts the Event.\n
        * Returns 'success' when the event has started, if not then a error as a string.
        :return: 
        """
        if self.status == "Ready":
            startDateTime = datetime.datetime.now().replace(microsecond=0)
            log(f"{self.name} Event has started: {startDateTime}", "SUCCESS")
            self.startTime = startDateTime
            self.status = "Started"
            return "success"

        log(f"{self.name} Event is not ready yet", "ERROR")
        return "Event not ready yet"
    
    def endEvent(self) -> str:
        """
        This function ends the Event.\n
        * Returns 'success' when the event has ended, if not then an error as a string.
        :return: 
        """
        if self.status == "Started":
            endDateTime = datetime.datetime.now().replace(microsecond=0)
            log(f"{self.name} Event has ended: {endDateTime}", "SUCCESS")
            self.endTime = endDateTime
            self.status = "Ended"
            return "success"
        
        log(f"{self.name} Event has not started.", "ERROR")
        return "Event not started yet"
    
    def readyEvent(self) -> str:
        """
        This function ready the Event.\n
        * Returns 'success' when the event has ready, if not then an error as a string.
        :return: 
        """
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
    
    def eventLength(self) -> datetime.datetime | None:
        """
        This function gets event length. If event has started it will return the length between when the event has started and now.
        If the event has ended it will return the length between when the event has started and ended.
        if ready then will return None.
        :return: 
        """
        if self.status == "Started": return datetime.datetime.now().replace(microsecond=0) - self.startTime
            
        if self.status == "Ended": return self.endTime - self.startTime

        if self.status == "Ready":
            log(f"{self.name} Event cannot have a length when ready.", "ERROR")
        return None

    def rankSettings(self, ranks: list[str], points: list[int], allowMultipleRanks: bool | None = None):
        """
        This function allows for modification of rank settings. This is what allows to allocate a rank to an amount of points.
        To use this you must pass through a list of ranks and a list of points. The rank you want the amount of points must be
        the same index as the amount of points you want.\n
        * Allow multiple ranks makes sure extra points cannot be added when the points are more than 0 for a team.
        :param ranks: 
        :param points: 
        :param allowMultipleRanks: 
        """
        self.rankPoints.clear()

        for rank, point in zip(ranks, points):
            self.rankPoints[rank] = point

        if not allowMultipleRanks is None: self.allowMultipleRanks = allowMultipleRanks

    def addTeam(self, team: tourney.classes.Teams.Teams) -> bool | str:
        """
        This function adds a team to an event. All it does is add it to the points variable with the amount of points set to 0.
        :param team: 
        :return: 
        """
        if team.id in self.points:
            log(f"Team: {team.name} is already in this event", "ERROR")
            return f"{team.name} is already in this event"

        self.points[team.id] = 0
        return True

    def removeTeam(self, team: tourney.classes.Teams.Teams) -> bool | str:
        """
        This function will remove a team from the Event removing all its points.
        :param team: 
        :return: 
        """
        result = self.points.pop(team.id)
        if result is None:
            log(f"{team.name} Team not found", "ERROR")
            return f"{team.name} not found"
        else:
            log(f"Team found: {team.name}", "SUCCESS")
        return True

    def isTeamInEvent(self, team: tourney.classes.Teams.Teams) -> bool:
        """
        This function returns true or false if a team is in this evnet.
        :param team: 
        :return: 
        """
        return team.id in self.points.keys()

    def addRank(self, team: tourney.classes.Teams.Teams, rank: str) -> bool | str:
        """
        This function adds a rank to a team for this event. Each rank gives an amount of points.\n
        * Ranks and its amount of points must be allocated to this event using rankSettings() function.
        :param team: 
        :param rank: 
        :return: 
        """
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

    def resetPoints(self, team: tourney.classes.Teams.Teams) -> bool | str:
        """
        This function resets the points for a team by setting the amount of points to 0.
        :param team: 
        :return: 
        """
        if team.id not in self.points:
            return "Team not in this event"
        self.points[team.id] = 0
        return True

    def removeRank(self, team: tourney.classes.Teams.Teams, rank: str) -> bool | str:
        """
        This function will remove a rank from a team by just subtracting the amount of points that rank gives.
        :param team: 
        :param rank: 
        :return: 
        """
        if team.id not in self.points:
            log(f"Team: {team.name} is not in this event", "ERROR")
            return f"Team: {team.name} is not in this event"

        points = self.points[team.id] - self.rankPoints[rank]
        self.points[team.id] = points
        log(f"Rank removed: {rank} points removed: {points}")
        return True

    def getAllTeamPoints(self) -> dict[str, int]:
        """
        Returns the points dictionary containing all participating teams and their amount of points.
        :return: 
        """
        return self.points

    def getTeamPoints(self, team: tourney.classes.Teams.Teams) -> int:
        """
        Returns the amount of points for a particular team.
        :param team: 
        :return: 
        """
        if team.id not in self.points.keys(): return 0

        return self.points[team.id]

