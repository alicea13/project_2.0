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

                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 353:
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

                    if 160 <= event.pos[0] <= 450 and 160 <= event.pos[1] <= 353:
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
        def __init__(self):
            super().__init__()
            pygame.init()

            size = width, height = 600, 500
            screen = pygame.display.set_mode(size)

            text_before = pygame.font.SysFont('arial', 36)
            self.titl = text_before.render("Перед началом игры", 1,
                                           pygame.Color("blue"))

            text_size = pygame.font.SysFont("arial", 25)
            self.t_size = text_size.render("Выберите размер поля", 1,
                                           pygame.Color("blue"))

            size_10 = pygame.font.SysFont("colibri", 25)
            self.size_10 = size_10.render("10x10", 1, pygame.Color("lightblue"))

            run_menu = True

            while run_menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_menu = False
                screen.blit(self.titl, (100, 60))
            pygame.quit()


start = StartWindow()


# меню с настройками
# карта для перехода между режимами игры
