import pygame
import sys
import surface
import game
import load_game
import settings
import leaderboards
import color as c
import os


class Menu(surface.Surface):
    def __init__(self):
        super().__init__()
        self.buttons_list = self.set_buttons()

    def set_buttons(self):
        button_image = pygame.image.load('icon/menu_option.png')
        new_game_button = surface.Button(self.screen, button_image, 200, 100, "New Game", self.new_game)
        load_game_button = surface.Button(self.screen, button_image, 200, 200, "Load Game", self.load_game)
        settings_button = surface.Button(self.screen, button_image, 200, 300, "Settings", self.settings)
        leaderboards_button = surface.Button(self.screen, button_image, 200, 400, "Leaderboards", self.leaderboards)
        exit_game_button = surface.Button(self.screen, button_image, 200, 500, "Quit", self.exit_game)
        buttons_list = [new_game_button, load_game_button, settings_button, leaderboards_button, exit_game_button]
        return buttons_list

    def draw(self):
        self.draw_background()
        self.draw_logo()
        self.draw_buttons()

    def draw_buttons(self):
        button_font = pygame.font.Font(self.font_path, 30)
        for button in self.buttons_list:
            button.add()
            mouse_on_button = self.mouse_on_button(button, 200, 70)
            self.add_text_on_button(button, button_font, (c.white if mouse_on_button else c.black),
                                    (button.x_start + 100, button.y_start + 35))

    @staticmethod
    def new_game():
        game.run()

    @staticmethod
    def load_game():
        path = "game_save.txt"
        if os.path.isfile(path):
            load_game.run()

    @staticmethod
    def settings():
        settings.run()

    @staticmethod
    def leaderboards():
        leaderboards.run()

    @staticmethod
    def exit_game():
        sys.exit(0)

    def handle_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons_list:
                        mouse_is_pressed_on_button = self.mouse_is_pressed_on_button(button, 200, 70)
                        if mouse_is_pressed_on_button:
                            button.action()
            self.draw()
            pygame.display.update()


def run():
    menu = Menu()
    menu.handle_events()











