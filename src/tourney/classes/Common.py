import random
from tourney.classes import Members as Members


def uniqueIDGenerator(registry=None, prefix=None):

    randomNum = random.randint(0, 1000)
    print("Generated:", randomNum)

    if not f"{prefix}-{randomNum}" in registry: return f"{prefix}-{randomNum}"

    uniqueIDGenerator(registry=None, prefix=None)

def saveAllData():
    print("Saving all data...")
    Members.Members.saveData()