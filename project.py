import pygame, os, random
import sys
import sqlite3
import random
import copy


all_sprites = pygame.sprite.Group()


class StartWindow:
    def __init__(self):
        global music_on
        super().__init__()
        pygame.init()

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('gadugi', 36)
        self.text1 = titl.render("One Little Warm", 1, (255, 20, 147))

        ask_input = pygame.font.SysFont('arial', 25)
        self.text2 = ask_input.render("Введите логин:", 1, (0, 49, 83))

        ex = False
        login = InputText(width // 2 - 70, height // 5 * 3 - 32, 140, 32, ex, (255, 20, 147))

        self.h_border = pygame.sprite.Group()
        self.v_border = pygame.sprite.Group()

        self.font = pygame.transform.scale(self.load_image('font_4.jpg'), (width, height))
        self.music = pygame.transform.scale(self.load_image('music_2.png', -1), (60, 60))


        clock = pygame.time.Clock()

        Border(5, 5, width - 5, 5, self)
        Border(5, height - 5, width - 5, height - 5, self)
        Border(5, 5, 5, height - 5, self)
        Border(width - 5, 5, width - 5, height - 5, self)

        for i in range(17):
            Bubble(5, 100, 100, self)

        run_st = True

        while run_st:
            if ex:
                run_st = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_st = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 5 <= event.pos[0] <= 65 and 5 <= event.pos[1] <= 65 and music_on:
                            pygame.mixer.music.pause()
                            music_on = False
                            continue
                        if 5 <= event.pos[0] <= 65 and 5 <= event.pos[1] <= 65 and not music_on:
                            pygame.mixer.music.unpause()
                            music_on = True
                    login.events(event)

            screen.blit(self.font, (0, 0))
            screen.blit(self.music, (5, 5))
            all_sprites.update()
            all_sprites.draw(screen)  # говорим прорисовывать sprites
            login.draw(screen)
            screen.blit(self.text1, (180, 60))
            screen.blit(self.text2, (220, 170))
            clock.tick(40)

            pygame.display.flip()
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

    def get_click(self, pos):
        print("here")


class Bubble(pygame.sprite.Sprite, StartWindow):
    def __init__(self, radius, x, y, par):
        super().__init__(all_sprites)

        self.par = par

        list = ["data/bubble_font_1.png", "data/bubble_font_2.png",
                "data/bubble_font_3.png",
                "data/bubble_font_4.png"]

        self.image = self.image = pygame.image.load(random.choice(list))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, self.par.h_border):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, self.par.v_border):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, par):
        super().__init__(all_sprites)

        self.par = par
        if x1 == x2:
            self.add(self.par.v_border)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(self.par.h_border)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class InputText:
    def __init__(self, x, y, width, height, ex, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.login_t = text
        self.color = color
        self.text_surf = pygame.font.Font(None, 32).render(text, True, (255, 20, 147))
        self.run_text = False
        self.exit = ex

        self.l = 0
        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound.play()
            if self.rect.collidepoint(event.pos):
                self.run_text = True
                self.color = (0, 49, 73)
            else:
                self.run_text = False
                self.color = (255, 20, 147)

        if event.type == pygame.KEYDOWN and self.run_text:
            if event.key == pygame.K_RETURN:
                self.open(self.login_t)
                self.login_t = ""
            elif event.key == pygame.K_BACKSPACE:
                self.login_t = self.login_t[:-1]
                if self.l != 1:
                    self.l -= 1
            else:
                if self.l <= 8:
                    self.login_t += event.unicode
                    self.l += 1
            self.text_surf = pygame.font.Font(None, 32).render(self.login_t, True, (255, 20, 147))

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

        pygame.draw.rect(screen, self.color, self.rect, 4)


class HaveLogin:
    def __init__(self, login):
        global music_on
        super().__init__()
        pygame.init()

        self.log = login
        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")

        self.font = pygame.transform.scale(load_image('font_2.jpg'),
                                           (width, height))
        self.music = pygame.transform.scale(load_image('music_2.png', -1),
                                            (60, 60))

        titl = pygame.font.SysFont('arial', 40)
        self.text1 = titl.render("Добро пожаловать,", 1, (153, 0, 102))

        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(login, 1, (112, 41, 99))

        act_open = pygame.font.SysFont("arial", 30, bold=True)
        self.text3 = act_open.render(f"Начать игру", 1, (189, 51, 164))

        act_chg = pygame.font.SysFont("arial", 30, bold=True)
        self.text4 = act_chg.render("Таблица рекордов", 1, (189, 51, 164))

        act_exit = pygame.font.SysFont("arial", 30, bold=True)
        self.text5 = act_exit.render("Сменить пользователя", 1, (189, 51, 164))

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

                        # выход к стартовому окну
                        run_havelog = False
                        StartWindow()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 5 <= event.pos[0] <= 65 and 5 <= event.pos[1] <= 65 and music_on:
                            pygame.mixer.music.pause()
                            music_on = False
                            continue
                        if 5 <= event.pos[0] <= 65 and 5 <= event.pos[1] <= 65 and not music_on:
                            pygame.mixer.music.unpause()
                            music_on = True

            if run_havelog:
                screen.blit(self.font, (0, 0))
                screen.blit(self.music, (5, 5))
                screen.blit(self.text1, (60, height // 8.3))
                screen.blit(self.text2, (420, height // 7.69))
                screen.blit(self.text3, (210, height // 2.94))
                screen.blit(self.text4, (165, height // 2.08))
                screen.blit(self.text5, (145, height // 1.61))
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

        self.font = pygame.transform.scale(load_image('font_2.jpg'), (width, height))
        self.music = pygame.transform.scale(load_image('music_2.png', -1), (60, 60))

        titl = pygame.font.SysFont('arial', 40)
        self.text1 = titl.render("Новый игрок,", 1, (153, 0, 102))


        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(login, 1, (112, 41, 99))

        act_open = pygame.font.SysFont("arial", 30, bold=True)
        self.text3 = act_open.render(f"Начать игру", 1, (189, 51, 164))

        act_chg = pygame.font.SysFont("arial", 30, bold=True)
        self.text4 = act_chg.render("Таблица рекордов", 1, (189, 51, 164))

        act_exit = pygame.font.SysFont("arial", 30, bold=True)
        self.text5 = act_exit.render("Сменить пользователя", 1, (189, 51, 164))

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
                    if 5 <= event.pos[0] <= 65 and 5 <= event.pos[
                        1] <= 65 and music_on:
                        pygame.mixer.music.pause()
                        music_on = False
                        continue
                    if 5 <= event.pos[0] <= 65 and 5 <= event.pos[
                        1] <= 65 and not music_on:
                        pygame.mixer.music.unpause()
                        music_on = True

            if run_nolog:
                screen.blit(self.font, (0, 0))
                screen.blit(self.music, (5, 5))
                screen.blit(self.text1, (60, height // 8.3))
                screen.blit(self.text2, (375, height // 7.69))
                screen.blit(self.text3, (210, height // 2.94))
                screen.blit(self.text4, (165, height // 2.08))
                screen.blit(self.text5, (145, height // 1.61))

                pygame.display.flip()

        pygame.quit()


class Menu:
    def __init__(self, log):
        global music_on
        super().__init__()
        pygame.init()

        self.login = log
        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        self.sound = pygame.mixer.Sound("music/click_sound_cut2.wav")
        text_before = pygame.font.SysFont("arial", 36)

        self.font = pygame.transform.scale(load_image('font_2.jpg'), (width, height))
        self.music = pygame.transform.scale(load_image('music_2.png', -1), (60, 60))

        titl = pygame.font.SysFont('arial', 40)
        self.titl = text_before.render("Перед началом игры", 1, (153, 0, 102))

        act_open = pygame.font.SysFont("arial", 30, bold=True)
        self.text3 = act_open.render(f"Начать игру", 1, (189, 51, 164))


        text_size = pygame.font.SysFont("arial", 25)
        self.t_size = text_size.render("Выберите размер поля :", 1, (189, 51, 164))

        size_10 = pygame.font.SysFont("colibri", 25)
        self.size_10 = size_10.render("10x10", 1, (112, 41, 99))

        size_20 = pygame.font.SysFont("colibri", 25)
        self.size_20 = size_20.render("15x15", 1, (112, 41, 99))

        size_30 = pygame.font.SysFont("colibri", 25)
        self.size_30 = size_30.render("20x20", 1, (112, 41, 99))

        text_mode = pygame.font.SysFont("arial", 25)
        self.t_mode = text_mode.render("Выберите режим игры :", 1, (189, 51, 164))

        mode_food = pygame.font.SysFont("colibri", 25)
        self.m_food = mode_food.render("еда", 1, (112, 41, 99))
        self.f_col = (223, 115, 255)

        mode_speed = pygame.font.SysFont("colibri", 25)
        self.m_speed = mode_speed.render("скорость", 1, (112, 41, 99))
        self.s_col = (223, 115, 255)

        mode_barrier = pygame.font.SysFont("colibri", 25)
        self.m_barrier = mode_barrier.render("препятствия", 1, (112, 41, 99))
        self.b_col = (223, 115, 255)

        text_character = pygame.font.SysFont("arial", 25)
        self.t_char = text_character.render("Выберите персонажа :", 1, (189, 51, 164))

        ch = pygame.font.SysFont("colibri", 30)
        self.ch = ch.render("Персонажи", 1, (112, 41, 99))

        play = pygame.font.SysFont("arial", 30)
        self.play = play.render("Играть", 1, (112, 41, 99))

        board_size = ''

        self.list_mode = [[(255, 20, 147), 3], [(255, 20, 147), 3], [(255, 20, 147), 3]]
        self.list_size = [[(83, 26, 80), 3], [(83, 26, 80), 3], [(83, 26, 80), 3]]

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

                        self.list_size[0] = [(162, 162, 208), 0]
                        self.list_size[1], self.list_size[2] = [(255, 20, 147), 3],[(255, 20, 147), 3]

                    if 265 <= event.pos[0] <= 335 and 165 <= event.pos[1] <= 215:
                        # print(15)
                        board_size = 15

                        self.list_size[1] = [(162, 162, 208), 0]
                        self.list_size[0], self.list_size[2] = [(255, 20, 147), 3], [(255, 20, 147), 3]

                    if 430 <= event.pos[0] <= 500 and 165 <= event.pos[1] <= 215:
                        #print(20)
                        board_size = 20

                        self.list_size[2] = [(162, 162, 208), 0]
                        self.list_size[1], self.list_size[0] = [(255, 20, 147), 3], [(255, 20, 147), 3]

                    if 90 <= event.pos[0] <= 210 and 295 <= event.pos[1] <= 345:

                        if "препятствия" not in self.game_mode:
                            self.game_mode.append("препятствия")
                            self.list_mode[0] = [(162, 162, 208), 0]
                        else:
                            self.game_mode.pop(self.game_mode.index("препятствия"))
                            self.list_mode[0] = [(255, 20, 147), 3]
                        #print(self.game_mode)
                        #print("barrier")

                        # game_mode = "препятствия"

                    if 240 <= event.pos[0] <= 360 and 295 <= event.pos[1] <= 345:

                        if "скорость" not in self.game_mode:
                            self.game_mode.append("скорость")
                            self.list_mode[1] = [(162, 162, 208), 0]
                        else:
                            self.game_mode.pop(self.game_mode.index("скорость"))
                            self.list_mode[1] = [(255, 20, 147), 3]
                        #print(self.game_mode)
                        #print("speed")

                        #game_mode = "скорость"

                    if 390 <= event.pos[0] <= 510 and 295 <+ event.pos[1] <= 345:

                        if "еда" not in self.game_mode:
                            self.game_mode.append("еда")
                            self.list_mode[2] = [(162, 162, 208), 0]
                        else:
                            self.game_mode.pop(self.game_mode.index("еда"))
                            self.list_mode[2] = [(255, 20, 147), 3]

                        #print(self.game_mode)
                        #print("food")

                        game_mode = "еда"

                    if 350 <= event.pos[0] <= 540 and 370 <= event.pos[1] <= 400:
                        print("barrier menu")
                        #Character(self.login)

                    if 40 <= event.pos[0] <= 560 and 420 <= event.pos[1] <= 475:
                        print("play")
                        #Game(self.login, self.game_mode, board_size)

                    if 5 <= event.pos[0] <= 65 and 5 <= event.pos[1] <= 65 and music_on:
                        pygame.mixer.music.pause()
                        music_on = False
                        continue

                    if 5 <= event.pos[0] <= 65 and 5 <= event.pos[1] <= 65 and not music_on:
                        pygame.mixer.music.unpause()
                        music_on = True

            if run_menu is True:
                screen.blit(self.font, (0, 0))
                screen.blit(self.music, (5, 5))
                for i in range(3):
                    pygame.draw.rect(screen, self.list_size[i][0],
                                     (100 + i * 165, 165, 70, 50), self.list_size[i][1])

                    screen.blit(self.size_list[i], (110 + i * 165, 180))

                    pygame.draw.rect(screen, self.list_mode[i][0],
                                     (90 + i * 150, 295, 120, 50 ),
                                     self.list_mode[i][1])
                    screen.blit(self.mode_list[i], (100 + i * 166, 310))

                screen.blit(self.titl, (width // 4.28, height // 10))   # (140, 50)
                screen.blit(self.t_size, (width // 12, height // 4.16))   # (50, 120)
                screen.blit(self.t_mode, (width // 12, height // 2))   # (50, 250)
                screen.blit(self.t_char, (width // 12, height // 1.315))   # (50, 380)
                pygame.draw.rect(screen, (112, 41, 99),
                                 (width // 1.71, height // 1.35, width // 3.15,
                                  height // 12.5), 3)   # (350, 370, 190, 60)
                screen.blit(self.ch, (width // 1.538, height // 1.315))   # (390, 380)
                screen.blit(self.play, (width // 2.3, height // 1.162))   # (260, 430)
                pygame.draw.rect(screen, (112, 41, 99),
                                 (width // 15, height // 1.19, width // 1.153,
                                  height // 9), 3)   # (40, 420, 520, 55)

                pygame.display.flip()
        pygame.quit()



music_on = True

class Board:
    # создание поля
    def __init__(self, screen, width, height, cell_count=10):

        self.width = width
        self.height = height
        # значения по умолчанию
        self.cell_size = 30  # (width - 120) // cell_count; width // int(cell_count)
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
                        # self.head_cell = list(board.get_cell(event.pos))
                        # self.end_cell = list(board.get_cell(event.pos))
                        # self.body_coord.append(list(board.get_cell(event.pos)))

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

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Snake():
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
        # print("step", self.c_dir)

        for x in range(self.width):
            for y in range(self.height):

                if -1 < y_cd < cell - 1 and -1 < x_cd < cell - 1:
                    if self.c_dir == "right" and temp[x_cd][y_cd + 1] == 0:
                        for i in range(len):
                            # print(temp[body[i][0]][body[i][1] + 1])
                            # print(temp[body[-1][0]][body[-1][1]])

                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0]][body[i][1] + 1] = 1
                        for j in range(len):
                            body[j][1] += 1

                    if self.c_dir == "left" and temp[x_cd][y_cd - 1] == 0:
                        for i in range(len):
                            # print(temp[body[i][0]][body[i][1] - 1])
                            # print(temp[body[-1][0]][body[-1][1]])

                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0]][body[i][1] - 1] = 1

                        for j in range(len):
                            body[j][1] -= 1

                    if self.c_dir == "up" and temp[x_cd - 1][y_cd] == 0:
                        for i in range(len):
                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0] - 1][body[i][1]] = 1
                        for j in range(len):
                            body[j][0] -= 1

                    if self.c_dir == "down" and temp[x_cd + 1][y_cd] == 0:
                        for i in range(len):
                            temp[body[-1][0]][body[-1][1]] = 0
                            temp[body[i][0] + 1][body[i][1]] = 1

                        for j in range(len):
                            body[j][0] += 1


        self.board = copy.deepcopy(temp)

class Bomb(pygame.sprite.Sprite):
    board = Board()
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)

class GetApples():
    def __init__(self):
        pass


def music():
    pygame.init()
    music_sp = ["music/melody_1.mp3", "music/melody_2.mp3",
                "music/melody_3.mp3", "music/melody_4.mp3"]
    pygame.mixer.music.load(random.choice(music_sp))
    pygame.mixer.music.play()


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

music_play = music()
start = StartWindow()
snake = Snake()




# меню с настройками #
# карта для перехода между режимами игры
