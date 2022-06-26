import pygame, random
 
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

movespeed = 3
bulletSpeed = 20
scrn_w = 1920
scrn_h = 1080



# define a main function
def main():
  global screen
  coolDown = 0
  activeWeapon = 0
  keyPressCD = 0
  enemySpawnRate = 300

  frametime = pygame.time.Clock()
   
  # initialize the pygame module
  pygame.init()
  # load and set the logo
  #pygame.display.set_icon(pygame.image.load("assets/logo.png"))
  pygame.display.set_caption("Space Invaders")
   
  # create a surface on screen that has the size of 240 x 180
  screen = pygame.display.set_mode((scrn_w,scrn_h), pygame.FULLSCREEN|pygame.SCALED)
   
  # define a variable to control the main loop
  running = True
   


  
  playerSprite = pygame.image.load("assets/Ship.png")
  playerShield = pygame.image.load("assets/Shield.png")
  bulletSprite = pygame.image.load("assets/playerBullet.png")
  laserSprite = pygame.image.load("assets/laser.png")
  backgroundSprite = pygame.image.load("assets/background.jpg")
  enemySprites = [
        pygame.image.load("assets/Ship.png"), #green enemy sprite      change this
        pygame.image.load("assets/Shield.png") #blue enemy sprite     change this
]

  Px, Py = 25, 400

  playerBullets = []
  enemies = [
      [], #0 - green enemies
      [] #1 - blue enemies
  ]

  # main loop
  while running:
      screen.fill((0,0,0)) #Clears the screen

      screen.blit(backgroundSprite, (0, 0))
      
      screen.blit(playerSprite, (Px, Py))    #starting position

      screen.blit(playerShield, (Px - 5, Py - 105))

      for bullet in range(len(playerBullets)):
          playerBullets[bullet][0] += bulletSpeed     #moves the bullet forward
          screen.blit(bulletSprite, (playerBullets[bullet][0], playerBullets[bullet][1]))     #displays the bullet

      for enemyType in range(len(enemies)):
          for enemy in range(len(enemies[enemyType])):
              screen.blit(enemySprites[enemyType], (enemies[enemyType][enemy][0],enemies[enemyType][enemy][1]))

      if not random.randrange(enemySpawnRate):
          enemies[0].append([random.randint(scrn_w/2,scrn_w-100),random.randint(100,scrn_h-100)])
      elif not random.randrange(enemySpawnRate):
          enemies[1].append([random.randint(scrn_w/2,scrn_w-100),random.randint(100,scrn_h-100)])
        

      # event handling, gets all event from the event queue
      for event in pygame.event.get():
          # only do something if the event is of type QUIT
          if event.type == pygame.QUIT:
              # change the value to False, to exit the main loop
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

     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main() 