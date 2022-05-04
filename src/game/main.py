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

    SEND_INFO_CMD = "_SEND-INFO_"
    GAME_INFO_CMD = "_GAME-INFO_"

    def __init__(self):
        self.gameName = None
        self.gameInfos = []
        self.menuState = MenuState.MAIN_MENU
        self.multicaster = Multicaster()
        self.server = None
        self.client = None

        self.multicaster.initSender()
        self.multicaster.initReceiver()

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

        def onMessageReceived(self, message):
            print(message)
            sys.stdout.flush()

            if message.startswith(GameInterface.SEND_INFO_CMD):
                self.multicaster.send(f"{GameInterface.GAME_INFO_CMD}gameName={self.gameName}_")

                print(f"{GameInterface.GAME_INFO_CMD}gameName={self.gameName}_")
                sys.stdout.flush()

            self.multicaster.receive(lambda msg : onMessageReceived(self, msg))
        
        self.multicaster.receive(lambda msg : onMessageReceived(self, msg))

        loop = True
        while loop:
            input()
            loop = False


    def handleJoinGame(self):
        GameInterface.printx("Looking for games...")

        def onMessageReceived(self, message):
            if message.startsWith(GameInterface.GAME_INFO_CMD):
                params = message[1:len(message) - 1].split("_")
                self.gameInfos.append(params[1])

            self.multicaster.receive(lambda msg : onMessageReceived(self, msg))
        
        self.multicaster.receive(lambda msg : onMessageReceived(self, msg))

        self.multicaster.send(GameInterface.SEND_INFO_CMD)
        print(GameInterface.SEND_INFO_CMD)
        sys.stdout.flush()



        timeout = 2
        while timeout > 0:
            timeout -= 0.1
            time.sleep(0.1)

        for i in range(len(self.gameInfos)):
            GameInterface.printx(f"1- {self.gameInfos[i]}")

        GameInterface.printx(type = "wi")
    
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
