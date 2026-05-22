from tourney.classes import Common as Common, Events as Events
from tourney.classes.Common import log as log
import copy

class Tourney:

    registry = {}

    def __init__(self, master=None, identifier=None, name=None):
        self.id = identifier

        self.name = name

        self.events = {}

    @classmethod
    def createTourney(cls, name):
        for ob in cls.registry.values():
        # Checking for every value (Which is an object) in the registry is the same as the name argument.
            if ob.name == name:
                log(f"The tourney: {name} already exists.", "ERROR")
                return None
            
        unqiueId = Common.uniqueIDGenerator(registry=cls.registry, prefix="TRN")

        newTourney = cls(master=cls, identifier=unqiueId, name=name)

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

    #
    # Object Functions
    #

    def addEvent(self, name, ob):
        
        # Checks if this event name already exists in this tournament.
        for event in self.events.values():
            if event.name == name:
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
        uniqueID = Common.uniqueIDGenerator(registry=self.events, prefix="T.EVENT")

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
            for ido in self.events.values():
                # Compares the id found in the object with the ID argument.
                if ido.id == id:
                    # Return the value in the registry (Which is the object).
                    return ido
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

    def checkEventDeletion(self):

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

        
    
