import pygame
import sys
import os
import surface
import color as c
import menu


class Settings(surface.Surface):
    def __init__(self):
        super().__init__()
        self.text_font = pygame.font.Font(self.font_path, 30)

        self.username = UsernameEntry()
        self.level_buttons_list, self.design_buttons_list, self.menu_buttons_list = self.set_buttons()

    def set_buttons(self):
        settings_image = pygame.image.load('icon/settings_option.png')
        settings_menu_image = pygame.image.load('icon/settings_option_2.png')

        # create level buttons
        easy_button = surface.Button(self.screen, settings_image, 130, 210, "Easy", self.set_level, 1)
        medium_button = surface.Button(self.screen, settings_image, 245, 210, "Medium", self.set_level, 2)
        hard_button = surface.Button(self.screen, settings_image, 360, 210, "Hard", self.set_level, 3)
        level_buttons_list = [easy_button, medium_button, hard_button]

        # create design buttons
        black_button = surface.Button(self.screen, settings_image, 15, 310, "Black", self.set_design, "black")
        dark_blue_button = surface.Button(self.screen, settings_image, 130, 310, "Dark Blue", self.set_design,
                                          "dark blue")
        dark_green_button = surface.Button(self.screen, settings_image, 245, 310, "Dark Green", self.set_design,
                                           "dark green")
        dark_red_button = surface.Button(self.screen, settings_image, 360, 310, "Dark Red", self.set_design,
                                         "dark red")
        dark_gray_button = surface.Button(self.screen, settings_image, 475, 310, "Dark Gray", self.set_design,
                                          "dark gray")

        design_buttons_list = [black_button, dark_blue_button, dark_green_button, dark_red_button, dark_gray_button]

        # create menu buttons
        confirm_button = surface.Button(self.screen, settings_menu_image, 20, 450, "Confirm",
                                        self.confirm_settings)
        reset_button = surface.Button(self.screen, settings_menu_image, 210, 450, "Reset settings",
                                      self.reset_settings)
        exit_button = surface.Button(self.screen, settings_menu_image, 400, 450, "Quit", self.exit_settings)
        menu_buttons_list = [confirm_button, reset_button, exit_button]

        # set which buttons will be selected
        path = "settings.txt"
        if os.path.isfile(path):
            file = open(path, "r")
            file_list = [line.strip() for line in file.readlines()]
            level = int(file_list[1])
            design = file_list[2]
            for button in level_buttons_list:
                if level == button.file_property:
                    button.selected = True
            for button in design_buttons_list:
                if design == button.file_property:
                    button.selected = True
        else:
            easy_button.selected = True
            black_button.selected = True

        return level_buttons_list, design_buttons_list, menu_buttons_list

    def draw(self):
        self.draw_background()
        self.draw_logo()
        self.draw_username()
        self.draw_buttons()

    def draw_username(self):
        self.add_text_on_screen(self.screen, "Enter username", self.text_font, c.white, (110, 100))
        pygame.draw.rect(self.screen, c.white, (15, 120, 250, 40))
        self.add_text_on_screen(self.screen, f"{self.username.text}", self.text_font, c.blue, (132.5, 140))

    def draw_buttons(self):
        button_font = pygame.font.Font(self.font_path, 15)

        self.add_text_on_screen(self.screen, "Difficulty level", self.text_font, c.white, (100, 190))
        self.add_text_on_screen(self.screen, "Design", self.text_font, c.white, (55, 290))

        for button in (self.level_buttons_list + self.design_buttons_list):
            button.add()
            mouse_on_button = self.mouse_on_button(button, 100, 50)
            self.add_text_on_button(button, button_font,
                                    (c.white if mouse_on_button else (c.blue if button.selected else c.black)),
                                    (button.x_start + 50, button.y_start + 25))

        for button in self.menu_buttons_list:
            button.add()
            mouse_on_button = self.mouse_on_button(button, 180, 100)
            self.add_text_on_button(button, button_font, (c.white if mouse_on_button else c.black),
                                    (button.x_start + 90, button.y_start + 50))

    def set_level(self, button):
        for level_button in self.level_buttons_list:
            if level_button.selected:
                level_button.selected = False
        button.selected = True

    def set_design(self, button):
        for design_button in self.design_buttons_list:
            if design_button.selected:
                design_button.selected = False
        button.selected = True

    def confirm_settings(self):
        path = "settings.txt"
        file = open(path, "w")

        if self.username:
            file.write(f"{self.username.text}\n")
        else:
            file.write("User1\n")
        for level_button in self.level_buttons_list:
            if level_button.selected:
                file.write(f"{level_button.file_property}\n")

        for design_button in self.design_buttons_list:
            if design_button.selected:
                file.write(f"{design_button.file_property}\n")
        file.close()

    def reset_settings(self):
        self.username.text = "User1"
        for index in range(3):
            if index == 0:
                self.level_buttons_list[index].selected = True
            else:
                self.level_buttons_list[index].selected = False

        for index in range(5):
            if index == 0:
                self.design_buttons_list[index].selected = True
            else:
                self.design_buttons_list[index].selected = False

    @staticmethod
    def exit_settings():
        menu.run()

    def handle_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in (self.menu_buttons_list + self.level_buttons_list + self.design_buttons_list):
                        mouse_is_pressed_on_button = (self.mouse_is_pressed_on_button(
                            button,
                            180 if button in self.menu_buttons_list else 100,
                            100 if button in self.menu_buttons_list else 50))
                        if mouse_is_pressed_on_button:
                            if button in self.menu_buttons_list:
                                button.action()
                            else:
                                button.action(button)

                    self.username.set_editable()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_settings()

                    if self.username.editable:
                        if event.key == pygame.K_DELETE:
                            self.username.delete_text()
                        if event.key == pygame.K_BACKSPACE:
                            self.username.remove_last_character()
                        else:
                            self.username.update_text(event.unicode)

            self.draw()
            pygame.display.update()


class UsernameEntry:
    def __init__(self):
        self.text = self.set_text()
        self.editable = False

    def set_text(self):
        path = "settings.txt"
        if os.path.isfile(path):
            file = open(path, "r")
            file_list = [line.strip() for line in file.readlines()]
            text = str(file_list[0])
        else:
            text = "User1"
        return text

    def mouse_on_entry(self):
        mouse = pygame.mouse.get_pos()
        if 275 > mouse[0] > 15 and 160 > mouse[1] > 120:
            mouse_on_entry = True
        else:
            mouse_on_entry = False
        return mouse_on_entry

    def set_editable(self):
        mouse_on_entry = self.mouse_on_entry()
        click = pygame.mouse.get_pressed()
        if mouse_on_entry:
            if click[0]:
                self.editable = True
        else:
            if click[0]:
                self.editable = False

    def update_text(self, character):
        if len(self.text) <= 15:
            self.text += character

    def remove_last_character(self):
        self.text = self.text[:-1]

    def delete_text(self):
        self.text = ""


def run():
    settings = Settings()
    settings.handle_events()