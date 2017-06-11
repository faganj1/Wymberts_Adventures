import pygame
from AnimatedSprite import AnimatedSprite
import random

#load images
mageWait = pygame.image.load("sprites/mageWait.png")
magePunch = pygame.image.load("sprites/magePunch.png")
mageMegaPunch = pygame.image.load("sprites/mageMegaPunch.png")
magePound = pygame.image.load("sprites/magePound.png")

fire = pygame.image.load("sprites/fireballSprite.png")
water = pygame.image.load("sprites/waterSprite.png")
wind = pygame.image.load("sprites/windSprite.png")

fireM = pygame.image.load("sprites/fireMinionSprite.png")
iceM = pygame.image.load("sprites/iceMinionSprite.png")
dustM = pygame.image.load("sprites/dustMinionSprite.png")


surf_sz = (640, 480)

mageX = surf_sz[0]/20
mageY = (.25*surf_sz[1], .5*surf_sz[1], .75*surf_sz[1])
spriteMage = AnimatedSprite(mageWait, (mageX, mageY[1]), 2, 1, 0, 2, 24)
spriteM = [spriteMage, spriteMage, spriteMage]
spriteAttack = [spriteMage, spriteMage, spriteMage]

mStart = [( surf_sz[0], mageY[0] + .1*spriteMage.frameHeight ), ( surf_sz[0], mageY[1] + .1*spriteMage.frameHeight ), ( surf_sz[0], mageY[2] + .1*spriteMage.frameHeight )]


def genM(lane):
    global spriteM
    
    typeM = random.randint(0,2)
    if typeM == 0:
        spriteM[lane] = AnimatedSprite(fireM, mStart[lane], 8, 1, 0, 8, 12)
    elif typeM == 1:
        spriteM[lane] = AnimatedSprite(iceM, mStart[lane], 8, 1, 0, 8, 12)
    elif typeM == 2:
        spriteM[lane] = AnimatedSprite(dustM, mStart[lane], 8, 1, 0, 8, 12)

    return typeM

