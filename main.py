from asyncio import constants
import pygame, random, math, json
 
pygame.init()
pygame.font.init()
pygame.mixer.init()

scrn_w = 1920
scrn_h = 1080

my_font = pygame.font.SysFont('Comic Sans MS', 30)

spawnRate = 60     #interval before enemies spawn
spawnDelay = 0    #Initial delay before spawning

enemiesR0 = []
enemiesR1 = []
enemiesR2 = []
enemiesR3 = []

dirR0 = random.choice([1, -1])
dirR1 = random.choice([1, -1])
dirR2 = random.choice([1, -1])
dirR3 = random.choice([1, -1])

pygameNumKeys = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
    pygame.K_0
]

explosions = []
rawExplosionSprites = []
for x in range(12):
    rawExplosionSprites.append(pygame.image.load("assets/sprites/explosion"+str(x)+".png"))

class Stage():
    def __init__(self):
        self.background = pygame.image.load("assets/sprites/background.png")
        self.enemyCap = 10
        self.toSpawn = 10
        self.spawned = 0
        self.stageEnd = 300
        self.enemyProgression = 0
        self.level = 1
        self.bossDead = False
        self.changeText = my_font.render("Stage "+str(self.level), True, (255, 255, 255))
        self.enemies = []
        self.test = False
        self.shop = Shop()
        self.title = Title()

        #music
        pygame.mixer.music.load("assets/audio/background.wav")#
        pygame.mixer.music.set_volume(0.1)#
        pygame.mixer.music.play(-1)# 
    

    def advance(self):
        self.level += 1
        self.enemyCap = 5+math.ceil(self.level**.5)*5
        self.toSpawn = 9+self.level
        self.spawned = 0
        self.shop.active = True
        self.stageEnd = 300
        self.changeText = my_font.render("Stage "+str(self.level), True, (255, 255, 255))

        # boss rewards
        if self.level%5 == 0:
            Enemy.hpMulti += 0.5
            player.moneyMulti += 0.1

        # unlock enemies
        if self.level >= 6:
            self.enemyProgression = 4
        elif self.level >= 3:
            self.enemyProgression = 3
        elif self.level >= 2:
            self.enemyProgression = 2

    def spawnBoss(self):
        bossTypes = [InsurgentCarrier()]
        self.enemies.append(random.choice(bossTypes.copy()))

    def paused(self):
        screen.blit(self.background, (0,0))

        for enemy in range(len(self.enemies)):
            self.enemies[enemy].draw()
    
    def update(self):
        global titleActive
        screen.blit(self.background, (0,0))
        

        if self.title.active:
            self.title.update()
        elif self.shop.active:
            self.shop.update()
        elif self.stageEnd > 0:
            self.stageEnd -= 1
            screen.blit(self.changeText, self.changeText.get_rect(center = screen.get_rect().center))
        elif len(self.enemies) == 0 and self.spawned >= self.toSpawn:
            if self.level%5 == 0:
                if self.bossDead:
                    self.advance()
                else:
                    self.spawnBoss()
            else:
                self.bossDead = False
                self.advance()
        else:
            for enemy in self.enemies:
                enemy.update()

class ShopButton():
    def __init__(self, item, details, x=0, y=0, width=0, height=0):
        self.item = item
        self.details = details
        self.rect = pygame.Rect(x, y, width, height)

    def isLocked(self):
        return self.details[5]
    
    def isMaxed(self):
        return self.details[0] >= self.details[1] and self.details[1] > 0

    def display(self):
        if self.isLocked():
            pygame.draw.rect(screen, (220, 220, 220), self.rect)
            screen.blit(my_font.render(self.item, True, (0, 0, 0)), self.rect)
            screen.blit(my_font.render("Locked", True, (0, 0, 0)), self.rect.center)
        elif self.isMaxed():
            pygame.draw.rect(screen, (220, 220, 220), self.rect)
            screen.blit(my_font.render(self.item, True, (0, 0, 0)), self.rect)
            screen.blit(my_font.render("Lv. MAX", True, (0, 0, 0)), self.rect.copy().move(350, 50))
        elif player.money < self.details[2]:
            pygame.draw.rect(screen, (220, 220, 220), self.rect)
            screen.blit(my_font.render(self.item, True, (0, 0, 0)), self.rect)
            screen.blit(my_font.render('$'+str(int(self.details[2]))[:-2]+'.'+str(int(self.details[2]))[-2:], True, (0, 0, 0)), (self.rect.x, self.rect.centery))
            if self.details[1] == -1:
                screen.blit(my_font.render("Lv. "+str(self.details[0]), True, (0, 0, 0)), self.rect.copy().move(350,50))
            else:
                screen.blit(my_font.render("Lv. "+str(self.details[0])+'/'+str(self.details[1]), True, (0, 0, 0)), self.rect.copy().move(350, 50))
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
            screen.blit(my_font.render(self.item, True, (0, 0, 0)), self.rect)
            screen.blit(my_font.render('$'+str(int(self.details[2]))[:-2]+'.'+str(int(self.details[2]))[-2:], True, (0, 0, 0)), (self.rect.x, self.rect.centery))
            if self.details[1] == -1:
                screen.blit(my_font.render("Lv. "+str(self.details[0]), True, (0, 0, 0)), self.rect.copy().move(350,50))
            else:
                screen.blit(my_font.render("Lv. "+str(self.details[0])+'/'+str(self.details[1]), True, (0, 0, 0)), self.rect.copy().move(350, 50))

class ButtonCarousel():
    def __init__(self, x, y, width, height, *buttons):
        self.rect = pygame.Rect(x, y, width, height)
        self.lBut = pygame.Rect(self.rect.x, self.rect.y, self.rect.height/5, self.rect.height)
        self.rBut = pygame.Rect(self.rect.x+self.rect.width-self.rect.height/5, self.rect.y, self.rect.height/5, self.rect.height)
        self.buttons = []
        x += height/2.5
        for button in buttons:
            button.rect.left = x
            button.rect.top = y
            button.rect.width = height*5
            button.rect.height = height
            self.buttons.append(button)
            x+=height*26/5

    def scroll(self, direction):
        if direction not in [-1, 1]:
            print("ERROR: ButtonCarousel scroll requires direction -1 or 1")
        for button in self.buttons:
            button.rect.x += self.rect.height*5*direction
    
    def display(self):
        pygame.draw.rect(screen, (220, 220, 220), self.lBut)
        pygame.draw.rect(screen, (220, 220, 220), self.rBut)
        for button in self.buttons:
            if self.rect.left+self.rect.height/5 <= button.rect.left and self.rect.right-self.rect.height/5 >= button.rect.right:
                button.display()

