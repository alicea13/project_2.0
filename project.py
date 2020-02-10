import pygame, os, random
import sys
import sqlite3
import copy


class StartWindow:
    def __init__(self):
        super().__init__()
        pygame.init()

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('gadugi', 36)
        self.text1 = titl.render("One Little Warm", 1, pygame.Color("blue"))

        ask_input = pygame.font.SysFont('arial', 25)
        self.text2 = ask_input.render("Введите логин:", 1, pygame.Color("lightblue"))

        ex = False
        login = InputText(width // 2 - 70, height // 5 * 3 - 32, 140, 32, ex, "lightblue")

        run_st = True

        while run_st:
            if ex:
                run_st = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_st = False
                    login.events(event)

            screen.fill((30, 30, 30))
            login.draw(screen)
            screen.blit(self.text1, (180, 60))
            screen.blit(self.text2, (220, 170))
            pygame.display.flip()

    def get_click(self, pos):
        print("here")


class InputText:
    def __init__(self, x, y, width, height, ex, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.login_t = text
        self.text_surf = pygame.font.Font(None, 32).render(text, True, pygame.Color('lightblue'))
        self.run_text = False
        self.exit = ex
        self.color = color

        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound.play()
            self.color = "blue"
            if self.rect.collidepoint(event.pos):
                self.run_text = True
            else:
                self.run_text = False

        if event.type == pygame.KEYDOWN and self.run_text:
            if event.key == pygame.K_RETURN:
                self.open(self.login_t)
                self.login_t = ""
            elif event.key == pygame.K_BACKSPACE:
                self.login_t = self.login_t[:-1]
            else:
                self.login_t += event.unicode
            self.text_surf = pygame.font.Font(None, 32).render(self.login_t, True, pygame.Color('lightblue'))

    def open(self, login_t):
        self.id_login = self.cur.execute("""SELECT id FROM logins
                                            WHERE login == ?""",
                                         (login_t,)).fetchall()
        print(self.id_login)
        if self.id_login != []:
            self.l, = self.id_login[0]

            self.have_login = HaveLogin(login_t)
            self.exit = True
        else:
            self.no_login = NoLogin(login_t)
            self.exit = True

    def update(self):
        width = max(200, self.text_surf.get_width() + 8)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.text_surf, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, pygame.Color(self.color), self.rect, 4)


class HaveLogin:
    def __init__(self, login):
        super().__init__()
        pygame.init()

        self.log = login
        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")

        titl = pygame.font.SysFont('arial', 36)
        self.text1 = titl.render("Добро пожаловать,", 1, pygame.Color("blue"))

        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(login, 1, pygame.Color('lightblue'))

        act_open = pygame.font.SysFont("arial", 25)
        self.text3 = act_open.render(f"Начать игру", 1, pygame.Color("lightblue"))

        act_chg = pygame.font.SysFont("arial", 25)
        self.text4 = act_chg.render("Таблица рекордов", 1, pygame.Color("lightblue"))

        act_authors = pygame.font.SysFont("colibri", 25)
        self.text6 = act_authors('Авторы программы', 1, pigame.Color("Yellow"))

        act_exit = pygame.font.SysFont("arial", 25)
        self.text5 = act_exit.render("Сменить пользователя", 1,
                                    pygame.Color("lightblue"))

        run_havelog = True

        while run_havelog:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_havelog = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.sound.play()
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 213:
                        print("game")

                        # открытие окна меню
                        Menu(self.log)

                        run_havelog = False
                    if 160 <= event.pos[0] <= 450 and 230 <= event.pos[1] <= 283:
                        print("record")
                        # вывод топ 10 (?)
                        # Record()

                    if 160 <= event.pos[0] <= 450 and 300 <= event.pos[1] <= 353:
                        print("back")

                    if 160 <= event.pos[0] <= 450 and 370 <= event.pos[1] <= 423:
                        print("authors")

                        # выход к стартовому окну
                        StartWindow()
                        run_havelog = False
            screen.fill((30, 30, 30))
            for i in range(3):
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (160, 160 + i * 70, 290, 53), 3)
            if run_havelog:
                screen.blit(self.text1, (width // 6, height // 8.3))   # (100, 60)
                screen.blit(self.text2, (width // 1.379, height // 7.69))   # (435, 65)
                screen.blit(self.text3, (width // 2.6, height // 2.94))   # (230, 170)
                screen.blit(self.text4, (width // 3, height // 2.08))   # (200, 240)
                screen.blit(self.text5, (width // 3.42, height // 1.61))   # (175, 310)
                screen.blit(self.text6, (width // 4, height // 1.4))
                pygame.display.flip()


class NoLogin:
    def __init__(self, login):
        super().__init__()
        pygame.init()

        self.log = login
        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")

        self.log_app = self.cur.execute("""INSERT INTO logins(login) VALUES(?)""", (self.log,))
#        self.main_app = self.cur.execute("""INSERT INTO Main(login) VALUES(?)""", (self.log,))
        self.con.commit()

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('arial', 36)
        self.text1 = titl.render("Новый игрок,", 1, pygame.Color("blue"))

        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(self.log, 1, pygame.Color('lightblue'))   # login.rjust((width - 435) % 8, " ")

        act_open = pygame.font.SysFont("arial", 25)
        self.text3 = act_open.render(f"Начать игру", 1, pygame.Color("lightblue"))

        act_chg = pygame.font.SysFont("arial", 25)
        self.text4 = act_chg.render("Таблица рекордов", 1, pygame.Color("lightblue"))

        act_exit = pygame.font.SysFont("arial", 25)
        self.text5 = act_exit.render("Сменить пользователя", 1, pygame.Color("lightblue"))

        run_nolog = True

        while run_nolog:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_nolog = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.sound.play()
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 213:
                        print("game")

                        # открытие окна меню
                        Menu(self.log)

                        run_nolog = False
                    if 160 <= event.pos[0] <= 450 and 230 <= event.pos[1] <= 283:
                        print("record")
                        # вывод топ 10 (?)
                        # Record()

                    if 160 <= event.pos[0] <= 450 and 300 <= event.pos[1] <= 353:
                        print("back")

                        # выход к стартовому окну
                        StartWindow()
                        run_nolog = False

                screen.fill((30, 30, 30))
                for i in range(3):
                    pygame.draw.rect(screen, pygame.Color("blue"),
                                     (160, 160 + i * 70, 290, 53), 3)

                screen.blit(self.text1, (width // 6, height // 8.3))  # (100, 60)
                screen.blit(self.text2, (width // 1.379, height // 7.69))  # (435, 65)
                screen.blit(self.text3, (width // 2.6, height // 2.94))  # (230, 170)
                screen.blit(self.text4, (width // 3, height // 2.08))  # (200, 240)
                screen.blit(self.text5, (width // 3.42, height // 1.61))  # (175, 310)

                pygame.display.flip()

        pygame.quit()


class Menu:
    def __init__(self, log):
        super().__init__()
        pygame.init()

        self.login = log
        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")
        text_before = pygame.font.SysFont("arial", 36)
        self.titl = text_before.render("Перед началом игры", 1, pygame.Color("blue"))

        text_size = pygame.font.SysFont("arial", 25)
        self.t_size = text_size.render("Выберите размер поля :", 1, pygame.Color("lightblue"))

        size_10 = pygame.font.SysFont("colibri", 25)
        self.size_10 = size_10.render("10x10", 1, pygame.Color("lightblue"))

        size_20 = pygame.font.SysFont("colibri", 25)
        self.size_20 = size_20.render("15x15", 1, pygame.Color("lightblue"))

        size_30 = pygame.font.SysFont("colibri", 25)
        self.size_30 = size_30.render("20x20", 1, pygame.Color("lightblue"))

        text_mode = pygame.font.SysFont("arial", 25)
        self.t_mode = text_mode.render("Выберите режим игры :", 1, pygame.Color("lightblue"))

        mode_food = pygame.font.SysFont("colibri", 25)
        self.m_food = mode_food.render("еда", 1, pygame.Color("lightblue"))
        self.f_col = "yellow"

        mode_speed = pygame.font.SysFont("colibri", 25)
        self.m_speed = mode_speed.render("скорость", 1, pygame.Color("lightblue"))
        self.s_col = "yellow"

        mode_barrier = pygame.font.SysFont("colibri", 25)
        self.m_barrier = mode_barrier.render("препятствия", 1, pygame.Color("lightblue"))
        self.b_col = "yellow"

        text_character = pygame.font.SysFont("arial", 25)
        self.t_char = text_character.render("Выберите персонажа :", 1, pygame.Color("lightblue"))

        ch = pygame.font.SysFont("colibri", 30)
        self.ch = ch.render("Персонажи", 1, pygame.Color("lightblue"))

        play = pygame.font.SysFont("arial", 25)
        self.play = play.render("Играть", 1, pygame.Color("lightblue"))

        board_size = ''

        self.list_mode = [["blue", 3], ["blue", 3], ["blue", 3]]
        self.list_size = [["blue", 3], ["blue", 3], ["blue", 3]]

        self.size_list = [self.size_10, self.size_20, self.size_30]
        self.mode_list = [self.m_barrier, self.m_speed, self.m_food]
        self.game_mode = []
        run_menu = True

        while run_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.sound.play()
                    print(event.pos)
                    if 100 <= event.pos[0] <= 170 and 165 <= event.pos[1] <= 215:
                        #print(10)
                        board_size = 10

                        self.list_size[0] = ["yellow", 0]
                        self.list_size[1], self.list_size[2] = ["blue", 3], ["blue", 3]

                    if 265 <= event.pos[0] <= 335 and 165 <= event.pos[1] <= 215:
                        # print(15)
                        board_size = 15

                        self.list_size[1] = ["yellow", 0]
                        self.list_size[0], self.list_size[2] = ["blue", 3], ["blue", 3]

                    if 430 <= event.pos[0] <= 500 and 165 <= event.pos[1] <= 215:
                        #print(20)
                        board_size = 20

                        self.list_size[2] = ["yellow", 0]
                        self.list_size[1], self.list_size[0] = ["blue", 3], ["blue", 3]

                    if 90 <= event.pos[0] <= 210 and 295 <= event.pos[1] <= 345:

                        if "препятствия" not in self.game_mode:
                            self.game_mode.append("препятствия")
                            self.list_mode[0] = ["yellow", 0]
                        else:
                            self.game_mode.pop(self.game_mode.index("препятствия"))
                            self.list_mode[0] = ["blue", 3]
                        #print(self.game_mode)
                        #print("barrier")

                        # game_mode = "препятствия"

                    if 240 <= event.pos[0] <= 360 and 295 <= event.pos[1] <= 345:

                        if "скорость" not in self.game_mode:
                            self.game_mode.append("скорость")
                            self.list_mode[1] = ["yellow", 0]
                        else:
                            self.game_mode.pop(self.game_mode.index("скорость"))
                            self.list_mode[1] = ["blue", 3]
                        #print(self.game_mode)
                        #print("speed")

                        #game_mode = "скорость"

                    if 390 <= event.pos[0] <= 510 and 295 <+ event.pos[1] <= 345:

                        if "еда" not in self.game_mode:
                            self.game_mode.append("еда")
                            self.list_mode[2] = ["yellow", 0]
                        else:
                            self.game_mode.pop(self.game_mode.index("еда"))
                            self.list_mode[2] = ["blue", 3]

                        #print(self.game_mode)
                        #print("food")

                        game_mode = "еда"

                    if 350 <= event.pos[0] <= 540 and 370 <= event.pos[1] <= 400:
                        print("barrier menu")
                        Character(self.login)

                    if 40 <= event.pos[0] <= 560 and 420 <= event.pos[1] <= 475:
                        print("play")
                        Game(self.login, self.game_mode, board_size)
            if run_menu is True:
                screen.fill((0, 0, 0))
                for i in range(3):
                    pygame.draw.rect(screen, pygame.Color(self.list_size[i][0]),
                                     (100 + i * 165, 165, 70, 50), self.list_size[i][1])

                    screen.blit(self.size_list[i], (110 + i * 165, 180))

                    pygame.draw.rect(screen, pygame.Color(self.list_mode[i][0]),
                                     (90 + i * 150, 295, 120, 50 ),
                                     self.list_mode[i][1])
                    screen.blit(self.mode_list[i], (100 + i * 166, 310))

                screen.blit(self.titl, (width // 4.28, height // 10))   # (140, 50)
                screen.blit(self.t_size, (width // 12, height // 4.16))   # (50, 120)
                screen.blit(self.t_mode, (width // 12, height // 2))   # (50, 250)
                screen.blit(self.t_char, (width // 12, height // 1.315))   # (50, 380)
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (width // 1.71, height // 1.35, width // 3.15,
                                  height // 12.5), 3)   # (350, 370, 190, 60)
                screen.blit(self.ch, (width // 1.538, height // 1.315))   # (390, 380)
                screen.blit(self.play, (width // 2.3, height // 1.162))   # (260, 430)
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (width // 15, height // 1.19, width // 1.153,
                                  height // 9), 3)   # (40, 420, 520, 55)

                pygame.display.flip()
        pygame.quit()


class Character:
    def __init__(self, login):
        super().__init__()
        pygame.init()

        self.login = login
        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        all_sprites = pygame.sprite.Group()

        self.text_char = pygame.font.SysFont("arial", 36)
        self.titl = self.text_char.render("Персонажи", 1,
                                          (255, 191, 0))

        emoji_1 = AnimatedSprite(self.load_image("emoji_1.3.png", -1), 3, 3, 40, 110,
                                 all_sprites)

        emoji_2 = AnimatedSprite(self.load_image("emoji_2.png", -1), 3, 3, 40, 210,
                                 all_sprites)

        emoji_10 = AnimatedSprite(self.load_image("emoji_10.png", -1), 3, 3, 40, 310,
                                 all_sprites)

        emoji_7 = AnimatedSprite(self.load_image("emoji_7.png", -1), 3, 3, 40,
                                 410, all_sprites)

        emoji_5 = AnimatedSprite(self.load_image("emoji_5.png", -1), 3, 3, 220,
                                 110, all_sprites)

        emoji_6 = AnimatedSprite(self.load_image("emoji_6.png", -1), 3, 3, 220,
                                 210, all_sprites)
        emoji_9 = AnimatedSprite(self.load_image("emoji_9.png", -1), 3, 3, 220,
                                 310, all_sprites)
        emoji_8 = AnimatedSprite(self.load_image("emoji_8.png", -1), 3, 3, 220,
                                 410, all_sprites)
        emoji_4 = AnimatedSprite(self.load_image("emoji_4.png", -1), 3, 3, 410,
                                 110, all_sprites)
        emoji_3 = AnimatedSprite(self.load_image("emoji_3.png", -1), 3, 3, 410,
                                 210, all_sprites)
        emoji_11 = AnimatedSprite(self.load_image("emoji_11.png", -1), 3, 3,
                                  410, 310, all_sprites)
        emoji_12 = AnimatedSprite(self.load_image("emoji_12.png", -1), 3, 3,
                                  410, 410, all_sprites)

        clock = pygame.time.Clock()

        run_char = True
        while run_char:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_char = False

                #if event.pos[0]
            screen.fill((0, 0, 0))
            screen.blit(self.titl, (width // 3, height // 11))  # (200, 50)
            all_sprites.draw(screen)  # прорисовываем sprites
            all_sprites.update()
            for i in range(3):
                pygame.draw.rect(screen, pygame.Color("blue"), (25 + i * 190, 95, 180, 90), 3)   # 255, 153, 51
                pygame.draw.rect(screen, pygame.Color("blue"), (25 + i * 190, 195, 180, 90), 3)
                pygame.draw.rect(screen, pygame.Color("blue"), (25 + i * 190, 295, 180, 90), 3)
                pygame.draw.rect(screen, pygame.Color("blue"), (25 + i * 190, 395, 180, 90), 3) # (204, 204, 255)
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()

    def load_image(self, name, color_key=None):
        fullname = os.path.join("data", name)
        image = pygame.image.load(fullname).convert()
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, sprite_group):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Board:
    # создание поля
    def __init__(self, screen, width, height, cell_count=10):

        self.width = width
        self.height = height
        # значения по умолчанию
        self.cell_size = 30   # (width - 120) // cell_count; width // int(cell_count)
        size = width, height = 800, 700
        self.screen = screen
        self.cell_c = cell_count
        self.board = [[0] * cell_count for _ in range(cell_count)]

        self.left = (width - self.cell_size * self.cell_c) // 2
        self.top = (width - self.cell_size * self.cell_c) // 5



    def render(self):
        for i in range(self.cell_c):
            for j in range(self.cell_c):
                pygame.draw.rect(self.screen, pygame.Color("white"),
                                 ((self.left + self.cell_size * i,
                                   self.top + self.cell_size * j),
                                  (self.cell_size, self.cell_size)), 1)

    def get_cell(self, mouse_pos):
        if (self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width and
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height):
            y = (mouse_pos[0] - self.left) // self.cell_size
            x = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        else:
            return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.board[cell[0]][cell[1]] = 1


class Game:
    def __init__(self, login, mode, cell_count=10):
        '''print()
        print("mode", mode)
        print("login", login)
        print("cell_count", cell_count)'''

        pygame.init()
        size = width, height = 800, 700
        screen = pygame.display.set_mode(size)

        board = Board(screen, width, height, cell_count)  # создаем поле
        clock = pygame.time.Clock()
        board = Snake(screen, width, height, cell_count)

        running_game = True
        snake_run = False

        clock = pygame.time.Clock()
        ticks = 0
        speed = 110
        # speed_2 = 0

        self.c_dir = None
        self.l_dir = None
        self.len = 1
        self.body_coord = []

        self.head_cell = [0, 0]
        self.end_cell = [0, 0]

        while running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_game = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.sound.play()
                    if not self.body_coord:
                        board.get_click(event.pos)
                        #self.head_cell = list(board.get_cell(event.pos))
                        #self.end_cell = list(board.get_cell(event.pos))
                        #self.body_coord.append(list(board.get_cell(event.pos)))

                        self.head_cell = list(board.get_cell(event.pos))
                        self.end_cell = list(board.get_cell(event.pos))
                        self.body_coord.append(list(board.get_cell(event.pos), None))

                    '''else:
                        #self.end_cell = list(board.get_cell(event.pos))
                        #self.body_coord.append(list(board.get_cell(event.pos)))
                        self.len += 1
                    print(f'head {self.head_cell}')
                    print(f'end {self.end_cell}')
                    print(f'body {self.body_coord}')'''

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or
                        event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
                    snake_run = not snake_run

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                    if self.l_dir is None:
                        self.c_dir = "down"
                        self.l_dir = "down"
                        print(self.c_dir)
                    else:
                        if self.c_dir != "up":
                            self.c_dir = "down"

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                    if self.l_dir is None:
                        self.c_dir = "up"
                        self.l_dir = "up"
                    else:
                        if self.c_dir != "down":
                            self.c_dir = "up"

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                    if self.l_dir is None:
                        self.c_dir = "left"
                        self.l_dir = "left"
                    else:
                        if self.c_dir != "right":
                            self.c_dir = "left"

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                    if self.l_dir is None:
                        self.c_dir = "right"
                        self.l_dir = "right"
                    else:
                        if self.c_dir != "left":
                            self.c_dir = "right"

            screen.fill((0, 0, 0))
            board.render()
            if ticks >= speed:

                if snake_run:
                    board.next_move(self.head_cell, self.len, self.body_coord,
                                    cell_count, self.c_dir)
                    if self.c_dir == "right":
                        self.head_cell[1] += 1
                        self.end_cell[1] += 1
                    if self.c_dir == "left":
                        self.head_cell[1] -= 1
                        self.end_cell[1] -= 1
                    if self.c_dir == "up":
                        self.head_cell[0] -= 1
                        self.end_cell[0] -= 1
                    if self.c_dir == "down":
                        self.head_cell[0] += 1
                        self.end_cell[0] += 1
                tick = 0
            pygame.display.flip()
            clock.tick(100)
            ticks += 1
        pygame.quit()


class Snake(Board):
    def __init__(self, screen, width, height, cell_count=10):
        super().__init__(screen, width, height, cell_count)
        self.screen = screen

        self.cell_c = cell_count

    def render(self):
        for x in range(self.cell_c):
            for y in range(self.cell_c):
                if self.board[y][x] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("yellow"),
                                     (self.left + self.cell_size * x,
                                      self.top + self.cell_size * y,
                                      self.cell_size, self.cell_size))
                # отрисовываем решетку поля
                pygame.draw.rect(self.screen, pygame.Color("blue"),
                                 (self.left + self.cell_size * x,
                                  self.top + self.cell_size * y,
                                  self.cell_size, self.cell_size), 1)

    def next_move(self, head, len, body, cell, c_dir='right'):
        x_cd, y_cd = head
        temp = copy.deepcopy(self.board)  # сохраняем поле для дальнейшего изменения текущего

        self.c_dir = c_dir
        #print("step", self.c_dir)

        for x in range(self.width):
            for y in range(self.height):

                if -1 < y_cd < cell - 1 and -1 < x_cd < cell - 1:
                    if self.c_dir == "right" and temp[x_cd][y_cd + 1] == 0:
                        for i in range(len):

                            #print(temp[body[i][0]][body[i][1] + 1])
                            #print(temp[body[-1][0]][body[-1][1]])

                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0]][body[i][1] + 1] = 1
                        for j in range(len):
                            body[j][1] += 10

                    if self.c_dir == "left" and temp[x_cd][y_cd - 1] == 0:
                        for i in range(len):
                            #print(temp[body[i][0]][body[i][1] - 1])
                            #print(temp[body[-1][0]][body[-1][1]])

                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0]][body[i][1] - 1] = 1

                        for j in range(len):
                            body[j][1] -= 10

                    if self.c_dir == "up" and temp[x_cd - 1][y_cd] == 0:
                        for i in range(len):

                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0] - 1][body[i][1]] = 1
                        for j in range(len):
                            body[j][0] -= 10

                    if self.c_dir == "down" and temp[x_cd + 1][y_cd] == 0:
                        for i in range(len):
                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0] + 1][body[i][1]] = 1

                        for j in range(len):
                            body[j][0] += 10
    def if_we_have_apple(self):
        apple = Apple()

        self.board = copy.deepcopy(temp)

class Apple():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_pos = food_pos
        self.food_sizex = 20
        self.food_sizey = 20
        self.food_pos = [random.randrange(1, screen_width / 10) * 10, random.randrange(1, screen_height/10)*10]

    def draw_food(self):
        board = Board()
        pygame.draw.rect(board, self.food_color,
                         pygame.Rect(self.food_pos[0], self.food_pos[1],
                                     self.food_sizex, self.food_sizey))

def music():
    pygame.init()
    music_sp = ["music/melody_1.mp3", "music/melody_2.mp3",
                "music/melody_3.mp3", "music/melody_4.mp3"]
    pygame.mixer.music.load(random.choice(music_sp))
    pygame.mixer.music.play()


music()
start = StartWindow()
food = Food(game.brown, game.screen_width, game.screen_height)
while True: