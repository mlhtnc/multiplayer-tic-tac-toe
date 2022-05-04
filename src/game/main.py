from enum import Enum
import sys
import time

sys.path.append('../network')

from multicaster import Multicaster

class MenuState(Enum):
    MAIN_MENU = 0
    CREATE_GAME = 1
    JOIN_GAME = 2
    WAITING_FOR_PLAYER = 3

class GameInterface:

    def __init__(self):
        self.gameName = None
        self.menuState = MenuState.MAIN_MENU
        self.multicaster = Multicaster()
        self.server = None
        self.client = None

    def start(self):
        self.handleMainMenu()
        if self.menuState == MenuState.CREATE_GAME:
            self.handleCreateGame()
            self.handleWaitingForPlayer()
        elif self.menuState == MenuState.JOIN_GAME:
            self.handleJoinGame()

    def handleMainMenu(self):
        GameInterface.printx("1- Create Game")
        GameInterface.printx("2- Join Game")
        
        while True:
            GameInterface.printx(type = "wi")
            inp = input()
            if inp == "1":
                self.menuState = MenuState.CREATE_GAME
                break
            elif inp == "2":
                self.menuState = MenuState.JOIN_GAME
                break
            else:
                GameInterface.printx("Please choose one of the options")

    def handleCreateGame(self):
        while True:    
            GameInterface.printx("Game Name: ", "wi")
            self.gameName = input()
            if len(self.gameName) > 30:
                GameInterface.printx("Game Name cannot be any longer than 30 characters")
            else:
                break

        GameInterface.printx("Game created")

    def handleWaitingForPlayer(self):
        GameInterface.printx("Waiting for players")

        self.ok = 0
        def onMessageReceived(self, message):
            print(message)
            sys.stdout.flush()
            self.ok += 1

            if self.ok < 3:
                self.multicaster.receive(lambda msg : onMessageReceived(self, msg))


        self.multicaster.initReceiver()
        self.multicaster.receive(lambda msg : onMessageReceived(self, msg))

        while self.ok < 3:
            print(self.ok)
            sys.stdout.flush()
            time.sleep(0.5)

        print("closing")
        sys.stdout.flush()
        self.multicaster.closeReceiver()



    def handleJoinGame(self):
        pass

    
    # jo = just output
    # wi = wait input
    @staticmethod
    def printx(s = "", type = "jo"):
        if type == "wi":
            print("--> ", end = "")
            print(s, end = "")
        elif "jo":
            print("> ", end = "")
            print(s)

        sys.stdout.flush()



gi = GameInterface()
gi.start()
