import copy
from itertools import product
import heapq

class BlockadeAI:
    def __init__(self, game):
        self.game = game
        self.dist_red1 = dict()
        self.dist_red2 = dict()
        self.dist_yellow1 = dict()
        self.dist_yellow2 = dict()
        self.initialize_dists(self.game)
        self.prev_paths = [set(), set()]



    def initialize_dists(self, game):
        red_start1 = tuple(game.board.startPositionsX[0])
        red_start2 = tuple(game.board.startPositionsX[1])
        yellow_start1 = tuple(game.board.startPositionsO[0])
        yellow_start2 = tuple(game.board.startPositionsO[1])

        for i in range (0, game.board.m):
            for j in range(0, game.board.n):
                self.dist_red1[(i, j)] = self.h_dist((i, j), red_start1)
                self.dist_red2[(i, j)] = self.h_dist((i, j), red_start2)
                self.dist_yellow1[(i, j)] = self.h_dist((i, j), yellow_start1)
                self.dist_yellow2[(i, j)] = self.h_dist((i, j), yellow_start2)

    
    def set_game(self, game):
        oldGame = self.game
        self.game = game
        return oldGame



    #generisanje mogucih poteza
    def generate_figure_lines(self, stepXY, state, visited):
        ret = list()
        pos = state

        new_row = pos[0] + stepXY
        if new_row < self.game.board.m:
            next_pos = (new_row, pos[1])
            if next_pos not in visited:
                if not self.game.isBlockedByWall('p', pos, next_pos):
                    ret.append(next_pos)
        
        new_row = pos[0] - stepXY
        if new_row >= 0:
            next_pos = (new_row, pos[1])
            if next_pos not in visited:
                if not self.game.isBlockedByWall('p', pos, next_pos):
                    ret.append(next_pos)


        new_col = pos[1] + stepXY
        if new_col < self.game.board.n:
            next_pos = (pos[0], new_col)
            if next_pos not in visited:
                if not self.game.isBlockedByWall('z', pos, next_pos):
                    ret.append(next_pos)
        
        new_col = pos[1] - stepXY
        if new_col >= 0:
            next_pos = (pos[0], new_col)
            if next_pos not in visited:
                if not self.game.isBlockedByWall('z', pos, next_pos):
                    ret.append(next_pos)
        
        ret.extend(self.generate_figure_diagonal_lines(state, visited))
        return ret



    def generate_figure_diagonal_lines(self, state, visited):
        ret = list()
        pos = state

        new_row = pos[0] - 1
        new_col = pos[1] - 1

        if new_row >= 0 and new_col >= 0:
            next_pos = (new_row, new_col)
            if next_pos not in visited:
                if self.game.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.game.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)
            

        new_row = pos[0] - 1
        new_col = pos[1] + 1
        
        if new_row >= 0 and new_col < self.game.board.n:
            next_pos = (new_row, new_col)
            if next_pos not in visited:
                if self.game.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.game.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)

        new_row = pos[0] + 1
        new_col = pos[1] - 1

        if new_row < self.game.board.m and new_col >= 0:
            next_pos = (new_row, new_col)
            if next_pos not in visited:
                if self.game.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.game.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)
        

        new_row = pos[0] + 1
        new_col = pos[1] + 1

        if new_row < self.game.board.m and new_col < self.game.board.n:
            next_pos = (new_row, new_col)
            if next_pos not in visited:
                if self.game.isBlockedByWall("p", pos, (next_pos[0], pos[1])):
                    if not (self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos) or self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1]))):
                        ret.append(next_pos)
                elif self.game.isBlockedByWall("z", (next_pos[0], pos[1]), next_pos):
                    if not (self.game.isBlockedByWall("z", pos, (pos[0], next_pos[1])) or self.game.isBlockedByWall("p", (pos[0], next_pos[1]), next_pos)):
                        ret.append(next_pos)
                else:
                    ret.append(next_pos)

        return ret



    def h_dist(self, state, dest):
        if state[0] - dest[0] == state[1] - dest[1]:
            return abs(state[0] - dest[0])
        return abs(state[0] - dest[0]) + abs(state[1] - dest[1])



     #proveravamo da li zid blokira put do oba odredisna polja
    def check_for_paths(self) -> bool:
        #trazenje puteva
        return self.check_all_paths(tuple(self.game.board.player1.positions[0]), tuple(self.game.board.player1.positions[1]), tuple(self.game.board.startPositionsO[0]), tuple(self.game.board.startPositionsO[1]), self.dist_yellow1, self.dist_yellow2) and \
        self.check_all_paths(tuple(self.game.board.player2.positions[0]), tuple(self.game.board.player2.positions[1]), tuple(self.game.board.startPositionsX[0]), tuple(self.game.board.startPositionsX[1]), self.dist_red1, self.dist_red2)

    
    #trazenje best-first
    def check_for_path(self, start_node, end_node, h_dists, paths) -> bool:

        found = False
        last_node = None
        prev_nodes = dict()
        visited_nodes = set()
        nodes_to_visit = []

        prev_nodes[start_node] = None
        heapq.heappush(nodes_to_visit, (h_dists[start_node], start_node))

        while(len(nodes_to_visit) > 0 and not found):
            state = heapq.heappop(nodes_to_visit)[1]

            if state == end_node or state in paths:
                last_node = state
                found = True
                break

            stepXY = 1 if h_dists[state] == 1 else 2
            for new_state in self.generate_figure_lines(stepXY, state, visited_nodes):
                if (h_dists[new_state], new_state) not in nodes_to_visit:
                    heapq.heappush(nodes_to_visit, (h_dists[new_state], new_state))
                    prev_nodes[new_state] = state
            
            #nodes_to_visit.remove(state)
            visited_nodes.add(state)
        
        if found:
            paths.add(last_node)
            state = last_node
            while(prev_nodes[state] is not None):
                state = prev_nodes[state]
                paths.add(state)
            paths.add(start_node)
            return (True, paths)
        
        return (False, set())



    def check_all_paths(self, p_pos1, p_pos2, s_dest1, s_dest2, h_dists1, h_dists2) -> bool:
        paths = set()

        res = self.check_for_path(s_dest1, s_dest2, h_dists2, paths)
        if not res[0]:
            return False

        res = None
        if h_dists1[p_pos1] <= h_dists2[p_pos1]:
            res = self.check_for_path(p_pos1, s_dest1, h_dists1, paths)
        else:
            res = self.check_for_path(p_pos1, s_dest2, h_dists2, paths)

        if not res[0]:
            return False
        
        res = None
        if h_dists1[p_pos2] <= h_dists2[p_pos2]:
            res = self.check_for_path(p_pos2, s_dest1, h_dists1, paths)
        else:
            res = self.check_for_path(p_pos2, s_dest2, h_dists2, paths)

        if res[0] and len(self.prev_paths) < 2:
            self.prev_paths.append(paths)
        return res[0]
    



    def generateState(self, playerNumber, wallPosition, wallType, playerPosition):
        newGame = copy.deepcopy(self.game)
        newGame.changeBoardState(
            playerNumber, playerPosition, wallPosition, wallType, newGame.playerToMove)
        newGame.isPlayerOneNext = not self.game.isPlayerOneNext
        newGame.playerToMove = "x" if newGame.playerToMove == "o" else "o"
        
        # provera da li zatvara
        if not self.game.checkNewWall(wallPosition, wallType):
            return newGame
        #if not self.wall_on_path(wallPosition, wallType):
            #return newGame

        oldGame = self.set_game(newGame)
        if self.check_for_paths():
            self.set_game(oldGame)
            return newGame
        self.set_game(oldGame)
        return None



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
            next_states = list(filter(lambda state: state != None, map(lambda params: self.generateState(
                params[0][0], [params[1][0], params[1][1]], params[1][2], params[0][1]), next_states)))
        else:
            next_states = list(filter(lambda state: state != None, map(
                lambda params: self.generateState(params[0], [], '', params[1]), player_moves)))
        # lista Game-ova sa novom pozicijom i dodatim zidom

        return next_states




    #proverava da li nam novi zid utice na nadjeni put. ukoliko ne utice, nema potrebe da ponovo proveravamo da li put postoji
    def wall_on_path(self, wallPos, wallType) -> bool:
        if wallType == 'p':
            for i in range(0, 2):
                if (wallPos[0] - 1, wallPos[1]) in self.prev_paths[i] and (wallPos[0] + 1, wallPos[1]) in self.prev_paths[i]:
                    return True
                if (wallPos[0], wallPos[1]) in self.prev_paths[i] and ((wallPos[0] + 2, wallPos[1]) in self.prev_paths[i] or (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i] or ((wallPos[0] + 1, wallPos[1] - 1) in self.prev_paths[i] and (wallPos[0] - 1, wallPos[1] - 1, 'z') in self.game.board.walls)):
                    return True
                if (wallPos[0] - 1, wallPos[1] + 1) in self.prev_paths[i] and (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i]:
                    return True
                if (wallPos[0], wallPos[1] + 1) in self.prev_paths[i] and ((wallPos[0] + 2, wallPos[1] + 1) in self.prev_paths[i] or (wallPos[0] + 1, wallPos[1]) in self.prev_paths[i] or ((wallPos[0] + 1, wallPos[1] + 2) in self.prev_paths[i] and  (wallPos[0] - 1, wallPos[1] + 1, 'z') in self.game.board.walls)):
                    return True
        else:
            for i in range(0, 2):
                if (wallPos[0], wallPos[1] - 1) in self.prev_paths[i] and (wallPos[0], wallPos[1] + 1) in self.prev_paths[i]:
                    return True
                if (wallPos[0], wallPos[1]) in self.prev_paths[i] and ((wallPos[0], wallPos[1] + 2) in self.prev_paths[i] or (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i]):
                    return True
                if (wallPos[0] + 1, wallPos[1] - 1) in self.prev_paths[i] and (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i]:
                    return True
                if (wallPos[0] + 1, wallPos[1]) in self.prev_paths[i] and ((wallPos[0] + 1, wallPos[1] + 2) in self.prev_paths[i] or (wallPos[0], wallPos[1] + 1) in self.prev_paths[i]):
                    return True
        return False





    def minmax(self, state, depth, alpha, beta, max_move):
        if depth == 0 or self.game.isEnd():
            return (state, self.evaluate(state))
        
        best_move = None
        #potez igraca koji maksimizuje efikasnost
        if max_move:
            max_val = float("-inf")
            for next_state in self.generateNextGameStates(state):
                next_val = self.minmax(next_state, depth - 1, alpha, beta, False)[1]
                if max_val < next_val:
                    max_val = next_val
                    best_move = next_state
                alpha = max(alpha, next_val)
                if beta <= alpha:
                    break
            return (best_move, max_val)

        else:
            min_val = float("+inf")
            for next_state in self.generateNextGameStates(state):
                next_val = self.minmax(next_state, depth - 1, alpha, beta, True)[1]
                if min_val > next_val:
                   min_val = next_val
                   best_move = next_state
                beta = min(beta, next_val)
                if beta <= alpha:
                    break
            return (best_move, min_val)

    


    def evaluate(self, state):
        if self.game.playerToMove == 'o':
            dist_f1 =  self.dist_red1[tuple(state.board.player2.positions[0])]
            dist_f2 = self.dist_red2[tuple(state.board.player2.positions[1])]
            dist_f3 = self.dist_red1[tuple(state.board.player2.positions[1])]
            dist_f4 = self.dist_red2[tuple(state.board.player2.positions[0])]
            return  100 - (dist_f1 + dist_f2 + dist_f3 + dist_f4)
        
        else:
            dist_f1 =  self.dist_yellow1[tuple(state.board.player1.positions[0])]
            dist_f2 = self.dist_yellow2[tuple(state.board.player1.positions[1])]
            dist_f3 = self.dist_yellow1[tuple(state.board.player1.positions[1])]
            dist_f4 = self.dist_yellow2[tuple(state.board.player1.positions[0])]
            return  100 - (dist_f1 + dist_f2 + dist_f3 + dist_f4)

        