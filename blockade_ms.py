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
        playerPositions = list(
            zip(playerPositions[0::2], playerPositions[1::2]))

        otherPlayerPositions = []
        while len(otherPlayerPositions) < 4:
            print("Unesite pocetne pozicije protivnickih igraca x1 y1 x2 y2 ")
            position = "5 6 7 8"  # input()
            otherPlayerPositions = re.findall(r"(\d+)", position)
        otherPlayerPositions = list(
            zip(otherPlayerPositions[0::2], otherPlayerPositions[1::2])
        )

        self.isPlayerOneNext = True if (first == "da") else False
        self.setBoard(Board(m, n, playerPositions,
                      otherPlayerPositions, k, self.isPlayerOneNext))

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
            playerPosition = (int(positions[0]), int(positions[1]))
            if len(positions) == 4:  # jer mozda nema vise zidova
                wallPosition = (int(positions[2]), int(positions[3]))
                wallType = re.findall("[zZ]|[Pp]", move)[0].lower()
            else:
                wallPosition = []
                wallType = None
            playerType = re.findall("[xX]|[oO]", move)[0].lower()

            valid = self.isValidMove(
                playerNumber, playerType, playerPosition, wallPosition, wallType
            )
            if valid:
                self.changeBoardState(
                    playerNumber, playerPosition, wallPosition, wallType
                )
                self.isPlayerOneNext = not self.isPlayerOneNext

    def isValidMove(self, playerNumber, playerType, playerPosition, wallPosition, wallType):
        if (self.isPlayerOneNext and self.board.player1.type != playerType) or (
            not self.isPlayerOneNext and self.board.player2.type != playerType
        ):
            print("Drugi igrac je na redu")
            return False

        player = self.board.player1 if playerType == "x" else self.board.player2
        otherPlayer = self.board.player2 if playerType == "x" else self.board.player1

        if len(wallPosition) == 0 and (player.greenWallNumber > 0 or player.blueWallNumber > 0):
            print("Niste uneli pozicije zida")
            return False

        if len(wallPosition) == 2:
            if (player.greenWallNumber == 0 and wallType == "z") or (player.blueWallNumber == 0 and wallType == "p"):
                print("Iskoristili ste sve zidove ove boje")
                return False
            # dozvoljeno je da stavi zid te boje, provera da li su pozicije zida validne
            if wallPosition[0] < 0 or wallPosition[0] > self.board.m-1 or wallPosition[1] < 0 or wallPosition[1] > self.board.n-1:
                print("Pozicije zida su van okvira table")
                return False
            allWalls = self.board.walls
            if wallType == "p":
                if wallPosition[0] == self.board.m-1:
                    return False
                if len(list(filter(lambda w: w.type == "p" and w.position[1] == wallPosition[1] and (w.position[0]-1 <= wallPosition[0] <= w.position[0]+1), allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
                if len(list(filter(lambda w: w.type == "z" and w.position[0]-1 == wallPosition[0] and w.position[1]+1 == wallPosition[1], allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            elif wallType == "z":
                if wallPosition[1] == self.board.n-1:
                    return False
                if len(list(filter(lambda w: w.type == "z" and w.position[0] == wallPosition[0] and (w.position[1]-1 <= wallPosition[1] <= w.position[1]+1), allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
                if len(list(filter(lambda w: w.type == "p" and wallPosition[0]-1 == w.position[0] and wallPosition[1]+1 == w.position[1], allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            # zid se postavlja na validnu poziciju
            # provera da li se pesak pomera na validnu poziciju
            if playerPosition[0] < 0 or playerPosition[0] > self.board.m-1 or playerPosition[1] < 0 or playerPosition[1] > self.board.n-1:
                print("Pozicije zida su van okvira table")
                return False
            if playerNumber != 0 and playerNumber != 1:
                return False
            currentPosition = player.positions[playerNumber]
            movedX = abs(int(currentPosition[0])-playerPosition[0])
            movedY = abs(int(currentPosition[1])-playerPosition[1])
            if (movedX == 0 and movedY == 2) or (movedX == 2 and movedY == 0) or (movedX == movedY == 1):
                # validan potez
                # moze da bude i validan ako je rastojanje 1-proveriti da li je pesak na sledecem pa znaci da je blokiran i moze samo jedno polje
                # proveriti da li postoji zid izmedju ovih pozicija
                # proveriti da li je ciljno polje zauzeto, ako je zauzeto proveriti da li je pocetno polje protivnika
                # if len(list(filter(lambda p:p==playerPosition,otherPlayer.positions)))==0:
                return True
            else:
                return False

        # da li moze pozicije

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
game.board.walls.append(Wall((5, 3), "p"))
game.board.walls.append(Wall((2, 3), "z"))
game.nextMove()

print("")
