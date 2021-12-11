import re


class Wall:
    def __init__(self, position: tuple[int, int], type):
        self.position = position
        self.type = type


class Player:
    def __init__(self, positions: tuple[list[int], list[int]], type, k):
        self.positions = positions
        self.type = type
        self.greenWallNumber = k
        self.blueWallNumber = k


class Board:
    def __init__(
        self, m, n, positions_p1: tuple[list[int], list[int]], positions_p2, k, first
    ):
        self.m = m
        self.n = n
        self.startPositionX = positions_p1
        self.startPositionO = positions_p2
        self.player1 = Player(positions_p1, "x" if first else "o", k)
        self.player2 = Player(positions_p2, "o" if first else "x", k)
        self.walls = []

    def getBoardState(self):
        return


class Game:
    def __init__(self):
        self.board = None
        self.isPlayerOneNext = None

    def setStartState(self, m, n, playerPositions, otherPlayerPositions, k, first):
        self.isPlayerOneNext = True if (first == "da") else False
        self.setBoard(
            Board(m, n, playerPositions, otherPlayerPositions, k, self.isPlayerOneNext)
        )

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

    def nextMove(
        self, playerNumber, wallPosition, wallType, playerType, playerPosition
    ):
        if self.isValidMove(
            playerNumber, playerType, playerPosition, wallPosition, wallType
        ):
            self.changeBoardState(playerNumber, playerPosition, wallPosition, wallType)
            self.isPlayerOneNext = not self.isPlayerOneNext

    def isValidMove(
        self, playerNumber, playerType, playerPosition, wallPosition, wallType
    ):
        if (
            playerNumber != 0
            and playerNumber != 1
            and playerType != "x"
            and playerType != "o"
        ):
            return False

        if (self.isPlayerOneNext and self.board.player1.type != playerType) or (
            not self.isPlayerOneNext and self.board.player2.type != playerType
        ):
            print("Drugi igrac je na redu")
            return False

        player = self.board.player1 if playerType == "x" else self.board.player2
        otherPlayer = self.board.player2 if playerType == "x" else self.board.player1
        if player.positions[playerNumber] == player.positions[abs(playerNumber - 1)]:
            return False
        if len(wallPosition) == 0 and (
            player.greenWallNumber > 0 or player.blueWallNumber > 0
        ):
            print("Niste uneli pozicije zida")
            return False
        if not self.isValidWallMove(player, wallPosition, wallType):
            return False
        # zid se postavlja na validnu poziciju
        # provera da li se pesak pomera na validnu poziciju
        otherPlayerStart = (
            self.board.startPositionO
            if playerType == "x"
            else self.board.startPositionX
        )
        if not self.isValidPlayerMove(
            player.positions[playerNumber],
            playerPosition,
            otherPlayer.positions,
            otherPlayerStart,
        ):
            return False
        return True

    def isValidWallMove(self, player, wallPosition, wallType):
        if len(wallPosition) == 2:
            if (player.greenWallNumber == 0 and wallType == "z") or (
                player.blueWallNumber == 0 and wallType == "p"
            ):
                print("Iskoristili ste sve zidove ove boje")
                return False
            # dozvoljeno je da stavi zid te boje, provera da li su pozicije zida validne
            if (
                wallPosition[0] < 0
                or wallPosition[0] > self.board.m - 1
                or wallPosition[1] < 0
                or wallPosition[1] > self.board.n - 1
            ):
                print("Pozicije zida su van okvira table")
                return False
            allWalls = self.board.walls
            if wallType == "p":
                if wallPosition[0] == self.board.m - 1:
                    return False
                if (
                    len(
                        list(
                            filter(
                                lambda w: w.type == "p"
                                and w.position[1] == wallPosition[1]
                                and (
                                    w.position[0] - 1
                                    <= wallPosition[0]
                                    <= w.position[0] + 1
                                ),
                                allWalls,
                            )
                        )
                    )
                    > 0
                ):
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
                if (
                    len(
                        list(
                            filter(
                                lambda w: w.type == "z"
                                and w.position[0] - 1 == wallPosition[0]
                                and w.position[1] + 1 == wallPosition[1],
                                allWalls,
                            )
                        )
                    )
                    > 0
                ):
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            elif wallType == "z":
                if wallPosition[1] == self.board.n - 1:
                    return False
                if (
                    len(
                        list(
                            filter(
                                lambda w: w.type == "z"
                                and w.position[0] == wallPosition[0]
                                and (
                                    w.position[1] - 1
                                    <= wallPosition[1]
                                    <= w.position[1] + 1
                                ),
                                allWalls,
                            )
                        )
                    )
                    > 0
                ):
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
                if (
                    len(
                        list(
                            filter(
                                lambda w: w.type == "p"
                                and wallPosition[0] - 1 == w.position[0]
                                and wallPosition[1] + 1 == w.position[1],
                                allWalls,
                            )
                        )
                    )
                    > 0
                ):
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            return True

    def isValidPlayerMove(
        self, currentPosition, nextPosition, otherPlayerPositions, otherPlayerStart
    ):
        if (
            nextPosition[0] < 0
            or nextPosition[0] > self.board.m - 1
            or nextPosition[1] < 0
            or nextPosition[1] > self.board.n - 1
        ):
            print("Pozicije zida su van okvira table")
            return False

        movedY = abs(int(currentPosition[0]) - nextPosition[0])
        movedX = abs(int(currentPosition[1]) - nextPosition[1])
        if movedX == movedY == 0:
            return False
        # jedno ili dva polja u levo/desno/gore/dole ili dijagonalno
        if movedX == 0 or movedY == 0 or movedX == movedY == 1:
            if movedX == movedY == 1:  # dijagonalno
                return True  # PROVERITI da li je blokirano zidom.. kako??
            elif movedX == 1 or movedY == 1:  # jedno polje levo/desno/gore/dole
                if self.isBlockedByWall(
                    "p" if movedX == 0 else "z", currentPosition, nextPosition
                ):
                    return False
                else:
                    return True  # PROVERI da li je blokiran pesakom

            elif movedX == 2 or movedY == 2:  # dva polja levo/desno/gore/dole
                if self.isBlockedByWall(
                    "p" if movedX == 0 else "z", currentPosition, nextPosition
                ):
                    return False

            if nextPosition in otherPlayerPositions:
                if nextPosition in otherPlayerStart:
                    # DA LI treba ukloniti protivnickog igraca??
                    return True
                return False

            return True
        else:
            return False

    def isBlockedByWall(self, type, position, nextPosition):
        if (
            type == "p"
            and len(
                list(
                    filter(
                        lambda w: w.type == type
                        and (
                            w.position[1] == position[1]
                            or w.position[1] + 1 == position[1]
                        )
                        and (
                            w.position[0]
                            in range(*sorted(position[0], nextPosition[0]))
                        ),
                        self.board.walls,
                    )
                )
            )
            > 0
        ):
            return False
        elif (
            type == "z"
            and len(
                list(
                    filter(
                        lambda w: w.type == type
                        and (
                            w.position[0] == position[0]
                            or w.position[0] + 1 == position[0]
                        )
                        and (
                            w.position[1]
                            in range(*sorted(position[1], nextPosition[1]))
                        ),
                        self.board.walls,
                    )
                )
            )
            > 0
        ):
            return False

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

    # def nextMove(self):
    #     valid = False
    #     while not valid:
    #         print("Unesite sledeci validan potez: X|O 1|2 m n p|z x y")
    #         move = input()
    #         playerNumber, *positions = re.findall(r"(\d+)", move)
    #         playerNumber = int(playerNumber) - 1
    #         playerPosition = (int(positions[0]), int(positions[1]))
    #         if len(positions) == 4:  # jer mozda nema vise zidova
    #             wallPosition = (int(positions[2]), int(positions[3]))
    #             wallType = re.findall("[zZ]|[Pp]", move)[0].lower()
    #         else:
    #             wallPosition = []
    #             wallType = None
    #         playerType = re.findall("[xX]|[oO]", move)[0].lower()

    #         valid = self.isValidMove(
    #             playerNumber, playerType, playerPosition, wallPosition, wallType
    #         )
    #         if valid:
    #             self.changeBoardState(
    #                 playerNumber, playerPosition, wallPosition, wallType
    #             )
    #             self.isPlayerOneNext = not self.isPlayerOneNext

    # def getStartState(self):
    #     m = 23
    #     while m > 21:
    #         print("Unesite sirinu table. Sirina mora biti manja od 22.")
    #         m = 14  # int(input())

    #     n = 30
    #     while n > 27:
    #         print("Unesite visinu table. Visina mora biti manja od 28.")
    #         n = 13  # int(input())

    #     k = 19
    #     while k > 18:
    #         print("Unesite broj zidova po igracu. Maksimalno 18.")
    #         k = 8  # int(input())

    #     first = None
    #     while not first:
    #         print('Da li zelite da igrate prvi? Unesite "da" ili "ne" ')
    #         first = "da"  # input().lower()

    #     playerPositions = []
    #     while len(playerPositions) < 4:
    #         print("Unesite pocetne pozicije vasih igraca x1 y1 x2 y2 ")
    #         position = "1 2 3 4"  # input()
    #         playerPositions = re.findall(r"(\d+)", position)
    #     playerPositions = (playerPositions[0::2], playerPositions[1::2])

    #     otherPlayerPositions = []
    #     while len(otherPlayerPositions) < 4:
    #         print("Unesite pocetne pozicije protivnickih igraca x1 y1 x2 y2 ")
    #         position = "5 6 7 8"  # input()
    #         otherPlayerPositions = re.findall(r"(\d+)", position)
    #     otherPlayerPositions = (
    #         otherPlayerPositions[0::2],
    #         otherPlayerPositions[1::2],
    #     )

    #     self.isPlayerOneNext = True if (first == "da") else False
    #     self.setBoard(
    #         Board(m, n, playerPositions, otherPlayerPositions, k, self.isPlayerOneNext)
    #     )


game = Game()
game.getStartState()
# game.nextMove()

print("")
