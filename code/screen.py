import random

import pygame

from button import Button
from servant import Servant
from support import load_images
from settings import *

#  屏幕选项
class Screen:

    def __init__(self):
        self.units = [] # 存储选择的单位
        self.rects = [] # 存储单位选择框
        self.selected_indices = set()  # 用于跟踪已选择的图片索引
        self.names = {}  # 用于存储角色名字

        self.load_images()

        self.game_started = False # 开始游戏状态
        self.game_loading = False # 加载游戏状态
        self.servant_select = False # 选择单位状态
        self.battle = False # 战斗状态

        self.buttons = [
            Button("Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50),
            Button("Loading Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
        ]
        self.create_player_button = Button("Start Game", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)

        self.current_input_index = None  # 当前正在输入的角色索引
        self.input_texts = [""] * len(self.images)  # 每个图片的输入文本列表

        self.units_created = False  # 添加一个标志来控制单位的创建
        self.battle_scene = False  # 添加一个标志来表示是否进入战斗场景

        self.scene = 1 # 当前关卡
        self.players = [] # 存储玩家单位
        self.ai_players = [] # 存储AI单位
        self.player_battle = True # 是否是ai攻击
        self.attacker = 0 # 攻击者

    def setup(self, screen, events, dt): # 初始化主屏幕
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started and not self.game_loading:  # 仅在游戏未开始且未加载时处理按钮点击
                    if self.buttons[0].rect.collidepoint(event.pos):
                        self.game_started = True
                        self.game_loading = False
                    elif self.buttons[1].rect.collidepoint(event.pos):
                        self.game_started = False
                        self.game_loading = True

                if len(self.units) >= 3 and len(self.names) == len(self.units):  # 如果选择了3个单位且每个单位都有名字
                    if self.create_player_button.rect.collidepoint(event.pos):
                        self.create_units() # 创建玩家单位
                        self.create_ai_player()  # 创建ai玩家
                        self.units_created = True # 设置标志为 True，避免重复创建
                        self.battle_scene = True

                if self.servant_select: # 处于选择角色状态
                    for index, rect in enumerate(self.rects):
                        if rect.collidepoint(event.pos):
                            if index in self.selected_indices:
                                print(f'取消选择图片: {index}')
                                self.units.remove(index)  # 从单位中移除
                                self.selected_indices.remove(index)  # 从已选择中移除
                                self.names.pop(index, None)  # 移除对应名字
                                self.input_texts[index] = ""  # 清空输入文本
                            else:
                                print(f'选择图片: {index}')
                                self.units.append(index)  # 添加角色
                                self.selected_indices.add(index)  # 记录已选择的索引


                if self.battle:
                    for index, player in enumerate(self.players):
                        if player.rect.collidepoint(event.pos):
                            print(f'选择玩家: {index}')

            # 处理文本输入
            for index in range(len(self.rects)):
                input_box_rect = pygame.Rect(self.rects[index].topleft[0], self.rects[index].bottom + 10, 80,
                                             40)
                if event.type == pygame.MOUSEBUTTONDOWN and input_box_rect.collidepoint(event.pos):
                    self.current_input_index = index  # 设置当前输入索引

                if self.current_input_index == index:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_texts[index] = self.input_texts[index][:-1]  # 删除最后一个字符
                        elif event.key == pygame.K_RETURN:
                            self.names[index] = self.input_texts[index]  # 保存角色名字
                            self.current_input_index = None  # 清空当前输入索引
                        else:
                            self.input_texts[index] += event.unicode  # 添加输入字符

        if self.battle_scene:
            self.servant_select = False  # 更新游戏状态
            self.battle = True # 进入战斗场景
            self.show_battle_scene(screen)
        else:
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

                # 在选中的图片下方绘制输入框
                input_box_rect = pygame.Rect(self.rects[index].topleft[0], self.rects[index].bottom + 10, 80, 40)
                pygame.draw.rect(screen, (255, 255, 255), input_box_rect)  # 绘制输入框背景
                input_surface = font.render(self.input_texts[index], True, (0, 0, 0))  # 绘制输入的文本
                screen.blit(input_surface, (input_box_rect.x + 5, input_box_rect.y + 5))
            else:
                screen.blit(image, self.rects[index])  # 绘制正常图片

        # 绘制创建角色的按钮
        is_active = True
        if len(self.units) < 3 or not len(self.units) == len(self.names):
            is_active = False
        self.create_player_button.draw(screen, is_active)

    def show_battle_scene(self, screen): # 战斗的画面
        # 在这里渲染战斗场景的内容
        screen.fill((0, 0, 0))  # 填充黑色背景
        font = pygame.font.Font(None, 48)
        text_surface = font.render(f"Battle Scene {self.scene}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text_surface, text_rect)  # 显示战斗场景的文本

        # 渲染单位
        spacing = 50  # 单位之间的间距

        start_x = SCREEN_WIDTH // 2 - (len(self.players) * (50 + spacing) // 2)  # 计算起始 X 位置
        up_y = 120 # 上半区位置
        down_y = SCREEN_HEIGHT // 2 + 50  # 下半区位置

        box_width = 50  # 框的宽度
        box_height = 120  # 框的高度，增加高度以容纳名称
        hp_bar_height = 10  # 血条高度
        exp_bar_height = 5  # 经验条高度

        # 渲染玩家
        for index, servant in enumerate(self.players):
            unit_x = start_x + index * (box_width + spacing)
            unit_y = down_y

            # 绘制框
            pygame.draw.rect(screen, (50, 50, 50), (unit_x, unit_y, box_width, box_height))  # 框的背景

            # 绘制等级
            level_text = f"Level: {servant.level}"  # 假设 Servant 类有一个 level 属性
            font = pygame.font.Font(None, 20)
            level_surface = font.render(level_text, True, (255, 255, 255))
            screen.blit(level_surface, (unit_x + 5, unit_y + 5))  # 显示等级

            # 绘制单位的图片
            screen.blit(servant.image, (unit_x, unit_y + 30))  # 绘制单位图片

            # 绘制血条
            hp = servant.hp  # 假设 Servant 类有一个 hp 属性
            pygame.draw.rect(screen, (255, 0, 0), (unit_x, unit_y + 80, box_width, hp_bar_height))  # 背景
            pygame.draw.rect(screen, (0, 255, 0),
                             (unit_x, unit_y + 80, box_width * (hp / 100), hp_bar_height))  # 血条

            # 绘制经验条
            exp = servant.exp  # 假设 Servant 类有一个 exp 属性
            pygame.draw.rect(screen, (255, 255, 0), (unit_x, unit_y + 95, box_width, exp_bar_height))  # 背景
            pygame.draw.rect(screen, (0, 0, 255),
                             (unit_x, unit_y + 95, box_width * (exp / 100), exp_bar_height))  # 经验条

            # 绘制玩家名称
            name_text = f"{servant.name}"  # 假设 Servant 类有一个 name 属性
            name_surface = font.render(name_text, True, (255, 255, 255))
            screen.blit(name_surface, (unit_x + 5, unit_y + 105))  # 显示玩家名称

        # 渲染ai
        for index, servant in enumerate(self.ai_players):
            unit_x = start_x + index * (box_width + spacing)
            unit_y = up_y

            # 绘制框
            pygame.draw.rect(screen, (50, 50, 50), (unit_x, unit_y, box_width, box_height))  # 框的背景

            # 绘制等级
            level_text = f"Level: {servant.level}"  # 假设 Servant 类有一个 level 属性
            font = pygame.font.Font(None, 20)
            level_surface = font.render(level_text, True, (255, 255, 255))
            screen.blit(level_surface, (unit_x + 5, unit_y + 5))  # 显示等级

            # 绘制单位的图片
            screen.blit(servant.image, (unit_x, unit_y + 30))  # 绘制单位图片

            # 绘制血条
            hp = servant.hp  # 假设 Servant 类有一个 hp 属性
            pygame.draw.rect(screen, (255, 0, 0), (unit_x, unit_y + 80, box_width, hp_bar_height))  # 背景
            pygame.draw.rect(screen, (0, 255, 0),
                             (unit_x, unit_y + 80, box_width * (hp / 100), hp_bar_height))  # 血条

            # 绘制经验条
            exp = servant.exp  # 假设 Servant 类有一个 exp 属性
            pygame.draw.rect(screen, (255, 255, 0), (unit_x, unit_y + 95, box_width, exp_bar_height))  # 背景
            pygame.draw.rect(screen, (0, 0, 255),
                             (unit_x, unit_y + 95, box_width * (exp / 100), exp_bar_height))  # 经验条

            # 绘制玩家名称
            name_text = f"{servant.name}"  # 假设 Servant 类有一个 name 属性
            name_surface = font.render(name_text, True, (255, 255, 255))
            screen.blit(name_surface, (unit_x + 5, unit_y + 105))  # 显示玩家名称

        # 展示当前攻击方
        if self.player_battle:
            font = pygame.font.Font(None, 30)
            text_surface = font.render(f"player attacker {self.players[self.attacker].name}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)  # 显示战斗场景的文本

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

    def create_ai_player(self):
        # 根据玩家的队伍数量生成ai
        numbers = random.choices(range(7), k=len(self.players))
        spacing = 50  # 单位之间的间距
        start_x = SCREEN_WIDTH // 2 - (len(self.units) * (50 + spacing) // 2)  # 计算起始 X 位置
        start_y = SCREEN_HEIGHT // 2 + 50  # 下半区位置
        for index, number in enumerate(numbers):
            unit_x = start_x + index * (50 + spacing)
            unit_y = start_y
            servant = Servant(number, self.images[number], (50, 50), unit_x, unit_y, 'ai', f'AI{random.randint(1, 9999)}')
            self.ai_players.append(servant)

    def create_units(self):
        spacing = 50  # 单位之间的间距
        start_x = SCREEN_WIDTH // 2 - (len(self.units) * (50 + spacing) // 2)  # 计算起始 X 位置
        start_y = SCREEN_HEIGHT // 2 + 50  # 下半区位置
        for index, unit in enumerate(self.units):
            unit_x = start_x + unit * (50 + spacing)
            unit_y = start_y
            # 第一个选择的玩家先攻击
            servant = Servant(unit, self.images[unit], (50, 50), unit_x, unit_y, 'player', self.names[unit])
            self.players.append(servant)
