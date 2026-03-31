import pygame,random,math
import files.sounds as sounds

class Rock():
    class Data(pygame.sprite.Sprite):
        screen_rect = pygame.Rect(0,0,600,450)
        image = pygame.image.load("./images/rock.png")
        image_small = pygame.transform.scale(image,(30,30))
        sound = "bonk.mp3"
        name = "rock"
        def __init__(self,direction:list=None,position:tuple=None):
            pygame.sprite.Sprite.__init__(self)
            self.image = Rock.Data.image_small
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(10,Rock.Data.screen_rect.right),random.randint(10,Rock.Data.screen_rect.bottom)) if position == None else position
            self.direction = [random.choice(("up","down")),random.choice(("left","right"))] if direction == None else direction

        def update(self):
            self.move()
            self.bounce()
            
        def move(self):
            #VERTICAL MOVEMENT
            if self.direction[0] == "down":
                self.rect.y += 1
            else:
                self.rect.y -= 1
            #HORIZONTAL MOVEMENT
            if self.direction[1] == "left":
                self.rect.x-=1 
            else:
                self.rect.x+=1
                
        def bounce(self):
            #COLLISION FOR BOUNCING
            if self.rect.bottom > Rock.Data.screen_rect.bottom:
                # print("BOUNCED")
                self.direction[0] = "up"
            if self.rect.top < Rock.Data.screen_rect.top:
                # print("BOUNCED")
                self.direction[0] = "down"
            if self.rect.right > Rock.Data.screen_rect.right:
                # print("BOUNCED")
                self.direction[1] = "left"
            if self.rect.left < Rock.Data.screen_rect.left:
                # print("BOUNCED")
                self.direction[1] = "right"
            #COLLISION FOR KILLING IF OFFSCREEN
            if not self.rect.colliderect(Rock.Data.screen_rect):
                self.kill()
                print("UH OH")
                
                

class Paper():
    class Data(Rock.Data):
        sound = "crumble.mp3"
        image = pygame.image.load("./images/paper.png")
        image_small = pygame.transform.scale(image,(30,30))
        name = "paper"
        def __init__(self, direction:list=None,position:tuple=None):
            Rock.Data.__init__(self,direction,position)
            self.image = Paper.Data.image_small
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(10,Rock.Data.screen_rect.right),random.randint(10,Rock.Data.screen_rect.bottom)) if position == None else position
            self.direction = [random.choice(("up","down")),random.choice(("left","right"))] if direction == None else direction


class Scissors():
    class Data(Rock.Data):
        sound = "snip.mp3"
        image = pygame.image.load("./images/scissors.png")
        image_small = pygame.transform.scale(image,(30,30))
        name = "scissors"
        def __init__(self, direction:list=None,position:tuple=None):
            Rock.Data.__init__(self,direction,position)
            self.image = Scissors.Data.image_small
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(10,Rock.Data.screen_rect.right),random.randint(10,Rock.Data.screen_rect.bottom)) if position == None else position
            self.direction = [random.choice(("up","down")),random.choice(("left","right"))] if direction == None else direction


##################KILLSPRITES###################
class Skull():
    class Data(Rock.Data):
        image = pygame.image.load("./images/skull.png")
        def __init__(self,direction:list=None,position:tuple=None,length:int = 60):
            Rock.Data.__init__(self,direction,position)
            self.name = "skull"
            self.image = pygame.transform.scale(Skull.Data.image,(30,30))
            self.framecounter = 0
            self.max = length
            sounds.sounds["drip.mp3"].play()
        def update(self):
            self.framecounter += 1
            if self.framecounter > self.max:
                self.kill()
class Bomb():
    class Data(pygame.sprite.Sprite):
        image = pygame.image.load("./images/bomb.png")
        boom = (pygame.transform.scale(pygame.image.load("./images/boom.png"),(100,100)),pygame.transform.scale(pygame.image.load("./images/boom2.png"),(60,60)))

        #start at top
        #slowly fall at a rate increasing by 1%
        #when you hit the bottom, cause a large explosion
        #the explosion repeatedly iterates through the "boom" section

        def __init__(self,direction:list=None,position:tuple=None,target:int=None):
            pygame.sprite.Sprite.__init__(self)
            self.name = "bomb"
            self.image = pygame.transform.scale(Bomb.Data.image,(30,30))
            self.rect = self.image.get_rect()
    
            #positioning
            self.rect.center = (
                position[0],0) if position is not None else (random.randint(10,Rock.Data.screen_rect.right),
                0)

            sounds.sounds["ka.mp3"].play()
            
            #momentum
            self.momentum = .25
            #kaboom timing
            self.kaboomed = False
            self.kaboom_length = 0
            self.kaboom_frame = 0
            self.kaboom_frame_length = 0
            #target placement
            self.target = random.randint(Rock.Data.screen_rect.bottom//2,Rock.Data.screen_rect.bottom) if target is None else target
            

        def update(self):
            #explody-ing
            if self.kaboomed:
                self.kaboom()
                return
            #moving
            self.momentum = self.momentum*1.05
            self.rect.y += self.momentum
            if self.rect.bottom >= self.target:
                #playing silly sound
                sounds.sounds["boom.mp3"].play()
                #saving previous coordinate for placement
                prev_coord = tuple(self.rect.center)
                self.kaboomed = True
                self.image = Bomb.Data.boom[self.kaboom_frame]
                self.rect = self.image.get_rect()
                self.rect.center = prev_coord
                del prev_coord
            
                

        def kaboom(self):
            self.kaboom_length += 1
            self.kaboom_frame_length += 1
            if self.kaboom_frame_length >= 5:
                #resetting kaboom frame length
                self.kaboom_frame_length = 0
                #adding onto kaboom frame
                self.kaboom_frame = (self.kaboom_frame) + 1 if (self.kaboom_frame < (len(Bomb.Data.boom)-1)) else 0
                #replacing image
                prev_coord = tuple(self.rect.center)
                self.image = Bomb.Data.boom[self.kaboom_frame]
                self.rect = self.image.get_rect()
                self.rect.center = prev_coord
                del prev_coord
            if self.kaboom_length > 60:
                self.kill()
                
                
            
            
                
        


#THE OUTPUTS

characters = {
    "rock":Rock,
    "paper":Paper,
    "scissors":Scissors,
    # "patryk":Patryk,
    # "david":David,
    # "eli":Eli,
    # "peterson":Peterson,
    # "alex":Alex,
    # "michel":Michel,
    }

killcharacters = {
    "skull":Skull,
    "bomb":Bomb
    
}