def main():
    pygame.init()
    surf_sz = (640, 480)
    
    main_surface = pygame.display.set_mode(surf_sz)

    global spriteMage, spriteM

    typeM = [0,0,0]
    for lane in range(0,3):
        typeM[lane] = genM(lane)

    curr = 1
    score = 0
    black = (0,0,0)
    red = (255,0,0)
    misses = 0
    
    my_clock = pygame.time.Clock()
    
    my_font = pygame.font.SysFont("Arial Black", 20)
    scoreN = my_font.render("Score:", False, black)
    miss = my_font.render("X", False, red)
    boxes = my_font.render("[  ] [  ] [  ]", False, black)

    game_font = pygame.font.SysFont("Macropsia", 40)
    game_over = game_font.render("Game Over", False, red)
    pause_game = game_font.render("Game Paused", False, red)

    title_font = pygame.font.SysFont("Lithograph", 50)
    title = title_font.render("Wymbert's Adventures", False, (128,0,255))

    moveM = [.5, .5, .5]

    accept = True
    attack = [False, False, False]
    explode = [False, False, False]
    pause = False

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        if accept and ev.type == pygame.KEYDOWN:
            key = ev.dict["key"]
            if key == 27:
                break
            if key == ord("q"):
                spriteMage = AnimatedSprite(magePunch, spriteMage.position, 2, 1, 0, 2, 6)
                accept = False
            elif key == ord("w"):
                spriteMage = AnimatedSprite(mageMegaPunch, spriteMage.position, 3, 1, 0, 3, 6)
                accept = False
            elif key == ord("e"):
                spriteMage = AnimatedSprite(magePound, spriteMage.position, 4, 1, 0, 4, 6)
                accept = False
            elif key == ord("p"):
                pause = not pause
            elif key == 273: #up key
                if not curr == 0:
                    curr -= 1
                    spriteMage.setPosition(spriteMage.position[0], mageY[curr])
            elif key == 274: #down key
                if not curr == 2:
                    curr += 1
                    spriteMage.setPosition(spriteMage.position[0], mageY[curr])
        
        if pause:
            main_surface.blit(pause_game, (225,85))
        elif misses < 3:
            scoreT = my_font.render(str(score), False, black)

            if spriteMage.image == magePunch and spriteMage.updateCount >= spriteMage.updateDivisor*2:
                spriteMage = AnimatedSprite(mageWait, (mageX,mageY[curr]), 2, 1, 0, 2, 15)
                accept = True
            elif spriteMage.image == mageMegaPunch and spriteMage.updateCount >= spriteMage.updateDivisor*3:
                spriteMage = AnimatedSprite(mageWait, (mageX,mageY[curr]), 2, 1, 0, 2, 15)
                accept = True
            elif spriteMage.image == magePound and spriteMage.updateCount >= spriteMage.updateDivisor*4:
                spriteMage = AnimatedSprite(mageWait, (mageX,mageY[curr]), 2, 1, 0, 2, 15)
                accept = True

            if spriteMage.image == magePunch and spriteMage.updateCount >= spriteMage.updateDivisor*1:
                attack[curr] = True
                spriteAttack[curr] = AnimatedSprite(fire, (spriteMage.position[0]+spriteMage.frameWidth, spriteMage.position[1]+(.25*spriteMage.frameHeight)), 5, 1, 0, 5, 6)
            elif spriteMage.image == mageMegaPunch and spriteMage.updateCount >= spriteMage.updateDivisor*2:
                attack[curr] = True
                spriteAttack[curr] = AnimatedSprite(water, (spriteMage.position[0]+spriteMage.frameWidth, spriteMage.position[1]+(.25*spriteMage.frameHeight)), 3, 1, 0, 3, 8)
            elif spriteMage.image == magePound and spriteMage.updateCount >= spriteMage.updateDivisor*3:
                attack[curr] = True
                spriteAttack[curr] = AnimatedSprite(wind, (spriteMage.position[0]+spriteMage.frameWidth, spriteMage.position[1]), 2, 1, 0, 2, 12)
                    
            main_surface.fill((255,255,255))
            main_surface.blit(scoreN, (10, 10))
            main_surface.blit(scoreT, (85, 10))
            main_surface.blit(boxes, (surf_sz[0]-120, 10))
            main_surface.blit(title, (125, 50))

            
            
            for lane in range(0,3):
                if spriteM[lane].position[0] > 0 and not explode[lane]:
                    spriteM[lane].update()
                    spriteM[lane].setPosition(spriteM[lane].position[0]-moveM[lane], spriteM[lane].position[1])
                    spriteM[lane].draw(main_surface)
                else:
                    if not explode[lane]:
                        misses += 1
                    spriteM[lane].setPosition(surf_sz[0], spriteMage.position[1]+(.1*spriteMage.frameHeight))
                    explode[lane] = False
                    typeM[lane] = genM(lane)

            for lane in range(0,3):
                if attack[lane]:
                    if spriteM[lane].containsPoint((spriteAttack[lane].position[0]+spriteAttack[lane].frameWidth,spriteAttack[lane].position[1]+spriteAttack[lane].frameHeight/2)):
                        attack[lane] = False
                        if (typeM[lane] == 0 and spriteAttack[lane].image == water )or (typeM[lane] == 1 and spriteAttack[lane].image == fire) or (typeM[lane] == 2 and spriteAttack[lane].image == wind):
                            explode[lane] = True
                            score += 1
                            moveM[lane] += .25
                            
                    else:
                        spriteAttack[lane].update()
                        spriteAttack[lane].setPosition(spriteAttack[lane].position[0]+3,spriteAttack[lane].position[1])
                        spriteAttack[lane].draw(main_surface)

            
            for x in range(0, misses):
                main_surface.blit(miss, (surf_sz[0]-113+37*x, 12))

            spriteMage.update()
            spriteMage.draw(main_surface)

        else:
            main_surface.blit(game_over, (250,85))
            
        pygame.display.flip()
        my_clock.tick(60)

    pygame.quit()

main()