class Shop():
    def __init__(self):
        self.active = False
        self.items = {# name = [level, max, price, price scaling[liner, exponential, ...], scaling start level[linear, exponential, ...], locked]
            "Upgrade Laser Cannon Damage": [1, -1, 1500, [500, 1.2, 1.01], [0, 0, 3], False],
            "Upgrade Laser Cannon Cooldown": [1, 9, 3000, [0, 1.5, 1.03], [0, 0, 3], False],
            "Upgrade Laser Cannon Velocity": [1, 11, 500, [100, 1.1], [0, 0], False],
            "Buy Laser Beam": [0, 1, 10000, [], [], False],
            "Upgrade Laser Beam Damage": [0, -1, 10000, [5000, 1.2, 1.07], [0, 0, 3], True],
            "Upgrade Laser Beam Duration": [0, 11, 100000, [0, 2], [0, 0], True],
            "Buy Bomb": [0, 1, 30000, [], [], True],
            "Upgrade Bomb Damage": [0, -1, 10000, [5000, 1.2, 1.07], [0, 0, 3], True],
            "Upgrade Bomb Cooldown": [0, 11, 50000, [0, 1.5, 1.1], [0, 0, 5], True],
            "Upgrade Shield Regen Speed": [1, 10, 10000, [0, 1.5, 1.1], [0, 0, 3], True]
        }

        self.buttons = []

        self.cannonCarousel = ButtonCarousel(150, 200, scrn_w-300, 100,
            ShopButton("Upgrade Laser Cannon Damage", self.items["Upgrade Laser Cannon Damage"]),
            ShopButton("Upgrade Laser Cannon Cooldown", self.items["Upgrade Laser Cannon Cooldown"]),
            ShopButton("Upgrade Laser Cannon Velocity", self.items["Upgrade Laser Cannon Velocity"])
        )
        for button in self.cannonCarousel.buttons:
            self.buttons.append(button)

        self.laserCarousel = ButtonCarousel(150, 350, scrn_w-300, 100,
            ShopButton("Buy Laser Beam", self.items["Buy Laser Beam"]),
            ShopButton("Upgrade Laser Beam Damage", self.items["Upgrade Laser Beam Damage"]),
            ShopButton("Upgrade Laser Beam Duration", self.items["Upgrade Laser Beam Duration"])
        )
        for button in self.laserCarousel.buttons:
            self.buttons.append(button)

        self.bombCarousel = ButtonCarousel(150, 500, scrn_w-300, 100,
            ShopButton("Buy Bomb", self.items["Buy Bomb"]),
            ShopButton("Upgrade Bomb Damage", self.items["Upgrade Bomb Damage"]),
            ShopButton("Upgrade Bomb Cooldown", self.items["Upgrade Bomb Cooldown"])
        )
        for button in self.bombCarousel.buttons:
            self.buttons.append(button)

        self.shieldCarousel = ButtonCarousel(150, 650, scrn_w-300, 100,
            ShopButton("Upgrade Shield Regen Speed", self.items["Upgrade Shield Regen Speed"])
        )
        for button in self.shieldCarousel.buttons:
            self.buttons.append(button)

        self.carousels = [
            self.cannonCarousel,
            self.laserCarousel,
            self.bombCarousel,
            self.shieldCarousel
        ]

        self.itemKeys = [
            "Upgrade Laser Cannon Damage",
            "Upgrade Laser Cannon Cooldown",
            "Upgrade Laser Cannon Velocity",
            "Buy Laser Beam",
            "Upgrade Laser Beam Damage",
            "Upgrade Laser Beam Duration",
            "Buy Bomb",
            "Upgrade Bomb Damage",
            "Upgrade Bomb Cooldown",
            "Upgrade Shield Regen Speed"
        ]
        self.clickToggle = False

    def buy(self, button):
        if not (button.isLocked() or button.isMaxed() or button.details[2] > player.money):
            print(button.item)
            upgrade = button.details
            player.money -= int(upgrade[2])
            for scale in range(len(upgrade[4])):
                if upgrade[0] > upgrade[4][scale]:
                    if scale == 0:
                        upgrade[2] += upgrade[3][0]
                    elif scale == 1:
                        upgrade[2] = upgrade[2] * upgrade[3][1]
                    elif scale == 2:
                        upgrade[2] = upgrade[2] ** upgrade[3][2]
                else:
                    break
            if button.item == "Upgrade Laser Cannon Damage":
                Bullet.damage += min(0.25, Bullet.damage**-0.9)
            elif button.item == "Upgrade Laser Cannon Cooldown":
                player.bullet_firerate -= 10
            elif button.item == "Upgrade Laser Cannon Velocity":
                player.bulletSpeed += 3
            elif button.item == "Buy Laser Beam":
                player.unlockedWeapons.append("Laser Beam")
                self.items["Upgrade Laser Beam Damage"][0] = 1
                self.items["Upgrade Laser Beam Duration"][0] = 1
            elif button.item == "Upgrade Laser Beam Damage":
                Laser.damage += 0.01
            elif button.item == "Upgrade Laser Beam Duration":
                player.laserDuration += 50
            elif button.item == "Buy Bomb":
                self.items["Upgrade Bomb Damage"][0] = 1
                self.items["Upgrade Bomb Cooldown"][0] = 1
                player.unlockedWeapons.append("Bomb")
            elif button.item == "Upgrade Bomb Damage":
                Bomb.damage += 0.5
            elif button.item == "Upgrade Bomb Cooldown":
                player.bomb_firerate -= 100
            elif button.item == "Upgrade Shield Regen Speed":
                player.shieldRegenSpeed = math.ceil(500*0.95**upgrade[0])

    def display(self):
        self.cannonCarousel.display()
        self.laserCarousel.display()
        self.bombCarousel.display()
        self.shieldCarousel.display()
        continue_text = my_font.render("Press ENTER to Continue", False, (255, 255, 255))
        screen.blit(continue_text, (screen.get_width()/2 - continue_text.get_width()/2, 3*screen.get_height()/4))

    def detectClick(self):
        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and not self.clickToggle:
            self.clickToggle = True
            for button in self.buttons:
                if button.rect.collidepoint(pos):
                    self.buy(button)
            for carousel in self.carousels:
                if carousel.lBut.collidepoint(pos):
                    carousel.scroll(-1)
                elif carousel.rBut.collidepoint(pos):
                    carousel.scroll(1)
        elif not mouse[0]:
            self.clickToggle = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.active = False
        self.detectClick()
        self.display()

