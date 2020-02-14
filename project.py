import pygame, os, random
import sys
import sqlite3
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
        login = InputText(width // 2 - 70, height // 5 * 3 - 32, 140, 32, ex)

        self.h_border = pygame.sprite.Group()
        self.v_border = pygame.sprite.Group()

        self.font = pygame.transform.scale(load_image('font_4.jpg'), (width, height))
        self.music = pygame.transform.scale(load_image('music_2.png', -1), (60, 60))


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
    def __init__(self, x, y, width, height, ex, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.login_t = text
        self.color = (255, 20, 147)
        self.text_surf = pygame.font.Font(None, 32).render(text, True, self.color)
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
                else:
                    if self.l <= 9:
                        self.login_t += event.unicode
                        self.l += 1
                self.text_surf = pygame.font.Font(None, 32).\
                    render(self.login_t, True, (255, 20, 147))

    def open(self, login_t):
        self.id_login = self.cur.execute("""SELECT id FROM logins
                                            WHERE login == ?""",
                                         (login_t,)).fetchall()
        print(self.id_login)
        if self.id_login != []:
            self.l, = self.id_login[0]

            # self.have_login = HaveLogin(login_t)
            self.exit = True
        else:
            # self.no_login = NoLogin(login_t)
            self.exit = True

    def update(self):
        width = max(200, self.text_surf.get_width() + 8)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.text_surf, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.color, self.rect, 4)


music_on = True


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


# меню с настройками #
# карта для перехода между режимами игры
