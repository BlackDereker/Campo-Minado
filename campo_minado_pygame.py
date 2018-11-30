# Dupla: Bruno Godoi Machado (31829929) e Lucas Quental (31852319)

import random
import pygame
from enum import Enum
import os
import sys


# Estados de Jogo
class GameState(Enum):
    SETUP = 1
    GAME = 2
    END = 3
    CUSTOM_SETUP = 4

# Dificuldades
class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    CUSTOM = 4

    
# Gerar aleatoriamente um campo dado o comprimento e a altura
def initialize(width, height, bombs):
    # Criar uma grade vazia
    grid = [[0 for _ in range(width)] for _ in range(height)]
    # Escolhas possiveis
    choices = []
    for y in range(height):
        for x in range(width):
            choices.append((x,y))
    # Colocar as bombas em posicoes aleatorias
    for i in range(bombs):
        coords = random.choice(choices)
        choices.remove(coords)
        rx = coords[0]
        ry = coords[1]
        grid[ry][rx] = -1
        if len(choices) == 0:
            break
        """
        while len(choices) > 0:
            
            
            rx = random.randrange(0, width-1)
            ry = random.randrange(0, height-1)
            if grid[ry][rx] != -1:
                grid[ry][rx] = -1
                break
            """
    # Numerar os espacos adjascentes das bombas
    for row in range(height):
        for col in range(width):
            place = grid[row][col]
            if place == -1:
                for i in range(-1, 2, 1):
                    for j in range(-1, 2, 1):
                        y = row + i
                        x = col + j
                        if x >= width or y >= height or x < 0 or y < 0:
                            continue
                        if grid[y][x] != -1:
                            grid[y][x] += 1
    return grid
        

# Estado atual do campo
def status(campo, revelado):
    for row in range(len(campo)):
        for col in range(len(campo[0])):
            # Se um espaco estiver marcado e nao for uma bomba, o jogo nao terminou
            if revelado[row][col] == 2 and campo[row][col] != -1:
                return False
            # Se um espaco nao estiver revelado e nao tem uma bomba, o jogo nao terminou
            elif revelado[row][col] == 0 and campo[row][col] != -1:
                return False
    return True


# Acao do jogador em uma posicao do campo
def step(campo, x, y, action):
    if action == 0:
        # Se o jogador revelou uma bomba, retorna 0
        if campo[y][x] == -1:
            return 0
        # Se o jogador revelou com sucesso, retorna -1
        else:
            return -1
    # Se o jogador simplesmente marcou um espaco, retorna 1
    else:
        return 1

# Funcao recursiva que revela os lugares vazios em uma reacao em cadeia
def revelar_vazio(campo, revelado, x, y):
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            # Se estiver fora das dimensoes do campo, ignore
            if x+j < 0 or y+i < 0 or x+j >= len(revelado[0]) or y+i >= len(revelado):
                continue
            # Revela um espaco nao ainda revelado
            if revelado[y+i][x+j] == 0:
                revelado[y+i][x+j] = 1
                # Se revelar um espaco vazio, aplica a mesma funcao nesse espaco
                if campo[y+i][x+j] == 0:
                    revelar_vazio(campo, revelado, x+j, y+i)


