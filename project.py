import pygame, os, random
import sys
import sqlite3


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

        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()


    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        size = width, height = 600, 500
        screen = pygame.display.set_mode(size)

        titl = pygame.font.SysFont('arial', 36)
        self.text1 = titl.render("Добро ожаловать,", 1, pygame.Color("blue"))

        log = pygame.font.SysFont('colibri', 50)
        self.text2 = log.render(login, 1, pygame.Color('lightblue'))   # login.rjust((width - 435) % 8, " ")

        act_open = pygame.font.SysFont("arial", 25)
        self.text3 = act_open.render(f"Начать игру", 1, pygame.Color("lightblue"))

        act_chg = pygame.font.SysFont("arial", 25)
        self.text4 = act_chg.render("Таблица рекордов", 1, pygame.Color("lightblue"))

        act_exit = pygame.font.SysFont("arial", 25)
        self.text5 = act_exit.render("Сменить пользователя", 1,
                                    pygame.Color("lightblue"))

        run_havelog = True

        while run_havelog:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_havelog = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 213:
                        print("game")

                        # открытие окна меню
                        # Menu()

                        # run_havelog = False
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 283:
                        print("record")
                        # вывод топ 10 (?)
                        # Record()

                    if 160 <= event.pos[0] <= 450 and 300 <= event.pos[1] <= 353:
                        print("back")

                        # выход к стартовому окну
                        StartWindow()
                        run_havelog = False
            screen.fill((30, 30, 30))
            for i in range(3):
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (160, 160 + i * 70, 290, 53), 3)

            screen.blit(self.text1, (width // 6, height // 8.3))   # (100, 60)
            screen.blit(self.text2, (width // 1.379, height // 7.69))   # (435, 65)
            screen.blit(self.text3, (width // 2.6, height // 2.94))   # (230, 170)
            screen.blit(self.text4, (width // 3, height // 2.08))   # (200, 240)
            screen.blit(self.text5, (width // 3.42, height // 1.61))   # (175, 310)
            pygame.display.flip()


class NoLogin:
    def __init__(self, login):
        super().__init__()
        pygame.init()

        self.log = login
        self.con = sqlite3.connect("one_little_worm.db")
        self.cur = self.con.cursor()

        self.log_app = self.cur.execute("""INSERT INTO logins(login) VALUES(?)""", (self.log,))
        # self.main_app = self.cur.execute("""INSERT INTO Main(login) VALUES("me")""", (self.log,))
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
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 213:
                        print("game")

                        # открытие окна меню
                        # Menu()

                        # run_nolog = False
                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 283:
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

            text_before = pygame.font.SysFont("arial", 36)
            self.titl = text_before.render("Перед началом игры", 1,
                                           pygame.Color("blue"))

            text_size = pygame.font.SysFont("arial", 25)
            self.t_size = text_size.render("Выберите размер поля :", 1,
                                           pygame.Color("lightblue"))

            size_10 = pygame.font.SysFont("colibri", 25)
            self.size_10 = size_10.render("10x10", 1, pygame.Color("lightblue"))

            size_20 = pygame.font.SysFont("colibri", 25)
            self.size_20 = size_20.render("15x15", 1, pygame.Color("lightblue"))

            size_30 = pygame.font.SysFont("colibri", 25)
            self.size_30 = size_30.render("20x20", 1, pygame.Color("lightblue"))

            text_mode = pygame.font.SysFont("arial", 25)
            self.t_mode = text_mode.render("Выберите режим игры :", 1,
                                           pygame.Color("lightblue"))

            mode_food = pygame.font.SysFont("colibri", 25)
            self.m_food = mode_food.render("еда", 1, pygame.Color("lightblue"))
            self.f_col = "yellow"

            mode_speed = pygame.font.SysFont("colibri", 25)
            self.m_speed = mode_speed.render("скорость", 1,
                                             pygame.Color("lightblue"))
            self.s_col = "yellow"

            mode_barrier = pygame.font.SysFont("colibri", 25)
            self.m_barrier = mode_barrier.render("препятствия", 1,
                                                 pygame.Color("lightblue"))
            self.b_col = "yellow"

            text_character = pygame.font.SysFont("arial", 25)
            self.t_char = text_character.render("Выберите персонажа :", 1,
                                                pygame.Color("lightblue"))

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

                        if 100 <= event.pos[0] <= 170 and 165 <= event.pos[
                            1] <= 215:
                            # print(10)
                            board_size = 10

                            self.list_size[0] = ["yellow", 0]
                            self.list_size[1], self.list_size[2] = ["blue",
                                                                    3], ["blue",
                                                                         3]

                        if 265 <= event.pos[0] <= 335 and 165 <= event.pos[
                            1] <= 215:
                            # print(15)
                            board_size = 15

                            self.list_size[1] = ["yellow", 0]
                            self.list_size[0], self.list_size[2] = ["blue",
                                                                    3], ["blue",
                                                                         3]

                        if 430 <= event.pos[0] <= 500 and 165 <= event.pos[
                            1] <= 215:
                            # print(20)
                            board_size = 20

                            self.list_size[2] = ["yellow", 0]
                            self.list_size[1], self.list_size[0] = ["blue",
                                                                    3], ["blue",
                                                                         3]

                        if 90 <= event.pos[0] <= 210 and 295 <= event.pos[
                            1] <= 345:

                            if "препятствия" not in self.game_mode:
                                self.game_mode.append("препятствия")
                                self.list_mode[0] = ["yellow", 0]
                            else:
                                self.game_mode.pop(
                                    self.game_mode.index("препятствия"))
                                self.list_mode[0] = ["blue", 3]
                            # print(self.game_mode)
                            # print("barrier")

                            # game_mode = "препятствия"

                        if 240 <= event.pos[0] <= 360 and 295 <= event.pos[
                            1] <= 345:

                            if "скорость" not in self.game_mode:
                                self.game_mode.append("скорость")
                                self.list_mode[1] = ["yellow", 0]
                            else:
                                self.game_mode.pop(
                                    self.game_mode.index("скорость"))
                                self.list_mode[1] = ["blue", 3]
                            # print(self.game_mode)
                            # print("speed")

                            # game_mode = "скорость"

                        if 390 <= event.pos[0] <= 510 and 295 < + event.pos[
                            1] <= 345:

                            if "еда" not in self.game_mode:
                                self.game_mode.append("еда")
                                self.list_mode[2] = ["yellow", 0]
                            else:
                                self.game_mode.pop(self.game_mode.index("еда"))
                                self.list_mode[2] = ["blue", 3]

                            # print(self.game_mode)
                            # print("food")

                            game_mode = "еда"

                        if 350 <= event.pos[0] <= 540 and 390 <= event.pos[
                            1] <= 450:
                            print("barrier menu")
                            # Character()

                        if 40 <= event.pos[0] <= 560 and 420 <= event.pos[
                            1] <= 475:
                            print("play")
                            Game(self.login, self.game_mode, board_size)

                screen.fill((0, 0, 0))
                for i in range(3):
                    pygame.draw.rect(screen, pygame.Color(self.list_size[i][0]),
                                     (100 + i * 165, 165, 70, 50),
                                     self.list_size[i][1])

                    screen.blit(self.size_list[i], (110 + i * 165, 180))

                    pygame.draw.rect(screen, pygame.Color(self.list_mode[i][0]),
                                     (90 + i * 150, 295, 120, 50),
                                     self.list_mode[i][1])
                    screen.blit(self.mode_list[i], (100 + i * 166, 310))

                screen.blit(self.titl,
                            (width // 4.28, height // 10))  # (140, 50)
                screen.blit(self.t_size,
                            (width // 12, height // 4.16))  # (50, 120)
                screen.blit(self.t_mode,
                            (width // 12, height // 2))  # (50, 250)
                screen.blit(self.t_char,
                            (width // 12, height // 1.315))  # (50, 380)
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (width // 1.71, height // 1.35, width // 3.15,
                                  height // 12.5), 3)  # (350, 370, 190, 60)
                screen.blit(self.ch,
                            (width // 1.538, height // 1.315))  # (390, 380)
                screen.blit(self.play,
                            (width // 2.3, height // 1.162))  # (260, 430)
                pygame.draw.rect(screen, pygame.Color("blue"),
                                 (width // 15, height // 1.19, width // 1.153,
                                  height // 9), 3)  # (40, 420, 520, 55)

                pygame.display.flip()
            pygame.quit()


start = StartWindow()


# меню с настройками
# карта для перехода между режимами игры
