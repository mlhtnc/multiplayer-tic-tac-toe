from enum import Enum
import sys
import time

sys.path.append('../network')

from multicast_sender import MulticastSender
from multicast_receiver import MulticastReceiver
from server import Server
from client import Client
from game import Game, GameState, Turn


class MenuState(Enum):
    MAIN_MENU = 0
    CREATE_GAME = 1
    SEARCH_GAMES = 2
    WAITING_FOR_PLAYER = 3
    JOIN_GAME = 4
    SERVER_GAME_LOOP = 5
    CLIENT_GAME_LOOP = 6

class GameInterface:

    JOIN_GAME_TIMEOUT = 1

    SEND_INFO_CMD = "_SEND-INFO_"
    GAME_INFO_CMD = "_GAME-INFO_"
    JOIN_GAME_CMD = "_JOIN-GAME_"
    JOIN_ACCEPTED_CMD = "_JOIN-ACCEPTED_"
    MOVE_CMD = "_MOVE_"

    def __init__(self):
        self.gameName = None
        self.gameInfos = []
        self.menuState = MenuState.MAIN_MENU
        self.multicastSender = MulticastSender()
        self.multicastReceiver = MulticastReceiver()
        self.server = Server()
        self.client = Client()

        self.clientPlayerName = None
        self.serverPlayerName = None

        self.isPlayerJoined = False

        self.serverPlayerIp = None

    def start(self):
        self.handleMainMenu()
        if self.menuState == MenuState.CREATE_GAME:
            self.handleCreateGame()
            self.handleWaitingForPlayer()
        elif self.menuState == MenuState.SEARCH_GAMES:
            self.handleSearchGames()

        if self.menuState == MenuState.SERVER_GAME_LOOP:
            self.handleServerGameLoop()
        elif self.menuState == MenuState.CLIENT_GAME_LOOP:
            self.handleClientGameLoop()

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
                self.menuState = MenuState.SEARCH_GAMES
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

        # Listen for game info requests

        def onMessageReceived(self, message, senderaddr):
            if message.startswith(GameInterface.SEND_INFO_CMD):
                self.multicastSender.send(f"{GameInterface.GAME_INFO_CMD}{self.gameName}_{self.multicastSender.nicIp}_")
        
        self.multicastReceiver.receive(lambda msg, senderaddr : onMessageReceived(self, msg, senderaddr))

        # Listen for join game requests

        def onClientMessageReceived(self, message):
            if not self.isPlayerJoined and message.startswith(GameInterface.JOIN_GAME_CMD):
                # params = message[1:len(message) - 1].split("_")
                # self.clientPlayerName = params[1]

                self.menuState = MenuState.SERVER_GAME_LOOP
                self.multicastReceiver.close()
                self.multicastSender.close()
                self.server.onMessageReceived.removeAllListeners()
        
                self.server.send(f"{GameInterface.JOIN_ACCEPTED_CMD}")

                self.isPlayerJoined = True

        self.server.onMessageReceived += lambda msg : onClientMessageReceived(self, msg)
        self.server.listen()            

        while not self.isPlayerJoined:
            time.sleep(0.1)

    def handleSearchGames(self):
        GameInterface.printx("Looking for games...")

        def onMessageReceived(self, message, senderaddr):
            if message.startswith(GameInterface.GAME_INFO_CMD):
                params = message[1:len(message) - 1].split("_")
                self.gameInfos.append((params[1], params[2]))
        
        self.multicastReceiver.receive(lambda msg, senderaddr : onMessageReceived(self, msg, senderaddr))
        self.multicastSender.send(GameInterface.SEND_INFO_CMD)

        timer = 0
        while True:
            time.sleep(0.1)
            timer += 0.1

            if timer >= GameInterface.JOIN_GAME_TIMEOUT:
                for i in range(len(self.gameInfos)):
                    GameInterface.printx(f"1- {self.gameInfos[i][0]}")

                GameInterface.printx(f"{len(self.gameInfos) + 1}- Refresh")
                GameInterface.printx(type = "wi")

                selectedGame = int(input())
                if selectedGame >= 1 and selectedGame <= len(self.gameInfos):
                    self.menuState = MenuState.JOIN_GAME
                    self.multicastSender.close()
                    self.multicastReceiver.close()

                    self.serverPlayerIp = self.gameInfos[selectedGame - 1][1]

                    self.handleJoinGame()

                    break
                else:
                    self.gameInfos = []
                    timer = 0

                    self.multicastSender.send(GameInterface.SEND_INFO_CMD)

    def handleJoinGame(self):
        def onMessageReceived(self, message):
            if not self.isPlayerJoined and message.startswith(GameInterface.JOIN_ACCEPTED_CMD):
                # params = message[1:len(message) - 1].split("_")
                # self.serverPlayerName = params[1]

                self.menuState = MenuState.CLIENT_GAME_LOOP
                self.client.onMessageReceived.removeAllListeners()


                self.isPlayerJoined = True

        def onConnected(self):
            self.client.send(f"{GameInterface.JOIN_GAME_CMD}")
            self.client.onConnected.removeAllListeners()

        self.client.onMessageReceived += lambda msg : onMessageReceived(self, msg)
        self.client.onConnected += lambda: onConnected(self)
        self.client.connect(self.serverPlayerIp)

        while not self.isPlayerJoined:
            time.sleep(0.1)

    def handleServerGameLoop(self):
        GameInterface.printx("Game Starting...")

        def onClientMessageReceived(self, message):
            if message.startswith(GameInterface.MOVE_CMD):
                params = message[1:len(message) - 1].split("_")
                row = int(params[1])
                col = int(params[2])

                g.move(row, col)
                g.printBoard()

        self.server.onMessageReceived += lambda msg : onClientMessageReceived(self, msg)


        g = Game()
        state = GameState.NOT_FINISHED

        while state == GameState.NOT_FINISHED or state == GameState.ILLEGAL_MOVE:
            row, col = self.getMoveFromUser()
            state = g.move(row, col)
            g.printBoard()

            self.server.send(f"{GameInterface.MOVE_CMD}{row}_{col}_")

            GameInterface.printx("Waiting for move...")

            while g.turn == Turn.O:
                time.sleep(0.1)

        GameInterface.printx("Game over")

        self.server.close()

    def handleClientGameLoop(self):
        GameInterface.printx("Game Starting...")
        GameInterface.printx("Waiting for move...")

        def onMessageReceived(self, message):
            GameInterface.printx(message)
            if message.startswith(GameInterface.MOVE_CMD):
                params = message[1:len(message) - 1].split("_")
                row = int(params[1])
                col = int(params[2])

                g.move(row, col)
                g.printBoard()

        self.client.onMessageReceived += lambda msg : onMessageReceived(self, msg)


        g = Game()
        state = GameState.NOT_FINISHED

        while g.turn == Turn.X:
                time.sleep(0.1)

        while state == GameState.NOT_FINISHED or state == GameState.ILLEGAL_MOVE:
            GameInterface.printx("z")

            row, col = self.getMoveFromUser()
            state = g.move(row, col)
            g.printBoard()

            self.client.send(f"{GameInterface.MOVE_CMD}{row}_{col}_")

            GameInterface.printx("Waiting for move...")

            while g.turn == Turn.X:
                time.sleep(0.1)
    

        GameInterface.printx("Game over")

        self.client.close()

    def getMoveFromUser(self):
        GameInterface.printx("Row: ", type = "wi")
        row = int(input())
        GameInterface.printx("Col: ", type = "wi")
        col = int(input())

        return row, col


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
