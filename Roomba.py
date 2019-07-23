from functools import partial
from BTHOFS import *
"""
Roomba is a class that represents the tasks in the Roomba's behavior tree. It
has the following properties:
    blackboard  - a dictionary containing what the Roomba detects
    time        - an integer that increases after each evaluation of the tree
    current     - the method in the Priority 2 subtree that represents the
                  current cleaning process.
It inherits from BTHOFS, which contains methods that represent the behavior
of special nodes in a behavior tree.
"""
class Roomba(BTHOFS):
    def __init__(self, blackboard):
        BTHOFS.__init__(self)
        self.blackboard  = blackboard
        self.time        = 0
        self.current     = self.cleaning

    """
    run is a method that represents the priority selection at the root of the
    behavior tree. It contains an infinite loop that evaluates the tree, and
    edits the blackboard at various time intervals.
    """
    def run(self):
        while self.time < 150:
            print("Time: " + str(self.time))
            result = self.selector([self.check_battery, self.current, self.do_nothing])
            print("Tree result: " + result)
            print("Blackboard: " + str(self.blackboard))
            print("--------------------------------------------------------------------------------")
            self.dirt_detected()

            self.time += 1
            self.blackboard["BATTERY_LEVEL"] -= 1

    """
    dirt_detected simulates the Roomba finding dirty spots at certain spots in
    the tree evaluations. Edit this method to change the environmental phenomena.
    """
    def dirt_detected(self):
        if self.time == 60:
            self.blackboard["SPOT"] = True
        if self.time == 75:
            self.blackboard["GENERAL"] = True
            self.blackboard["DUSTY_SPOT"] = True
        if self.time % 30 == 0:
            self.blackboard["GENERAL"] = True

    """
    check_battery is a method that represents the root of the Priority 1 subtree.
    """
    def check_battery(self):
        cond = partial(self.conditional, c=(self.blackboard["BATTERY_LEVEL"] < 30))
        return self.sequence([cond, self.find_home, self.go_home, self.dock])

    """
    find_home is a method that represents the Roomba finding a path home
    """
    def find_home(self):
        print("Find Home: SUCCESS")
        self.blackboard["HOME_PATH"] = "PATH_TO_DOCK"
        return "SUCCESS"

    """
    go_home is a method that represents the Roomba going to the dock.
    """
    def go_home(self):
        print("Go Home: SUCCESS")
        return "SUCCESS"

    """
    dock is a method that represents the Roomba charging at the dock.
    """
    def dock(self):
        print("Dock: SUCCEESS")
        self.blackboard["BATTERY_LEVEL"] = 100
        self.blackboard["HOME_PATH"] = "NONE"
        return "SUCCESS"

    """
    cleaning is a method that represents the root of the Priority 2 subtree.
    """
    def cleaning(self):
        return self.selector([self.spot_check, self.general_cleaning])

    """
    spot_check is a method that represents the spot cleaning procedure.
    """
    def spot_check(self):
        cond    = partial(self.conditional, c=self.blackboard["SPOT"])
        process = partial(self.timer, threshold=20)
        return self.sequence([cond, process, self.done_spot])

    """
    done_spot is a method that edits SPOT on the blackboard when a spot cleaning
    procedure is complete.
    """
    def done_spot(self):
        self.blackboard["SPOT"] = False
        print("Done Spot: SUCCESS")
        return "SUCCESS"

    """
    general_cleaning is a method that runs the general cleaning procedure. If
    a subtree is running a task at the end of evaluation, it sets itself to the
    current. Otherwise, it sets current to the root of the Priority 2 subtree.
    """
    def general_cleaning(self):
        cond   = partial(self.conditional, c=self.blackboard["GENERAL"])
        result = self.sequence([cond, self.cleaning_rotation, self.done_general])
        if result == "RUNNING":
            self.current = self.general_cleaning
        else:
            self.current = self.cleaning
        return result

    """
    cleaning_rotation is a method that represents the standard cleaning rotation.
    """
    def cleaning_rotation(self):
        cond = partial(self.negate, task=partial(self.conditional, c=(self.blackboard["BATTERY_LEVEL"] <= 30)))
        return self.until_fail(self.sequence([cond, self.basic_clean]))

    """
    basic_clean is a method that represents the basic cleaning routine
    """
    def basic_clean(self):
        return self.selector([self.dusty, self.clean])

    """
    done_general is a method that edits GENERAL on blackboard.
    """
    def done_general(self):
        print("Done General: SUCCESS")
        self.blackboard["GENERAL"] = False
        return "SUCCESS"

    """
    dusty is a method that represents the dusty spot cleaning procedure.
    """
    def dusty(self):
        cond    = partial(self.conditional, c=self.blackboard["DUSTY_SPOT"])
        process = partial(self.timer, threshold=35)
        return self.sequence([cond, process, self.done_dusty])

    """
    done_dusty is a method that sets DUSTY_SPOT in blackboard.
    """
    def done_dusty(self):
        self.blackboard["DUSTY_SPOT"] = False
        return "SUCCESS"
    """
    clean is a method that represents a successful cleaning operation.
    """
    def clean(self):
        print("Clean: SUCCESS")
        return "SUCCESS"

    """
    do_nothing is a method that represents the Priority 3 subtree.
    """
    def do_nothing(self):
        print("Do Nothing: SUCCESS")
        return("SUCCESS")
