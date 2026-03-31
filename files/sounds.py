import pygame,os
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
sounds = {}
# songs = os.listdir("./music/")
volumes = [0.5,0.25]

for sound in os.listdir("./sounds"):
    try:
        sounds[sound] = pygame.mixer.Sound(("./sounds/"+sound))
        sounds[sound].set_volume(volumes[0])
    except Exception as e:
        print(e)

# def play_song(song):
#     if song not in songs: return "file no found"
#     pygame.mixer.music.load("./music/"+str(song))
#     pygame.mixer.music.set_volume(volumes[1])
#     pygame.mixer.music.play(loops=-1)
# def pause_song():
#     pygame.mixer.music.pause()
# def stop_song():
#     pygame.mixer.music.stop()
