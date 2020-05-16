import pygame
from classes import Wolf , Lamb , Grass
from environment_constants import *
from threading import Thread


graphics_active = True

class CevecLogic(Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        global epoch , tick , wolfs , lambs , grasses , graphics_active
        while graphics_active == True:
     
            for w in wolfs:
               w.update(wolfs=wolfs,lambs=lambs)

            
            for l in lambs:
                l.update(lambs=lambs,grasses=grasses)

            index_deads = []        
            for i in range(len(wolfs)):
                if wolfs[i].status == 'dead':
                    index_deads.append(i)
                    
            index_deads.sort(reverse=True)
            for i in index_deads:
                del(wolfs[i])
            
            index_deads = []
            for i in range(len(lambs)):
                if lambs[i].status == 'dead':
                    index_deads.append(i)
                    
            index_deads.sort(reverse=True)
            for i in index_deads:
                del(lambs[i])  
                
            index_deads = []
            for i in range(len(grasses)):
                if grasses[i].status == 'dead':
                    index_deads.append(i)
                    
            index_deads.sort(reverse=True)        
            for i in index_deads:
                del(grasses[i])
            
            if pygame.time.get_ticks() - tick >= MILLISECONDS_ONE_EPOCH:
                epoch += 1
                tick = pygame.time.get_ticks()
                grasses += [ Grass() for i in range(GRASSES_INCREMENT_PER_EPOCH) ]
            

class CevecDraw(Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        global font , screen , clock , epoch , tick , wolfs , lambs , grasses , graphics_active
        graphics_active = True
        while graphics_active == True:
            
            clock.tick(FPS)
            screen.fill( (167,73,22) )
           
            for g in grasses:
                g.draw(screen)
            
            for w in wolfs:
                w.draw(screen,True)
 
            for l in lambs:
                l.draw(screen,True)
 
            hud_epoch = font.render("Epoch: %d"%epoch , True , (255,255,255))
            screen.blit(hud_epoch , (SCREEN_WIDTH // 2 , 20))
            
            hud_wolfs = font.render("Wolfs: %d"%len(wolfs) , True , (255,255,255))
            screen.blit(hud_wolfs , (20 , SCREEN_HEIGHT // 2))
            
            
            wm = 0
            wf = 0
            for w in wolfs:
                if w.gender == 'male':
                    wm += 1
                elif w.gender == 'female':
                    wf += 1
            

            hud_wolfs = font.render("males: %d"%wm , True , (255,255,255))
            screen.blit(hud_wolfs , (100 , SCREEN_HEIGHT // 2))
            
            hud_wolfs = font.render("females: %d"%wf , True , (255,255,255))
            screen.blit(hud_wolfs , (180 , SCREEN_HEIGHT // 2))
            
            lm = 0
            lf = 0
            for l in lambs:
                if l.gender == 'male':
                    lm += 1
                elif l.gender == 'female':
                    lf += 1

            hud_lambs = font.render("Lambs: %d"%len(lambs) , True , (255,255,255))
            screen.blit(hud_lambs , (20 , SCREEN_HEIGHT // 2 + 20))
            
            hud_lambs = font.render("males: %d"%lm , True , (255,255,255))
            screen.blit(hud_lambs , (100 , SCREEN_HEIGHT // 2 + 20))
            
            hud_lambs = font.render("females: %d"%lf , True , (255,255,255))
            screen.blit(hud_lambs , (180 , SCREEN_HEIGHT // 2 + 20))
            
            
            
            hud_grasses = font.render("Grasses: %d"%len(grasses) , True , (255,255,255))
            screen.blit(hud_grasses , (20 , SCREEN_HEIGHT // 2 + 40))
        
            pygame.display.update()
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    graphics_active = False
                    pygame.quit()

            
                
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    
    if ENABLE_GRAPHICS == True:
        screen = pygame.display.set_mode( (SCREEN_WIDTH , SCREEN_HEIGHT) )
    
    wolfs = [Wolf() for i in range(5)]
    lambs = [Lamb() for i in range(15)]
    grasses = [Grass() for i in range(GRASSES_INCREMENT_PER_EPOCH)]
    
    epoch = 0
    tick = pygame.time.get_ticks()
    font = pygame.font.SysFont('arial',12)
    
    thcl = CevecLogic()
    thcl.start()
    
    if ENABLE_GRAPHICS == True:
        thcd = CevecDraw()
        thcd.start()
    
    
    
    
    
    

        
        
        
