import pygame

from button import Button
from support import load_images
from settings import *

#  屏幕选项
class Screen:

    def __init__(self):
        self.units = []
        self.rects = []
        self.selected_indices = set()  # 用于跟踪已选择的图片索引

        self.load_images()

        self.game_started = False
        self.game_loading = False
        self.servant_select = False

        self.buttons = [
            Button("Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50),
            Button("Loading Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        ]
        self.create_player_button = Button("Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

    def setup(self, screen, events, dt): # 初始化主屏幕
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.buttons[0].rect.collidepoint(event.pos):
                    self.game_started = True  # 更新游戏状态
                    self.game_loading = False
                elif self.buttons[1].rect.collidepoint(event.pos):
                    self.game_started = False  # 更新游戏状态
                    self.game_loading = True  # 更新游戏状态

                if len(self.units) >= 3:
                    if self.create_player_button.rect.collidepoint(event.pos):
                        print("create player....")

                if self.servant_select:
                    for index, rect in enumerate(self.rects):
                        if rect.collidepoint(event.pos):
                            if index in self.selected_indices:
                                print(f'取消选择图片: {index}')
                                self.units.remove(index)  # 从单位中移除
                                self.selected_indices.remove(index)  # 从已选择中移除
                            else:
                                print(f'选择图片: {index}')
                                self.units.append(index)  # 添加角色
                                self.selected_indices.add(index)  # 记录已选择的索引

        if self.game_started:
            # print(f'start game...{dt}')
            self.servant_select = True  # 更新游戏状态
            self.show_character_creation(screen) # 创建玩家
        elif self.game_loading:
            print(f'loading game...{dt}')
        else:
            for button in self.buttons:
                button.draw(screen)

    def show_character_creation(self, screen):
        screen.fill((100, 100, 100))  # 改变背景颜色
        font = pygame.font.Font(None, 48) # 设置字体大小
        text_surface = font.render("Create Player", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text_surface, text_rect) # 显示文本

        for index, image in enumerate(self.images):
            # 判断该图片是否被选中
            if index in self.selected_indices:
                # 创建一个新的表面，并填充颜色
                colored_image = image.copy()
                colored_image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)  # 红色覆盖
                screen.blit(colored_image, self.rects[index])  # 绘制变色的图片
            else:
                screen.blit(image, self.rects[index])  # 绘制正常图片

        # 绘制创建角色的按钮
        is_active = True
        if len(self.units) < 3:
            is_active = False
        self.create_player_button.draw(screen, is_active)

    def load_images(self):
        self.images = load_images("./assets/servant", (100, 300)) # 加载图片
        # 并列绘制图片
        x_offset = 35  # 起始 X 位置
        y_position = 100  # Y 位置
        spacing = 5  # 图片之间的间距

        for image in self.images:
            rect = image.get_rect(topleft=(x_offset, y_position))  # 创建一个新的矩形
            self.rects.append(rect)  # 将矩形添加到列表中
            x_offset += image.get_width() + spacing  # 更新下一个图片的 X 位置
