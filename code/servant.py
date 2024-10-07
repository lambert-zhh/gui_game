import random

import pygame

class Servant:
    servant_name = ['saber', 'archer', 'lancer', 'rider', 'caster', 'assassin', 'berserker']

    def __init__(self, index, image, size, x, y, camp, name, level=1):
        self.servant_class = self.servant_name[index]
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.select = False

        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 50, 50)  # 假人的矩形表示
        self.hp = 100  # 生命值
        self.atk = self.random_atk()  # 攻击力
        self.def_ = self.random_def_()  # 防御力
        self.exp = 0  # 经验值
        self.level = level # 等级
        self.camp = camp  # 阵营
        self.name = name  # 名称

    def random_atk(self): # 随机生成攻击力
        if self.servant_class == 'saber':
            return random.randint(5, 20)
        elif self.servant_class == 'archer':
            return random.randint(7, 15)
        elif self.servant_class == 'lancer':
            return random.randint(3, 17)
        elif self.servant_class == 'rider':
            return random.randint(1, 10)
        elif self.servant_class == 'caster':
            return random.randint(15, 20)
        elif self.servant_class == 'assassin':
            return random.randint(8, 16)
        elif self.servant_class == 'berserker':
            return random.randint(20, 25)
        else:
            return random.randint(10, 30)

    def random_def_(self): # 随机生成防御力
        if self.servant_class == 'saber':
            return random.randint(5, 10)
        elif self.servant_class == 'archer':
            return random.randint(3, 7)
        elif self.servant_class == 'lancer':
            return random.randint(7, 12)
        elif self.servant_class == 'rider':
            return random.randint(10, 15)
        elif self.servant_class == 'caster':
            return random.randint(1, 8)
        elif self.servant_class == 'assassin':
            return random.randint(1, 6)
        elif self.servant_class == 'berserker':
            return random.randint(0, 6)
        else:
            return random.randint(5, 15)

    def attack(self, target, attack_logs):
        """攻击目标，返回True如果目标被移除，否则返回False"""
        is_gone = False

        # 计算伤害
        damage = self.atk - target.def_ + random.randint(-5, 10)
        damage = max(0, damage)  # 确保伤害不为负

        # 更新目标生命值
        target.hp -= damage

        # 计算经验
        self.exp += damage
        target.exp += target.def_

        # 经验值奖励
        if damage > 10:
            target.exp += int(0.2 * target.def_)
        elif damage <= 0:
            target.exp += int(0.5 * target.def_)

        # 检查目标是否被移除
        if target.hp <= 0:
            target.hp = 0  # 确保生命值不为负
            is_gone = True
        else:
            if target.exp >= 100:
                target.level += 1
                target.exp -= 100

        # 检查攻击者是否升级
        while self.exp >= 100:
            self.level += 1
            self.exp -= 100

        # 输出攻击结果，并记录到日志
        # log_entry = (f"[Game Message]time {datetime.datetime.now()} {self.name} attacked "
        #              f"{target.name} for {damage} damage!: +{damage}EXP")
        # attack_logs.append(log_entry)
        # self.save_log_to_file(log_entry)  # 将日志保存到文件

        return is_gone  # 目标未被移除
