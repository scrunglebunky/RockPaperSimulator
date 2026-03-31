# PROGRAM BY ANDREW CHURCH
# MADE IN WINTER 2022 / SPRING 2023
import pygame,os,random,math,sys

# CHANGING THE WORKING DIRECTORY, IF THE PROGRAM IS RUNNING IN A PYINSTALLER BUNDLE -- thanks, pyinstaller ;)
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # print('Running via: PyInstaller Bundle')
    os.chdir(sys._MEIPASS)
else:
    # print('Running via: Python Process')
    pass

import files.sounds as sounds
from files.characters import characters as loaded_char
from files.characters import killcharacters as loaded_kill
# PROGRAM BY JABBLE.DEV SOMETIME IN 2022/2023.

#INITIALIZATION
pygame.font.init()
window = pygame.display.set_mode((600,450), pygame.SCALED)
pygame.display.set_caption("ROCK PAPER SCISSORS SIMULATOR")
pygame.display.set_icon(pygame.image.load("./images/icon.ico"))
clock = pygame.time.Clock()
run = True
FPS = 60
speed = 1
fullscreen = True
graphical = True
loop = False
bg = "random"
song_name = "random"
prev_vol = (0,0)


#GAMEPLAY ELEMENTS
sprites = pygame.sprite.Group()
killsprites = pygame.sprite.Group()
hierarchy_list = ["rock","scissors","paper"]



#PRELOADING ALL IMAGES
images = {}
for _ in os.listdir("./images/"):
    images[_] = pygame.image.load("./images/"+str(_))
backgrounds = {}
# for _ in os.listdir("./backgrounds/"):
#     backgrounds[_] = pygame.transform.scale(pygame.image.load("./backgrounds/"+str(_)),(window.get_width(),window.get_height()))
images["beats.png"] = pygame.transform.scale(images["beats.png"],(30,30))
images["beats_big.png"] = pygame.transform.scale(images["beats.png"],(50,50))


#LOADING TEXT
load_list = []
loaded_text = {}
#NUMBERS
load_list = [0,1,2,3,4,5,6,7,8,9]
for num in load_list:
    loaded_text[str(num)] = pygame.font.Font("./files/font.ttf",20)
    loaded_text[str(num)] = loaded_text[str(num)].render(str(num) if num != 1 else (str(num) + " "),False,"black","white")
def display_numbers(num:int,pos:tuple):
    num = str(num)
    for i in range(len(num)):
        window.blit(loaded_text[num[i]],(
            pos[0]+(loaded_text[num[i]].get_width()*i),
            pos[1]
            )) 

 
#MAKING A LIST OF WHO EATS WHO
#an entity will eat an entity the index below, get eaten by the index higher, and is unaffected by everyone else
#an entity at the lowest will be eaten by the highest, and the highest will eat the lowest


        

#SETTING VALUES FOR FUNSIES
#hierarchy_list = ["eli","patryk","david","scissors","paper","rock"]
#hierarchy_list = list(loaded_char.keys())
#random.shuffle(hierarchy_list)
#hierarchy_list = ["scissors","alex"]
#hierarchy_list = ["scissors","paper","rock"]
#hierarchy_list = ["scissors","michel"]


