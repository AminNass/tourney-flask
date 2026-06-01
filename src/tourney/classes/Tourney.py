from tourney.classes.Common import uniqueIDGenerator, log as log, removeWhitespace as remWs, isInCharLimit as limCheck, zeroChar as zChar
import copy

class Tourney:

    registry = {}
    nameCharLimit = 100

    def __init__(self, identifier=None, name=None, events=None):
        self.id = identifier

        self.name = name

        self.events = events

        if events is None: self.events = {}

    @classmethod
    def createTourney(cls, name):
        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name == name:
                log(f"The tourney: {name} already exists.", "ERROR")
                return None
            
        unqiueId = uniqueIDGenerator(registry=cls.registry, prefix="TRN")

        newTourney = cls(identifier=unqiueId, name=name)

        cls.registry[unqiueId] = newTourney
        log(f"Team '{name}' created.", "SUCCESS")

        return newTourney
    
    @classmethod
    def delTourney(cls, ob):
        # It pops out the ID from the registry. The pop() function returns true when successful.
        removedTourney = cls.registry.pop(ob.id, None)

        # Checks if it was successfully popped out. If False then team is not in the registry
        if removedTourney:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return False
    
    @classmethod
    def getTourney(cls, id=None, name=None):

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
            return None
            
        # Returns None when no Member is found in the registry with the ID or Username.
        log(f"No tourney was found with the name: {name} or the ID: {id}", "ERROR")
        return None

    @classmethod
    def getTourneyRegistry(cls):
        return cls.registry

    #
    # Object Functions
    #

    def addEvent(self, name, ob):
        
        # Checks if this event name already exists in this tournament.
        for event in self.events.values():
            if event.name.lower() == name.lower():
                log(f"The Event: {name} already exists in this tournament.", "ERROR")
                return None

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
    
    def removeEvent(self, ob):

        removedEvent = self.events.pop(ob.id, None)

        # Checks if it was successfully popped out. If False then team is not in the registry
        if removedEvent:
            log(f"Team: {ob.name} removed", "SUCCESS")
            return True
        else:
            log(f"Team: {ob.name} not found", "ERROR")
            return False
    
    def getEvent(self, id=None, name=None):

        # This gives 2 options for getting the object of the event.

        # Runs when there is something other than None in the ID argument.
        if not id == None:
            # Loops through every value in the event registry.
            for ido in self.events.keys():
                # Compares the id found in the object with the ID argument.
                if ido == id:
                    # Return the value in the registry (Which is the object).
                    return self.events[ido]
        # Runs when id is none and name is something other than None.
        elif not name == None:
            for ob in self.events.values():
            # Checking for every value (Which is an object) in the registry is the same as the name argument.
                if ob.name == name:
                    # Returns when found the name.
                    return ob
        else:
            # Returns nothing when both arguments are None.
            log(f"No arguments was entered", "ERROR")
            return None
        
        # Returns None when no event is found in the registry with the ID or Username.
        log(f"No event was found with the name: {name} or the ID: {id} in this tournament.", "ERROR")
        return None

    def changeEvent(self, name, ob):
        from tourney.classes import Events as Events

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

    def getAllTeamPoints(self):
        from collections import Counter

        totalPoints = {}

        for event in self.events.values():
            totalPoints = dict(Counter(totalPoints) + Counter(event.getAllTeamPoints()))

        log(totalPoints, "SUCCESS")
        return totalPoints

    def getTeamPoints(self, team):

        totalPoints = 0

        for event in self.events.values():
            if not event.isTeamInEvent(team=team): continue

            totalPoints = totalPoints + event.getTeamPoints(team=team)

        log(totalPoints, "SUCCESS")
        return totalPoints

    def checkEventDeletion(self):
        from tourney.classes import Events as Events

        # Gets events registry
        eventsRegistry = Events.Events.registry
        missingEvents = []

        for eventObject in self.events.values():
            # gets id of object
            id = eventObject.id
            # Gets the value using that id in the events' registry.
            result = eventsRegistry.get(id)
            # if there isn't an id found it will return none.
            if result == None:
                log(f"[{self.name}]: Missing event found: {id}")
                self.removeEvent(eventObject)
                missingEvents.append(id)
            else:
                log(f"[{self.name}]: Found ID: {id} is in events registry.")
        return

        
    
