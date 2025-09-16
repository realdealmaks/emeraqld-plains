
import pygame, random

#Inicializacija
pygame.init()

#Definicija zaslona
s = 500
v = 300
zaslon = pygame.display.set_mode((s, v))

#Barve
bela = (255, 255, 255)
rdeca = (255, 0, 0)
rumena = (255, 255, 0)
ena_barva = (128, 128, 128)

#Definicija koordinat
kv_x = 0
kv_y = 0

random_st = random.randint(1, 40)
barva_k = ena_barva

#Zapiranje okna
running = True

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pozicija = event.pos #koordinate miške
            kv_x = pozicija[0] #zapis x koordinate
            kv_y = pozicija[1] #zapis y koordinate
            if event.button == 3:
                barva_k = rumena

            

    #Barvanje zaslona
    zaslon.fill(bela)

    #Risanje kvadrata
    pygame.draw.rect(zaslon, barva_k, (kv_x, kv_y, random_st, random_st))

    #Posodobitev zaslona

    pygame.display.update()


pygame.quit()