class Title():
    def __init__(self):
        self.active = True
        self.titleFont = pygame.font.Font("assets/fonts/IshimuraRegular.otf", 108)
        self.contFont = pygame.font.Font("assets/fonts/IshimuraRegular.otf", 44)

    def display(self):
        title = self.titleFont.render("Space Force", True, (249,4,5))
        cont = self.contFont.render("Press ENTER to Play!", True, (255, 255, 255))
        quit_text = my_font.render("Press Q to Exit", False, (255, 255, 255))

        with open('hs.json', 'r') as f:
            hs = json.loads(f.read())["highscore"]
        highscore_text = my_font.render(f"Highscore: {hs}", False, (255, 255, 255))
        
        tW = title.get_rect().width
        contW = cont.get_rect().width
        contH = cont.get_rect().height
        screen.blit(title, (960-(tW//2),25))

        screen.blit(cont, (960-(contW//2), 540 - (contH//2)))

        screen.blit(quit_text, (960-(quit_text.get_width()//2), screen.get_height() - 50))

        screen.blit(highscore_text, (screen.get_width()-highscore_text.get_width() - 30, screen.get_height() - highscore_text.get_height() - 20))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.active = False
        self.display()

class Entity():
    def __init__(self):
        self.dead = False

class Player(Entity):
    playerSprite = pygame.image.load("assets/sprites/player.png")
    shieldSprite = pygame.image.load("assets/sprites/shield.png")
    width = playerSprite.get_width()
    height = playerSprite.get_height()
    shieldWidth = shieldSprite.get_width()
    shieldHeight = shieldSprite.get_height()

    #sfx
    laserSound = pygame.mixer.Sound("assets/audio/laser.wav")
    laserSound.set_volume(0.2)
    bulletSound = pygame.mixer.Sound("assets/audio/bullet.wav")
    shipHit = pygame.mixer.Sound("assets/audio/ship_hit.wav")
    shipHit.set_volume(0.3)
    shieldHit = pygame.mixer.Sound("assets/audio/shield_hit.wav")
    shieldHit.set_volume(0.2)
    reloadSound = pygame.mixer.Sound("assets/audio/reloaded.wav")
    reloadSound.set_volume(0.1)
    shieldBreak = pygame.mixer.Sound("assets/audio/shield_break.wav")
    shieldBreak.set_volume(0.5)
    shipExplode = pygame.mixer.Sound("assets/audio/explosion.wav")
    shipExplode.set_volume(0.5)
    regenSound = pygame.mixer.Sound("assets/audio/shield_regen.wav")
    regenSound.set_volume(0.3)
    gameLose = pygame.mixer.Sound("assets/audio/lose.wav")
    gameLose.set_volume(0.5)

    def __init__(self):
        super().__init__()
        self.coords = [25, (scrn_h-Player.height)/2]
        self.hp = 3
        self.shield = 5
        self.shieldMax = 5
        self.shieldRegenSpeed = 500
        self.shieldTimer = 0
        self.speed = 3
        self.bulletCD = 0
        self.bullet_firerate = 200
        self.laserCD = 0
        self.laser_firerate = 1000
        self.laserTime = 0
        self.laserDuration = 300
        self.bombCD = 0
        self.bomb_firerate = 1500
        self.bullets = []
        self.bombs = []
        self.bulletSpeed = 20
        self.bulletDistance = scrn_w*3/4
        self.bombDistance = 1450
        self.bombRadius = 200
        self.weapon = 0
        self.unlockedWeapons = ["Laser Cannon"]
        self.invTime = 0
        self.money=0
        self.moneyMulti = 1
        self.score = 0

    def getWeapon(self):
        return self.weapon

    def switchWeapon(self, slot):
        self.weapon = slot
        if self.weapon < 0:
            self.weapon = len(self.unlockedWeapons)-1
        elif self.weapon >= len(self.unlockedWeapons):
            self.weapon = 0

    def shoot(self):
        if self.unlockedWeapons[self.weapon] == "Laser Cannon":
            if self.bulletCD <= 0:
                self.bullets.append(Bullet(self.coords.copy(), self.bulletSpeed, 0))
                self.bulletCD = self.bullet_firerate
                Player.bulletSound.play()
        elif self.unlockedWeapons[self.weapon] == "Laser Beam":
            if self.laserCD <= 0 and self.laserTime < self.laserDuration:
                self.bullets.append(Laser(self.coords.copy(), 0))
                self.laserTime += 1
                Player.laserSound.play()
            elif self.laserTime >= self.laserDuration:
                self.laserCD = self.laser_firerate
                self.laserTime = 0
                Player.laserSound.fadeout(300)
        elif self.unlockedWeapons[self.weapon] == "Bomb":
            if self.bombCD <= 0:
                self.bombs.append(Bomb(self.coords.copy(), self.bombDistance, self.bombRadius, 0))
                self.bombCD = self.bomb_firerate
                Player.bulletSound.play()

    def collide(self, other):
        if isinstance(other, Enemy) and not self.invTime:
            self.invTime = 20
            if self.shield:
                self.shield -= 1
                x_offset = random.randrange(-25, 25)
                y_offset = 0
                explosions.append([50, [0, other.coords[0] + x_offset, other.coords[1] + y_offset]])
                if self.shield == 0:
                    Player.shieldBreak.play()
                else:
                    Player.shieldHit.play()

            else:
                self.hp -= 1
                x_offset = random.randrange(-25, 25)
                y_offset = 0
                explosions.append([50, [0, other.coords[0] + x_offset, other.coords[1] + y_offset]])
                if self.hp == 0:
                    Player.shipExplode.play()
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    Player.gameLose.play()
                    
                    #highscore
                    with open('hs.json', 'r') as f:
                        hs = json.loads(f.read())

                    if hs['highscore'] < player.score:
                        with open('hs.json', 'w') as f:
                            f.write(json.dumps({"highscore": player.score}))

                else:
                    Player.shipHit.play()

            if self.shield <= 0:
                self.shieldTimer = self.shieldRegenSpeed * -1
    
    def regenShield(self):
        if self.shield < self.shieldMax:
            self.shieldTimer += 1
        if self.shieldTimer >= self.shieldRegenSpeed:
            self.shield += 1
            Player.regenSound.play()
            self.shieldTimer = 0

    def earn(self, amt):
        self.money += amt*self.moneyMulti
        self.score += amt*self.moneyMulti

    def update(self, shopactive):
        screen.blit(Player.playerSprite, self.coords)
        
        if not shopactive: #only regen shield and reload weapons if not in shop menu
            self.regenShield()

            if self.bulletCD > 0 :
                self.bulletCD -= 1
                if self.bulletCD == 0:
                    Player.reloadSound.play()
            if self.laserCD > 0:
                self.laserCD -= 1
                if self.laserCD == 0:
                    Player.reloadSound.play()
            if self.bombCD > 0:
                self.bombCD -= 1
                if self.bombCD == 0:
                    Player.reloadSound.play()
            if self.invTime > 0:
                self.invTime -= 1

        if self.shield > 0:
            screen.blit(Player.shieldSprite, [self.coords[0]-(Player.shieldWidth-Player.width)/2, self.coords[1]-(Player.shieldHeight-Player.height)/2])
        for bullet in self.bullets:
            bullet.update()
        for bomb in self.bombs:
            bomb.update()
            if bomb.dead:
                self.bombs.remove(bomb)

    def paused(self):
        screen.blit(Player.playerSprite, self.coords)
        if self.shield > 0:
            screen.blit(Player.shieldSprite, [self.coords[0]-(Player.shieldWidth-Player.width)/2, self.coords[1]-(Player.shieldHeight-Player.height)/2])

        for bullet in self.bullets:
            bullet.draw()

class PlayerProjectile(Entity):
    def __init__(self, coords, speed, angle):
        super().__init__()
        self.coords = coords
        self.speed = speed
        self.angle = angle

    def move(self):
        self.coords[0] += math.cos(self.angle)*self.speed
        self.coords[1] += math.sin(self.angle)*self.speed
        if self.coords[0] > scrn_w:
            self.dead = True

class Bullet(PlayerProjectile):
    sprite = pygame.image.load("assets/sprites/player_bullet.png")
    width = sprite.get_width()
    height = sprite.get_height()
    damage = 1

    def __init__(self, coords, speed, angle):
        super().__init__(coords, speed, angle)
    
    def collide(self, other):
        if isinstance(other, Enemy) and not isinstance(other, EnemyProjectile):
            self.dead = True

    def update(self):
        self.move()
        screen.blit(Bullet.sprite, self.coords)
    
    def draw(self):
        screen.blit(Bullet.sprite, self.coords)

class Laser(PlayerProjectile):
    baseSprite = pygame.image.load("assets/sprites/laser_base.png")
    sprite = pygame.image.load("assets/sprites/laser.png")
    width = sprite.get_width()
    height = sprite.get_height()
    baseOffsetY = (baseSprite.get_height()-height)/2
    damage = 0.05

    def __init__(self, coords, angle, speed=sprite.get_width()):
        super().__init__([coords[0]+player.width*5/7, coords[1]+(player.height-Laser.height)/2], speed, angle)
    
    def collide(self, other):
        if isinstance(other, Enemy) and not isinstance(other, EnemyProjectile):
            self.dead = True

    def update(self):
        self.move()
        if self.coords != [player.coords[0]+player.width*5/7+Laser.width, player.coords[1]+(player.height-Laser.height)/2]:
            screen.blit(Laser.sprite, self.coords)
        else:
            screen.blit(Laser.baseSprite, [self.coords[0], self.coords[1]-Laser.baseOffsetY])

    def draw(self):
        if self.coords != [player.coords[0]+player.width*5/7+Laser.width, player.coords[1]+(player.height-Laser.height)/2]:
            screen.blit(Laser.sprite, self.coords)
        else:
            screen.blit(Laser.baseSprite, [self.coords[0], self.coords[1]-Laser.baseOffsetY])

class Bomb(PlayerProjectile):
    sprite = pygame.image.load("assets/sprites/bomb.png")                                                      #change this
    width = sprite.get_width()
    height = sprite.get_height()
    bombExplosionSprites = rawExplosionSprites.copy()
    damage = 5
    
    def __init__(self, coords, bombDistance, radius, angle):
        super().__init__(coords, None, angle)
        self.fuse = 400
        self.timer = 0
        self.speed = bombDistance/200
        self.radius = radius
        self.explosionSprites = []
        for e in range(12):
            self.explosionSprites.append(pygame.transform.scale(pygame.image.load("assets/sprites/explosion"+str(e)+".png"), (radius*2, radius*2)))

    def move(self):
        self.coords[0] += self.speed
        if self.speed > 0:
            self.coords[0] += math.cos(self.angle)*self.speed
            self.coords[1] += math.sin(self.angle)*self.speed
            self.speed -= 0.04
        elif self.speed != 0:
            self.speed = 0

    def explode(self):
        screen.blit(self.explosionSprites[int(self.explosions[0])], (self.explosions[1], self.explosions[2]))
        self.explosions[0] += 0.25

    def update(self):
        self.timer += 1
        if self.timer <= self.fuse:
            self.move()
            screen.blit(self.sprite, self.coords)
            if self.timer == self.fuse:
                self.explosions = [0, self.coords[0]+self.width/2-self.radius, self.coords[1]+self.height/2-self.radius]
                for enemy in stage.enemies:
                    if isinstance(enemy, Fleet):
                        for member in enemy.fleetMembers:
                            if circ_rect_collide(self.coords, self.radius, member.sprite.get_rect()):
                                member.hp -= self.damage
                                if member.hp <= 0:
                                    member.dead = True
                                    enemy.memberCount -= 1
                                    player.earn(member.bounty)
                                    enemy.fleetMembers.remove(member)
                        if enemy.memberCount == 0:
                            enemy.dead = True
                            player.earn(enemy.bounty)
                            stage.enemies.remove(enemy)
                    elif not isinstance(enemy, EnemyProjectile):
                        if circ_rect_collide(self.coords, self.radius, enemy.sprite.get_rect()):
                            enemy.hp -= self.damage
                            if enemy.hp <= 0:
                                enemy.dead = True
                                player.earn(enemy.bounty)
                                stage.enemies.remove(enemy)
        elif self.timer > self.fuse+36:# add 12 / what is added to self.explosions[0] in self.explode()
            self.dead = True
        else:
            self.explode()

class Enemy(Entity):
    hpMulti = 1
    shipExplode = pygame.mixer.Sound("assets/audio/explosion.wav")
    shipExplode.set_volume(0.5)
    spawnMargin = 25 #Closest 2 ships can spawn (Only affects CargoShips and Blue turrets)
    def __init__(self):
        super().__init__()

    def positionChooser(self, type):
        global enemiesR0, enemiesR1, enemiesR2, enemiesR3, dirR0, dirR1, dirR2, dirR3

        if type == "CargoShip":
            self.w = CargoShip.width
            self.h = CargoShip.height
        elif type == "Fighter":
            self.w = Fighter.width
            self.h = Fighter.height

        iteration = 0
        while True:
            overlap = False
            POS = [random.choice([950, 1200, 1200, 1450, 1450, 1700, 1700]), random.randint(scrn_h/2-CargoShip.height*5, scrn_h/2+CargoShip.height*4)]
            if iteration > 100: #If overcrowded ignore overlaping
                break
            if POS[0] == 950 and len(enemiesR0) > 0:
                for x in enemiesR0:
                    if not (POS[1]+self.h+Enemy.spawnMargin < x.coords[1] or POS[1] > x.coords[1]+x.h+Enemy.spawnMargin):
                        overlap = True
            elif POS[0] == 1200 and len(enemiesR1) > 0:
                for x in enemiesR1:
                    if not (POS[1]+self.h+Enemy.spawnMargin < x.coords[1] or POS[1] > x.coords[1]+x.h+Enemy.spawnMargin):
                        overlap = True
            elif POS[0] == 1450:
                for x in enemiesR2:
                    if not (POS[1]+self.h+Enemy.spawnMargin < x.coords[1] or POS[1] > x.coords[1]+x.h+Enemy.spawnMargin):
                        overlap = True
            elif POS[0] == 1700:
                for x in enemiesR3:
                    if not (POS[1]+self.h+Enemy.spawnMargin < x.coords[1] or POS[1] > x.coords[1]+x.h+Enemy.spawnMargin):
                        overlap = True
            if overlap == False:
                break
                
            iteration += 1

        if POS[0] == 950:
            enemiesR0.append(self)
        elif POS[0] == 1200:
            enemiesR1.append(self)
        elif POS[0] == 1450:
            enemiesR2.append(self)
        else:
            enemiesR3.append(self)

        direction = random.choice([-1,1])

        return POS, direction

    def move(self):
        global enemiesR0, enemiesR1, enemiesR2, enemiesR3, dirR0, dirR1, dirR2, dirR3


        if self in enemiesR0:
            if self.coords[1] <= 0:
                dirR0 = 1
            elif self.coords[1] > scrn_h-100:
                dirR0 = -1
            self.coords[1] += dirR0*CargoShip.speed
        elif self in enemiesR1:
            if self.coords[1] <= 0:
                dirR1 = 1
            elif self.coords[1] > scrn_h-100:
                dirR1 = -1
            self.coords[1] += dirR1*CargoShip.speed
        elif self in enemiesR2:
            if self.coords[1] <= 0:
                dirR2 = 1
            elif self.coords[1] > scrn_h-100:
                dirR2 = -1
            self.coords[1] += dirR2*CargoShip.speed
        else:
            if self.coords[1] <= 0:
                dirR3 = 1
            elif self.coords[1] > scrn_h-100:
                dirR3 = -1
            self.coords[1] += dirR3*CargoShip.speed

class CargoShip(Enemy):
    sprite = pygame.image.load("assets/sprites/cargo_ship.png")
    bounty = 100
    speed = 1
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self):
        super().__init__()
        self.coords, self.direction = self.positionChooser("CargoShip")
        self.hp = 1*Enemy.hpMulti


    def collide(self, other):
        if isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True
            Enemy.shipExplode.play()
      
    def update(self):
        self.move()
        screen.blit(CargoShip.sprite, self.coords)
    
    def draw(self):
        screen.blit(CargoShip.sprite, self.coords)

class Fighter(Enemy):
    sprite = pygame.image.load("assets/sprites/insurgent_fighter.png")
    bounty = 200
    speed = 0.5
    firerate = 300
    width = sprite.get_width()
    height = sprite.get_height()
    bulletSound = pygame.mixer.Sound("assets/audio/enemy_shoot.wav")
    bulletSound.set_volume(0.08)#idk too loud

    def __init__(self):
        super().__init__()
        self.coords, self.direction = self.positionChooser("Fighter")
        self.cooldown = Fighter.firerate
        self.hp = 3*Enemy.hpMulti

    def shoot(self):
        if self.cooldown <= 0:
            Fighter.bulletSound.play()
            stage.enemies.append(EnemyBullet([self.coords[0], self.coords[1]+(Fighter.height-EnemyBullet.height)/2]))
            self.cooldown = Fighter.firerate
    
    def collide(self, other):
        if isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True
                Enemy.shipExplode.play()
    
    def update(self):
        self.cooldown -= 1
        self.move()
        self.shoot()
        screen.blit(Fighter.sprite, self.coords)
    
    def draw(self):
        screen.blit(Fighter.sprite, self.coords)

class EnemyProjectile(Enemy):
    def __init__(self, coords):
        super().__init__()
        self.coords = coords
    
    def collide(self, other):
        if isinstance(other, Player):
            self.dead = True

class EnemyBullet(EnemyProjectile):
    sprite = pygame.image.load("assets/sprites/EnemyBullet.png")
    speed = 10
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self, coords):
        super().__init__(coords)
    
    def move(self):
        self.coords[0] -= EnemyBullet.speed
        if self.coords[0] <= 0-EnemyBullet.width:
            self.dead = True
    
    def update(self):
        self.move()
        screen.blit(EnemyBullet.sprite, self.coords)

    def draw(self):
        screen.blit(EnemyBullet.sprite, self.coords)

class KamikazeSpacecraft(Enemy):
    sprite = pygame.transform.scale(pygame.image.load("assets/sprites/kamikaze_spacecraft.png"), (50, 50))
    bounty = 250
    speed = 10
    width = sprite.get_width()
    height = sprite.get_height()
    prepTime = 500

    def __init__(self):
        super().__init__()
        self.coords = [random.randint(scrn_w/2, scrn_w*3/4), random.randint(100, scrn_h-100)]
        self.time = KamikazeSpacecraft.prepTime
        self.hp = 0.5*Enemy.hpMulti
    
    def move(self):
        if(self.time > 0):
            self.angle = math.atan((self.coords[1]-player.coords[1])/(self.coords[0]-player.coords[0]))
            self.coords[0] += KamikazeSpacecraft.speed/100
        else:
            self.coords[0] -= math.cos(self.angle)*KamikazeSpacecraft.speed
            self.coords[1] -= math.sin(self.angle)*KamikazeSpacecraft.speed
            if self.coords[0] <= 0-KamikazeSpacecraft.width:
                self.dead = True

    def collide(self, other):
        if isinstance(other, Player):
            self.hp = 0
            self.dead = True
            Enemy.shipExplode.play()
        elif isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True

    def update(self):
        if self.time:
            self.time -= 1
        self.move()
        screen.blit(KamikazeSpacecraft.sprite, self.coords)
    
    def draw(self):
        screen.blit(KamikazeSpacecraft.sprite, self.coords)

class Fleet(Enemy):
    bounty = 250
    speed = 1

    def __init__(self):
        super().__init__()
        self.coords = [scrn_w, random.randint(0, ConvoyShip.height*5)]
        self.fleetMembers = [
            ConvoyShip([self.coords[0]+ConvoyShip.width*2, self.coords[1]]),
            ConvoyShip([self.coords[0]+ConvoyShip.width, self.coords[1]+ConvoyShip.height]),
            ConvoyShip([self.coords[0], self.coords[1]+ConvoyShip.height*2]),
            ConvoyShip([self.coords[0]+ConvoyShip.width, self.coords[1]+ConvoyShip.height*3]),
            ConvoyShip([self.coords[0]+ConvoyShip.width*2, self.coords[1]+ConvoyShip.height*4])
        ]
        for member in self.fleetMembers:
            member.speed = self.speed
        self.memberCount = len(self.fleetMembers)
        self.bountyMsg = my_font.render("Wipe out the insurgent convoy to claim a large bounty!", True, (255, 255, 255))
    
    def move(self):
        self.coords[0] -= self.speed
        if self.coords[0] + ConvoyShip.width*3 < 0:
            for member in self.fleetMembers:
                self.fleetMembers.remove(member)
            self.dead = True
    
    def update(self):
        if len(self.fleetMembers) <= 0:
            self.dead = True
            if self.memberCount <= 0:
                player.earn(Fleet.bounty)
            return
        screen.blit(self.bountyMsg, (screen.get_rect().centerx - self.bountyMsg.get_width()/2, self.bountyMsg.get_height()*2))
        self.move()
        for member in self.fleetMembers:
            if member.dead:
                self.fleetMembers.remove(member)
                continue
            member.update()

    def draw(self):
        if len(self.fleetMembers) <= 0:
            self.dead = True
            if self.memberCount <= 0:
                player.earn(Fleet.bounty)
            return
    
        for member in self.fleetMembers:
            if member.dead:
                self.fleetMembers.remove(member)
                continue
            member.draw()

class ConvoyShip(Enemy):
    sprite = pygame.image.load("assets/sprites/convoy_ship.png")
    bounty = 20
    speed = 1
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self, coords):
        super().__init__()
        self.hp = 1*Enemy.hpMulti
        self.coords = coords

    def move(self):
        self.coords[0] -= self.speed

    def collide(self, other):
        if isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True
        elif isinstance(other, Player):
            self.hp = 0
            self.dead = True
            Enemy.shipExplode.play()
    
    def update(self):
        self.move()
        screen.blit(ConvoyShip.sprite, self.coords)
    
    def draw(self):
        screen.blit(ConvoyShip.sprite, self.coords)

class Boss(Enemy):
    bounty = 10000

    def __init__(self):
        super().__init__()
        self.bounty *= stage.level/5

    def collide(self, other):
        if isinstance(other, PlayerProjectile):
            self.hp -= other.damage
            if self.hp <= 0:
                self.dead = True
                stage.bossDead = True

class InsurgentCarrier(Boss):
    sprite = pygame.image.load("assets/sprites/insurgent_carrier.png")                                                                         #change this
    firerate = 100
    suicide_firerate = 500
    speed = 0.5
    width = sprite.get_width()
    height = sprite.get_height()
    bulletSound = pygame.mixer.Sound("assets/audio/enemy_shoot.wav")
    bulletSound.set_volume(0.08)#idk too loud

    def __init__(self):
        super().__init__()
        self.coords = [(scrn_w-InsurgentCarrier.width)*4/5, (scrn_h-InsurgentCarrier.height)/2]
        self.hp = 20*Enemy.hpMulti
        self.cooldown = InsurgentCarrier.firerate
        self.suicideCooldown = InsurgentCarrier.suicide_firerate
        self.direction = random.choice([-1,1])
        self.bossBar = Bar(self.coords[0], self.coords[1], InsurgentCarrier.sprite.get_width(), 13, "", maxval=self.hp, color=(255, 0, 0))

    def move(self):
        if self.coords[1] <= 0:
            self.direction = 1
        elif self.coords[1] >= scrn_h-InsurgentCarrier.height:
            self.direction = -1
        self.coords[1] += self.direction*InsurgentCarrier.speed

    def shoot(self):
        if self.cooldown <= 0:
            InsurgentCarrier.bulletSound.play()
            stage.enemies.append(EnemyBullet([self.coords[0], self.coords[1]+(InsurgentCarrier.height-InsurgentCarrier.height)/2]))
            self.cooldown = InsurgentCarrier.firerate
        if self.suicideCooldown <= 0:
            stage.enemies.append(KamikazeSpacecraft())
            self.suicideCooldown = InsurgentCarrier.suicide_firerate
    
    def update(self):
        self.cooldown -= 1
        self.suicideCooldown -= 1
        self.move()
        self.shoot()
        screen.blit(InsurgentCarrier.sprite, self.coords)

        self.bossBar.update(self.hp)
        self.bossBar.x = self.coords[0]
        self.bossBar.y = self.coords[1]+InsurgentCarrier.sprite.get_height()+25
        self.bossBar.display()
    
    def draw(self):
        screen.blit(InsurgentCarrier.sprite, self.coords)

        self.bossBar.display()

class Bar():
    def __init__(self, xpos, ypos, width, height, title, maxval=10, notch=False, color=(0,255,0)):
        super().__init__()
        self.value = 0
        self.maxvalue = maxval
        self.w = width
        self.h = height
        self.x = xpos
        self.y = ypos
        self.title = title
        self.notch = notch
        self.color = color

    def display(self):
        if stage.title.active:
            return
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, (self.value/self.maxvalue)*self.w,self.h))
        barText = my_font.render(self.title, True, (255, 255, 255))
        screen.blit(barText, (self.x+self.w+15, self.y - 5))

        if (self.notch):
            for x in range(self.maxvalue):
                pygame.draw.line(screen, (0, 0, 0), (self.x+(x*(self.w/self.maxvalue)), self.y), (self.x+(x*(self.w/self.maxvalue)), self.y+self.h))
   
    def update(self, val):
        self.value = val

def main():
    global screen, stage, player

    paused = False

    running = True
    
    frametime = pygame.time.Clock()

    pygame.display.set_icon(pygame.image.load("assets/sprites/icon.png"))
    pygame.display.set_caption("Space Invaders")
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN|pygame.SCALED)

    stage = Stage()
     
    player = Player()

    ##########
    health_bar = Bar(15, 10, 100, 35, "Health", maxval=player.hp, notch=True, color=(255, 0, 0))
    shield_bar = Bar(15, 55, 100, 35, "Shield", maxval=player.shieldMax, notch=True, color=(30, 50, 255))   
    cooldown_bar = Bar(250, 10, 100, 35, "Cooldown")
    ##########

    # death screen vars
    death_font = pygame.font.SysFont('Comic Sans MS', 300)
    death_text = death_font.render("Game Over!", False, (200, 0, 0))
    score_text = my_font.render("Score: "+str(player.score), False, (255, 255, 255))
    score_text.set_alpha(0)
    deathLoc = -death_font.get_height()
    deathVel = 1
    deathAcc = 0.1
    deathBounce = 0
    # main loop
    while running:
        if stage.test:# put code for testing here
            player.money += 100
            if stage.level < 8:
                stage.level = 8
            pass

        screen.fill((0,0,0)) #Clears the screen

        if paused:
            stage.paused()
            player.paused()
        else:
            stage.update()
            player.update(stage.shop.active)

        health_bar.update(player.hp)
        shield_bar.update(player.shield)

        if player.getWeapon() == 0:
            cooldown_bar.update(cooldown_bar.maxvalue-(player.bulletCD/player.bullet_firerate)*cooldown_bar.maxvalue)

        elif player.getWeapon() == 1:
            if player.laserTime > 0:
                cooldown_bar.update(cooldown_bar.maxvalue-((player.laserTime)/player.laserDuration)*cooldown_bar.maxvalue)
            else:
                cooldown_bar.update(cooldown_bar.maxvalue-(player.laserCD/player.laser_firerate)*cooldown_bar.maxvalue)

        elif player.getWeapon() == 2:
            cooldown_bar.update(cooldown_bar.maxvalue-(player.bombCD/player.bomb_firerate)*cooldown_bar.maxvalue)


        health_bar.display()
        shield_bar.display()
        cooldown_bar.display()
        renderHUD(frametime.get_fps())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                player.switchWeapon(player.getWeapon()+event.y*-1)

        keys = pygame.key.get_pressed()

        if player.hp <= 0:
            paused = True
            backdrop = pygame.Surface((screen.get_width(), screen.get_height()))
            backdrop.set_alpha(120)
            backdrop.fill((0, 0, 0))
            screen.blit(backdrop, (0,0))

            screen.blit(death_text, (screen.get_width()/2 - death_text.get_width()/2, deathLoc))

            if deathBounce > 5:
                screen.blit(score_text, (screen.get_width()/2 - score_text.get_width()/2, screen.get_height()/2 + death_text.get_height()/2))
                score_text.set_alpha(min(254,score_text.get_alpha()+1))

                exit_text = my_font.render("Press E to Return to Main Menu", False, (255, 255, 255))
                screen.blit(exit_text, (screen.get_width()/2 - exit_text.get_width()/2, screen.get_height()/2 + death_text.get_height()/2 + score_text.get_height() + 30))

                if keys[pygame.K_e]:
                    stage = Stage()
                    player = Player()
                    paused = False

            else:
                score_text = my_font.render("Score: "+str(player.score), False, (255, 255, 255))
                score_text.set_alpha(0)
                deathLoc += deathVel
                if deathLoc < screen.get_height()/2 - death_text.get_height()*3/5:
                    deathVel += deathAcc
                else:
                    deathVel *= -0.5
                    deathBounce += 1

                if keys[pygame.K_RETURN]:
                    return

        elif not paused:
            
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.coords[1] - (Player.shieldHeight-Player.height)/2 > 0:
                player.coords[1] -= player.speed
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.coords[1] + (Player.shieldHeight-Player.height/2) < scrn_h:
                player.coords[1] += player.speed

            for num in range(len(pygameNumKeys)):
                if keys[pygameNumKeys[num]]:
                    player.switchWeapon(num)

            if keys[pygame.K_SPACE]:
                player.shoot()
            elif player.getWeapon() == 1 and player.laserTime != player.laserDuration and player.laserTime != 0:
                    player.laserCD = math.floor(player.laser_firerate * max(0.5, player.laserTime / player.laserDuration))
                    player.laserTime = 0
                    Player.laserSound.fadeout(300)

            if keys[pygame.K_ESCAPE]:
                paused = True
                
            if keys[pygame.K_UP] and keys[pygame.K_DOWN] and keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] and keys[pygame.K_b] and keys[pygame.K_a] and not stage.test:
                stage.test = True
                print("=========TESTING=========")
            
            if keys[pygame.K_q] and stage.title.active:
                running = False

            enemyCore(stage.enemies)
            playerBulletCore()
            explosionCore(explosions)

        else:
            backdrop = pygame.Surface((screen.get_width(), screen.get_height()))
            backdrop.set_alpha(120)
            backdrop.fill((0, 0, 0))
            screen.blit(backdrop, (0,0))

            text = my_font.render('Press ENTER to Resume', False, (255, 255, 255))
            subtext = my_font.render('Press E to Exit to Main Menu', False, (255, 255, 255))
            screen.blit(text, (screen.get_width()/2 - text.get_width()/2, screen.get_height()/2))
            screen.blit(subtext, (screen.get_width()/2 - subtext.get_width()/2, screen.get_height()/2 + text.get_height() + 15))

            if keys[pygame.K_RETURN]:
                paused = False
            
            if keys[pygame.K_e]:
                stage = Stage()
                player = Player()
                paused = False
            
        
        pygame.display.flip()
        frametime.tick(120)

def explosionCore(explosions):
    if len(explosions) != 0:
        for y in explosions:
            explosionSprites = []
            for sprite in rawExplosionSprites:
                explosionSprites.append(pygame.transform.scale(sprite, (y[0]*1.5, y[0]*1.5)))
            x = y[1]
            if x[0] % 2 == 0:
                h = explosionSprites[x[0]//2].get_height()
                screen.blit(explosionSprites[x[0]//2], (x[1] + 50, x[2] - h/2))
            x[0] += 1
            if x[0] > 22:
                explosions.remove(y)

def playerBulletCore():
    for x in player.bullets:
        x.update()

        if x.dead:
            player.bullets.remove(x)
            continue

        for ship in stage.enemies:
            if not isinstance(ship, EnemyProjectile) and not isinstance(ship, Fleet):
                if ship.coords[0] <= x.coords[0] + x.width and ship.coords[0] + ship.width >= x.coords[0] and ship.coords[1] <= x.coords[1] + x.height and ship.coords[1] + ship.height >= x.coords[1]:          #detects bullet collision
                    ship.collide(x)
                    x.collide(ship)

                    x_offset = random.randrange(-25, 25)
                    y_offset = 0
                    if ship.dead:
                        player.earn(ship.bounty)
                        stage.enemies.remove(ship)
                        try:
                            if ship.width > ship.height:
                                    explosions.append([ship.width,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                            else:
                                    explosions.append([ship.height,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                        except:
                            explosions.append([100,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                    else:
                        explosions.append([50, [0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                    
                    if x.dead:
                        try:
                            player.bullets.remove(x)
                        except ValueError:
                            pass
                    break
            
            elif isinstance(ship, Fleet):
                for member in ship.fleetMembers:
                    if member.coords[0] <= x.coords[0] + x.width and member.coords[0] + member.width >= x.coords[0] and member.coords[1] <= x.coords[1] + x.height and member.coords[1] + member.height >= x.coords[1]:          #detects bullet collision
                        member.collide(x)
                        x.collide(member)

                        x_offset = random.randrange(-25, 25)
                        y_offset = 0

                        if member.dead:
                            player.earn(member.bounty)
                            ship.memberCount -= 1
                            try:
                                if ship.width > ship.height:
                                    explosions.append([ship.width,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                                else:
                                    explosions.append([ship.height,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                            except:
                                explosions.append([100,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                        else:
                            explosions.append([50,[0, x.coords[0] + x_offset, x.coords[1] + y_offset]])
                        
                        if x.dead:
                            try:
                                player.bullets.remove(x)
                            except ValueError:
                                pass
                        break

def enemyCore(enemies):
    global spawnRate
    global spawnDelay
    if stage.shop.active or stage.title.active:
        return
    numEnemies = 0
    if spawnDelay == 0:
        for x in enemies:
            if not isinstance(x, EnemyProjectile):
                numEnemies += 1
        if numEnemies < stage.enemyCap and stage.spawned < stage.toSpawn:

            enemySpawner(enemies)

            stage.spawned += 1
            spawnDelay = spawnRate

    if spawnDelay != 0:
        spawnDelay -= 1

    for x in enemies:
        if isinstance(x, Fleet):
            for member in x.fleetMembers:
                if member.coords[0] <= player.coords[0] + player.width and member.coords[0] + member.width >= player.coords[0] and member.coords[1] <= player.coords[1] + player.height and member.coords[1] + member.height >= player.coords[1]:
                    player.collide(x)
                    member.collide(player)
            if x.dead:
                enemies.remove(x)
            else:
                x.update()

        else:
            if x.coords[0] <= player.coords[0] + player.width and x.coords[0] + x.width >= player.coords[0] and x.coords[1] <= player.coords[1] + player.height and x.coords[1] + x.height >= player.coords[1]:
                player.collide(x)
                x.collide(player)
            if x.dead:
                enemies.remove(x)
            else:
                x.update()

def enemySpawner(enemies):
    rng = random.randint(0, stage.enemyProgression)
    if rng == 0:
        enemies.append(CargoShip())
    elif rng == 1:
        enemies.append(Fighter())
    elif rng == 2:
        enemies.append(Fleet())
    elif rng == 3:
        enemies.append(KamikazeSpacecraft())
    else:
        print("ERROR: no enemy at enemy progression stage ", rng)

def renderHUD(fps):
    if stage.title.active:
        return
    activeWeaponText = my_font.render(player.unlockedWeapons[player.getWeapon()]+" Active", True, (255, 255, 255))
    if player.money < 10:
        money = my_font.render("$0.0"+str(int(player.money)), True, (255, 255, 255))
    elif player.money < 100:
        money = my_font.render("$0."+str(int(player.money)), True, (255, 255, 255))
    else:
        money = my_font.render('$'+str(int(player.money))[:-2]+'.'+str(int(player.money))[-2:], True, (255, 255, 255))

    frameRate = my_font.render(str(int(fps)), False, (0, 255, 0))
    screen.blit(activeWeaponText, (15, 100))
    screen.blit(frameRate, (1865, 0))
    screen.blit(money, (600,0))

def circ_rect_collide(circleCoords, radius, rect):
    rectPoints = [
        [rect.left, rect.top],
        [rect.left+rect.width, rect.top],
        [rect.left, rect.top+rect.height],
        [rect.left+rect.width, rect.top+rect.height]
    ]
    for point in rectPoints:
        if radius < ((circleCoords[0] - point[0])**2 + (circleCoords[1] - point[1]) **2)**.5:
            return True
    return False
     
if __name__=="__main__":
    # call the main function
    main() 