class GamePlayState():
    #startup
    def __init__(self,
                 amount_spawned:int=25,
                 timer_frames=600, #-1 means disabled
                 isglobal:bool = True #this is to ignore 
                 ):
        
        #copying the hierarchy list
        self.hierarchy_list = hierarchy_list.copy()

        #setting up hierarchy list spawn set
        #the hierarchy list contains the names, and the hierarchy list spawned contains the spawns
        self.hierarchy_list_spawned = []
        for _ in self.hierarchy_list:
            self.hierarchy_list_spawned.append([])

        #setting the background
        # if bg == "random" and len(backgrounds) > 0:
        #     self.bg = random.choice(list(backgrounds.keys()))
        # elif bg in backgrounds.keys():
        #     self.bg = bg
        # else:
        #     self.bg = None 
        self.bg = None
        
        #playing the music
        # if song_name == "random" and len(sounds.songs) > 0:
        #     song = random.choice(sounds.songs)
        #     sounds.play_song(song)
        # else:
        #     sounds.play_song(song_name) #errors handled in the module
            
        #spawning the characters
        for _ in range(len(self.hierarchy_list)):
            for i in range(amount_spawned):
                char = loaded_char[self.hierarchy_list[_]].Data()
                sprites.add(char)
                self.hierarchy_list_spawned[_].append(char)
                
        #UI VALUES
    
        self.started = False 
        self.finished = False
        self.name = "gameplay"
        self.ready_x = -30
        self.go_y = -30

        self.hurry_graphic_playing = False
        self.hurry_graphic_x = 0
        self.hurry_graphic_y = window.get_height() // 2

        self.win_graphic_playing = False
        self.win_graphic_frames = 0
        self.restart_y = 0
        self.winner = None
        
        self.hurry_timer = 0
        self.hurry_limit = timer_frames
        self.hurry_skull_counter = 0
        self.hurry_skull_max = random.randint(180,360)
        self.hurry_bomb_counter = 3199
        #self.hurry_bomb_max = random.randint(800,3200)
        self.hurry_bomb_max = 800

        #(1/9) * (((self.hurry_graphic_x)-30)**2) + (window.get_height()/2)
        

        
        
    #called every frame
    def update(self,debug=False):

        if self.finished:
            if loop: self.__init__()
            else:
                self.finish_graphic()
            return "complete"

        #GRAPHICAL UPDATE
            #this is called before everything because UI elements will appear up top, and will halt the program. sorry
        window.fill("black")
        if self.bg is not None: window.blit(backgrounds[self.bg],(0,0))
        sprites.draw(window)
        killsprites.draw(window)


        #GRAPHICAL "GET READY" CODE
        if not self.started:
            self.readygo_graphic()
            return "waiting.."
        #GRAPHICAL "HURRY" CODE
        if self.hurry_graphic_playing:
            self.hurry_graphic()
            return "hurry!"
        #GRAPHICAL "WIN" CODE
        if self.win_graphic_playing:
            self.win_graphic()
            return "winner!"



        #UPDATING ALL SPRITES
        sprites.update()
        killsprites.update()


        #COLLISION FOR CHARACTERS BEATING CHARACTERS
        for i in range(len(self.hierarchy_list)):
            
            for j in range(len(self.hierarchy_list_spawned[i])):
                
                #figuring out the list to check; this only exists because the first index cannot check the last index automatically like the others
                i_to_check = (i-1) if i!=0 else (len(self.hierarchy_list)-1)

                #checking for collision
                if self.hierarchy_list_spawned[i][j].rect.collidelist(self.hierarchy_list_spawned[i_to_check]) > -1:
                    
                    #IF a collision is detected, the character being iterated turns into the new character with the same position and direction
                    transformed = loaded_char[
                        self.hierarchy_list[i_to_check]].Data(
                            self.hierarchy_list_spawned[i][j].direction,
                            self.hierarchy_list_spawned[i][j].rect.center)

                    #adding the new sprite
                    self.hierarchy_list_spawned[i_to_check].append(transformed)
                    sprites.add(transformed)

                    #killing the old sprite
                    self.hierarchy_list_spawned[i][j].kill()
                    del self.hierarchy_list_spawned[i][j]


                    #playing goofy ahh sound
                    pygame.mixer.Channel(random.randint(0,9)).play(sounds.sounds[loaded_char[self.hierarchy_list[i_to_check]].Data.sound])

                    break

                #checking for collision with KILLSPRITES
                if len(pygame.sprite.spritecollide(self.hierarchy_list_spawned[i][j],killsprites,False)) > 0:
                    self.hierarchy_list_spawned[i][j].kill()
                    del self.hierarchy_list_spawned[i][j]
                    #print("DED",len(sprites))
                    break
                
                
            #killing extra lists if empty
            if len(self.hierarchy_list_spawned[i])==0 and len(self.hierarchy_list_spawned)>3:
                #print(hierarchy_list)
                del self.hierarchy_list_spawned[i]
                del self.hierarchy_list[i]
                break


        #CHECKING FOR WINNER
        total_full = []
        amounts = [len(_) for _ in self.hierarchy_list_spawned]
        for num in amounts:
            if num > 0:
                total_full.append(amounts.index(num))
        if len(total_full) == 1:
            #updating everything one last time for display
            killsprites.empty()
            sprites.draw(window)
            pygame.display.update()
            #print(hierarchy_list[total_full[0]],"WINS")
            sprites.empty()
            self.win_graphic_playing = True
            self.winner = self.hierarchy_list[total_full[0]]
            
        #HURRYUP
        self.hurry_timer += 1
        #the hurry graphic only plays for one gameplay frame, so it doesn't play duplicates and skips over after playing once
        if self.hurry_timer == self.hurry_limit and self.hurry_limit != -1:
            self.hurry_graphic_playing = True
            # sounds.play_song("hurry.mp3")
        if self.hurry_timer > self.hurry_limit and self.hurry_limit != -1:
            self.hurry_up()

        self.ui_beats((0,0))
        

    #called with controls
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.started = True if not self.started else self.started
            self.hurry_graphic_playing = False if self.hurry_graphic_playing else self.hurry_graphic_playing

            if self.win_graphic_playing:
                if event.button == 1:
                    self.__init__()
                elif event.button == 3:
                    self.finished = True

    #done when the game is starting
    def readygo_graphic(self):
        self.ready_x += 2
        if self.ready_x > 500:
            self.go_y += 5
        
        window.blit(
            images["ready.png"],
                (
                self.ready_x,
                (window.get_height()/2) - (images["ready.png"].get_height()/2)
                )
            )
        window.blit(
            images["go.png"],
                (
                (window.get_width()/2) - (images["go.png"].get_width()/2),
                self.go_y
                )
            )
        if self.go_y > 450:
            self.started = True
            
    def hurry_graphic(self):
        self.hurry_graphic_x += 5
        self.hurry_graphic_y = math.sin(self.hurry_graphic_x/50)*50 + ((window.get_height()/2)-(images["hurryup.png"].get_height()/2))
        window.blit(images["hurryup.png"],(self.hurry_graphic_x,self.hurry_graphic_y))
        if self.hurry_graphic_x > window.get_width():
            self.hurry_graphic_playing = False
        
    def win_graphic(self):
        if self.win_graphic_frames == 0:
            #FIRST FRAME - GATHERING STARTUP PHOTOS
            self.winner_icon = pygame.transform.scale(
                loaded_char[self.winner].Data.image,
                (100,
                 100))
            restart_scale = window.get_width() / images["restart.png"].get_width()
            images["restart.png"] = pygame.transform.scale(
                images["restart.png"],(
                    images["restart.png"].get_width()*restart_scale,
                    images["restart.png"].get_height()*restart_scale,
                ))
            self.restart_y = window.get_height() - images["restart.png"].get_height()
            self.winner_icon_y = (window.get_height()/2) - (self.winner_icon.get_height()/2)

            #sounds.sounds["tada.mp3"].set_volume(sounds.sounds["tada.mp3"].get_volume()*1.75)
            sounds.sounds["tada.mp3"].play()
                
        self.win_graphic_frames += 1

        #displaying restart
        window.blit(images["restart.png"],(0,self.restart_y))

        #displaying winner icon
        iconx = round(
            math.sin(self.win_graphic_frames/100)*250 - 50 + window.get_width()/2,
            2)
        icony = round(
            math.sin(iconx/25)*50+self.winner_icon_y ,
            2) 
        window.blit(
            self.winner_icon,(
                iconx,
                icony
                )
            )
        

    #causing a "oops you're taking too long time to die"
    def hurry_up(self):
        #print(self.hurry_skull_counter,self.hurry_skull_max,"|",self.hurry_bomb_counter,self.hurry_bomb_max)
        
        #skull counter
        self.hurry_skull_counter += 1
        if self.hurry_skull_counter >= self.hurry_skull_max:
            killsprites.add(loaded_kill["skull"].Data())
            self.hurry_skull_counter = 0
            self.hurry_skull_max = self.hurry_skull_max - 1 if self.hurry_skull_max > 5 else self.hurry_skull_max
        #bomb counter
        self.hurry_bomb_counter += 1
        if self.hurry_bomb_counter >= self.hurry_bomb_max:
            killsprites.add(loaded_kill["bomb"].Data())
            self.hurry_bomb_max /= 1.25
            self.hurry_bomb_counter = 0

    def ui_beats(self,position):
        subtractors = 0 
        for i in range(len(self.hierarchy_list)):
            if len(self.hierarchy_list_spawned[i]) > 0:
                #character
                window.blit(
                    loaded_char[self.hierarchy_list[i]].Data.image_small,
                    ((position[0]+(60*i)-(60*subtractors)),position[1])
                    )
                #"beats"
                if i != (len(self.hierarchy_list) - 1):
                    window.blit(
                        images["beats.png"],
                        ((position[0]+((60*i)+30)-(60*subtractors)),position[1])
                        )
                #character amount
                display_numbers(
                    str(len(self.hierarchy_list_spawned[i])),
                    ((position[0]+(60*i)-(60*subtractors)),position[1]+30)
                    )
                
            else:
                subtractors += 1
    
# current_state = StartMenu()
current_state = GamePlayState()

while run:

    graphical:clock.tick(FPS)

    for i in range(speed):
        current_state.update()

    for event in pygame.event.get():
        current_state.event_handler(event)
        if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
            run=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_g:
                graphical = False if graphical else True
            if event.key == pygame.K_m:
                sounds.pygame.mixer.stop()
            if event.key == pygame.K_LEFT and speed>1:
                speed -= 1
            if event.key == pygame.K_RIGHT:
                speed += 1
            if event.key == pygame.K_RETURN:
                try:print("---\n"+str(current_state.hierarchy_list)+'\n'+str([len(_) for _ in current_state.hierarchy_list_spawned]))
                except:pass
            if event.key == pygame.K_l:
                loop = True if not loop else False
                

    if graphical:pygame.display.update()

    #changing state if menu is complete
    if current_state.finished:
        if current_state.name == "menu":
            current_state = GamePlayState()
        else:
            run=False

pygame.display.quit()

