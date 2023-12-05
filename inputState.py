STARTS = 0
CONTAINS = 1
StartsOrContains_Map = {"Starts With:": STARTS, 'Contains:':CONTAINS}

NAME = 0
RANDOM = 1
SortBy_Map = {"Name": NAME, "Random": RANDOM}

ORIGINAL = 0
FIT = 1
FILL = 2
STRETCH = 3
Fit_Map = {"Original": ORIGINAL, "Fit": FIT, "Fill": FILL, "Stretch": STRETCH}

DEFAULT_SLIDE_DELAY = 30

class InputState:
    def __init__(self):
        self.folderPathInput = ''
        self.startsOrContains_mode = STARTS
        self.startsOrContains_text = ''
        self.sortBy = RANDOM
        self.fit_mode = FIT
        self.slideDelay = DEFAULT_SLIDE_DELAY
        self.didQuit = False
        
    def setValues(self, newInputState):
        self.folderPathInput = newInputState.folderPathInput
        self.startsOrContains_mode = newInputState.startsOrContains_mode
        self.startsOrContains_text = newInputState.startsOrContains_text
        self.sortBy = newInputState.sortBy
        self.fit_mode = newInputState.fit_mode
        self.slideDelay = newInputState.slideDelay
        self.didQuit = newInputState.didQuit