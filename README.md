Decision Tree for a Roomba - Showcasing Higher Order Functions and Inheritance

To run the Roomba simulation, run clean.py. It runs a 150s simulation that
starts off detecting a dusty spot, after 60s detecting a spot, and every 30s
detecting the need for general cleaning.

The implementation of the Behavior Tree appears in two classes:
    BTHOFS - a class of higher-order methods that represent the behavior of
             conditional, composite, and decorator nodes

    Roomba - a subclass of BTHOFS that represents the tasks and relationships
             between tasks in the Roomba's Roamings Behavior Tree

This solution uses higher-order functions to simulate a hierarchy of node types.

Includes a copy of functools.py, as it is not as popular as other Python
packages.
