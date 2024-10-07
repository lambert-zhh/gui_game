import os

import pygame

def load_images(path, size):
    images = []
    for _, _, image_files in os.walk(path):
        for image in image_files:
            full_path = path + "/" + image
            image = pygame.image.load(full_path).convert_alpha()  # 加载并转换图像
            image = pygame.transform.scale(image, size)  # 缩小图像
            images.append(image)
    return images

