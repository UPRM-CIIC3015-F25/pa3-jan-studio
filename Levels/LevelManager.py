from Levels.SubLevel import SubLevel, Blind
class LevelManager():
    def __init__(self, p = None):
        #-------------------Initialize Levels and Player-------------------
        self.levelsDict = {} # Dict of levels, key : ante: int, value : list of sublevels : list[SubLevel]
        self.p = None # Player info (must be set up later) -> setUpPlayer()
        self.curLevel = [] # List of current sublevels : list[SubLevel]
        self.curSubLevel = None # Current sublevel : SubLevel
        self.playerWins = False
        #----------Setup Levels and Player----------------------
        self.setUpPlayer(p)
        self.setUpLevels()
        self.updateLevels()

    def setUpPlayer(self, p): # Sets up player info
        if p != None:
            self.p = p

    # TODO (TASK 0) - Set up all levels and their corresponding sublevels.
    #   Each level should include a Small, Big, and Boss Blind, with Boss Blinds assigned unique names.
    #   Organize them in a dictionary structure where each key represents a level number.
    def setUpLevels(self): # Sets up all levels and sublevels
        self.levelsDict[1] = [SubLevel(Blind.SMALL, 1), SubLevel(Blind.BIG, 1), SubLevel(Blind.BOSS, 1, "The Water")]
        self.levelsDict[2] = [SubLevel(Blind.SMALL, 2), SubLevel(Blind.BIG, 2), SubLevel(Blind.BOSS, 2, "The Mark")]
        self.levelsDict[3] = [SubLevel(Blind.SMALL, 3), SubLevel(Blind.BIG, 3), SubLevel(Blind.BOSS, 3, "The House")]
        self.levelsDict[4] = [SubLevel(Blind.SMALL, 4), SubLevel(Blind.BIG, 4), SubLevel(Blind.BOSS, 4, "The Hook")]
        self.levelsDict[5] = [SubLevel(Blind.SMALL, 5), SubLevel(Blind.BIG, 5), SubLevel(Blind.BOSS, 5, "The Manacle")]
        self.levelsDict[6] = [SubLevel(Blind.SMALL, 6), SubLevel(Blind.BIG, 6), SubLevel(Blind.BOSS, 6, "The Needle")]

    def updateLevels(self):
        # Load sublevels list for the player's current ante
        self.curLevel = self.levelsDict[self.p.playerAnte]
        # Pick the first unfinished sublevel as current
        self.curSubLevel = None
        for s in self.curLevel:
            if not s.finished:
                self.curSubLevel = s
                break
    
    def update(self):
        if self.curSubLevel and not self.curSubLevel.finished:  # Check if current sublevel is finished
            if self.p.roundScore >= self.curSubLevel.score:     # If player's round score meets or exceeds sublevel score requirement
                self.curSubLevel.finished = True
                self.p.roundScore = 0
                if self.next_unfinished_sublevel() is None:  # Check if all sublevels in the current ante are finished
                    self.p.playerAnte += 1
                    # If no more levels exist, set playerWins to True
                    if self.p.playerAnte not in self.levelsDict:
                        self.curLevel = []
                        self.curSubLevel = None
                        self.playerWins = True
                        return
                    self.updateLevels()
                    self.curSubLevel = self.curLevel[0]
                self.p.levelFinished = True  # Signal UI to open LevelSelectState

    # TODO (TASK 8) - Create a recursive function that finds the next unfinished sublevel.
    #   It should check each sublevel in order and return the first one that isn’t finished.
    #   Stop once all have been checked or one is found. Avoid using loops. (USE RECURSIONS)
    def next_unfinished_sublevel(self, index=0):
        print("Entered next_unfinished_sublevel")
        print(index)
        return None
    