from pygame import *
import random
window = display.set_mode(    (800, 800)   )
clock = time.Clock()

init()
game = True

background = transform.scale(
    image.load('galaxy.jpg'), (window.get_width(), window.get_height())
)
def draw_background():
    window.blit(background, (0,0))


class GameSprite(sprite.Sprite):                                                #### !!!!!!!!!
    # init - функція конструктор (вона створює екземпляри класу)
    def __init__(self, filename, x, y, width=50, height=50, speed=0):

        super().__init__()  # викликати ініт супер-класу                        #### !!!!!!!!!

        # завантажити текстуру картинки і змінити її розмір
        self.image = transform.scale(
            image.load(filename), (width, height)
        )
        self.rect = self.image.get_rect()  # get_rect - створює хітбокс розміру картинки
        # задаю кординати хітбоксу
        self.rect.x, self.rect.y = x, y  # одночасне присвоювання
        # self.rect.x = x
        # self.rect.y = y те ж саме, але одним рядком
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def update(self):
        # отримати словник кнопок, які натиснуті
        pressed_keys = key.get_pressed()
        if pressed_keys[K_a]:
            self.rect.x -= self.speed  # до кординати додати швидкість
        if pressed_keys[K_d]:
            self.rect.x += self.speed  # до кординати додати швидкість

'''
    1. Зробити клас UFO (з супер-класом GameSprite)
    2. Зробити метод update, в якому просто переміщувати персонажа вниз
    (додавати до у якесь значення)
    3. Створити 3 об'єкти НЛО і використати метод update в ігровому циклі
    Результат вашої роботи: Коли запускається гра 3 НЛОшки летять згори вниз
'''
class UFO(GameSprite):

    def update(self):
        # рухає нло вниз
        self.rect.y += self.speed
        if self.rect.y > window.get_height(): # якщо кординати НЛОшки більша висоту вікна
            # пропадає
            self.kill() # знищити себе

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= self.speed

def label(text, size, label_font, color, x, y):
    # Створити шрифт
    new_font = font.SysFont(label_font, size)
    # На основі шрифта створити текст
    text = new_font.render(text, True, color)
    # намалювати текст
    window.blit(text, (x, y))

rocket = Player('rocket.png', 500, 700, height=80, speed=5)   # і в циклі малювати!

game_score = 0

ufos = sprite.Group() # створити групу спрайтів
bullets = sprite.Group()


run = True
lifes = 3
while game:
    if run == True:
        # якщо життів не залишилось - запуск гри - False
        if lifes < 1:
            run = False
        # поки уфошок у групі менше 7
        while len(ufos) < 7:
            # створюю уфошку з випадковою кординатою x в межах вікна
            new_ufo = UFO('ufo.png', random.randint(0, window.get_width() - 100), -100, 100, 50, 1)
            ufos.add(new_ufo)

        # event.get() - отримати події
        # for e in event.get() - для кожної події, яка зараз відбувається
        for e in event.get():
            # якщо тип події - вийти
            if e.type == QUIT:
                game = False  # завершити цикл

            if e.type == KEYDOWN: # якщо тип події - клавішу опустили
                if e.key == K_SPACE: # якщо ця клавіша space
                    bullets.add(
                        Bullet('bullet.png', rocket.rect.x, rocket.rect.y, 10, 30, 5)
                    )

        ufos.update() # група спрайтів - оновитись
        rocket.update()
        bullets.update()                            ### НЕ ЗАБУДЬТЕ ОНОВИТИ
        # Клік по функції і Ctrl+B
        interaction = sprite.groupcollide(bullets, ufos, True, True)
        for bullet in interaction:
            game_score += len(interaction[bullet])

        inter1 = sprite.spritecollide(rocket, ufos, True) # якщо ракета торкнулась уфошок - знищити уфо
        if len(inter1) > 0:
            lifes -= 1
        draw_background()
        ufos.draw(window)
        rocket.draw()
        bullets.draw(window)                            ### НЕ ЗАБУДЬТЕ МАЛЮВАТИ
        # \n - перенос рядка
        label("Рахунок: " + str(game_score), 40, "Montserrat", (255,255,255), 620, 50)
        label("Життя: " + str(lifes), 40, "Montserrat", (255, 255, 255), 40, 50)
        '''
        Задача до кінця уроку - зробити життя, щоб спочатку було 3, потім 2, потім 1, коли монстри 
        проходять вниз
        '''
    else:
        for e in event.get():
            # якщо тип події - вийти
            if e.type == QUIT:
                game = False  # завершити цикл
        label('You lose', 60, 'Algerian', 200, 200)
    display.update()
    clock.tick(60)

