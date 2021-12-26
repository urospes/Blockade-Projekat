from math import sqrt

class BlockadeAI:
    def __init__(self, game):
        self.game = game
        """  self.dist_red1 = dict()
        self.dist_red2 = dict()
        self.dist_yellow1 = dict()
        self.dist_yellow2 = dict()
        self.initialize_dists(self.game) """



    """ def initialize_dists(self, game):
        red_start1 = game.board.startPositionsX[0]
        red_start2 = game.board.startPositionsX[1]
        yellow_start1 = game.board.startPositionsO[0]
        yellow_start2 = game.board.startPositionsO[1]

        for i in range (0, game.board.m):
            for j in range(0, game.board.n):
                self.dist_red1[(i, j)] = self.h_dist((i, j), red_start1)
                self.dist_red2[(i, j)] = self.h_dist((i, j), red_start2)
                self.dist_yellow1[(i, j)] = self.h_dist((i, j), yellow_start1)
                self.dist_yellow2[(i, j)] = self.h_dist((i, j), yellow_start2) """



    #generisanje mogucih poteza
    def generate_figure_lines(self, stepXY, state, visited, to_visit):
        ret = list()
        pos = state

        new_row = pos[0] + stepXY
        if new_row < self.game.board.m:
            next_pos = (new_row, pos[1])
            if next_pos not in visited and next_pos not in to_visit:
                if not self.game.isBlockedByWall('p', pos, next_pos):
                    ret.append(next_pos)
        
        new_row = pos[0] - stepXY
        if new_row >= 0:
            next_pos = (new_row, pos[1])
            if next_pos not in visited and next_pos not in to_visit:
                if not self.game.isBlockedByWall('p', pos, next_pos):
                    ret.append(next_pos)


        new_col = pos[1] + stepXY
        if new_col < self.game.board.n:
            next_pos = (pos[0], new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if not self.game.isBlockedByWall('z', pos, next_pos):
                    ret.append(next_pos)
        
        new_col = pos[1] - stepXY
        if new_col >= 0:
            next_pos = (pos[0], new_col)
            if next_pos not in visited and next_pos not in to_visit:
                if not self.game.isBlockedByWall('z', pos, next_pos):
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
            if next_pos not in visited and next_pos not in to_visit:
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
            if next_pos not in visited and next_pos not in to_visit:
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
            if next_pos not in visited and next_pos not in to_visit:
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
            #return abs(state[0] - dest[0]) + abs(state[1] - dest[1])
        return sqrt((state[0] - dest[0]) ** 2 + (state[1] - dest[1]) ** 2)



     #proveravamo da li zid blokira put do oba odredisna polja
    def check_for_paths(self) -> bool:
        #ovde idu provere za 2 i 3 i 4 zida, za 5 krecemo trazenje od svake figurice do oba ciljna polja

        if len(self.game.board.walls) == 1:
            return True
        #if len(self.game.board.walls) == 2:
            #return
            

        #trazenje puteva
        return self.check_all_paths(tuple(self.game.board.player1.positions[0]), tuple(self.game.board.player1.positions[1]), tuple(self.game.board.startPositionsO[0]), tuple(self.game.board.startPositionsO[1])) and \
        self.check_all_paths(tuple(self.game.board.player2.positions[0]), tuple(self.game.board.player2.positions[1]), tuple(self.game.board.startPositionsX[0]), tuple(self.game.board.startPositionsX[1]))

    
    #trazenje best-first
    def check_for_path(self, start_node, end_node, paths) -> tuple[bool, set]:

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

        return (True, paths)



    def check_all_paths(self, p_pos1, p_pos2, s_dest1, s_dest2) -> bool:
        paths = set()

        res = self.check_for_path(s_dest1, s_dest2, paths)
        if not res[0]:
            return False

        res = None
        if self.h_dist(p_pos1, s_dest1) <= self.h_dist(p_pos1, s_dest2):
            res = self.check_for_path(p_pos1, s_dest1, paths)
        else:
            res = self.check_for_path(p_pos1, s_dest2, paths)

        if not res[0]:
            return False
        
        res = None
        if self.h_dist(p_pos2, s_dest1) <= self.h_dist(p_pos2, s_dest2):
            res = self.check_for_path(p_pos2, s_dest1, paths)
        else:
            res = self.check_for_path(p_pos2, s_dest2, paths)

        return res[0]
