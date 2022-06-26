import pygame, random

class Enemy:
    def __init__(self):
        pass

class GreenEnemy(Enemy):
    sprite = pygame.image.load("assets/Ship.png")                                                   #change this
    speed = 1
    width = 250                                                                                     #adjust
    height = 100                                                                                    #adjust

    def __init__(self):
        super().__init__()
        self.coords = [random.randint(scrn_w/2, scrn_w-100), random.randint(100, scrn_h-100)]
        self.direction = random.choice([-1,1])

    def move(self):
        if self.coords[1] <= 0:
            self.direction = 1
        elif self.coords[1] >= scrn_h-GreenEnemy.height:
            self.direction = -1
        self.coords[1] += self.direction*GreenEnemy.speed
      
    def update(self):
        self.move()
        screen.blit(GreenEnemy.sprite, self.coords)

class BlueEnemy(Enemy):
    sprite = pygame.image.load("assets/Shield.png")                                                 #change this
    speed = 0.5
    firerate = 300
    hp = 3
    width = 250                                                                                     #adjust
    height = 100                                                                                    #adjust

    def __init__(self):
        super().__init__()
        self.coords = [random.choice([scrn_w/2, scrn_w*2/3, scrn_w*5/6]), random.randint(100, scrn_h-100)]
        self.direction = random.choice([-1,1])
        self.cooldown = BlueEnemy.firerate

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
    
    def update(self):
        self.cooldown -= 1
        self.move()
        self.shoot()
        screen.blit(BlueEnemy.sprite, self.coords)

class BlueBullet(Enemy):
    sprite = pygame.image.load("assets/playerBullet.png")                                           #change this
    speed = 10
    width = 20                                                                                      #adjust
    height = 10                                                                                     #adjust

    def __init__(self, coords):
        super().__init__()
        self.coords = coords
    
    def move(self):
        self.coords[0] -= BlueBullet.speed
    
    def update(self):
        self.move()
        screen.blit(BlueBullet.sprite, self.coords)
        
        

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

movespeed = 3
bulletSpeed = 20
scrn_w = 1920
scrn_h = 1080

def main():
    global screen, enemies
    coolDown = 0
    activeWeapon = 0
    keyPressCD = 0
    enemySpawnRate = 300
  
    frametime = pygame.time.Clock()
    
    pygame.init()
  
    #pygame.display.set_icon(pygame.image.load("assets/logo.png"))                              reenable this
    pygame.display.set_caption("Space Invaders")
    
    screen = pygame.display.set_mode((scrn_w,scrn_h), pygame.FULLSCREEN|pygame.SCALED)
    
    running = True
    
    playerSprite = pygame.image.load("assets/Ship.png")
    playerShield = pygame.image.load("assets/Shield.png")
    bulletSprite = pygame.image.load("assets/playerBullet.png")
    laserSprite = pygame.image.load("assets/laser.png")
    backgroundSprite = pygame.image.load("assets/background.jpg")
    enemySprites = [
        pygame.image.load("assets/Ship.png"), #green enemy sprite                               change this
        pygame.image.load("assets/Shield.png") #blue enemy sprite                               change this
    ]
  
    Px, Py = 25, 400
  
    playerBullets = []
    enemies = []
  
    while running:
        screen.fill((0,0,0))
  
        screen.blit(backgroundSprite, (0, 0))
        
        screen.blit(playerSprite, (Px, Py))    #starting position
  
        screen.blit(playerShield, (Px - 5, Py - 105))
  
        for bullet in range(len(playerBullets)):
            playerBullets[bullet][0] += bulletSpeed     #moves the bullet forward
            screen.blit(bulletSprite, (playerBullets[bullet][0], playerBullets[bullet][1]))     #displays the bullet

        # enemy actions
        for enemy in range(len(enemies)):
            enemies[enemy].update()

        #enemy spawning
        if not random.randrange(enemySpawnRate):
            enemies.append(GreenEnemy())
        if not random.randrange(enemySpawnRate*1.5):
            enemies.append(BlueEnemy())
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
     
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            Py -= movespeed
  
            if Py <= 0-(playerShield.get_height()//2):
              Py = screen.get_height()
              
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            Py += movespeed
              
            if Py >= screen.get_height()+(playerShield.get_height()//2):
              Py = 0
        if keys[pygame.K_c] and keyPressCD == 0:
            keyPressCD = 100
            if activeWeapon == 0:
                activeWeapon = 1
            else:
                activeWeapon = 0
        if keys[pygame.K_SPACE]:
            if activeWeapon == 0:
                if coolDown == 0:
                    playerBullets.append([Px+150, Py+16])
                    coolDown += 60 #frames
            elif activeWeapon == 1:
                screen.blit(laserSprite, (Px+210, Py+24))
        
        if coolDown != 0:
            coolDown -= 1
        if keyPressCD != 0:
            keyPressCD -= 1
  
        renderHUD(coolDown, activeWeapon, frametime.get_fps())
        pygame.display.flip()
        frametime.tick(120)
  
  
def renderHUD(coolDown, activeWeapon, fps):
        bulletCDtext = my_font.render(str(coolDown), False, (255, 255, 255))
        
        if activeWeapon == 0:
            activeWeaponText = my_font.render("Laser Cannon Active", False, (255, 255, 255))
        else:
            activeWeaponText = my_font.render("Laser Beam Active", False, (255, 255, 255))

        frameRate = my_font.render(str(int(fps)), False, (0, 255, 0))



        screen.blit(bulletCDtext, (10,0))
        screen.blit(activeWeaponText, (50, 0))
        screen.blit(frameRate, (1865, 0))

if __name__=="__main__":
    main() 