def print_campo(screen, campo, revelado):

    # Carregar a fonte para os quadrados
    square_font = pygame.font.SysFont('Arial', 18)

    # Carregar as imagens
    bomb_img = pygame.image.load("Images/bomb.png").convert_alpha()
    flag_img = pygame.image.load("Images/flag.png").convert_alpha()

    # Mudar o tamanho das imagens
    bomb_img = pygame.transform.scale(bomb_img, (25,25))
    flag_img = pygame.transform.scale(flag_img, (25,25))

    # Dicionario de cores segundo o numero da casa
    colors_dict = {1: (0,0,255), 2: (0,150,0), 3: (255,0,0), 4: (0,0,100),
                   5: (0,0,100), 6: (0,255,255), 7: (255,255,255), 8: (50,50,50)}

    # Iniciar uma lista vazia para os botoes
    buttons = [[0 for _ in range(len(campo[0]))] for _ in range(len(campo))]
    # Espacamento entre os botoes
    offset = 26
    # Espacamento das bordas da tela
    margin = (10, 70)
    # Pintar o fundo da tela
    screen.fill((100,100,100))

    # Posicionar os botoes na tela
    for row in range(len(campo)):
        for col in range(len(campo[0])):
            # Criar o botao
            button = pygame.Rect(col * offset + margin[0], row * offset + margin[1], 25, 25)
            # Guardar o botao na lista
            buttons[row][col] = button
            # Se a casa nao estiver revelad
            if revelado[row][col] == 0:
                # Desenhar um botao cinza
                pygame.draw.rect(screen, (150,150,150), button)
            # Se estiver revelado
            elif revelado[row][col] == 1:
                # Desenhar um quadrado cinza
                pygame.draw.rect(screen, (200,200,200), button)
                # Pegar o numero do quadrado
                number = campo[row][col]
                # Se for uma bomba
                if number == -1:
                    # Desenhar a imagem de uma bomba no quadrado
                    screen.blit(bomb_img, (button.left, button.top))
                # Se nao for um quadrado vazio
                elif number != 0:
                    # Pegar a cor correspondente do numero
                    color = colors_dict[number]
                    # Prepar o numero do quadrado em texto
                    number_text = square_font.render(str(campo[row][col]), True, color)
                    # Renderizar o numero na tela
                    screen.blit(number_text, (button.left + 6.5, button.top))
            # Se estiver marcado
            else:
                # Desenhar um quadrado vermelho
                pygame.draw.rect(screen, (100,0,0), button)
                # Desenhar uma imagem de uma bandeira no quadrado
                screen.blit(flag_img, (button.left, button.top))

    # Retornar os botoes criados
    return buttons
    

# Funcao que retorna uma cor aleatoria
def random_color():
    # Gerar os valores R G B aleatoriamente entre 0 e 255
    r = random.randrange(0,255)
    g = random.randrange(0,255)
    b = random.randrange(0,255)
    # Retornar os valores em um tuple
    return (r,g,b)

# Pegar imagens de um diretorio relativo
def get_images(path):
    # Lista para guardar os arquivos
    files = []
    # Iterar os arquivos do diretorio
    for file in os.listdir(path):
        # Checar se o arquivo tem extensao ".png"
        if file.endswith(".png"):
            # Guardar a imagem na lista
            files.append(file)
    # Retornar as imagens
    return files


                    
