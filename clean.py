from Roomba import *
if __name__ == "__main__":
    blackboard = {"BATTERY_LEVEL":100, "SPOT":False, "GENERAL":True,
                  "DUSTY_SPOT":True, "HOME_PATH":"NONE"}
    roomba = Roomba(blackboard)
    roomba.run()
