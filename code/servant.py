import pygame

class Servant:
    servant_name = ['saber', 'archer', 'lancer', 'rider', 'caster', 'assassin', 'berserker']

    def __init__(self, index, image, size):
        self.servant_class = self.servant_name[index]
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.select = False
