import re


class Wall:
    def __init__(self, position, type):
        self.position = position
        self.type = type


class Player:
    def __init__(self, positions, type, k):
        self.positions = positions
        self.type = type
        self.greenWallNumber = k
        self.blueWallNumber = k


class Board:
    def __init__(self, m, n, position1, position2, k, first):
        self.m = m
        self.n = n
        self.startPositionX = position1
        self.startPositionO = position2
        self.player1 = Player(position1, "x" if first else "o", k)
        self.player2 = Player(position2, "o" if first else "x", k)
        self.walls = []


class Game:
    def __init__(self):
        self.board = None
        self.isPlayerOneNext = None

    def getStartState(self):
        m = 23
        while m > 21:
            print("Unesite sirinu table. Sirina mora biti manja od 22.")
            m = 14  # int(input())

        n = 30
        while n > 27:
            print("Unesite visinu table. Visina mora biti manja od 28.")
            n = 13  # int(input())

        k = 19
        while k > 18:
            print("Unesite broj zidova po igracu. Maksimalno 18.")
            k = 8  # int(input())

        first = None
        while not first:
            print('Da li zelite da igrate prvi? Unesite "da" ili "ne" ')
            first = "da"  # input().lower()

        playerPositions = []
        while len(playerPositions) < 4:
            print("Unesite pocetne pozicije vasih igraca x1 y1 x2 y2 ")
            position = "1 2 3 4"  # input()
            playerPositions = re.findall(r"(\d+)", position)
        playerPositions = list(zip(playerPositions[0::2], playerPositions[1::2]))

        otherPlayerPositions = []
        while len(otherPlayerPositions) < 4:
            print("Unesite pocetne pozicije protivnickih igraca x1 y1 x2 y2 ")
            position = "5 6 7 8"  # input()
            otherPlayerPositions = re.findall(r"(\d+)", position)
        otherPlayerPositions = list(
            zip(otherPlayerPositions[0::2], otherPlayerPositions[1::2])
        )

        self.setBoard(Board(m, n, playerPositions, otherPlayerPositions, k, first))
        self.isPlayerOneNext = True if (first == "da") else False

    def isEnd(self):
        return bool(
            set(self.board.player1.positions).intersection(
                set(self.board.startPositionO)
            )
            or set(self.board.player2.positions).intersection(
                set(self.board.startPositionX)
            )
        )

    def setBoard(self, board):
        self.board = board

    def nextMove(self):
        valid = False
        while not valid:
            print("Unesite sledeci validan potez: X|O 1|2 m n p|z x y")
            move = input()
            playerNumber, *positions = re.findall(r"(\d+)", move)
            playerNumber = int(playerNumber) - 1
            playerPosition = (positions[0], positions[1])
            if len(positions) > 2:  # jer mozda nema vise zidova
                wallPosition = (positions[2], positions[3])
            playerType = re.findall("[xX]|[oO]", move)[0].lower()
            wallType = re.findall("[zZ]|[Pp]", move)[0].lower()
            valid = self.isValidMove(
                playerNumber, playerType, playerPosition, wallPosition, wallType
            )
            if valid:
                self.changeBoardState(
                    playerNumber, playerPosition, wallPosition, wallType
                )
                self.isPlayerOneNext = not self.isPlayerOneNext

    def isValidMove(
        self, playerNumber, playerType, playerPosition, wallPosition, wallType
    ):
        if (self.isPlayerOneNext and self.board.player1.type != playerType) or (
            not self.isPlayerOneNext and self.board.player2.type != playerType
        ):
            print("Drugi igrac je na redu")
            return False
        # da li moze pozicije
        # je l moze zid

        return True

    def changeBoardState(self, playerNumber, playerPosition, wallPosition, wallType):
        if self.isPlayerOneNext:
            self.changePlayerStats(
                self.board.player1, wallType, playerPosition, playerNumber
            )
        else:
            self.changePlayerStats(
                self.board.player2, wallType, playerPosition, playerNumber
            )
        self.board.walls.append(Wall(wallPosition, wallType))

    def changePlayerStats(self, player, wallType, playerPosition, playerNumber):
        player.positions[playerNumber] = playerPosition
        if wallType == "z":
            player.greenWallNumber -= 1
        else:
            player.blueWallNumber -= 1


game = Game()
game.getStartState()
game.nextMove()

print("")
