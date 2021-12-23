import re


class Wall:
    def __init__(self, position: tuple[int, int], type):
        self.position = position
        self.type = type


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
        self.walls = []


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
            print("Unesite pocetne pozicije crvenih igraca x1 y1 x2 y2 ")
            position = input()
            playerPositions = re.findall(r"(\d+|\w+)", position, re.ASCII)
            playerPositions = list(
                map(lambda x: labels.index(x.upper()), playerPositions))
        playerPositions = ([playerPositions[0], playerPositions[1]], [
                           playerPositions[2], playerPositions[3]])

        otherPlayerPositions = []
        while len(otherPlayerPositions) < 4:
            print("Unesite pocetne pozicije zutih igraca x1 y1 x2 y2 ")
            position = input()
            otherPlayerPositions = re.findall(r"(\d+|\w+)", position, re.ASCII)
            otherPlayerPositions = list(
                map(lambda x: labels.index(x.upper()), otherPlayerPositions))
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

    def nextMove(self, playerNumber, wallPosition, wallType, playerType, playerPosition):
        if playerType != self.playerToMove:
            return False

        if self.isValidMove(playerNumber, playerType, list(playerPosition), wallPosition, wallType):

            self.changeBoardState(
                playerNumber, playerPosition, wallPosition, wallType, playerType)
            self.isPlayerOneNext = not self.isPlayerOneNext
            self.playerToMove = "x" if self.playerToMove == "o" else "o"
            return True
        return False

    def isValidMove(self, playerNumber, playerType, playerPosition, wallPosition, wallType):
        if playerNumber != 0 and playerNumber != 1 and playerType != "x" and playerType != "o":
            return False

        if(self.playerToMove != playerType):
            print("Drugi igrac je na redu")
            return False

        player = self.board.player1 if playerType == "x" else self.board.player2
        otherPlayer = self.board.player2 if playerType == "x" else self.board.player1
        # if playerPosition == player.positions[abs(playerNumber-1)]:
        # return False
        if player.greenWallNumber > 0 or player.blueWallNumber > 0:
            if len(wallPosition) == 0:
                print("Niste uneli pozicije zida")
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
                if len(list(filter(lambda w: w.type == "p" and w.position[0] == wallPosition[0] and (w.position[1]-1 <= wallPosition[1] <= w.position[1]+1), allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
                if len(list(filter(lambda w: w.type == "z" and w.position[0] == wallPosition[0] and w.position[1] == wallPosition[1], allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            elif wallType == "z":
                if wallPosition[1] == self.board.n-1:
                    return False
                if len(list(filter(lambda w: w.type == "z" and w.position[1] == wallPosition[1] and (w.position[0]-1 <= wallPosition[0] <= w.position[0]+1), allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
                if len(list(filter(lambda w: w.type == "p" and wallPosition[0] == w.position[0] and wallPosition[1] == w.position[1], allWalls))) > 0:
                    print("Na tabli postoji zid koji zauzima ovu poziciju")
                    return False
            return True

    def isValidPlayerMove(self, currentPosition, nextPosition, otherPlayerPositions, otherPlayerStart, currentPosition2):
        if nextPosition == currentPosition2:
            return False
        if nextPosition[0] < 0 or nextPosition[0] > self.board.m-1 or nextPosition[1] < 0 or nextPosition[1] > self.board.n-1:
            print("Pozicije zida su van okvira table")
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
        if type == "p" and len(list(filter(lambda w: w.type == type and (w.position[1] == position[1] or w.position[1]+1 == position[1]) and (w.position[0] in range(*sorted([position[0], nextPosition[0]]))), self.board.walls))) > 0:
            return True
        elif type == "z" and len(list(filter(lambda w: w.type == type and (w.position[0] == position[0] or w.position[0]+1 == position[0]) and (w.position[1] in range(*sorted([position[1], nextPosition[1]]))), self.board.walls))) > 0:
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
            self.board.walls.append(Wall(wallPosition, wallType))

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

    def generate_figure_lines(self, state, stepXY, stepD):
        ret = list()

        pos = state
        next_pos = (pos[0] + 2, pos[1])
        while next_pos[0] < self.board.m:
            if not self.isBlockedByWall('p', pos, next_pos):
                ret.append(next_pos)
                pos = next_pos
                next_pos = (next_pos[0] + 2, pos[1])
            else:
                break

        pos = state
        next_pos = (pos[0] - 2, pos[1])
        while next_pos[0] >= 0:
            if not self.isBlockedByWall('p', pos, next_pos):
                ret.append(next_pos)
                pos = next_pos
                next_pos = (next_pos[0] - 2, pos[1])
            else:
                break

        pos = state
        next_pos = (pos[0], pos[1] + 2)
        while next_pos[1] < self.board.n:
            if not self.isBlockedByWall('z', pos, next_pos):
                ret.append(next_pos)
                pos = next_pos
                next_pos = (next_pos[0], pos[1] + 2)
            else:
                break

        pos = state
        next_pos = (pos[0], pos[1] - 2)
        while next_pos[1] >= 0:
            if not self.isBlockedByWall('z', pos, next_pos):
                ret.append(next_pos)
                pos = next_pos
                next_pos = (next_pos[0], pos[1] - 2)
            else:
                break

        ret.append(self.generate_figure_diagonal_lines(state, stepXY, stepD))
        return ret

    def generate_figure_diagonal_lines(self, state, stepXY, stepD):
        ret = list()
        pos = state
        next_pos = (pos[0] - 1, pos[1] - 1)
        while next_pos[0] >= 0 and next_pos[1] >= 0:
            if self.isBlockedByWall("p", pos, (next_pos[0], next_pos[1])):
                if self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1])):
                    break
            elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                if self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos):
                    break
            ret.append(next_pos)
            pos = next_pos
            next_pos = (next_pos[0]-1, pos[1] - 1)

        pos = state
        next_pos = (pos[0] - 1, pos[1] + 1)
        while next_pos[0] >= 0 and next_pos[1] < self.board.n:
            if self.isBlockedByWall("p", pos, (next_pos[0], next_pos[1])):
                if self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1])):
                    break
            elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                if self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos):
                    break
            ret.append(next_pos)
            pos = next_pos
            next_pos = (next_pos[0]-1, pos[1] + 1)

        pos = state
        next_pos = (pos[0] + 1, pos[1] - 1)
        while next_pos[0] < self.board.m and next_pos[1] >= 0:
            if self.isBlockedByWall("p", pos, (next_pos[0], next_pos[1])):
                if self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1])):
                    break
            elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                if self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos):
                    break
            ret.append(next_pos)
            pos = next_pos
            next_pos = (next_pos[0]+1, pos[1] - 1)

        pos = state
        next_pos = (pos[0] + 1, pos[1] + 1)
        while next_pos[0] < self.board.m and next_pos[1] < self.board.n:
            if self.isBlockedByWall("p", pos, (next_pos[0], next_pos[1])):
                if self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1])):
                    break
            elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                if self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos):
                    break
            ret.append(next_pos)
            pos = next_pos
            next_pos = (next_pos[0]+1, pos[1] + 1)

        return ret

    def h_dist(self, state, dest):
        if state[0] - dest[0] == state[1] - dest[1]:
            return state[0] - dest[0]
        else:
            return abs(state[0] - dest[0]) + abs(state[1] - dest[1])

    # proveravamo da li zid blokira put do oba odredisna polja

    def check_for_paths() -> bool:
        return

    def check_red_paths(self, stepXY: int, stepD: int) -> bool:

        start_f1 = tuple(self.board.player1.positions[0])
        start_f2 = tuple(self.board.player2.positions[1])
        dest_1 = tuple(self.board.startPositionsO[0])
        dest_2 = tuple(self.board.startPositionsO[1])

        # moramo da nadjemo put do oba ciljna cvora
        found_1 = found_2 = False
        path_1 = list()
        path_2 = set()
        prev_nodes = dict()
        visited_nodes = set()
        nodes_to_visit = set()
        g = dict()

        prev_nodes[start_f1] = None
        g[start_f1] = None
        nodes_to_visit.add(start_f1)

        while(len(nodes_to_visit) > 0 and not found_1):
            state = None
            for next_state in nodes_to_visit:
                if state is None or g[state] > g[next_state]:
                    state = next_state

            if state == dest_1:
                found_1 = True
                break

            for new_state in self.generate_figure_lines(state, stepXY, stepD):
                if new_state not in visited_nodes and new_state not in nodes_to_visit:
                    g[new_state] = self.h_dist(new_state, dest_1)
                    nodes_to_visit.add(new_state)
                    prev_nodes[new_state] = state

            nodes_to_visit.remove(state)
            visited_nodes.add(state)

        if found_1:
            state = dest_1
            while prev_nodes[state] is not None:
                path_1.append(state)
                state = prev_nodes[state]
            path_1.append(start_f1)
            path_1.reverse()
            print(path_1)

        return path_1
