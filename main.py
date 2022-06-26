import pygame, random, math
 
pygame.init()
pygame.font.init()
pygame.mixer.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

movespeed = 3
spawnRate = 60     #interval before enemies spawn
spawnDelay = 0    #Initial delay before spawning
popCap = 5          #Max enemy count
enemyMoveSpeed = 1

explosions = []
explosionSprites = []
for x in range(12):
    explosionSprites.append(pygame.image.load("assets/explosion/"+str(x)+".png"))


class Player():
    playerSprite = pygame.image.load("assets/Ship.png")
    shieldSprite = pygame.image.load("assets/Shield.png")
    width = playerSprite.get_width()
    height = playerSprite.get_height()
    shieldWidth = shieldSprite.get_width()
    shieldHeight = shieldSprite.get_height()

    def __init__(self):
        self.coords = [25, (scrn_h-Player.height)/2]
        self.shield = 10
        self.speed = 3
        self.bulletCD = 0
        self.bullet_firerate = 200
        self.laserCD = 0
        self.laser_firerate = 1000
        self.laserTime = 0
        self.laserDuration = 300
        self.bullets = []
        self.bulletSpeed = 20
        self.weapon = 0
        self.unlockedWeapons = 2

    def getWeapon(self):
        return self.weapon

    def switchWeapon(self, slot):
        self.weapon = slot
        if self.weapon < 0:
            self.weapon = self.unlockedWeapons-1
        elif self.weapon >= self.unlockedWeapons:
            self.weapon = 0

    def shoot(self):
        if self.weapon == 0:
            if self.bulletCD <= 0:
                self.bullets.append(Bullet(self.coords.copy(), self.bulletSpeed, 0))
                self.bulletCD = self.bullet_firerate
        elif self.weapon == 1:
            if self.laserCD <= 0 and self.laserTime < self.laserDuration:
                self.bullets.append(Laser(self.coords.copy(), 0))
                self.laserTime += 1
            elif self.laserTime >= self.laserDuration:
                self.laserCD = self.laser_firerate
                self.laserTime = 0

    def collide(self, other):
        if isinstance(other, Enemy):
            if self.shield:
                self.shield -= 1

    def update(self):
        screen.blit(Player.playerSprite, self.coords)
        if self.shield > 0:
            screen.blit(Player.shieldSprite, [self.coords[0]-(Player.shieldWidth-Player.width)/2, self.coords[1]-(Player.shieldHeight-Player.height)/2])
        if self.bulletCD > 0 :
            self.bulletCD -= 1
        if self.laserCD > 0:
            self.laserCD -= 1
        for bullet in self.bullets:
            bullet.update()

class Bullet():
    sprite = pygame.image.load("assets/playerBullet.png")
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self, coords, speed, angle):
        self.coords = coords
        self.speed = speed
        self.angle = angle

    def move(self):
        self.coords[0] += math.cos(self.angle)*self.speed
        self.coords[1] += math.sin(self.angle)*self.speed

    def update(self):
        self.move()
        screen.blit(Bullet.sprite, self.coords)

class Laser(Bullet):
    baseSprite = pygame.image.load("assets/laser_base.png")
    sprite = pygame.image.load("assets/laser.png")

    def __init__(self, coords, angle, speed=sprite.get_width()):
        super().__init__(coords, speed, angle)

    def update(self):
        self.move()
        if self.coords != player.coords:
            screen.blit(Laser.sprite, self.coords)
        else:
            screen.blit(Laser.baseSprite, self.coords)


class Enemy():
    def __init__(self):
        pass

class GreenEnemy(Enemy):
    sprite = pygame.image.load("assets/Ship.png")                                                   #change this
    speed = 1
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self):
        super().__init__()
        self.coords = [random.randint(scrn_w/2, scrn_w-100), random.randint(100, scrn_h-100)]
        self.direction = random.choice([-1,1])
        self.dead = False

    def move(self):
        if self.coords[1] <= 0:
            self.direction = 1
        elif self.coords[1] >= scrn_h-GreenEnemy.height:
            self.direction = -1
        self.coords[1] += self.direction*GreenEnemy.speed
    
    def collide(self, other):
        if isinstance(other, Bullet):
            self.dead = True
      
    def update(self):
        self.move()
        screen.blit(GreenEnemy.sprite, self.coords)

