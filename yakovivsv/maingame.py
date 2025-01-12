from pygame import *
from random import randint


font.init()
font2 = font.Font(None, 36)
lose = font2.render('YOU LOSE!', True, (255, 0, 0))
win = font2.render('YOU WIN!', True, (0, 255, 0))


score = 0
lost = 0
# фонова музика
#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')



# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас головного гравця
class Player(GameSprite):


    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet("skibidi.jpg",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.x += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.x >=700 :
            self.rect.x = 0
            self.rect.y = randint(80, 400)
            lost = lost + 1
class Enemy2(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.x <=0 :
            self.rect.x = 700
            self.rect.y = randint(80, 400)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y<0:
            self.kill()



# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("opo.jpg"), (win_width, win_height))


# створюємо спрайти
ship = Player("shovelmet.png", 5, win_height - 100, 80, 100, 10)
monsters2 = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(1,6):
    m = Enemy ("orelb.png",5, randint(80,300), 80,50,randint(1,5))
    monsters.add(m)
for i in range(1,6):
    m2 = Enemy2 ("yxxtimoha.png",700, randint(80,300), 80,50,randint(1,5))
    monsters2.add(m2)




# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False


# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна


while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                



    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))

        text = font2.render("Рахунок: "+ str(score),1,(255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render("Пропущено: "+ str(lost),1,(255,255,255))
        window.blit(text_lose, (10,50))


        # рухи спрайтів
        ship.update()
        monsters2.update()
        monsters.update()
        bullets.update()


        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        monsters2.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides2 = sprite.groupcollide(monsters2, bullets, True, True)
        for c in collides:
            score +=1
            m = Enemy ("orelb.png",randint(80,620), -40, 80,50,randint(1,5))
            monsters.add(m)
        for c in collides2:
            score +=1
            m2 = Enemy2 ("yxxtimoha.png",randint(80,620), -40, 80,50,randint(1,5))
            monsters2.add(m2)

        if sprite.spritecollide(ship,monsters,False) or lost >= 3:
            finish = True
            window.blit(lose, (200,200))
        if sprite.spritecollide(ship,monsters2,False) or lost >= 3:
            finish = True
            window.blit(lose, (200,200))
        if score >= 10:
            finish = True
            window.blit(win, (200,200))


        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)
                