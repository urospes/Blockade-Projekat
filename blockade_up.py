import pygame
import consts as const
from sys import exit
import blockade_up_classes as bl

pygame.init()

game = bl.Game()
game.getStartState()

screen = pygame.display.set_mode((const.WIN_WIDTH, const.WIN_HEIGHT))
screen.fill(const.WIN_COLOR)
pygame.display.set_caption(const.TITLE)
clock = pygame.time.Clock()




#funkcija za iscrtavanje header-a igre
def DrawHeader(p1_walls: tuple[int, int], p2_walls: tuple[int, int], redFirst: bool):

    text_font = pygame.font.Font(None, const.FONT_SIZE)

    text_surface_p1 = text_font.render("CRVENI IGRAC", False, "RED")
    text_rect_p1 = text_surface_p1.get_rect(topleft = (const.TEXT_OFFSET, const.TEXT_OFFSET))

    text_surface_p2 = text_font.render("ZUTI IGRAC", False, "YELLOW")
    text_rect_p2 = text_surface_p2.get_rect(topright = (const.WIN_WIDTH - const.TEXT_OFFSET, const.TEXT_OFFSET))

    next_player_text = "Na potezu je : "
    next_player_text += "Crveni" if redFirst else "Zuti"

    text_surface_next_move = text_font.render(next_player_text, True, "Gray")
    text_rect_next_move = text_surface_next_move.get_rect(center = (const.WIN_WIDTH // 2, const.TEXT_OFFSET + const.FONT_SIZE // 2))


    screen.blit(text_surface_p1, text_rect_p1)
    screen.blit(text_surface_p2, text_rect_p2)
    screen.blit(text_surface_next_move, text_rect_next_move)

    #iscrtavamo broj dostupnih zidova za svakog igraca

    #prvi igrac plavi zidovi
    num_blue_surface = text_font.render("x " + str(p1_walls[0]), False, "Gray")
    num_blue_rect = num_blue_surface.get_rect(bottomleft = (text_rect_p1.right + 40, text_rect_p1.bottom))
    pygame.draw.rect(screen, "GREEN", pygame.rect.Rect(text_rect_p1.right + 20, text_rect_p1.top, 15, 40))
    screen.blit(num_blue_surface, num_blue_rect)

    #prvi igrac zeleni zidovi
    num_green_surface = text_font.render("x " + str(p1_walls[1]), False, "Gray")
    num_green_rect = num_blue_surface.get_rect(topleft = (num_blue_rect.right + 70, text_rect_p1.top))
    pygame.draw.rect(screen, "CYAN", pygame.rect.Rect(num_blue_rect.right + 20, text_rect_p1.top + 5, 40, 15))
    screen.blit(num_green_surface, num_green_rect)

    #drugi igrac plavi zidovi
    num_blue_surface = text_font.render("x " + str(p2_walls[0]), False, "Gray")
    num_blue_rect = num_blue_surface.get_rect(bottomright = (text_rect_p2.left - 20, text_rect_p1.bottom))
    pygame.draw.rect(screen, "GREEN", pygame.rect.Rect(num_blue_rect.left - 20, text_rect_p1.top, 15, 40))
    screen.blit(num_blue_surface, num_blue_rect)

    #drugi igrac zeleni zidovi
    num_green_surface = text_font.render("x " + str(p2_walls[1]), False, "Gray")
    num_green_rect = num_blue_surface.get_rect(topright = (num_blue_rect.left - 50, text_rect_p1.top))
    pygame.draw.rect(screen, "CYAN", pygame.rect.Rect(num_green_rect.left - 50, text_rect_p1.top + 5, 40, 15))
    screen.blit(num_green_surface, num_green_rect)



#funckija za crtanje oznaka kolona i vrsta
def DrawLabels(game_rect: pygame.Rect, size: tuple[int, int]):

    #sve vezano za tablu crtamo u okviru game_rect pravougaonika
    labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"];

    #crtamo oznake za vrste i kolone
    label_font = pygame.font.Font(None, const.LABEL_FONT_SIZE)

    #oznake vrsta
    for i in range(0, size[0]):
        label_surface = label_font.render(str(labels[i]), False, "WHITE")
        label_rect = pygame.rect.Rect(game_rect.left + const.WALL_W, game_rect.top + (i + 1) * (const.SQUARE + const.WALL_W), const.SQUARE, const.SQUARE)
        screen.blit(label_surface, label_rect)

    #oznake kolona
    for i in range(0, size[1]):
        label_surface = label_font.render(str(labels[i]), False, "WHITE")
        label_rect = pygame.rect.Rect(game_rect.left + (i + 1) * (const.WALL_W + const.SQUARE), game_rect.top + const.WALL_W, const.SQUARE, const.SQUARE)
        screen.blit(label_surface, label_rect)



#funkcija koja crta zidove na tabli
def DrawWalls(board_rect: pygame.Rect, walls: bl.Wall):
    
    for wall in walls:
        wall_rect = None
        color = None
        if wall.type == "blue":
            left = board_rect.left + wall.position[1] * (const.SQUARE + const.WALL_W)
            top = board_rect.top + (wall.position[0] + 1) * (const.SQUARE + const.WALL_W) - const.WALL_W
            wall_rect = pygame.rect.Rect(left, top, const.WALL_H, const.WALL_W)
            color = "CYAN"
        else:
            left = board_rect.left + (wall.position[1] + 1) * (const.SQUARE + const.WALL_W) - const.WALL_W 
            top = board_rect.top + wall.position[0] * (const.SQUARE + const.WALL_W)
            wall_rect = pygame.rect.Rect(left, top, const.WALL_W, const.WALL_H)
            color = "GREEN"

        if(wall_rect and color):
            pygame.draw.rect(screen, color, wall_rect)


#funckija za iscrtavanje trenutnog stanja na tabli
def DrawGameBoard(size: tuple[int, int], player_1: tuple[tuple[int, int]], player_2: tuple[tuple[int, int]], walls: list[tuple[int, int]]):

    game_rect = pygame.rect.Rect(const.GAME_BOARD_X, const.GAME_BOARD_Y, const.GAME_BOARD_W, const.GAME_BOARD_H)
    pygame.draw.rect(screen, const.GAME_RECT_COLOR, game_rect, 3)

    DrawLabels(game_rect, size)

    board_w = size[1] * const.SQUARE + (size[1] - 1) * const.WALL_W
    board_h = size[0] * const.SQUARE + (size[0] - 1) * const.WALL_W
    board_rect = pygame.rect.Rect(game_rect.left + const.WALL_W + const.SQUARE, game_rect.top + const.WALL_W + const.SQUARE, board_w, board_h)

    #crtamo polja u odnosu na pravougaonik board_rect
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            square = pygame.rect.Rect(board_rect.left + j * (const.SQUARE + const.WALL_W), board_rect.top + i * (const.SQUARE + const.WALL_W), const.SQUARE, const.SQUARE)
            pygame.draw.rect(screen, const.SQUARE_COLOR, square)

    #crtamo igrace na odgovarajucim pozicijama
    p_1_fig_1 = player_1[0]
    c_x = board_rect.left + int(p_1_fig_1[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + int(p_1_fig_1[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p1_f1_rect = pygame.draw.circle(screen, "RED", (c_x, c_y), const.SQUARE // 3)

    p_1_fig_2 = player_1[1]
    c_x = board_rect.left + int(p_1_fig_2[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + int(p_1_fig_2[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p1_f2_rect = pygame.draw.circle(screen, "RED", (c_x, c_y), const.SQUARE // 3)

    p_2_fig_1 = player_2[0]
    c_x = board_rect.left + int(p_2_fig_1[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + int(p_2_fig_1[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p2_f1_rect = pygame.draw.circle(screen, "YELLOW", (c_x, c_y), const.SQUARE // 3)

    p_2_fig_2 = player_2[1]
    c_x = board_rect.left + int(p_2_fig_2[1]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    c_y = board_rect.top + int(p_2_fig_2[0]) * (const.SQUARE + const.WALL_W) + const.SQUARE // 2
    p2_f2_rect = pygame.draw.circle(screen, "YELLOW", (c_x, c_y), const.SQUARE // 3)

    DrawWalls(board_rect, walls)

    return {"player_boxes" : ([p1_f1_rect, p1_f2_rect], [p2_f1_rect, p2_f2_rect]), "board_rect" : (board_rect.x, board_rect.y)}



#game loop
red_to_move = True
#move_state je lista koja pamti stanje poteza (prvi element pamti da li je izabran igrac kog zelimo da pomerimo, drugi element pamti da li je izabrano odredisno polje,
#treci element pokazuje da li je izabran zid). Kada su sva tri elementa True, potez je odigran i prelazimo na drugog igraca
move_state = [False, False, False]
move = [None, None, None]
MOVE_FINISHED = pygame.USEREVENT + 1


#funckija za obradu klikova
def HandleClickEvent(click_pos : tuple[int, int], board_info):

    #izbor igraca koji se pomera
    if not move_state[0]:
        player_boxes = board_info["player_boxes"]
        #znaci da jos uvek nije izabran igrac kojeg hocemo da pomerimo
        if red_to_move:
            if player_boxes[0][0].collidepoint(click_pos):
                move[0] = 0
                move_state[0] = True
            elif player_boxes[0][1].collidepoint(click_pos):
                move[0] = 1
                move_state[0] = True
        else:
            if player_boxes[1][0].collidepoint(click_pos):
                move[0] = 0
                move_state[0] = True
            elif player_boxes[1][1].collidepoint(click_pos):
                move[0] = 1
                move_state[0] = True
    
    #izbor odredisne pozicije igraca
    elif move_state[0] and not move_state[1]:
        #sada biramo odredisno polje
        click_pos = list(click_pos)
        board_rect = board_info["board_rect"]

        click_pos[0] -= board_rect[0]
        click_pos[1] -= board_rect[1]
        newPos = [-1, -1]

        #sada imamo koordinata klika u odnosu na pocetak table i mozemo da nadjemo indekse
        for i in range(0, game.board.n):
            if ((const.WALL_W + const.SQUARE) * i < click_pos[0]) and ((const.WALL_W + const.SQUARE) * i + const.SQUARE > click_pos[0]):
                newPos[1] = i
                break
        
        for i in range(0, game.board.m):
            if ((const.WALL_W + const.SQUARE) * i < click_pos[1]) and ((const.WALL_W + const.SQUARE) * i + const.SQUARE > click_pos[1]):
                newPos[0] = i
                break
        
        if newPos[0] != -1 and newPos[1] != -1:
            move[1] = (newPos[0], newPos[1])
            move_state[1] = True
            print(move)
    
    #izbor pozicije zida
    elif move_state[0] and move_state[1] and not move_state[2]:
        #sada biramo gde hocemo da postavimo zid
        click_pos = list(click_pos)
        board_rect = board_info["board_rect"]

        click_pos[0] -= board_rect[0]
        click_pos[1] -= board_rect[1]
        wallPos = [-1, -1]

        #proveravamo da li je izabran vertikalni zid
        for i in range(0, game.board.n):
            if (click_pos[0] > const.SQUARE + i * (const.SQUARE + const.WALL_W)) and (click_pos[0] < (i + 1) * (const.SQUARE + const.WALL_W)):
                wallPos[1] = i

                for i in range(0, game.board.m):
                    if (click_pos[1] > i * (const.SQUARE + const.WALL_W)) and (click_pos[1] < const.SQUARE + i * (const.SQUARE + const.WALL_W)):
                        wallPos[0] = i
                        break

                break
        
        if wallPos[0] != -1 and wallPos[1] != -1:
            move_state[2] = True
            move[2] = (wallPos[0], wallPos[1], 'z')
            print(move)
            move_state[2] = True
            pygame.event.post(pygame.event.Event(MOVE_FINISHED))
            return
        
        #ako nije nadjen vertikalni zid, trazimo horizontalni
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
            move_state[2] = True
            move[2] = (wallPos[0], wallPos[1], 'p')
            print(move)
            move_state[2] = True
            pygame.event.post(pygame.event.Event(MOVE_FINISHED))
            return

    #ukoliko je sve izabrano, zavrsavamo potez
    if move_state[0] and move_state[1] and move_state[2]:
        pygame.event.post(pygame.event.Event(MOVE_FINISHED))



while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            HandleClickEvent(event.pos, board_info)
        
        if event.type == MOVE_FINISHED:
            #igranje poteza
            wall_move_pos = (move[2][0], move[2][1]) if move[2] else ()
            wall_type = move[2][2] if move[2] else ''
            player_type = 'x' if red_to_move else 'o'
            game.nextMove(move[0], wall_move_pos, wall_type, player_type, move[1])

            #promena stanja
            if (game.board.player1.greenWallNumber == game.board.player2.blueWallNumber == 0) and (game.board.player2.greenWallNumber == game.board.player2.blueWallNumber == 0):
                #ako nemamo vise zidova
                new_state = [False, False, True]
            else:
                new_state = [False, False, False]
            
            red_to_move = not red_to_move
            move = [None, None, None]
            move_state = new_state
            #ovde treba da ubacimo proveru da li je stiglo do kraja
            print(red_to_move)
            

    #draw
    DrawHeader((game.board.player1.greenWallNumber, game.board.player1.blueWallNumber), (game.board.player1.greenWallNumber, game.board.player1.blueWallNumber), game.isPlayerOneNext)
    board_info = DrawGameBoard((game.board.m, game.board.n), game.board.player1.positions, game.board.player2.positions, game.board.walls)

    #update
    pygame.display.update()
    clock.tick(60)