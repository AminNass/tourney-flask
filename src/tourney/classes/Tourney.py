import json
from typing import Self, Any

import tourney.classes.Teams
from tourney.classes import Events
from tourney.classes.Common import uniqueIDGenerator, log as log, removeWhitespace as remWs, isInCharLimit as limCheck, zeroChar as zChar, saveDataDirectory as saveDir, timeNow as now
import copy

class Tourney:

    registry = {}
    nameCharLimit = 100
    saveDirectory = saveDir() / "Tourneys"

    def __init__(self, identifier=None, name=None, events=None):
        """
        This is the init for the class tourney which creates a tourney object.
        This shouldn't be used to create a tourney as it doesn't add it to the registry.
        :param identifier:
        :param name:
        :param events:
        """
        self.id = identifier

        self.name = name

        self.events = events

        if events is None: self.events = {}

    # Save and load data

    @classmethod
    def saveData(cls, autoSave=False):
        """
        Function for saving data to local save directory.
        :param autoSave:
        """
        cls.saveDirectory.mkdir(parents=True, exist_ok=True)

        if autoSave:
            file = cls.saveDirectory / f"(autoSave) Tourneys-{now()}.json"
        else:
            log("Attempting to save data for tourneys.", "INFO")
            file = cls.saveDirectory / "Tourneys.json"

        tourneysData = {}

        for tourney in cls.registry.values():

            eventDict = {}
            # Loop through the event objects inside this tournament and extract their data
            for eventID, event in tourney.events.items():
                startTimeStr = event.startTime.isoformat() if event.startTime else None
                endTimeStr = event.endTime.isoformat() if event.endTime else None

                eventDict[eventID] = {
                    "name": event.name,
                    "points": event.points,
                    "rankPoints": event.rankPoints,
                    "allowMultipleRanks": event.allowMultipleRanks,
                    "status": event.status,
                    "startTime": startTimeStr,
                    "endTime": endTimeStr,
                }

            tourneysData[tourney.id] = {
                "name": tourney.name,
                "events": eventDict
            }

        with open(file, "w") as f:
            json.dump(tourneysData, f, indent=4)

        log(f"File at {file} has been saved", "SUCCESS")

    @classmethod
    def loadData(cls):
        """
        Function for loading tourney data from local save directory.
        :return:
        """
        from tourney.classes import Events as Events
        from datetime import datetime

        file = cls.saveDirectory / "Tourneys.json"

        if not file.exists():
            log("No Tourneys data found.", "INFO")
            return

        with open(file, "r") as f:
            tourneysData = json.load(f)

        failLoads = 0

        for tourneyID, tourneyInfo in tourneysData.items():
            try:
                loadedTourney = cls(
                    identifier=tourneyID,
                    name=tourneyInfo["name"]
                )

                # Reconstruct the events dictionary full of Event objects
                loadedEvents = {}
                for eventID, eventInfo in tourneyInfo.get("events", {}).items():
                    startTime = None
                    endTime = None

                    if eventInfo["startTime"]: startTime = datetime.fromisoformat(eventInfo["startTime"])
                    if eventInfo["endTime"]: endTime = datetime.fromisoformat(eventInfo["endTime"])

                    # Recreate the event object using the Events class
                    loadedEvent = Events.Events(
                        identifier=eventID,
                        name=eventInfo["name"],
                        points=eventInfo["points"],
                        rankPoints=eventInfo["rankPoints"],
                        allowMultipleRanks=eventInfo["allowMultipleRanks"],
                        status=eventInfo["status"],
                        startTime=startTime,
                        endTime=endTime
                    )
                    loadedEvents[eventID] = loadedEvent

                loadedTourney.events = loadedEvents

                cls.registry[loadedTourney.id] = loadedTourney
                log(f"Tourney '{loadedTourney.name}' loaded.", "SUCCESS")

            except Exception as e:
                failLoads = failLoads + 1
                log(f"({failLoads}) Failed to load tourney {tourneyID} due to error: {e}", "ERROR")

        log(f"Successfully loaded {len(cls.registry)} / {len(cls.registry) + failLoads} tourneys.", "SUCCESS")

    #
    # Class methods
    #

    @classmethod
    def createTourney(cls, name: str) -> Self | str:
        """
        This function creates a tourney. Name duplication checks are in place.
        Tourney is automatically added to the registry.
        :param name:
        :return:
        """
        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name == name:
                log(f"The tourney: {name} already exists.", "ERROR")
                return f"The tourney: {name} already exists."
            
        uniqueId = uniqueIDGenerator(registry=cls.registry, prefix="TRN")

        newTourney = cls(identifier=uniqueId, name=name)

        cls.registry[uniqueId] = newTourney
        log(f"Team '{name}' created.", "SUCCESS")

        return newTourney
    
    @classmethod
    def delTourney(cls, ob: Self) -> bool | str:
        """
        This function deletes a tourney from the registry.
        :param ob:
        :return:
        """
        # It pops out the ID from the registry. The pop() function returns true when successful.
        removedTourney = cls.registry.pop(ob.id)

        # Checks if it was successfully popped out. If False then team is not in the registry
        if removedTourney:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return f"Team: {ob.name} not found"
    
    @classmethod
    def getTourney(cls, id: str | None = None, name: str | None = None) -> Self | str:
        """
        This function gets and returns the tourney search the registry with the id or name.
        :param id:
        :param name:
        :return:
        """
        # This gives 2 options for getting the object of the tourney.

        # Runs when there is something other than None in the ID argument.
        if not id == None:
            # Loops through every value in the tourney registry.
            for ido in cls.registry.values():
                # Compares the id found in the object with the ID argument.
                if ido.id == id:
                    # Return the value in the registry (Which is the object).
                    return ido
        # Runs when id is none and name is something other than None.
        elif not name == None:
            for ob in cls.registry.values():
            # Checking for every value (Which is an object) in the registry is the same as the name argument.
                if ob.name == name:
                    # Returns when found the name.
                    return ob
        else:
            # Returns nothing when both arguments are None.
            log(f"No arguments was entered", "ERROR")
            return "No arguments entered"
            
        # Returns None when no Member is found in the registry with the ID or Username.
        log(f"No tourney was found with the name: {name} or the ID: {id}", "ERROR")
        return "No tourney found"

    @classmethod
    def getTourneyRegistry(cls) -> dict[str, Self]:
        """
        This function returns the tourney registry.
        :return:
        """
        return cls.registry

    #
    # Object Functions
    #

    def addEvent(self, name: str, ob: Events.Events) -> Events.Events | str:
        """
        This function adds an event to the tourney. This WILL create a HARD COPY of this Event meaning changes
        to this event later will not appear inside of this tourney. Instead, you can get this event from this tourney
        and make changes there. This event is stored inside of this tourney Events dictionary.
        :param name:
        :param ob:
        :return:
        """
        # Checks if this event name already exists in this tournament.
        for event in self.events.values():
            if event.name.lower() == name.lower():
                log(f"The Event: {name} already exists in this tournament.", "ERROR")
                return f"The Event: {name} already exists in this tournament."

        # Creates a deep copy of this instance.
        # This is so that if the original instance is changed in any way it will not affect this new instance.
        # Changes to this instance will not change the original either.
        newInstance = copy.deepcopy(ob)
        newInstance.name = name
        # This changes the name of the event.
        # This can be anything that is not already inside the self.events

        # Generates a unique ID with the prefix T.EVENT
        uniqueID = uniqueIDGenerator(registry=self.events, prefix="T.EVENT")

        self.events[uniqueID] = newInstance
        return newInstance
    
    def removeEvent(self, ob: Events.Events) -> bool | str:
        """
        This will remove the event from the tourney permanently deleting it.
        :param ob:
        :return:
        """
        removedEvent = self.events.pop(ob.id, None)

        # Checks if it was successfully popped out. If False then team is not in the registry
        if removedEvent:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return f"Team: {ob.name} not found"
    
    def getEvent(self, id: str | None= None, name: str | None = None) -> Events.Events | str:
        """
        This function will get the event found in the event dictionary of ths tourney.
        :param id:
        :param name:
        :return:
        """
        # This gives 2 options for getting the object of the event.

        # Runs when there is something other than None in the ID argument.
        if not id is None:
            # Loops through every value in the event registry.
            for ido in self.events.keys():
                # Compares the id found in the object with the ID argument.
                if ido == id:
                    # Return the value in the registry (Which is the object).
                    return self.events[ido]
        # Runs when id is none and name is something other than None.
        elif not name is None:
            for ob in self.events.values():
            # Checking for every value (Which is an object) in the registry is the same as the name argument.
                if ob.name == name:
                    # Returns when found the name.
                    return ob
        else:
            # Returns nothing when both arguments are None.
            log(f"No arguments was entered", "ERROR")
            return "No arguments was entered"
        
        # Returns None when no event is found in the registry with the ID or Username.
        log(f"No event was found with the name: {name} or the ID: {id} in this tournament.", "ERROR")
        return f"No event was found with the name: {name} or the ID: {id} in this tournament."

    def changeEvent(self, name: str, ob: Events.Events) -> Events.Events | str:
        """
        This will change the event info for an event that is inside of this tourney. 
        :param name: 
        :param ob: 
        :return: 
        """
        

        lim = Events.Events.nameCharLimit

        newName = remWs(name)

        if zChar(newName) is None:
            return ob

        for event in self.events.keys():
            if event.lower() == newName.lower():
                log(f"The Event: {newName} already exists in this tournament.", "ERROR")
                return f"{newName} already exists"

        if not limCheck(newName, lim):
            log(f"{newName} is above {lim} characters.", "ERROR")
            return f"{newName} is above {lim} characters."

        ob.name = newName

        return ob

    def getAllTeamPoints(self) -> dict[str, int]:
        """
        This will get all the team points for every event in this tourney.
        :return: 
        """
        from collections import Counter

        totalPoints = {}

        for event in self.events.values():
            totalPoints = dict(Counter(totalPoints) + Counter(event.getAllTeamPoints()))

        log(totalPoints, "SUCCESS")
        return totalPoints

    def getTeamPoints(self, team: tourney.classes.Teams.Teams) -> int:
        """
        This function will get the total event points in every event in this tourney for a team.
        :param team: 
        :return: 
        """
        totalPoints = 0

        for event in self.events.values():
            if not event.isTeamInEvent(team=team): continue

            totalPoints = totalPoints + event.getTeamPoints(team=team)

        log(totalPoints, "SUCCESS")
        return totalPoints

    def checkEventDeletion(self) -> list[str]:
        """
        This function will go through every single event in the event registry and check if an event ID that is in this
        tourney does not exist in the event registry. Meaning the original event most of been deleted.
        :return: 
        """
        # Gets events registry
        eventsRegistry = Events.Events.registry
        missingEvents = []

        for eventObject in self.events.values():
            # gets id of object
            id = eventObject.id
            # Gets the value using that id in the events' registry.
            result = eventsRegistry.get(id)
            # if there isn't an id found it will return none.
            if result is None:
                log(f"[{self.name}]: Missing event found: {id}")
                self.removeEvent(eventObject)
                missingEvents.append(id)
            else:
                log(f"[{self.name}]: Found ID: {id} is in events registry.")
        return missingEvents

        
    
