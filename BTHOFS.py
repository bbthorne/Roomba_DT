"""
BTHOFS (Behavior Tree Higher Order Functions) is a class that includes methods
that perform higher-order operations on the tasks in the Roomba's Roamings
problem. Each method corresponds to a special node-type. While not using classes
as node types, this model mimics the hierarchy of node type behavior using HOF
paradigms instead of class inheritance.
It includes one property:
    processTime - a counter for the current multi-second process
"""
class BTHOFS:
    def __init__(self):
        self.processTime = 0

    """
    ////////////////////////////////////////////////////////////////////////////
                                    COMPOSITES
    ////////////////////////////////////////////////////////////////////////////
    """
    def sequence(self, tasks):
        for task in tasks:
            result = task()
            if result != "SUCCESS":
                return result
        return "SUCCESS"

    def selector(self, tasks):
        for task in tasks:
            result = task()
            if result != "FAILURE":
                return result
        return "FAILURE"

    """
    ////////////////////////////////////////////////////////////////////////////
                                    CONDITION
    ////////////////////////////////////////////////////////////////////////////
    """
    def conditional(self, c):
        if c:
            return "SUCCESS"
        return "FAILURE"

    """
    ////////////////////////////////////////////////////////////////////////////
                                    DECORATORS
    ////////////////////////////////////////////////////////////////////////////
    """
    def negate(self, task):
        result = task()
        if result == "SUCCESS":
            return "FAILURE"
        if result == "FAILURE":
            return "SUCCESS"
        return result

    def until_fail(self, result):
        if result != "FAILURE":
            return "RUNNING"
        return "SUCCESS"

    def timer(self, threshold):
        if self.processTime < threshold:
            self.processTime += 1
            print("Clean Spot: RUNNING")
            return "RUNNING"
        self.processTime = 0
        print("Clean Spot: SUCCESS")
        return "SUCCESS"
