import copy
from itertools import product
import heapq
from re import L


class BlockadeAI:
    def __init__(self, game):
        self.game = game
        self.dist_red1 = dict()
        self.dist_red2 = dict()
        self.dist_yellow1 = dict()
        self.dist_yellow2 = dict()
        self.prev_paths = [set(), set()]
        self.initialize_dists(self.game)

    def initialize_dists(self, game):
        red_start1 = tuple(game.board.startPositionsX[0])
        red_start2 = tuple(game.board.startPositionsX[1])
        yellow_start1 = tuple(game.board.startPositionsO[0])
        yellow_start2 = tuple(game.board.startPositionsO[1])

        for i in range(0, game.board.m):
            for j in range(0, game.board.n):
                self.dist_red1[(i, j)] = self.h_dist((i, j), red_start1)
                self.dist_red2[(i, j)] = self.h_dist((i, j), red_start2)
                self.dist_yellow1[(i, j)] = self.h_dist((i, j), yellow_start1)
                self.dist_yellow2[(i, j)] = self.h_dist((i, j), yellow_start2)
        self.check_for_paths()

    def set_game(self, game):
        oldGame = self.game
        self.game = game
        return oldGame

    # generisanje mogucih poteza

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

     # proveravamo da li zid blokira put do oba odredisna polja

    def check_for_paths(self) -> bool:
        # trazenje puteva
        return self.check_all_paths(tuple(self.game.board.player1.positions[0]), tuple(self.game.board.player1.positions[1]), tuple(self.game.board.startPositionsO[0]), tuple(self.game.board.startPositionsO[1]), self.dist_yellow1, self.dist_yellow2, True) and \
            self.check_all_paths(tuple(self.game.board.player2.positions[0]), tuple(self.game.board.player2.positions[1]), tuple(
                self.game.board.startPositionsX[0]), tuple(self.game.board.startPositionsX[1]), self.dist_red1, self.dist_red2, False)

    # trazenje best-first

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
                    heapq.heappush(
                        nodes_to_visit, (h_dists[new_state], new_state))
                    prev_nodes[new_state] = state

            # nodes_to_visit.remove(state)
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

    def check_all_paths(self, p_pos1, p_pos2, s_dest1, s_dest2, h_dists1, h_dists2, is_red) -> bool:

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

        if res[0]:
            if(is_red):
                self.prev_paths[0] = paths.copy()
            else:
                self.prev_paths[1] = paths.copy()

        return res[0]

    def generateState(self, game, playerNumber, wallPosition, wallType, playerPosition):
        newGame = copy.deepcopy(game)
        newGame.changeBoardState(
            playerNumber, playerPosition, wallPosition, wallType, newGame.playerToMove)
        newGame.isPlayerOneNext = not game.isPlayerOneNext
        newGame.playerToMove = "x" if newGame.playerToMove == "o" else "o"

        # provera da li zatvara
        """ if len(self.prev_paths[0]) > 0 and len(self.prev_paths[1]) > 0:
            if not self.wall_on_path(wallPosition, wallType):
                #return (newGame, [len(self.prev_paths[0]) - 1, len(self.prev_paths[1]) - 1])
                return newGame
            self.prev_paths[0].clear()
            self.prev_paths[1].clear() """

        if not game.checkNewWall(wallPosition, wallType):
            # return (newGame, [len(self.prev_paths[0]), len(self.prev_paths[1])])
            return newGame

        oldGame = self.set_game(newGame)
        if self.check_for_paths():
            self.set_game(oldGame)
            # return (newGame, [len(self.prev_paths[0]), len(self.prev_paths[1])])
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
            next_states = list(filter(lambda state: state != None, map(lambda params: self.generateState(game,
                                                                                                         params[0][0], [params[1][0], params[1][1]], params[1][2], params[0][1]), next_states)))
        else:
            next_states = list(filter(lambda state: state != None, map(
                lambda params: self.generateState(game, params[0], [], '', params[1]), player_moves)))
        # lista Game-ova sa novom pozicijom i dodatim zidom

        return next_states

    # proverava da li nam novi zid utice na nadjeni put. ukoliko ne utice, nema potrebe da ponovo proveravamo da li put postoji

    def wall_on_path(self, wallPos, wallType) -> bool:
        if wallType == 'p':
            for i in range(0, 2):
                if (wallPos[0] + 1, wallPos[1]) in self.prev_paths[i] and \
                    ((wallPos[0] - 1, wallPos[1]) in self.prev_paths[i] or
                     ((wallPos[0], wallPos[1]-1) in self.prev_paths[i] and
                      ((wallPos[0]+1, wallPos[1]-1, 'z') in self.game.board.walls or (wallPos[0], wallPos[1] - 2, 'p') in self.game.board.walls))):
                    return True
                if (wallPos[0], wallPos[1]) in self.prev_paths[i] and \
                    ((wallPos[0] + 2, wallPos[1]) in self.prev_paths[i] or
                     (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i] or
                     ((wallPos[0] + 1, wallPos[1] - 1) in self.prev_paths[i] and
                     ((wallPos[0] - 1, wallPos[1] - 1, 'z') in self.game.board.walls or (wallPos[0], wallPos[1] - 2, 'p') in self.game.board.walls))):
                    return True
                if (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i] and \
                    ((wallPos[0] - 1, wallPos[1] + 1) in self.prev_paths[i] or
                     ((wallPos[0], wallPos[1]+2) in self.prev_paths[i] and
                      ((wallPos[0]+1, wallPos[1]+1, 'z') in self.game.board.walls or (wallPos[0], wallPos[1] + 2, 'p') in self.game.board.walls))):
                    return True
                if (wallPos[0], wallPos[1] + 1) in self.prev_paths[i] and \
                    ((wallPos[0] + 2, wallPos[1] + 1) in self.prev_paths[i] or
                     (wallPos[0] + 1, wallPos[1]) in self.prev_paths[i] or
                     ((wallPos[0] + 1, wallPos[1] + 2) in self.prev_paths[i] and
                     ((wallPos[0] - 1, wallPos[1] + 1, 'z') in self.game.board.walls or (wallPos[0], wallPos[1] + 2, 'p') in self.game.board.walls))):
                    return True
        else:
            for i in range(0, 2):
                if (wallPos[0], wallPos[1] + 1) in self.prev_paths[i] and \
                    ((wallPos[0], wallPos[1] - 1) in self.prev_paths[i] or
                     ((wallPos[0]-1, wallPos[1]) in self.prev_paths[i] and
                      ((wallPos[0] - 2, wallPos[1], 'z') in self.game.board.walls or (wallPos[0] - 1, wallPos[1]+1, 'p') in self.game.board.walls))):
                    return True
                if (wallPos[0], wallPos[1]) in self.prev_paths[i] and \
                    ((wallPos[0], wallPos[1] + 2) in self.prev_paths[i] or
                     (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i] or
                     ((wallPos[0] - 1, wallPos[1] + 1) in self.prev_paths[i] and
                     ((wallPos[0] - 1, wallPos[1] - 1, 'p') in self.game.board.walls or (wallPos[0]-2, wallPos[1], 'z') in self.game.board.walls))):
                    return True
                if (wallPos[0] + 1, wallPos[1] + 1) in self.prev_paths[i] and \
                    ((wallPos[0] + 1, wallPos[1] - 1) in self.prev_paths[i] or
                     ((wallPos[0] + 2, wallPos[1]) in self.prev_paths[i] and
                     ((wallPos[0] + 1, wallPos[1] + 1, 'p') in self.game.board.walls or (wallPos[0] + 2, wallPos[1], 'z') in self.game.board.walls))):
                    return True
                if (wallPos[0] + 1, wallPos[1]) in self.prev_paths[i] and \
                    ((wallPos[0] + 1, wallPos[1] + 2) in self.prev_paths[i] or
                     (wallPos[0], wallPos[1] + 1) in self.prev_paths[i] or
                     ((wallPos[0] + 2, wallPos[1] + 1) in self.prev_paths[i] and
                     ((wallPos[0] + 1, wallPos[1] - 1, 'p') in self.game.board.walls or (wallPos[0]+2, wallPos[1], 'z') in self.game.board.walls))):
                    return True
        return False

    def minmax(self, state, depth, alpha, beta, max_move, prev_state):

        if depth == 0 or self.game.isEnd():
            return (state, self.evaluate(state, prev_state[state]))

        best_move = None
        # potez igraca koji maksimizuje efikasnost
        if max_move:
            max_val = float("-inf")
            for next_state in self.generateNextGameStates(state):
                prev_state[next_state] = state
                next_val = self.minmax(
                    next_state, depth - 1, alpha, beta, False, prev_state)[1]
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
                prev_state[next_state] = state
                next_val = self.minmax(
                    next_state, depth - 1, alpha, beta, True, prev_state)[1]
                if min_val > next_val:
                    min_val = next_val
                    best_move = next_state
                beta = min(beta, next_val)
                if beta <= alpha:
                    break
            return (best_move, min_val)

    def evaluate(self, state, prev_state):
        end_node = None
        h_dists = None
        new_wall = state.board.walls.difference(prev_state.board.walls)

        p1 = tuple(state.board.player1.positions[0])
        p2 = tuple(state.board.player1.positions[1])

        if self.dist_yellow1[p1] < self.dist_yellow2[p1]:
            end_node = tuple(state.board.startPositionsO[0])
            h_dists = self.dist_yellow1
        else:
            end_node = tuple(state.board.startPositionsO[1])
            h_dists = self.dist_yellow2

        path1 = self.find_shortest(p1, end_node, h_dists)

        if self.dist_yellow1[p2] < self.dist_yellow2[p2]:
            end_node = tuple(state.board.startPositionsO[0])
            h_dists = self.dist_yellow1
        else:
            end_node = tuple(state.board.startPositionsO[1])
            h_dists = self.dist_yellow2

        path2 = self.find_shortest(p2, end_node, h_dists)

        xBestLen = None
        xBestPath = None
        if path1[1] < path2[1]:
            xBestLen = path1[1]
            xBestPath = path1[0]
        else:
            xBestLen = path2[1]
            xBestPath = path2[0]

        p1 = tuple(state.board.player2.positions[0])
        p2 = tuple(state.board.player2.positions[1])

        if self.dist_red1[p1] < self.dist_red2[p1]:
            end_node = tuple(state.board.startPositionsX[0])
            h_dists = self.dist_red1
        else:
            end_node = tuple(state.board.startPositionsX[1])
            h_dists = self.dist_red2

        path1 = self.find_shortest(p1, end_node, h_dists)

        if self.dist_red1[p2] < self.dist_red2[p2]:
            end_node = tuple(state.board.startPositionsX[0])
            h_dists = self.dist_red1
        else:
            end_node = tuple(state.board.startPositionsX[1])
            h_dists = self.dist_red2

        path2 = self.find_shortest(p2, end_node, h_dists)

        oBestPath = None
        oBestLen = None
        if path1[1] < path2[1]:
            oBestLen = path1[1]
            oBestPath = path1[0]
        else:
            oBestLen = path2[1]
            oBestPath = path2[0]

        """ if state.playerToMove == 'x':
            return 10 / oBestLen + xBestLen """
        return 20 / oBestLen + xBestLen

    def find_shortest(self, start_node, end_node, h_dists) -> bool:

        found = False
        last_node = None
        prev_nodes = dict()
        visited_nodes = set()
        nodes_to_visit = set()
        g = dict()
        g[start_node] = 0
        path = []

        prev_nodes[start_node] = None
        nodes_to_visit.add(start_node)

        while(not found and len(nodes_to_visit) > 0):
            state = None
            for next_state in nodes_to_visit:
                if state is None or g[next_state] + h_dists[next_state] < g[state] + h_dists[state]:
                    state = next_state

            if state == end_node:
                last_node = state
                found = True
                break

            stepXY = 1 if h_dists[state] == 1 else 2
            for new_state in self.generate_figure_lines(stepXY, state, visited_nodes):
                if new_state not in nodes_to_visit:
                    g[new_state] = g[state] + stepXY
                    prev_nodes[new_state] = state
                    nodes_to_visit.add(new_state)

                else:
                    if g[new_state] > g[state] + stepXY:
                        g[new_state] = g[state] + stepXY
                        prev_nodes[new_state] = state

            nodes_to_visit.remove(state)
            visited_nodes.add(state)

        if found:
            count = 1
            state = last_node
            path.append(state)
            while(prev_nodes[state] is not None):
                state = prev_nodes[state]
                count = count + 1
                path.append(state)
            return (path, count)

        return ([], -1)
