import re
import time


class Player:
    def __init__(self, positions: tuple[list[int], list[int]], type, num_walls):
        self.positions = positions
        self.type = type
        self.greenWallNumber = num_walls
        self.blueWallNumber = num_walls


class Board:
    def __init__(self, m, n, positions_p1: tuple[list[int], list[int]], positions_p2: tuple[list[int], list[int]], num_walls: int):
        self.m = m
        self.n = n
        self.startPositionsX = positions_p1
        self.startPositionsO = positions_p2
        self.player1 = Player(positions_p1, "x", num_walls)
        self.player2 = Player(positions_p2, "o", num_walls)
        self.walls = set()


class Game:
    def __init__(self):
        self.board = None
        self.isPlayerOneNext = None
        self.playerToMove = "x"

    def getStartState(self):
        print("Unesite broj vrsta table :")
        m = int(input())
        while m > 22 or m < 11:
            print("Broj vrsta mora biti izmedju 11 i 22!")
            m = int(input())

        print("Unesite broj kolona table :")
        n = int(input())
        while n > 28 or n < 14:
            print("Broj kolona mora biti izmedju 14 i 28!")
            n = int(input())

        print("Unesite broj zidova : ")
        k = int(input())
        while k > 18:
            print("Broj zidova mora biti manji od 18")
            k = int(input())

        print('Da li zelite da igrate prvi? Unesite "da" ili "ne" ')
        first = True if str(input()).lower() == "da" else False

        labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C",
                  "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]
        playerPositions = []
        while len(playerPositions) < 4:
            print("Unesite validne pocetne pozicije crvenih igraca x1 y1 x2 y2 ")
            position = input()
            playerPositions = re.findall(r"(\d+|\w+)", position, re.ASCII)
            for pp in playerPositions:
                if pp not in labels:
                    playerPositions = []
                    break
            if playerPositions == []:
                continue
            playerPositions = list(
                map(lambda x: labels.index(x.upper()), playerPositions))
            if playerPositions[0] > m or playerPositions[1] > n or playerPositions[2] > m or playerPositions[3] > n:
                playerPositions = []
                print("Pozicije su van okvira table")
            elif playerPositions[0] == playerPositions[2] and playerPositions[1] == playerPositions[3]:
                playerPositions = []
                print("Dva igraca ne mogu biti na istoj poziciji.")

        playerPositions = ([playerPositions[0], playerPositions[1]], [
                           playerPositions[2], playerPositions[3]])

        otherPlayerPositions = []
        while len(otherPlayerPositions) < 4:
            print("Unesite validne pocetne pozicije zutih igraca x1 y1 x2 y2 ")
            position = input()
            otherPlayerPositions = re.findall(r"(\d+|\w+)", position, re.ASCII)
            for op in otherPlayerPositions:
                if op not in labels:
                    otherPlayerPositions = []
                    break
            if otherPlayerPositions == []:
                continue
            otherPlayerPositions = list(
                map(lambda x: labels.index(x.upper()), otherPlayerPositions))
            if otherPlayerPositions[0] > m or otherPlayerPositions[1] > n or otherPlayerPositions[2] > m or otherPlayerPositions[3] > n:
                otherPlayerPositions = []
                print("Pozicije su van okvira table")
            elif otherPlayerPositions[0] == otherPlayerPositions[2] and otherPlayerPositions[1] == otherPlayerPositions[3]:
                otherPlayerPositions = []
                print("Dva igraca ne mogu biti na istoj poziciji.")
            else:
                for i in range(2):
                    for j in range(2):
                        if playerPositions[i][0] == otherPlayerPositions[j*2] and playerPositions[i][1] == otherPlayerPositions[j*2+1]:
                            otherPlayerPositions = []
                            print("Crveni igrac vec zauzima ovu poziciju")
                            break
                    if otherPlayerPositions == []:
                        break

        otherPlayerPositions = ([otherPlayerPositions[0], otherPlayerPositions[1]], [
                                otherPlayerPositions[2], otherPlayerPositions[3]])

        self.setBoard(Board(m, n, playerPositions, otherPlayerPositions, k))
        self.isPlayerOneNext = True if (first) else False

    def isEnd(self):
        return bool(
            len(list(x for x in self.board.player1.positions if x in self.board.startPositionsO))
            or len(list(x for x in self.board.player2.positions if x in self.board.startPositionsX)))

    def setBoard(self, board):
        self.board = board

    """  def nextMove(self):
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
                self.isPlayerOneNext = not self.isPlayerOneNext """

    def nextMove(self, ai, playerNumber, wallPosition, wallType, playerType, playerPosition):
        if playerType != self.playerToMove:
            return False

        if self.isValidMove(playerNumber, playerType, list(playerPosition), wallPosition, wallType):
            # generise stanje i onda da se proveri da l zatvara, pa to stanje se salje u change
            newState = ai.generateState(self, playerNumber, wallPosition, wallType, playerPosition)
            if (newState):
                self.changeBoardState(
                    playerNumber, playerPosition, wallPosition, wallType, playerType)
                self.isPlayerOneNext = not self.isPlayerOneNext
                self.playerToMove = "x" if self.playerToMove == "o" else "o"
                #ovo dodajem
                #ai.check_for_paths()
                #kraj dodavanja
                return True
        return False

    """  def generateState(self, playerNumber, wallPosition, wallType, playerPosition):
        newGame = copy.deepcopy(self)
        newGame.changeBoardState(
            playerNumber, playerPosition, wallPosition, wallType, newGame.playerToMove)
        newGame.isPlayerOneNext = not self.isPlayerOneNext
        newGame.playerToMove = "x" if newGame.playerToMove == "o" else "x"
        # provera da li zatvara
        oldGame = .set_game(newGame)
        return newGame if ai.check_for_paths() else None

    def generateNextGameStates(self, game):
        next_states = []
        # koji je igrac na redu
        player = game.board.player1 if game.playerToMove == "x" else game.board.player2
        # potezi za svaku figuru
        player0_moves = list(
            map(lambda pair: (0, pair), game.generate_player_moves(0)))
        player1_moves = list(
            map(lambda pair: (1, pair), game.generate_player_moves(1)))
        player_moves = [*player0_moves, *player1_moves]
        # sve moguce pozicije za postavljanje zida, bilo plavi bilo zeleni - ukoliko je njihov br veci od 0
        wall_moves = game.generate_wall_moves(
            game, player.greenWallNumber, player.blueWallNumber)
        # ((br igraca, pozicija), zid)
        if (len(wall_moves) > 0):
            next_states = list(product(player_moves, wall_moves))
            next_states = list(filter(lambda state: state != None, map(lambda params: game.generateState(
                params[0][0], [params[1][0], params[1][1]], params[1][2], params[0][1]), next_states)))
        else:
            next_states = list(filter(lambda state: state != None, map(
                lambda params: game.generateState(params[0], [], '', params[1]), player_moves)))
        # lista Game-ova sa novom pozicijom i dodatim zidom

        return next_states """



    def isValidMove(self, playerNumber, playerType, playerPosition, wallPosition, wallType):
        if playerNumber != 0 and playerNumber != 1 and playerType != "x" and playerType != "o":
            return False

        if(self.playerToMove != playerType):
            #print("Drugi igrac je na redu")
            return False

        player = self.board.player1 if playerType == "x" else self.board.player2
        otherPlayer = self.board.player2 if playerType == "x" else self.board.player1
        # if playerPosition == player.positions[abs(playerNumber-1)]:
        # return False
        if player.greenWallNumber > 0 or player.blueWallNumber > 0:
            if len(wallPosition) == 0:
                #print("Niste uneli pozicije zida")
                return False
            if not self.isValidWallMove(player, wallPosition, wallType):
                return False

        # zid se postavlja na validnu poziciju
        # provera da li se pesak pomera na validnu poziciju
        otherPlayerStart = self.board.startPositionsO if playerType == "x" else self.board.startPositionsX
        if not self.isValidPlayerMove(player.positions[playerNumber], playerPosition, otherPlayer.positions, otherPlayerStart, player.positions[abs(playerNumber-1)]):
            return False
        return True

    def isValidWallMove(self, player, wallPosition, wallType):
        if len(wallPosition) == 2:
            if (player.greenWallNumber == 0 and wallType == "z") or (player.blueWallNumber == 0 and wallType == "p"):
                #print("Iskoristili ste sve zidove ove boje")
                return False
            # dozvoljeno je da stavi zid te boje, provera da li su pozicije zida validne
            if wallPosition[0] < 0 or wallPosition[0] > self.board.m-1 or wallPosition[1] < 0 or wallPosition[1] > self.board.n-1:
                #print("Pozicije zida su van okvira table")
                return False
            if wallType == "p":
                if wallPosition[0] == self.board.m-1:
                    return False
                if (wallPosition[0], wallPosition[1]-1, 'p') in self.board.walls or (wallPosition[0], wallPosition[1]+1, 'p') in self.board.walls:
                    #print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            elif wallType == "z":
                if wallPosition[1] == self.board.n-1:
                    return False
                if (wallPosition[0]-1, wallPosition[1], 'z') in self.board.walls or (wallPosition[0]+1, wallPosition[1], 'z') in self.board.walls:
                    #print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            if (wallPosition[0], wallPosition[1], 'z') in self.board.walls or (wallPosition[0], wallPosition[1], 'p') in self.board.walls:
                #print("Na tabli postoji zid koji zauzima ovu poziciju")
                return False
            return True

    def isValidPlayerMove(self, currentPosition, nextPosition, otherPlayerPositions, otherPlayerStart, currentPosition2):
        if nextPosition == currentPosition2:
            return False
        if nextPosition[0] < 0 or nextPosition[0] > self.board.m-1 or nextPosition[1] < 0 or nextPosition[1] > self.board.n-1:
            #print("Pozicije zida su van okvira table")
            return False
        movedY = abs(currentPosition[0]-nextPosition[0])
        movedX = abs(currentPosition[1]-nextPosition[1])

        # jedno ili dva polja u levo/desno/gore/dole ili dijagonalno
        if movedX == 0 or movedY == 0 or movedX == movedY == 1:
            if movedX == movedY == 1:  # dijagonalno
                if self.isBlockedByWall("p", currentPosition, (nextPosition[0], currentPosition[1])):
                    if self.isBlockedByWall("p", (currentPosition[0], nextPosition[1]), nextPosition) or self.isBlockedByWall("z", currentPosition, (currentPosition[0], nextPosition[1])):
                        return False
                elif self.isBlockedByWall("z", (nextPosition[0], currentPosition[1]), nextPosition):
                    if self.isBlockedByWall("z", currentPosition, (currentPosition[0], nextPosition[1])) or self.isBlockedByWall("p", (currentPosition[0], nextPosition[1]), nextPosition):
                        return False
                # Nije blokiran zidom
            elif movedX == 1 or movedY == 1:  # jedno polje levo/desno/gore/dole
                if self.isBlockedByWall("p" if movedX == 0 else "z", currentPosition, nextPosition):
                    return False
                else:
                    if movedX == 0:
                        pos = [
                            currentPosition[0]-(currentPosition[0]-nextPosition[0])*2, currentPosition[1]]
                        if not (pos in otherPlayerPositions or nextPosition in otherPlayerStart):
                            return False
                    elif movedY == 0:
                        pos = [currentPosition[0], currentPosition[1] -
                               (currentPosition[1]-nextPosition[1])*2]
                        if not (pos in otherPlayerPositions or nextPosition in otherPlayerStart):
                            return False
                    # blokiran je pesakom pa sme jedno polje levo/desno/gore/dole
            elif movedX == 2 or movedY == 2:  # dva polja levo/desno/gore/dole
                if self.isBlockedByWall("p" if movedX == 0 else "z", currentPosition, nextPosition):
                    return False
            else:  # nevalidna pozicija
                return False
            if nextPosition in otherPlayerPositions:
                if nextPosition in otherPlayerStart:
                    return True
                return False

            return True
        else:
            return False

    def isBlockedByWall(self, type, position, nextPosition):
        if type == 'p':
            r = range(position[0], nextPosition[0]) if position[0] < nextPosition[0] else range(
                nextPosition[0], position[0])
            for i in r:
                if (i, position[1], 'p') in self.board.walls or (i, position[1]-1, 'p') in self.board.walls:
                    return True
        else:
            r = range(position[1], nextPosition[1]) if position[1] < nextPosition[1] else range(
                nextPosition[1], position[1])
            for i in r:
                if (position[0], i, 'z') in self.board.walls or (position[0]-1, i, 'z') in self.board.walls:
                    return True
        return False

    def changeBoardState(self, playerNumber, playerPosition, wallPosition, wallType, playerType):
        if playerType == "x":
            self.changePlayerStats(
                self.board.player1, wallType, playerPosition, playerNumber)
        else:
            self.changePlayerStats(
                self.board.player2, wallType, playerPosition, playerNumber)

        if(len(wallPosition) == 2):
            self.board.walls.add((wallPosition[0], wallPosition[1], wallType))

    def changePlayerStats(self, player, wallType, playerPosition, playerNumber):
        player.positions = (
            player.positions[0] if playerNumber else list(playerPosition),
            player.positions[1] if not playerNumber else list(playerPosition),
        )
        if wallType == "z":
            player.greenWallNumber -= 1
        elif wallType == "p":
            player.blueWallNumber -= 1

    def generate_player_moves(self, figure_num):
        figure_pos = self.board.player1.positions[
            figure_num] if self.playerToMove == 'x' else self.board.player2.positions[figure_num]

        all_moves = [[figure_pos[0] + 2, figure_pos[1]], [figure_pos[0] - 2, figure_pos[1]], [figure_pos[0], figure_pos[1] + 2],
                     [figure_pos[0], figure_pos[1] - 2], [figure_pos[0] + 1,
                                                          figure_pos[1] + 1], [figure_pos[0] - 1, figure_pos[1] - 1],
                     [figure_pos[0] + 1, figure_pos[1] - 1], [figure_pos[0] - 1,
                                                              figure_pos[1] + 1], [figure_pos[0] + 1, figure_pos[1]],
                     [figure_pos[0] - 1, figure_pos[1]], [figure_pos[0], figure_pos[1] + 1], [figure_pos[0], figure_pos[1] - 1]]

        ret = list()
        other_players = self.board.player1.positions if self.playerToMove == 'o' else self.board.player2.positions
        other_start = self.board.startPositionsX if self.playerToMove == 'o' else self.board.startPositionsO
        player = self.board.player1 if self.playerToMove == 'x' else self.board.player2
        player_figure_2 = player.positions[0] if figure_num == 1 else player.positions[1]

        for move in all_moves:
            if self.isValidPlayerMove(figure_pos, move, other_players, other_start, player_figure_2):
                ret.append(tuple(move))

        return ret

    def generate_wall_moves(self, game, green, blue):
        walls = set()
        for x in range(0, game.board.m-1):
            for y in range(0, game.board.n-1):
                if green:
                    walls.add((x, y, "z"))
                if blue:
                    walls.add((x, y, "p"))
        player = game.board.player1 if game.playerToMove == "x" else game.board.player2
        walls = set(filter(lambda wall: game.isValidWallMove(
            player, [wall[0], wall[1]], wall[2]), walls))
        #return walls

        """ if len(game.board.walls) != 0:
            walls = set(
                filter(
                    lambda wall: game.filterWallMoves(wall[0], wall[1], wall[2]), walls
                )
            ) """
        return walls
    


    def checkNewWall(self, wallPosition, wallType):
        #ovde idu provere za 2 i 3 i 4 zida, za 5 krecemo trazenje od svake figurice do oba ciljna polja
        if len(self.board.walls) == 0:
            return False

        num = 0
        if wallType == 'p':
            if wallPosition[1] == 0 or wallPosition[1] == self.board.n-2:
                num = num+1
            positions = [(wallPosition[0], wallPosition[1]-2, 'p'),
                         (wallPosition[0], wallPosition[1]+2, 'p')]
            for p in positions:
                if p in self.board.walls:
                    num = num+1
                    if num == 2:
                        # print("true")
                        return True
        else:
            if wallPosition[0] == 0 or wallPosition[0] == self.board.m-2:
                num = num+1
            positions = [(wallPosition[0]-2, wallPosition[1], 'z'),
                         (wallPosition[0]+2, wallPosition[1], 'z')]
            for p in positions:
                if p in self.board.walls:
                    num = num+1
                    if num == 2:
                        # print("true")
                        return True
        type = 'p' if wallType == 'z' else 'z'
        positions = [(wallPosition[0]-1, wallPosition[1]-1, type), (wallPosition[0]-1, wallPosition[1], type), (wallPosition[0]-1, wallPosition[1]+1, type),
                     (wallPosition[0]+1, wallPosition[1]-1, type), (wallPosition[0]+1,
                                                                    wallPosition[1], type), (wallPosition[0]+1, wallPosition[1]+1, type),
                     (wallPosition[0], wallPosition[1]-1, type), (wallPosition[0], wallPosition[1]+1, type)]
        for p in positions:
            if p in self.board.walls:
                num = num+1
                if num == 2:
                    # print("true")
                    return True
        # print("false")
        return False



    def computerMove(self, ai, depth1, depth2):
        prev_state = dict()
        depth = depth1

        if self.board.player1.greenWallNumber == 0 and self.board.player1.blueWallNumber == 0 \
            and self.board.player2.greenWallNumber == 0 and self.board.player2.blueWallNumber == 0:
            depth = depth2

        max_player = None
        if self.playerToMove == 'o':
            max_player = True
        else:
            max_player = False

        best_state = ai.minmax(self, depth, -10000, 10000, max_player, prev_state)
        return best_state[0]
    









    def filterWallMoves(self, x, y, type):

        player = (
            self.board.player2.positions
            if self.playerToMove == "x"
            else self.board.player1.positions
        )
        start = (
            self.board.startPositionsX
            if self.playerToMove == "x"
            else self.board.startPositionsO
        )
        size = 1  # self.board.m/4  if type=='z' else self.board.n/4
        # ukoliko je blizu vrati true
        if (
            self.distance((x, y), start[0]) < size
            or self.distance((x, y), start[1]) < size
        ):
            return True
        if (
            self.distance((x, y), player[0]) < size
            or self.distance((x, y), player[1]) < size
        ):
            return True
        # ne dodiruje sa drugim zidom
        if type == "z":
            if (
                (x - 2, y, "z") in self.board.walls
                or (x + 2, y, "z") in self.board.walls
                or (x, y - 1, "p") in self.board.walls 
                or (x - 1,y - 1,"p") in self.board.walls
                or (x + 1, y - 1, "p") in self.board.walls 
                or (x-1,y + 1 ,"p") in self.board.walls
                or (x, y + 1, "p") in self.board.walls 
                or (x+1,y+1 ,"p") in self.board.walls
                or (x-1,y ,"p") in self.board.walls
                or (x+1,y ,"p") in self.board.walls
            ):
                return True
        if type == "p":
            if (
                (x, y - 2, "p") in self.board.walls 
                or (x,y + 2,"p") in self.board.walls
                or (x - 1, y - 1, "z") in self.board.walls
                or (x, y - 1, "z") in self.board.walls
                or (x + 1, y-1, "z") in self.board.walls
                or (x - 1, y, "z") in self.board.walls
                or (x + 1, y, "z") in self.board.walls
                or (x - 1, y + 1, "z") in self.board.walls
                or (x, y + 1, "z") in self.board.walls
                or (x + 1, y + 1, "z") in self.board.walls

            ):
                return True
        return False

    def distance(self, state, dest):
        if state[0] - dest[0] == state[1] - dest[1]:
            return abs(state[0] - dest[0])
        return abs(state[0] - dest[0]) + abs(state[1] - dest[1])