import pygame, sys

from screen import Screen
from settings import *

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 屏幕大小
        self.clock = pygame.time.Clock() # 时钟
        pygame.display.set_caption("PSB Battle Game") # 窗口标题
        self.screen.fill(BACKGROUND_COLOR) # 背景颜色
        self.screen_manager = Screen()
    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.screen_manager.setup(self.screen, events, dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()