# Funcao principal do jogo com pygame
def game():

    # Configuracoes iniciais
    sys.setrecursionlimit(15000)
    
    # Inicializar o pygame
    pygame.init()

    # Definir o display e o clock
    screen = pygame.display.set_mode((400, 500))
    clock = pygame.time.Clock()

    # Colocar um titulo
    pygame.display.set_caption("Minesweeper")

    # Definir uma fonte para o texto
    difficulty_font = pygame.font.SysFont('Arial', 30)
    title_font = pygame.font.SysFont('Arial', 40)
    timer_font = pygame.font.SysFont('Impact', 37)
    custom_font = pygame.font.SysFont('Impact', 40)
    credits_font = pygame.font.SysFont('Arial', 12)

    # Estados do Jogo
    current_state = GameState.SETUP

    # Carregamento das imagens necessarios
    title_bomb = pygame.image.load("Images/title_bomb.png").convert_alpha()
    title_background = get_images("Images/Martelo")
    back_arrow = pygame.image.load("Images/back_arrow.png").convert_alpha()
    smile = pygame.image.load("Images/smile.png").convert_alpha()
    surprised = pygame.image.load("Images/surprised.png").convert_alpha()
    dead = pygame.image.load("Images/dead.png").convert_alpha()
    sunglasses = pygame.image.load("Images/sunglasses.png").convert_alpha()
    up_arrow_img = pygame.image.load("Images/up_arrow.png").convert_alpha()
    down_arrow_img = pygame.image.load("Images/down_arrow.png").convert_alpha()

    # Ajustar o tamanho das imagens
    back_arrow = pygame.transform.scale(back_arrow, (30, 20))
    smile = pygame.transform.scale(smile, (40,40))
    surprised = pygame.transform.scale(surprised, (40,40))
    dead = pygame.transform.scale(dead, (40,40))
    sunglasses = pygame.transform.scale(sunglasses, (40,40))
    up_arrow_img = pygame.transform.scale(up_arrow_img, (30,20))
    down_arrow_img = pygame.transform.scale(down_arrow_img, (30,20))

    # Gerenciamento de frames
    fps = 30
    bg_frame = 0
    flag = 1
    current_frame = 0

    # Variaveis do CUSTOM_SETUP
    custom_width = 9
    custom_height = 9
    custom_bombs = 10

    # Loop principal do jogo
    running = True
    while running:
        # -- Renderizar -- 
        # Se tiver na tela de SETUP
        if current_state == GameState.SETUP:
            # Fazer o fundo
            screen.fill((150,150,150))
            # Carregar a imagem do fundo segundo o frame atual
            image = pygame.image.load("Images/Martelo/" + title_background[bg_frame])
            # Ajustar o tamanho da imagem para o tamanho da tela
            image = pygame.transform.scale(image, (screen.get_width() + 6, screen.get_height() + 20))
            # Renderizar a imagem
            screen.blit(image, (-5,-5))
            # Progredir o frame e reseta quando atinge o limite
            bg_frame += flag
            if bg_frame == len(title_background) - 1:
                #bg_frame = 0
                flag = -1
            elif bg_frame == 0:
                flag = 1
            # Definir a imagem da bomba
            title_bomb = pygame.transform.scale(title_bomb, (100,100))
            # Definir o titulo
            title = title_font.render("Minesweeper", True, (0,0,0))
            # Renderizar o titulo e a bomba
            screen.blit(title, (40,50))
            screen.blit(title_bomb, (290, 25))
            # Iteracao entre as dificuldades existentes
            buttons = []
            # Espacamento inicial dos botoes
            offset = 175
            for difficulty in Difficulty:
                # Comprimento e altura do botao
                width = 150
                height = 50
                # Definir a borda do botao
                outter_button = pygame.Rect((screen.get_width()/2 - width/2, offset - height/2), (width, height))
                # Salvar o botao
                buttons.append(outter_button)
                # Definir o botao
                inner_button = outter_button.inflate(-10,-10).clamp(outter_button)
                # Texto do botao correspondendo a dificuldade
                text = difficulty_font.render(difficulty.name, True, (0, 0, 0))
                # Renderizar os botoes e texto
                pygame.draw.rect(screen, (100,100,100), outter_button)
                # Ver se o mouse esta em cima do botao
                if outter_button.collidepoint(pygame.mouse.get_pos()):
                    # Muda a cor do botao de acordo com a dificuldade
                    if difficulty.name == "EASY":
                        color = (0,255,0)
                    elif difficulty.name == "MEDIUM":
                        color = (255,255,0)
                    elif difficulty.name == "HARD":
                        color = (255,0,0)
                    else:
                        color = random_color()
                    pygame.draw.rect(screen, color, inner_button)
                else:
                    pygame.draw.rect(screen, (185,185,185), inner_button)
                # Renderizar o texto da dificuldade no botao
                screen.blit(text, (screen.get_width()/2 - len(difficulty.name) * 10 - 3, offset + 8 - height/2))
                # Dar um espaco entre o botao atual e o proximo
                offset += 75
                # Colocar os creditos
                credits_text = credits_font.render("Credits:", True, (0,0,0))
                credits_text1 = credits_font.render("Bruno Godoi Machado", True, (0,0,0))
                credits_text2 = credits_font.render("Lucas Quental", True, (0,0,0))
                screen.blit(credits_text, (10, screen.get_height() - 45))
                screen.blit(credits_text1, (20, screen.get_height() - 30))
                screen.blit(credits_text2, (20, screen.get_height() - 20))
            # Detectar o evento do jogador fechar o jogo
        # Checar se o jogo esta rodando ou esta finalizado
        elif current_state == GameState.GAME or current_state == GameState.END:
            # Printar os quadrados no campo
            buttons = print_campo(screen, campo, revelado)
            # Criar o botao de resetar
            reset_button = pygame.Rect(screen.get_width() / 2 - 20, 20, 40, 40)
            reset_button_border = pygame.Rect(screen.get_width() / 2 - 25, 15, 50, 50)
            # Criar o botao de voltar
            back_button = pygame.Rect(0, 0, 40, 15)
            # Criar o timer
            timer_bg = pygame.Rect(screen.get_width() - 70, 20, 60, 40)
            timer_text = timer_font.render("{:03}".format(current_frame // fps), True, (255,0,0))
            # Criar o contador de bomba
            hidden_bombs = bombs
            for row in revelado:
                hidden_bombs -= row.count(2)
            bomb_counter = pygame.Rect(10, 20, 60, 40)
            bomb_text = timer_font.render("{:03}".format(hidden_bombs), True, (255,0,0))
            # Renderizar os botao de voltar
            pygame.draw.rect(screen, (200,200,200), back_button)
            screen.blit(back_arrow, (3,-3))
            # Renderizar o botao de resetar
            pygame.draw.rect(screen, (50,50,50), reset_button_border)
            pygame.draw.rect(screen, (200,200,200), reset_button)
            # Renderizar o timer
            pygame.draw.rect(screen, (0,0,0), timer_bg)
            screen.blit(timer_text, (timer_bg.left, timer_bg.top - 2.5))
            # Renderizar o contador de bombas
            pygame.draw.rect(screen, (0,0,0), bomb_counter)
            screen.blit(bomb_text, (bomb_counter.left, bomb_counter.top - 2.5))
            # Checar se o jogo esta rodando
            if current_state == GameState.GAME:
                current_frame += 1
                # Estado do mouse
                pressed = pygame.mouse.get_pressed()
                # Se o botao esquerdo estiver pressionado
                if pressed[0]:
                    # Muda o rosto para surpreso
                    screen.blit(surprised, (reset_button.left, reset_button.top))
                # Se nao estiver pressionado
                else:
                    # Deixa o rosto feliz
                    screen.blit(smile, (reset_button.left, reset_button.top))
            # Se o jogado estiver finalizado
            else:
                # Checa se o jogador ganhou
                if status(campo, revelado):
                    # Coloca oculos de sol no rosto
                    screen.blit(sunglasses, (reset_button.left, reset_button.top))
                # Se o jogador perdeu
                else:
                    # Coloca o rosto morto
                    screen.blit(dead, (reset_button.left, reset_button.top))
        # Enquanto estiver no menu de customizacao
        elif current_state == GameState.CUSTOM_SETUP:
            # Preencha a tela
            screen.fill((150,150,150))
            # Prepara os numeros
            custom_width_num = custom_font.render("{:02}".format(custom_width), True, (0,0,0))
            custom_height_num = custom_font.render("{:02}".format(custom_height), True, (0,0,0))
            custom_bombs_num = custom_font.render("{:02}".format(custom_bombs), True, (0,0,0))
            # Prepara os textos
            custom_width_text = custom_font.render("Width", True, (0,0,0))
            custom_height_text = custom_font.render("Height", True, (0,0,0))
            custom_bombs_text = custom_font.render("Bombs", True, (0,0,0))
            # Cria o botao "generate"
            generate_button = pygame.Rect(screen.get_width() / 2 - 80, screen.get_height() - 75, 160, 50)
            generate_button_border = generate_button.inflate(10,10).clamp(generate_button)
            generate_button_text = custom_font.render("Generate", True, (0,0,0))

            # Cria o botao "back"
            back_button = pygame.Rect(0, 0, 40, 15)

            # Renderiza as setas
            up_arrow_width = screen.blit(up_arrow_img, (screen.get_width() / 5 - 5, screen.get_height() / 2 - 60))
            down_arrow_width = screen.blit(down_arrow_img, (screen.get_width() / 5 - 5, screen.get_height() / 2 + 10))
            up_arrow_height = screen.blit(up_arrow_img, (screen.get_width() / 2 - 5, screen.get_height() / 2 - 60))
            down_arrow_height = screen.blit(down_arrow_img, (screen.get_width() / 2 - 5, screen.get_height() / 2 + 10))
            up_arrow_bombs = screen.blit(up_arrow_img, (screen.get_width() / 1.3 - 5, screen.get_height() / 2 - 60))
            down_arrow_bombs = screen.blit(down_arrow_img, (screen.get_width() / 1.3 - 5, screen.get_height() / 2 + 10))

            # Renderiza os textos
            screen.blit(custom_width_text, (screen.get_width() / 5 - 40, screen.get_height() / 2 - 120))
            screen.blit(custom_height_text, (screen.get_width() / 2 - 50, screen.get_height() / 2 - 120))
            screen.blit(custom_bombs_text, (screen.get_width() / 1.3 - 40, screen.get_height() / 2 - 120))

            # Renderiza os numeros
            screen.blit(custom_width_num, (screen.get_width() / 5 - 10, screen.get_height() / 2 - 40))
            screen.blit(custom_height_num, (screen.get_width() / 2 - 10, screen.get_height() / 2 - 40))
            screen.blit(custom_bombs_num, (screen.get_width() / 1.3 - 10, screen.get_height() / 2 - 40))

            # Renderiza o botao "generate"
            pygame.draw.rect(screen, (100,100,100), generate_button_border)
            pygame.draw.rect(screen, (180,180,180), generate_button)
            screen.blit(generate_button_text, (generate_button.left + 5, generate_button.top))

            # Renderiza o botao "back"
            pygame.draw.rect(screen, (200,200,200), back_button)
            screen.blit(back_arrow, (3,-3))

        # -- Eventos -- 
        for event in pygame.event.get():
            # Detecta se o jogador apertou para sair do jogo
            if event.type == pygame.QUIT:
                # Finaliza o loop principal do jogo
                running = False
            # Eventos enquanto esta no estado de SETUP
            if current_state == GameState.SETUP:
                # Detectar se o jogador soltou o botao
                if event.type == pygame.MOUSEBUTTONUP:
                    # Pegar a posicao do mouse
                    mouse_pos = pygame.mouse.get_pos()
                    # Passar pelos botoes existentes na tela
                    for i in range(len(buttons)):
                        # Botao atual
                        button = buttons[i]
                        # Checar se o mouse esta no botao atual
                        if button.collidepoint(mouse_pos):
                            # Tamanho do campo e a quantidade de bombas conforme a dificuldade
                            if i == 0:
                                size = (9,9)
                                bombs = 10
                                screen = pygame.display.set_mode((253,312))
                            elif i == 1:
                                size = (16,16)
                                bombs = 40
                                screen = pygame.display.set_mode((433, 492))
                            elif i == 2:
                                size = (32,16)
                                bombs = 99
                                screen = pygame.display.set_mode((850, 492))
                            elif i == 3:
                                screen = pygame.display.set_mode((400,300))
                                current_state = GameState.CUSTOM_SETUP
                                break
                            # Inicializa o campo
                            campo = initialize(size[0], size[1], bombs)
                            # Define a matriz dos espacos revelados
                            revelado = [[0 for _ in range(size[0])] for _ in range(size[1])]
                            # Muda o estado do jogo para GAME
                            current_state = GameState.GAME
                            # Reseta o contador
                            current_frame = 0
                            break
            # Enquanto estiver jogando
            elif current_state == GameState.GAME or current_state == GameState.END:
                # Quando tiver o evento de click de mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Pega a posicao do mouse
                    mouse_pos = pygame.mouse.get_pos()
                    pressed = pygame.mouse.get_pressed()
                    # Se clicar no botao de reset
                    if reset_button_border.collidepoint(mouse_pos):
                        campo = initialize(len(campo[0]), len(campo), bombs)
                        revelado = [[0 for _ in range(len(campo[0]))] for _ in range(len(campo))]
                        current_state = GameState.GAME
                        current_frame = 0
                    elif back_button.collidepoint(mouse_pos):
                        current_state = GameState.SETUP
                        screen = pygame.display.set_mode((400,500))
                        current_frame = 0
                        break
                    elif current_state == GameState.GAME:
                        # Passa pelos botoes e checa se clicou em uma casa
                        for row in range(len(buttons)):
                            for col in range(len(buttons[0])):
                                button = buttons[row][col]
                                if button.collidepoint(mouse_pos):
                                    action = 0
                                    # Se pressionou o botao direito
                                    if pressed[0]:
                                        action = 0
                                    # Se pressionou o botao esquerdo
                                    elif pressed[2]:
                                        action = 1
                                    # Fazer a jogada
                                    jogada = step(campo, col, row, action)
                                    # Se revelou uma casa sem bomba
                                    if jogada == -1 and revelado[row][col] == 0:
                                        # Revelar a casa
                                        revelado[row][col] = 1
                                        # Se revelar uma casa sem bomba por perto
                                        if campo[row][col] == 0:
                                            revelar_vazio(campo, revelado, col, row)
                                    # Se revelou uma casa com bomba
                                    elif jogada == 0 and not revelado[row][col] == 2:
                                        # Revelar a casa
                                        revelado[row][col] = 1
                                        # Finalizar o jogo
                                        current_state = GameState.END
                                        # Revelar todas as bombas
                                        for row in range(len(campo)):
                                            for col in range(len(campo[0])):
                                                if campo[row][col] == -1:
                                                    revelado[row][col] = 1
                                    # Se marcou ou desmarcou uma casa
                                    elif jogada == 1:
                                        if revelado[row][col] == 0:
                                            revelado[row][col] = 2
                                        elif revelado[row][col] == 2:
                                            revelado[row][col] = 0
                                    # Checar se o jogador ganhou
                                    ganhou = status(campo, revelado)
                                    if ganhou:
                                        for row in range(len(campo)):
                                            for col in range(len(campo[0])):
                                                if campo[row][col] == -1:
                                                    revelado[row][col] = 2
                                        current_state = GameState.END
            # Se o jogador estiver na customizacao
            elif current_state == GameState.CUSTOM_SETUP:
                # Se ele aperta o mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Se apertou nas setas, aumenta ou abaixa o numero
                    if up_arrow_width.collidepoint(mouse_pos):
                        if custom_width < 64:
                            custom_width += 1
                    elif down_arrow_width.collidepoint(mouse_pos):
                        if custom_width > 1:
                            custom_width -= 1
                            if custom_bombs >= custom_width * custom_height:
                                custom_bombs = custom_width * custom_height - 1
                    elif up_arrow_height.collidepoint(mouse_pos):
                        if custom_height < 64:
                            custom_height += 1
                    elif down_arrow_height.collidepoint(mouse_pos):
                        if custom_height > 1:
                            custom_height -= 1
                            if custom_bombs >= custom_width * custom_height:
                                custom_bombs = custom_width * custom_height - 1
                    elif up_arrow_bombs.collidepoint(mouse_pos):
                        if custom_bombs < custom_width * custom_height:
                            if custom_bombs < custom_width * custom_height - 1:
                                custom_bombs += 1
                    elif down_arrow_bombs.collidepoint(mouse_pos):
                        if custom_bombs > 1:
                            custom_bombs -= 1
                    # Se apertar em Generate, iniciar o jogo
                    elif generate_button_border.collidepoint(mouse_pos):
                        campo = initialize(custom_width, custom_height, custom_bombs)
                        revelado = [[0 for _ in range(custom_width)] for _ in range(custom_height)]
                        bombs = custom_bombs
                        if custom_width > 6:
                            screen = pygame.display.set_mode((26 * custom_width + 20, 26 * custom_height + 80))
                        else:
                            screen = pygame.display.set_mode((26 * 7 + 20, 26 * custom_height + 80))
                        current_state = GameState.GAME
                    # Se apertar em Back, voltar ao menu principal
                    elif back_button.collidepoint(mouse_pos):
                        current_state = GameState.SETUP
                        screen = pygame.display.set_mode((400,500))
                    
                                    
                        
        # Atualizar a tela
        pygame.display.update()
        # Limitar o jogo em 30 fps
        clock.tick(fps)

    # Sair do jogo e do shell
    pygame.quit()
    exit()

# Executar a funcao principal do jogo
game()
