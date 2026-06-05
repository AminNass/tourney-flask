import os
import random
import datetime
import platform

from pathlib import Path
import inspect

def uniqueIDGenerator(registry=None, prefix=None):

    randomNum = random.randint(0, 1000)
    log(f"Generated: {randomNum}")

    if not f"{prefix}-{randomNum}" in registry: return f"{prefix}-{randomNum}"

    return uniqueIDGenerator(registry=registry, prefix=prefix)
    # If there is no ids it will infinitely loop.
    # If there is little amount of ids it may take a long time to find one.

def saveAllData():
    from tourney.classes import Members, Teams, Events, Tourney
    log("Saving all data...")
    Members.Members.saveData()
    Teams.Teams.saveData()
    Events.Events.saveData()
    Tourney.Tourney.saveData()

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
    return type

def removeWhitespace(string):  return " ".join(string.split())

def isInCharLimit(string, limit): return len(removeWhitespace(string)) <= limit

def zeroChar(string):
    if string == "":
        return None
    return string

def getDataDirectory():

    log(f"Getting data directory: {platform.system()}")
    # Gets the app directories for the OS for
    if os.name == 'nt':  # Windows
        baseDirectory = os.environ.get('APPDATA')
    elif os.uname().sysname == 'Darwin':  # macOS
        baseDirectory = os.path.expanduser('~/Library/Application Support')
    else:  # Linux
        baseDirectory = os.path.expanduser('~/.config')

    log(f"Machine data directory: {baseDirectory}")

    appDataPath = Path(baseDirectory) / "TourneyApp"

    appDataPath.mkdir(parents=True, exist_ok=True)

    log(f"App data path: {appDataPath}")

    return appDataPath

def saveDataDirectory():
    return getDataDirectory() / "SaveData"

def timeNow():
    return datetime.datetime.now()