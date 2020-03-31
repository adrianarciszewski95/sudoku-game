import pygame
import os
import color as c


class Surface:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Sudoku')

        self.icon = pygame.image.load('icon/ikona.png')
        pygame.display.set_icon(self.icon)

        pygame.font.init()
        self.font_path = pygame.font.match_font('calibri')
        self.color = self.set_color()

    def draw_background(self):
        self.screen.fill(self.color)

    def draw_logo(self):
        game_logo = pygame.image.load('icon/logo.png')
        self.screen.blit(game_logo, (0, 0))

    @staticmethod
    def set_color():
        color = None
        path = "settings.txt"
        if os.path.isfile(path):
            file = open(path, "r")
            file_list = [line.strip() for line in file.readlines()]
            design = file_list[2]
            if design == "black":
                color = c.black
            if design == "dark blue":
                color = c.dark_blue
            if design == "dark green":
                color = c.dark_green
            if design == "dark red":
                color = c.dark_red
            if design == "dark gray":
                color = c.dark_gray
        else:
            color = c.black
        return color

    @staticmethod
    def mouse_on_button(button, width, height):
        mouse = pygame.mouse.get_pos()
        mouse_on_button = False

        if button.x_start + width > mouse[0] > button.x_start and button.y_start + height > mouse[1] > button.y_start:
            mouse_on_button = True

        return mouse_on_button

    def mouse_is_pressed_on_button(self, button, width, height):
        click = pygame.mouse.get_pressed()
        mouse_is_pressed_on_button = False

        if self.mouse_on_button(button, width, height):
            if click[0] == 1:
                mouse_is_pressed_on_button = True

        return mouse_is_pressed_on_button

    @staticmethod
    def add_text_on_screen(surf, text, font, color, center):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = center
        surf.blit(text_surface, text_rect)

    def add_text_on_button(self, button, font, color, center):
        self.add_text_on_screen(self.screen, button.text, font, color, center)


class Button:
    def __init__(self, surface, image, x_start, y_start, text, action, file_property=None):
        self.surface = surface
        self.image = image
        self.x_start = x_start
        self.y_start = y_start
        self.text = text
        self.action = action
        self.file_property = file_property
        self.selected = False

    def add(self):
        self.surface.blit(self.image, (self.x_start, self.y_start))