class BlueEnemy(Enemy):
    sprite = pygame.image.load("assets/Shield.png")                                                 #change this
    speed = 0.5
    firerate = 300
    hp = 3
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self):
        super().__init__()
        self.coords = [random.choice([scrn_w/2, scrn_w*2/3, scrn_w*5/6]), random.randint(100, scrn_h-100)]
        self.direction = random.choice([-1,1])
        self.cooldown = BlueEnemy.firerate
        self.dead = False

    def move(self):
        if self.coords[1] <= 0:
            self.direction = 1
        elif self.coords[1] >= scrn_h-BlueEnemy.height:
            self.direction = -1
        self.coords[1] += self.direction*BlueEnemy.speed

    def shoot(self):
        if self.cooldown <= 0:
            enemies.append(BlueBullet([self.coords[0], self.coords[1]+(BlueEnemy.height-BlueBullet.height)/2]))
            self.cooldown = BlueEnemy.firerate
    
    def collide(self, other):
        if isinstance(other, Bullet):
            self.hp -= 1
            if self.hp == 0:
                self.dead = True
    
    def update(self):
        self.cooldown -= 1
        self.move()
        self.shoot()
        screen.blit(BlueEnemy.sprite, self.coords)

class BlueBullet(Enemy):
    sprite = pygame.image.load("assets/playerBullet.png")                                           #change this
    speed = 10
    width = sprite.get_width()
    height = sprite.get_height()

    def __init__(self, coords):
        super().__init__()
        self.coords = coords
    
    def move(self):
        self.coords[0] -= BlueBullet.speed
    
    def update(self):
        self.move()
        screen.blit(BlueBullet.sprite, self.coords)

scrn_w = 1920
scrn_h = 1080

# define a main function
def main():
    global screen, enemies, player
    coolDown = 0
    activeWeapon = 0
    keyPressCD = 0

    running = True
    
    frametime = pygame.time.Clock()
  

    #pygame.display.set_icon(pygame.image.load("assets/logo.png"))                              reenable this
    pygame.display.set_caption("Space Invaders")
    screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN|pygame.SCALED)
    
    laserSprite = pygame.image.load("assets/laser.png")
    backgroundSprite = pygame.image.load("assets/background.jpg")

    enemies = []
     
    player = Player()

    # main loop
    while running:
        screen.fill((0,0,0)) #Clears the screen
  
        screen.blit(backgroundSprite, (0, 0))

        player.update()
        
        for enemy in range(len(enemies)):
            enemies[enemy].update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                player.switchWeapon(player.getWeapon()+event.y*-1)
     
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.coords[1] - (Player.shieldHeight-Player.height)/2 > 0:
            player.coords[1] -= player.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.coords[1] + (Player.shieldHeight-Player.height)/2 < scrn_h:
            player.coords[1] += player.speed

        if keys[pygame.K_1]:
            player.switchWeapon(0)
        if keys[pygame.K_2]:
            player.switchWeapon(1)

        if keys[pygame.K_SPACE]:
            player.shoot()
        elif player.getWeapon() == 1 and player.laserTime != player.laserDuration and player.laserTime != 0:
                player.laserCD = math.floor(player.laser_firerate * player.laserTime / player.laserDuration)
                player.laserTime = 0
        
        if keyPressCD != 0:
            keyPressCD -= 1

        enemyCore(enemies)
        playerBulletCore()
        explosionCore(explosions)

        renderHUD(coolDown, activeWeapon, frametime.get_fps())
        pygame.display.flip()
        frametime.tick(120)


