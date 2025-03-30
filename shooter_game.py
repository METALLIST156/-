from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('Kolda')
background = transform.scale(image.load('galaxy.jpg'),(700,500))
width = 700
height = 500
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
font.init()
font2 = font.SysFont('Arial', 36)
score = 0
lost = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def go(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width - 50:
            self.rect.x += self.speed
    def attack(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

hero = Player('rocket.png', 10, height - 100, 40, 80, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
FPS = 60
clock = time.Clock()
game = True
finish = False
font1 = font.SysFont('Arial',60)
win = font1.render('Ай кросавчег дарагой', True, (98, 65, 94))
lose = font1.render('АХХАХ ЛОШАРА УХХУХУ', True, (98, 65, 94))
bullets = sprite.Group()
max_enemy = 30  
max_collide = 1
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                hero.attack()
    if not finish:
        window.blit(background, (0,0))
        text = font2.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        hero.reset()
        monsters.draw(window)
        monsters.update()
        hero.go()
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(hero, monsters, False) or lost >= 15  :
            finish = True
            window.blit(lose, (200,200))
        if score >= max_enemy:
            finish = True
            window.blit(win, (200,200))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy('ufo.png', randint(80, width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster) 
    clock.tick(FPS)
