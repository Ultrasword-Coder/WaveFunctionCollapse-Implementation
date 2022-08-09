"""
A simple cutscene system that allows for:
- moving to a point
- timers


To be finished
- try to implementing loading scripts

"""

print("CutScene.py is not finished")

import json

from . import statehandler


class CutScene:
    """
    A cutscene object
    - handles cutscenes
    - given a series of characters and a series of actions,
        the cutsene handles each of the states of each character
    - the system is goal oriented:
        - whether it be a time or position goal
    """
    def __init__(self, file: str):
        """
        CutScene Constructor
        contains:
        - file              = str
        - systems           = [CutSceneStates]
        """
        self.systems = []

    def load_cutscene(self):
        """Load a cutscene"""
        with open(file, 'r') as file:
            data = json.load(file)
            file.close()
        # parse
        print("make parsing")



class CutSceneState:
    """
    a cut scene state
    - handles a current state for an object
    """
    def __init__(self, obj, data):
        """
        !update functions are custom made and use data in the self.data dict
        CutSceneState Constructor
        contains:
        - object                = Entity
        - next_state            = CutSceneState
        """
        self.obj = obj
        self.data = data
        self.next_state = None

    def update(self):
        """Default update function"""
        pass
