import random
import datetime
from tourney.classes import Members as Members
import inspect


def uniqueIDGenerator(registry=None, prefix=None):

    randomNum = random.randint(0, 1000)
    log(f"Generated: {randomNum}")

    if not f"{prefix}-{randomNum}" in registry: return f"{prefix}-{randomNum}"

    uniqueIDGenerator(registry=registry, prefix=prefix)
    # If there is no ids it will infinitely loop.
    # If there is little amount of ids it may take a long time to find one.

def saveAllData():
    log("Saving all data...")
    Members.Members.saveData()

def log(message, type="INFO"):

    # gets the callers frame of the function that called log.
    callerFrame = inspect.currentframe().f_back
    # Gets the caller function name.
    functionName = callerFrame.f_code.co_name

    if 'self' in callerFrame.f_locals:
        callerClass = callerFrame.f_locals['self'].__class__.__name__
    elif 'cls' in callerFrame.f_locals:
        callerClass = callerFrame.f_locals['cls'].__name__
    else:
        callerClass = "Global"

    print(f"{datetime.datetime.now()} - {type}: [{callerClass}] ({functionName}): {message}")