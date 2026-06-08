import os
import random
import datetime
import platform
from datetime import datetime

from pathlib import Path
import inspect
from typing import Any, LiteralString


def uniqueIDGenerator(registry: dict[str, object], prefix: str | None = None) -> str:
    """
    This function generates a unique id for a registry. You must pass through a registry so that it can check for any
    duplicate IDs. It's recommended to enter a prefix as it makes it easier to distinguish to what the IDs are.
    :param registry:
    :param prefix:
    :return:
    """
    # Decided to update the range from 1000 to 100000 which isn't that necessary for a college, but it's better to be safe.
    randomNum = random.randint(0, 100000)
    log(f"Generated: {randomNum}")

    if not f"{prefix}-{randomNum}" in registry: return f"{prefix}-{randomNum}"

    return uniqueIDGenerator(registry=registry, prefix=prefix)
    # If there is no ids it will infinitely loop.
    # If there is little amount of ids it may take a long time to find one.

def saveAllData():
    """
    This just calls all the entities saveData functions.
    """
    from tourney.classes import Members, Teams, Events, Tourney
    log("Saving all data...")
    Members.Members.saveData()
    Teams.Teams.saveData()
    Events.Events.saveData()
    Tourney.Tourney.saveData()

def log(message: str, type: str = "INFO"):
    """
    This is the alternative print function that shows more data than a normal print function.
    This includes the time of execution, the class who called this function, the function who called this function and the specified error type.

    This allows for better debugging for errors (since my code doesn't throw any errors) and rather just strings.
    Tracing a log from the exact class to the exact function makes troubleshooting easier.\n
    * Functions that do not belong to a class just show as 'Global'\n
    * There are 3 types: INFO, SUCCESS, ERROR (Function defaults to 'INFO').
    :param message:
    :param type:
    :return:
    """
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

    print(f"{timeNow()} - {type}: [{callerClass}] ({functionName}): {message}")
    return type

def removeWhitespace(string: str) -> LiteralString | str:
    """
    This function removes whitespace from a string, including any extra spaces.
    :param string:
    :return:
    """
    return " ".join(string.split())

def isInCharLimit(string: str, limit: int):
    """
    This function checks if the given string is in the given limit.\n
    * Returns true when is in limit\n
    * Returns false otherwise\n
    :param string:
    :param limit:
    :return:
    """
    return len(removeWhitespace(string)) <= limit

def zeroChar(string: str) -> str | None:
    """
    This function returns None, when a string is empty.\n
    * Since is due to JavaScript sending empty strings when users type nothing.\n
    * If it's not empty it will return the same string.
    :param string:
    :return:
    """
    if string == "":
        return None
    return string

def getDataDirectory() -> Path:
    """
    This function gets the local users data directory.\n
    * Its compatible with Windows, MacOS and linux.
    :return:
    """
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

def saveDataDirectory() -> Path:
    """
    This function gets the local users save data directory.\n
    :return:
    """
    return getDataDirectory() / "SaveData"

def timeNow() -> datetime:
    """
    This think returns the current time.
    :return:
    """
    return datetime.now()