def explosionCore(explosions):
    for x in explosions:
        if x[0] % 2 == 0:
            screen.blit(explosionSprites[x[0]//2], (x[1], x[2]))
        x[0] += 1
        if x[0] > 22:
            explosions.remove(x)
        



def playerBulletCore():
    for x in player.bullets:
        x.update()

        for ship in enemies:
            if ship.coords[0] < x.coords[0] and ship.coords[1] - 50 < x.coords[1] and ship.coords[1] > x.coords[1] - 50:          #detects bullet collision
                ship.collide(x)

                if ship.dead:
                    enemies.remove(ship)

                x_offset = random.randrange(-25, 25)
                y_offset = 0


                explosions.append([0, x.coords[0] + x_offset, x.coords[1] + y_offset])
                player.bullets.remove(x)





        if x.coords[0] > 2000:             #removes off-screen bullets
            try:                        #needed because harmless bug would take too much time to fix
                player.bullets.remove(x)
            except ValueError:
                print("ERROR: Bullet not in list")


def enemyCore(enemies):
    global spawnRate
    global spawnDelay
    if spawnDelay == 0 and len(enemies) < popCap:
        enemies.append(GreenEnemy())
        spawnDelay = spawnRate

    if spawnDelay != 0:
        spawnDelay -= 1

    for x in enemies:
        x.update()

    enemyMove(enemies)


def enemyMove(enemies):
        g1 = []
        g2 = []
        g3 = []

        for index in range(len(enemies)):
            if enemies[index].coords[0] == 1250:
                g1.append(index)
            elif enemies[index].coords[0] == 1450:
                g2.append(index)
            else:
                g3.append(index)
        
        if len(g1) > 0:                 #makes newly spawned enemies move in the same direction as others
            for x in g1:
                if enemies[x].direction != enemies[g1[0]].direction:
                    enemies[x].direction = enemies[g1[0]].direction
        if len(g2) > 0:
            for x in g2:
                if enemies[x].direction != enemies[g2[0]].direction:
                    enemies[x].direction = enemies[g2[0]].direction
        if len(g3) > 0:
            for x in g3:
                if enemies[x].direction != enemies[g3[0]].direction:
                    enemies[x].direction = enemies[g3[0]].direction

        large_g1 = 0                                        #inverts direction of column if out of bounds
        small_g1 = 1080
        for index in g1:
            if enemies[index].pos[1] > large_g1:
                large_g1 = enemies[index].pos[1]
            if enemies[index].pos[1] < small_g1:
                small_g1 = enemies[index].pos[1]
        if small_g1 < 10 or large_g1 > 1000:
            for x in g1:
                enemies[x].direction = -enemies[x].direction

        large_g2 = 0                                        #inverts direction of column if out of bounds
        small_g2 = 1080
        for index in g2:
            if enemies[index].pos[1] > large_g2:
                large_g2 = enemies[index].pos[1]
            if enemies[index].pos[1] < small_g2:
                small_g2 = enemies[index].pos[1]
        if small_g2 < 10 or large_g2 > 1000:
            for x in g2:
                enemies[x].direction = -enemies[x].direction

        large_g3 = 0                                        #inverts direction of column if out of bounds
        small_g3 = 1080
        for index in g3:
            if enemies[index].coords[1] > large_g3:
                large_g3 = enemies[index].coords[1]
            if enemies[index].coords[1] < small_g3:
                small_g3 = enemies[index].coords[1]
        if small_g3 < 10 or large_g3 > 1000:
            for x in g3:
                enemies[x].direction = -enemies[x].direction

        for x in enemies:
            x.update()


    


def renderHUD(coolDown, activeWeapon, fps):
        
        if player.getWeapon() == 0:
            CDtext = my_font.render(str(player.bulletCD), False, (255, 255, 255))
            activeWeaponText = my_font.render("Laser Cannon Active", False, (255, 255, 255))
        elif player.getWeapon() == 1:
            CDtext = my_font.render(str(player.laserCD), False, (255, 255, 255))
            activeWeaponText = my_font.render("Laser Beam Active", False, (255, 255, 255))

        frameRate = my_font.render(str(int(fps)), False, (0, 255, 0))



        screen.blit(CDtext, (10,0))
        screen.blit(activeWeaponText, (80, 0))
        screen.blit(frameRate, (1865, 0))

     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main() 