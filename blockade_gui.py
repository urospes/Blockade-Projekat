import pygame
import consts as const
from sys import exit
import blockade_ms as bl

pygame.init()

game = bl.Game()
game.getStartState()
const.SQUARE = 40 if game.board.m < 13 else 30 if game.board.m < 18 else 24
const.WALL_W = 10 if game.board.m < 13 else 7
const.WALL_H = 2 * const.SQUARE + const.WALL_W

screen = pygame.display.set_mode((const.WIN_WIDTH, const.WIN_HEIGHT))
screen.fill(const.WIN_COLOR)
pygame.display.set_caption(const.TITLE)
clock = pygame.time.Clock()


# funkcija za iscrtavanje header-a igre
def DrawHeader(p1_walls: tuple[int, int], p2_walls: tuple[int, int], redFirst: bool):

    text_font = pygame.font.Font(None, const.FONT_SIZE)

    text_surface_p1 = text_font.render("CRVENI IGRAC", False, "RED")
    text_rect_p1 = text_surface_p1.get_rect(
        topleft=(const.TEXT_OFFSET, const.TEXT_OFFSET))

    text_surface_p2 = text_font.render("ZUTI IGRAC", False, "YELLOW")
    text_rect_p2 = text_surface_p2.get_rect(
        topright=(const.WIN_WIDTH - const.TEXT_OFFSET, const.TEXT_OFFSET))

    next_player_text = "Na potezu je : "
    next_player_text += "Crveni" if redFirst else "Zuti"

    text_surface_next_move = text_font.render(next_player_text, True, "Gray")
    text_rect_next_move = text_surface_next_move.get_rect(
        center=(const.WIN_WIDTH // 2, const.TEXT_OFFSET + const.FONT_SIZE // 2))

    screen.fill("BLACK")
    screen.blit(text_surface_p1, text_rect_p1)
    screen.blit(text_surface_p2, text_rect_p2)
    screen.blit(text_surface_next_move, text_rect_next_move)

    # iscrtavamo broj dostupnih zidova za svakog igraca

    # prvi igrac plavi zidovi
    num_blue_surface = text_font.render("x " + str(p1_walls[0]), False, "Gray")
    num_blue_rect = num_blue_surface.get_rect(
        bottomleft=(text_rect_p1.right + 40, text_rect_p1.bottom))
    pygame.draw.rect(screen, "GREEN", pygame.rect.Rect(
        text_rect_p1.right + 20, text_rect_p1.top, 15, 40))
    screen.blit(num_blue_surface, num_blue_rect)

    # prvi igrac zeleni zidovi
    num_green_surface = text_font.render(
        "x " + str(p1_walls[1]), False, "Gray")
    num_green_rect = num_blue_surface.get_rect(
        topleft=(num_blue_rect.right + 70, text_rect_p1.top))
    pygame.draw.rect(screen, "CYAN", pygame.rect.Rect(
        num_blue_rect.right + 20, text_rect_p1.top + 5, 40, 15))
    screen.blit(num_green_surface, num_green_rect)

    # drugi igrac plavi zidovi
    num_blue_surface = text_font.render("x " + str(p2_walls[0]), False, "Gray")
    num_blue_rect = num_blue_surface.get_rect(
        bottomright=(text_rect_p2.left - 20, text_rect_p1.bottom))
    pygame.draw.rect(screen, "GREEN", pygame.rect.Rect(
        num_blue_rect.left - 20, text_rect_p1.top, 15, 40))
    screen.blit(num_blue_surface, num_blue_rect)

    # drugi igrac zeleni zidovi
    num_green_surface = text_font.render(
        "x " + str(p2_walls[1]), False, "Gray")
    num_green_rect = num_blue_surface.get_rect(
        topright=(num_blue_rect.left - 50, text_rect_p1.top))
    pygame.draw.rect(screen, "CYAN", pygame.rect.Rect(
        num_green_rect.left - 50, text_rect_p1.top + 5, 40, 15))
    screen.blit(num_green_surface, num_green_rect)


# funckija za crtanje oznaka kolona i vrsta
def DrawLabels(game_rect: pygame.Rect, size: tuple[int, int], offset: int):

    # sve vezano za tablu crtamo u okviru game_rect pravougaonika
    labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E",
              "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]

    # crtamo oznake za vrste i kolone
    label_font = pygame.font.Font(None, const.LABEL_FONT_SIZE)

    # oznake vrsta
    for i in range(0, size[0]):
        label_surface = label_font.render(str(labels[i]), False, "WHITE")
        label_rect = pygame.rect.Rect(game_rect.left + const.WALL_W + offset, game_rect.top + (
            i + 1) * (const.SQUARE + const.WALL_W), const.SQUARE, const.SQUARE)
        screen.blit(label_surface, label_rect)

    # oznake kolona
    for i in range(0, size[1]):
        label_surface = label_font.render(str(labels[i]), False, "WHITE")
        label_rect = pygame.rect.Rect(game_rect.left + (i + 1) * (const.WALL_W + const.SQUARE) +
                                      offset, game_rect.top + const.WALL_W, const.SQUARE, const.SQUARE)
        screen.blit(label_surface, label_rect)


# funkcija koja crta zidove na tabli
def DrawWalls(board_rect: pygame.Rect, walls: bl.Wall):

    for wall in walls:
        wall_rect = None
        color = None
        if wall[2] == "p":
            left = board_rect.left + \
                wall[1] * (const.SQUARE + const.WALL_W)
            top = board_rect.top + \
                (wall[0] + 1) * \
                (const.SQUARE + const.WALL_W) - const.WALL_W
            wall_rect = pygame.rect.Rect(left, top, const.WALL_H, const.WALL_W)
            color = "CYAN"
        else:
            left = board_rect.left + \
                (wall[1] + 1) * \
                (const.SQUARE + const.WALL_W) - const.WALL_W
            top = board_rect.top + \
                wall[0] * (const.SQUARE + const.WALL_W)
            wall_rect = pygame.rect.Rect(left, top, const.WALL_W, const.WALL_H)
            color = "GREEN"

        if(wall_rect and color):
            pygame.draw.rect(screen, color, wall_rect)


# funckija za iscrtavanje trenutnog stanja na tabli
def DrawGameBoard(size: tuple[int, int], player_1: tuple[tuple[int, int]], player_2: tuple[tuple[int, int]], walls: list[tuple[int, int]], start_positions):

    game_rect = pygame.rect.Rect(
        const.GAME_BOARD_X, const.GAME_BOARD_Y, const.GAME_BOARD_W, const.GAME_BOARD_H)
    pygame.draw.rect(screen, const.GAME_RECT_COLOR, game_rect, 3)

    board_w = size[1] * const.SQUARE + (size[1] - 1) * const.WALL_W
    board_h = size[0] * const.SQUARE + (size[0] - 1) * const.WALL_W
    offset = (game_rect.width - board_w) // 2
    DrawLabels(game_rect, size, offset)

    board_rect = pygame.rect.Rect(game_rect.left + const.WALL_W + const.SQUARE + (
        game_rect.width - board_w) // 2, game_rect.top + const.WALL_W + const.SQUARE, board_w, board_h)

    # crtamo polja u odnosu na pravougaonik board_rect
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            square = pygame.rect.Rect(board_rect.left + j * (const.SQUARE + const.WALL_W),
                                      board_rect.top + i * (const.SQUARE + const.WALL_W), const.SQUARE, const.SQUARE)
            if [i, j] in start_positions[0]:
                pygame.draw.rect(screen, const.START_RED_COLOR, square)
            elif [i, j] in start_positions[1]:
                pygame.draw.rect(screen, const.START_YELLOW_COLOR, square)
            else:
                pygame.draw.rect(screen, const.SQUARE_COLOR, square)

    # crtamo igrace na odgovarajucim pozicijama
    p_1_fig_1 = player_1[0]
    c_x = board_rect.left + \
        int(p_1_fig_1[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + \
        int(p_1_fig_1[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p1_f1_rect = pygame.draw.circle(
        screen, const.RED_PLAYER, (c_x, c_y), const.SQUARE // 3)

    p_1_fig_2 = player_1[1]
    c_x = board_rect.left + \
        int(p_1_fig_2[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + \
        int(p_1_fig_2[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p1_f2_rect = pygame.draw.circle(
        screen, const.RED_PLAYER, (c_x, c_y), const.SQUARE // 3)

    p_2_fig_1 = player_2[0]
    c_x = board_rect.left + \
        int(p_2_fig_1[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + \
        int(p_2_fig_1[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p2_f1_rect = pygame.draw.circle(
        screen, const.YELLOW_PLAYER, (c_x, c_y), const.SQUARE // 3)

    p_2_fig_2 = player_2[1]
    c_x = board_rect.left + \
        int(p_2_fig_2[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + \
        int(p_2_fig_2[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p2_f2_rect = pygame.draw.circle(
        screen, const.YELLOW_PLAYER, (c_x, c_y), const.SQUARE // 3)

    DrawWalls(board_rect, walls)

    return {"player_boxes": ([p1_f1_rect, p1_f2_rect], [p2_f1_rect, p2_f2_rect]), "board_rect": (board_rect.x, board_rect.y)}


def DrawPossibleMoves(valid_moves, chosen_move, board):
    for move in valid_moves:
        square = pygame.rect.Rect(board[0] + move[1] * (const.SQUARE + const.WALL_W), board[1] + move[0] * (const.SQUARE + const.WALL_W),
                                  const.SQUARE, const.SQUARE)
        pygame.draw.rect(screen, const.DEST_COLOR, square)

    if chosen_move[0] != -1 and chosen_move[1] != -1:
        dest_square = pygame.rect.Rect(board[0] + chosen_move[1] * (const.SQUARE + const.WALL_W), board[1] + chosen_move[0] * (const.SQUARE + const.WALL_W),
                                       const.SQUARE, const.SQUARE)
        pygame.draw.rect(screen, const.DEST_COLOR, dest_square)


class MoveState:
    def __init__(self, game: bl.Game, board_info):
        self.game = game
        self.red_to_move = True if game.playerToMove == 'x' else False
        self.figure_num = -1
        self.valid_moves = []
        self.new_figure_pos = [-1, -1]
        self.wall_pos = [-1, -1, '']
        self.board_info = board_info

    def switch_players(self):
        self.red_to_move = not self.red_to_move
        self.figure_num = -1
        self.new_figure_pos[0] = self.new_figure_pos[1] = -1
        if self.game.board.player1.greenWallNumber == 0 and self.game.board.player1.blueWallNumber == 0 and self.game.board.player2.greenWallNumber == 0 and self.game.board.player2.blueWallNumber == 0:
            self.wall_pos = ()
        else:
            self.wall_pos = [-1, -1, '']

    def choose_figure(self, click: tuple[int, int]):
        player_boxes = self.board_info["player_boxes"]
        if self.red_to_move:
            if player_boxes[0][0].collidepoint(click):
                self.figure_num = 0
            elif player_boxes[0][1].collidepoint(click):
                self.figure_num = 1
        else:
            if player_boxes[1][0].collidepoint(click):
                self.figure_num = 0
            elif player_boxes[1][1].collidepoint(click):
                self.figure_num = 1

        if self.figure_num != -1:
            self.new_figure_pos = [-1, -1]
            self.wall_pos = [-1, -1, ''] if len(self.wall_pos) > 0 else ()
            self.valid_moves = self.game.generate_player_moves(self.figure_num)

    def choose_figure_position(self, click_pos: tuple[int, int]):
        if self.new_figure_pos[0] != -1 and self.new_figure_pos[1] != -1:
            return

        click_pos = list(click_pos)
        board_rect = self.board_info["board_rect"]
        click_pos[0] -= board_rect[0]
        click_pos[1] -= board_rect[1]

        for i in range(0, game.board.n):
            if ((const.WALL_W + const.SQUARE) * i < click_pos[0]) and ((const.WALL_W + const.SQUARE) * i + const.SQUARE > click_pos[0]):
                self.new_figure_pos[1] = i
                break

        for i in range(0, game.board.m):
            if ((const.WALL_W + const.SQUARE) * i < click_pos[1]) and ((const.WALL_W + const.SQUARE) * i + const.SQUARE > click_pos[1]):
                self.new_figure_pos[0] = i
                break

        if self.new_figure_pos[0] != -1 and self.new_figure_pos[1] != -1:
            if (self.new_figure_pos[0], self.new_figure_pos[1]) not in self.valid_moves:
                self.new_figure_pos[0] = self.new_figure_pos[1] = -1
            else:
                self.valid_moves = []
        else:
            self.new_figure_pos[0] = -1
            self.new_figure_pos[1] = -1

    def choose_wall_position(self, click_pos: tuple[int, int]):
        click_pos = list(click_pos)
        board_rect = board_info["board_rect"]

        click_pos[0] -= board_rect[0]
        click_pos[1] -= board_rect[1]
        wallPos = [-1, -1]

        # proveravamo da li je izabran vertikalni zid
        for i in range(0, game.board.n):
            if (click_pos[0] > const.SQUARE + i * (const.SQUARE + const.WALL_W)) and (click_pos[0] < (i + 1) * (const.SQUARE + const.WALL_W)):
                wallPos[1] = i

                for i in range(0, game.board.m):
                    if (click_pos[1] > i * (const.SQUARE + const.WALL_W)) and (click_pos[1] < const.SQUARE + i * (const.SQUARE + const.WALL_W)):
                        wallPos[0] = i
                        break

                break

        if wallPos[0] != -1 and wallPos[1] != -1:
            self.wall_pos = (wallPos[0], wallPos[1], 'z')
            return

        # ako nije postavljen vertikalni zid, trazimo horizontalni zid
        wallPos = [-1, -1]
        for i in range(0, game.board.m):
            if (click_pos[1] > const.SQUARE + i * (const.SQUARE + const.WALL_W)) and (click_pos[1] < (i + 1) * (const.SQUARE + const.WALL_W)):
                wallPos[0] = i

                for i in range(0, game.board.n):
                    if (click_pos[0] > i * (const.SQUARE + const.WALL_W)) and (click_pos[0] < const.SQUARE + i * (const.SQUARE + const.WALL_W)):
                        wallPos[1] = i
                        break

                break

        if wallPos[0] != -1 and wallPos[1] != -1:
            self.wall_pos = (wallPos[0], wallPos[1], 'p')
            return


# funckija za obradu klikova
def HandleClickEvent(click_pos: tuple[int, int], move_state: MoveState):

    if move_state.figure_num == -1:
        move_state.choose_figure(click_pos)
    elif move_state.new_figure_pos[0] == -1 and move_state.new_figure_pos[1] == -1:
        move_state.choose_figure_position(click_pos)
    elif len(move_state.wall_pos) > 0 and move_state.wall_pos[0] == -1 and move_state.wall_pos[0] == -1:
        move_state.choose_wall_position(click_pos)

    # ukoliko je sve izabrano, zavrsavamo potez
    if move_state.figure_num != -1 and move_state.new_figure_pos[0] != -1 and move_state.new_figure_pos[1] != -1 and (len(move_state.wall_pos) == 0 or move_state.wall_pos[2] != ''):
        pygame.event.post(pygame.event.Event(MOVE_FINISHED))


# funkcija za prikaz pobednika na kraju igre
def PrintWinner(winner_red: bool):
    screen.fill("BLACK")
    winner_font = pygame.font.Font(None, const.WIN_FONT_SIZE)
    winner_color = "crveni" if winner_red else "zuti"
    winner_text = "Cestitamo, pobedio je " + winner_color + " igrac!"
    winner_text_surface = winner_font.render(
        winner_text, True, const.WIN_TEXT_COLOR)
    winner_text_rect = winner_text_surface.get_rect(
        center=(const.WIN_WIDTH // 2, const.WIN_HEIGHT // 2))
    screen.blit(winner_text_surface, winner_text_rect)


# game loop
game_end = False
# move_state je lista koja pamti stanje poteza (prvi element pamti da li je izabran igrac kog zelimo da pomerimo, drugi element pamti da li je izabrano odredisno polje,
# treci element pokazuje da li je izabran zid). Kada su sva tri elementa True, potez je odigran i prelazimo na drugog igraca
MOVE_FINISHED = pygame.USEREVENT + 1

move_state = MoveState(game, None)
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            HandleClickEvent(event.pos, move_state)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                move_state.game.check_red_paths(0, 0)

        if event.type == MOVE_FINISHED:
            # igranje poteza
            wall_move_pos = (move_state.wall_pos[0], move_state.wall_pos[1]) if len(
                move_state.wall_pos) != 0 else ()
            wall_type = move_state.wall_pos[2] if len(
                move_state.wall_pos) != 0 else ''
            player_type = 'x' if move_state.red_to_move else 'o'
            move_done = game.nextMove(
                move_state.figure_num, wall_move_pos, wall_type, player_type, move_state.new_figure_pos)
            if game.isEnd():
                game_end = True
            else:
                move_state.switch_players()
                if not move_done:
                    # ukoliko je potez nevalidan, moramo da resetujemo potez
                    move_state.red_to_move = not move_state.red_to_move

    if not game_end:
        # draw
        screen.fill("BLACK")
        DrawHeader((game.board.player1.greenWallNumber, game.board.player1.blueWallNumber),
                   (game.board.player2.greenWallNumber, game.board.player2.blueWallNumber), move_state.red_to_move)
        board_info = DrawGameBoard((game.board.m, game.board.n), game.board.player1.positions,
                                   game.board.player2.positions, game.board.walls, (game.board.startPositionsX, game.board.startPositionsO))
        move_state.board_info = board_info
        DrawPossibleMoves(move_state.valid_moves, move_state.new_figure_pos,
                          move_state.board_info["board_rect"])
    else:
        PrintWinner(move_state.red_to_move)

    # update
    pygame.display.update()
    clock.tick(60)
