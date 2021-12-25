import re
import time
from math import sqrt

#from blockade_ai import check_for_paths

""" class Wall:
    def __init__(self, position: tuple[int, int], type):
        self.position = position
        self.type = type """


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


    def generate_figure_lines(self, stepXY, state, visited, to_visit):
        ret = list()
        pos = state

        new_row = pos[0] + stepXY
        if new_row < self.board.m:
            next_pos = (new_row, pos[1])
            if next_pos not in visited and next_pos not in to_visit:
                if not self.isBlockedByWall('p', pos, next_pos):
                    ret.append(next_pos)
        
        new_row = pos[0] - stepXY
        if new_row >= 0:
            next_pos = (new_row, pos[1])
            if next_pos not in visited and next_pos not in to_visit:
                if not self.isBlockedByWall('p', pos, next_pos):
                    ret.append(next_pos)


        new_col = pos[1] + stepXY
        if new_col < self.board.n:
            next_pos = (pos[0], new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if not self.isBlockedByWall('z', pos, next_pos):
                    ret.append(next_pos)
        
        new_col = pos[1] - stepXY
        if new_col >= 0:
            next_pos = (pos[0], new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if not self.isBlockedByWall('z', pos, next_pos):
                    ret.append(next_pos)
        
        ret.extend(self.generate_figure_diagonal_lines(state, visited, to_visit))
        return ret
    


    def generate_figure_diagonal_lines(self, state, visited, to_visit):
        ret = list()
        pos = state

        new_row = pos[0] - 1
        new_col = pos[1] - 1

        if new_row >= 0 and new_col >= 0:
            next_pos = (new_row, new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if self.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)
            

        new_row = pos[0] - 1
        new_col = pos[1] + 1
        
        if new_row >= 0 and new_col < self.board.n:
            next_pos = (new_row, new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if self.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)

        new_row = pos[0] + 1
        new_col = pos[1] - 1

        if new_row < self.board.m and new_col >= 0:
            next_pos = (new_row, new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if self.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)
        

        new_row = pos[0] + 1
        new_col = pos[1] + 1

        if new_row < self.board.m and new_col < self.board.n:
            next_pos = (new_row, new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if self.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)

        return ret



    def h_dist(self, state, dest):
        if state[0] - dest[0] == state[1] - dest[1]:
            return abs(state[0] - dest[0])
            #return abs(state[0] - dest[0]) + abs(state[1] - dest[1])
        return sqrt((state[0] - dest[0]) ** 2 + (state[1] - dest[1]) ** 2)


    #proveravamo da li zid blokira put do oba odredisna polja
    def check_for_paths(self) -> bool:
        #ovde idu provere za 2 i 3 i 4 zida, za 5 krecemo trazenje od svake figurice do oba ciljna polja

        #if len(self.board.walls) == 2:
            

        #trazenje puteva
        return self.check_all_paths(tuple(self.board.player1.positions[0]), tuple(self.board.player1.positions[1]), tuple(self.board.startPositionsO[0]), tuple(self.board.startPositionsO[1])) and \
        self.check_all_paths(tuple(self.board.player2.positions[0]), tuple(self.board.player2.positions[1]), tuple(self.board.startPositionsX[0]), tuple(self.board.startPositionsX[1]))

    
    def check_for_path(self, start_node, end_node, paths) -> tuple[bool, set]:

        start = time.time()
        """ start_f1 = tuple(self.board.player1.positions[0])
        start_f2 = tuple(self.board.player2.positions[1])
        dest_1 = tuple(self.board.startPositionsO[0])
        dest_2 = tuple(self.board.startPositionsO[1]) """

        found = False
        prev_nodes = dict()
        visited_nodes = set()
        nodes_to_visit = set()

        prev_nodes[start_node] = None
        nodes_to_visit.add(start_node)

        while(len(nodes_to_visit) > 0 and not found):
            state = None
            for next_state in nodes_to_visit:
                if next_state in paths:
                    state = next_state
                    break
                #if state is None or g[next_state] + self.h_dist(next_state, dest_1) < g[state] + self.h_dist(state, dest_1):
                if state is None or self.h_dist(next_state, end_node) < self.h_dist(state, end_node):
                    state = next_state

            if state == end_node:
                found = True
                break

            stepXY = 1 if self.h_dist(state, end_node) == 1 else 2
            for new_state in self.generate_figure_lines(stepXY, state, visited_nodes, nodes_to_visit):
                if new_state not in visited_nodes and new_state not in nodes_to_visit:
                    #g[new_state] = self.h_dist(new_state, start_f1)
                    nodes_to_visit.add(new_state)
                    prev_nodes[new_state] = state
                #elif new_state in nodes_to_visit:
                    #new_dist = self.h_dist(new_state, state)
                    #if g[new_state] > g[state] + new_dist:
                        #g[new_state] = g[state] + new_dist
                        #prev_nodes[new_state] = state
            

            nodes_to_visit.remove(state)
            visited_nodes.add(state)
        
        if not found:
            return (False, set())
        
        #ako je nadjen put dodajemo na prthodni put nove cvorove
        state = end_node
        while prev_nodes[state] is not None:
            paths.add(state)
            state = prev_nodes[state]
        paths.add(start_node)
        
        end = time.time()
        print(start_node, end_node)
        print(paths)
        print("A* : " +  str(end - start))
        return (True, paths)



    def check_all_paths(self, p_pos1, p_pos2, s_dest1, s_dest2) -> bool:
        paths = set()

        res = self.check_for_path(s_dest1, s_dest2, paths)
        if res[0] == False:
            return False

        res = self.check_for_path(p_pos1, s_dest1, paths)
        if res[0] == False:
            return False
        
        res = self.check_for_path(p_pos2, s_dest1, paths)
        return res[0]
