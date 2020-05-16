import pygame
from random import randrange , random , choice
from math import sqrt , pow
from environment_constants import *

#FALTAM ALGUMAS COISAS AINDA INCLUSIVE CONTROLAR AS TAXAS DE REPRODUCAO E COMPETICAO...

class Animal:
    def __init__(self , animal_type , dna=None):
        self.animal_type = animal_type
        if self.animal_type == 'wolf':
            if dna == None:
                self.dna = {
                'force':randrange(MIN_FORCE_WOLFS,MAX_FORCE_WOLFS + 1) ,
                'speed':randrange(MIN_SPEED_WOLFS,MAX_SPEED_WOLFS + 1) , 
                'acceleration':randrange(MIN_ACCELERATION_WOLFS,MAX_ACCELERATION_WOLFS + 1) ,
                'vision_ray':randrange(MIN_VISION_RAY_WOLFS , MAX_VISION_RAY_WOLFS + 1) ,
                'defense':randrange(MIN_DEFENSE_WOLFS,MAX_DEFENSE_WOLFS + 1)
                }
            else:
                self.dna = dna
            
            gender = choice( ["male" , "female"] )
            image_path = "../images/wolf_" + gender + ".png"
                
        elif self.animal_type == 'lamb':
            if dna == None:
                self.dna = {
                'force':randrange(MIN_FORCE_LAMBS,MAX_FORCE_LAMBS + 1) ,
                'speed':randrange(MIN_SPEED_LAMBS,MAX_SPEED_LAMBS + 1) , 
                'acceleration':randrange(MIN_ACCELERATION_LAMBS,MAX_ACCELERATION_LAMBS + 1) ,
                'vision_ray':randrange(MIN_VISION_RAY_LAMBS , MAX_VISION_RAY_LAMBS + 1) ,
                'defense':randrange(MIN_DEFENSE_LAMBS,MAX_DEFENSE_LAMBS + 1)
                }
            else:
                self.dna = dna
            
            gender = choice( ["male" , "female"] )
            image_path = "../images/lamb_" + gender + ".png"
           
        

        self.status = 'alive'
        self.lifes = 100
        self.born = pygame.time.get_ticks()
        self.age = 0
        
        self.image = pygame.image.load(image_path)        
        self.gender = gender
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.pos = [randrange(SCREEN_WIDTH) , randrange(SCREEN_HEIGHT)]
        
        self.pos[0] = (self.pos[0] + self.width / 2)
        self.pos[1] = (self.pos[1] + self.height / 2)
        
        self.old_pos = list(self.pos)
       
        if animal_type == "wolf":
            self.max_speed = MAX_SPEED_WOLFS
        elif animal_type == "lamb":
            self.max_speed = MAX_SPEED_LAMBS
            
        self.time_last_movement = pygame.time.get_ticks()    
        self.step_movement = 5


        self.speed = self.dna['speed']
        self.initial_speed = self.speed
        self.acceleration = self.dna['acceleration']
        self.force = self.dna['force']
        self.vision_ray = self.dna['vision_ray']
        self.defense = self.dna['defense']
            
        self.target_pos = [randrange(SCREEN_WIDTH) , randrange(SCREEN_HEIGHT)]
        self.vector_old_to_target = [self.target_pos[0] - self.old_pos[0] , self.target_pos[1] - self.old_pos[1]]
   
    def moving_state(self):

        if pygame.time.get_ticks() >= (self.time_last_movement + ( 1000 / self.speed)):
            print("moving...")
            pos = list(self.pos)
            
            if self.vector_old_to_target[0] -  self.step_movement > 0:
                self.pos[0] +=  self.step_movement
                self.vector_old_to_target[0] -=  self.step_movement
            elif self.vector_old_to_target[0] +  self.step_movement < 0:
                self.pos[0] -=  self.step_movement
                self.vector_old_to_target[0] +=  self.step_movement
                
            if self.vector_old_to_target[1] -  self.step_movement > 0:
                self.pos[1] +=  self.step_movement
                self.vector_old_to_target[1] -=  self.step_movement
            elif self.vector_old_to_target[1] +  self.step_movement < 0:
                self.pos[1] -=  self.step_movement
                self.vector_old_to_target[1] +=  self.step_movement
            
            #movement...
            if pos != self.pos:
                self.time_last_movement = pygame.time.get_ticks()
                self.speed += self.acceleration
            
        if abs(self.vector_old_to_target[0]) <=  self.step_movement and abs(self.vector_old_to_target[1]) <=  self.step_movement:
            self.old_pos = list(self.pos)
            self.target_pos = [randrange(SCREEN_WIDTH) , randrange(SCREEN_HEIGHT)]
            self.vector_old_to_target = [self.target_pos[0] - self.old_pos[0] , self.target_pos[1] - self.old_pos[1]]
            self.speed = self.initial_speed
    
    def reproducing_state(self , female , probabilitie_reproduction,probabilitie_mutation_environment):
        son_dna = {}
        
        #crossover...
        r = random()
        if r <= probabilitie_reproduction:
            print("reproducing...")    
            random_index = randrange(len(self.dna))
            keys = list(self.dna.keys())
            for i in range(len(self.dna)):
                if i < random_index:
                    son_dna[keys[i]] = self.dna[keys[i]]
                else:
                    son_dna[keys[i]] = female.dna[keys[i]]
            
            #mutation...
            r = random()
            if r <= probabilitie_mutation_environment:
                random_index = randrange(len(son_dna))
                keys = list(son_dna.keys())
                if keys[random_index] == 'force':
                    son_dna['force'] += randrange(-10,10)
                    if son_dna['force'] < 0:
                        son_dna['force'] = 0
                elif keys[random_index] == 'speed':
                    son_dna['speed'] += randrange(-5,5)
                    if son_dna['speed'] < 1:
                        son_dna['speed'] = 1
                elif keys[random_index] == 'acceleration':
                    son_dna['acceleration'] += randrange(-2,2)
                    if son_dna['acceleration'] < 0:
                        son_dna['acceleration'] = 0
                elif keys[random_index] == 'vision_ray':
                    son_dna['vision_ray'] += randrange(-5,5)
                    if son_dna['vision_ray'] < 0:
                        son_dna['vision_ray'] = 0
                elif keys[random_index] == 'defense':
                    son_dna['defense'] += randrange(-5,5)
                    if son_dna['defense'] < 0:
                        son_dna['defense'] = 0
                    
            self.pos[0] += self.dna['vision_ray']
            self.pos[1] += self.dna['vision_ray']
            
        return son_dna
    
    def fighting_state(self,male_oponent,probabilitie_competition):
        r = random()
        if r <= probabilitie_competition:
            print("fighting...")
            if self.dna['force'] > male_oponent.dna['defense']:
                male_oponent.lifes = 0
                male_oponent.status = 'dead'
            elif male_oponent.dna['force'] > self.dna['defense']:
                self.lifes = 0
                self.status = 'dead'
            else:
                self.lifes -= (self.lifes // 2)
                male_oponent.lifes -= (male_oponent.lifes // 2)  

    def draw(self , screen,debug):
        pos = [int(self.pos[0]) , int(self.pos[1]) ]

        width = int(self.width)
        height = int(self.height)
        vision_ray = int(self.vision_ray)
        force = int(self.force)
        defense = int(self.defense)
        initial_speed = int(self.initial_speed)
        
        screen.blit(self.image , (pos[0] - width // 2 , pos[1] - height // 2))
        
        if debug == True:
            pygame.draw.circle(screen , (0,0,0) , pos , vision_ray , 1 )
            pygame.draw.aaline(screen , (255,0,0) , pos , [pos[0] + force , pos[1]])
            pygame.draw.aaline(screen , (0,255,0) , pos , [pos[0] , pos[1] - defense])
            pygame.draw.aaline(screen , (0,0,255) , pos , [pos[0] , pos[1] + initial_speed])

        
class Wolf(Animal):
    def __init__(self,dna=None):
        super().__init__(animal_type='wolf',dna=dna)
    
    def eating_state(self,lamb):
        print("eating...")
        if self.dna['force'] > lamb.dna['force']:
            self.lifes += 1
            lamb.status = 'dead'
        else:
            self.lifes -= 1
            lamb.lifes -= 1
        
    def update(self,wolfs,lambs):
        if self.lifes <= 0 or self.age >= MAX_AGE:
            self.status = 'dead'
            return
        
        old_age = self.age
        
        #increment age...
        self.age = int( (pygame.time.get_ticks() - self.born) / MILLISECONDS_ONE_EPOCH )
      
        #decrement lifes...
        if self.age > old_age:
            self.lifes = self.lifes - DECREMENT_LIFES_PER_AGE
        
        self.moving_state()
        
        wm = 0
        wf = 0
        na = len(lambs)
        
        for w in wolfs:
            if w.gender == 'male':
                wm += 1
            elif w.gender == 'female':
                wf += 1
               
        for w in wolfs:
            if sqrt(pow(self.pos[0] - w.pos[0] , 2) + pow(self.pos[1] - w.pos[1] , 2)) <= self.dna['vision_ray'] and w != self:
                if self.gender == 'male' and w.gender == 'female':
                    probabilitie_reproduction_physical_attributes_male = ((self.dna['force'] + self.dna['speed'] + self.dna['acceleration'] + self.dna['vision_ray'] ) / 4)  / (MAX_ALL_ATTRIBUTES_WOLFS * 10)
                    probabilitie_reproduction = PROBABILITIE_REPRODUCTION + probabilitie_reproduction_physical_attributes_male
                    print("pr wolfs:",probabilitie_reproduction)
                    dna_son = self.reproducing_state(female=w,probabilitie_reproduction=probabilitie_reproduction,probabilitie_mutation_environment=PROBABILITIE_MUTATION)
                    if len(dna_son) > 0:
                        wolfs.append( Wolf( dna=dict( dna_son ) ) )
                elif self.gender == 'male' and w.gender == 'male':
                    probabilitie_competition = PROBABILITIE_COMPETITION + ( ( wm / (wf + 0.01) ) + ( ( wm + wf ) / (na + 0.01) ) ) / (wm + wf) 
                    print("pc wolfs:",probabilitie_competition)
                    self.fighting_state(male_oponent=w,probabilitie_competition=probabilitie_competition)
                    
        for l in lambs:
            if sqrt(pow(self.pos[0] - l.pos[0] , 2) + pow(self.pos[1] - l.pos[1] , 2)) <= self.dna['vision_ray']:
                self.eating_state(lamb=l)
                
                
                
class Lamb(Animal):
    def __init__(self,dna=None):
        super().__init__(animal_type='lamb' , dna=dna)

    def eating_state(self,grass):
        print("eating...")

        self.lifes += 1
        grass.status = 'dead'

        
    def update(self,lambs,grasses):
        if self.lifes <= 0 or self.age >= MAX_AGE:
            self.status = 'dead'
            return
        
        old_age = self.age
        
        #increment age...
        self.age = int( (pygame.time.get_ticks() - self.born) / MILLISECONDS_ONE_EPOCH )
      
        #decrement lifes...
        if self.age > old_age:
            self.lifes = self.lifes - DECREMENT_LIFES_PER_AGE
            
        self.moving_state()
        
        lm = 0
        lf = 0
        na = len(grasses)
        
        for l in lambs:
            if l.gender == 'male':
                lm += 1
            elif l.gender == 'female':
                lf += 1
                    
        for l in lambs:
            if sqrt(pow(self.pos[0] - l.pos[0] , 2) + pow(self.pos[1] - l.pos[1] , 2)) <= self.dna['vision_ray'] and l != self:
              
                if self.gender == 'male' and l.gender == 'female':
                    probabilitie_reproduction_physical_attributes_male = ((self.dna['force'] + self.dna['speed'] + self.dna['acceleration'] + self.dna['vision_ray'] ) / 4)  / (MAX_ALL_ATTRIBUTES_LAMBS * 10)
                    probabilitie_reproduction = PROBABILITIE_REPRODUCTION + probabilitie_reproduction_physical_attributes_male
                    print("pr lambs:",probabilitie_reproduction)
                    dna_son = self.reproducing_state(female=l,probabilitie_reproduction=probabilitie_reproduction,probabilitie_mutation_environment=PROBABILITIE_MUTATION)
                    if len(dna_son) > 0:
                        lambs.append( Lamb( dna=dict( dna_son ) ) )
                elif self.gender == 'male' and l.gender == 'male':
                    probabilitie_competition = PROBABILITIE_COMPETITION + ( ( lm / (lf + 0.01) ) + ( ( lm + lf ) / (na + 0.01) ) ) / (lm + lf)
                    print("pc lambs:",probabilitie_competition)
                    self.fighting_state(male_oponent=l,probabilitie_competition=probabilitie_competition)
        for g in grasses:
            if sqrt(pow(self.pos[0] - g.pos[0] , 2) + pow(self.pos[1] - g.pos[1] , 2)) <= self.dna['vision_ray']:
                self.eating_state(grass=g)
                
                
           

class Grass:
    def __init__(self,pos=None):
        self.image_path = "../images/grass.png"
        self.image = pygame.image.load(self.image_path)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        if pos == None:
            self.pos = [randrange(SCREEN_WIDTH) , randrange(SCREEN_HEIGHT)]
        else:
            self.pos = list(pos)
             
        self.status = 'alive'
        
  
    def draw(self,screen):
        if self.status == 'alive':
            screen.blit(self.image , [self.pos[0] - self.width // 2 , self.pos[1] - self.height // 2])

                
            
  