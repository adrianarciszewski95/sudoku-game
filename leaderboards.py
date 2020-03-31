import pygame
import sys
import surface
import menu
import color as c
import sqlraw


class Leaderboard(surface.Surface):
    def __init__(self):
        super().__init__()
        self.buttons_list = self.set_buttons()
        self.arrows_list = self.set_arrows()
        self.level_text = "Easy"

    def set_buttons(self):
        leaderboards_image = pygame.image.load('icon/settings_option_2.png')

        reset_button = surface.Button(self.screen, leaderboards_image, 80, 480, "Reset statistics",
                                      self.reset_statistics)
        exit_button = surface.Button(self.screen, leaderboards_image, 340, 480, "Quit", self.exit_leaderboards)
        buttons_list = [reset_button, exit_button]
        return buttons_list

    def set_arrows(self):
        left_arrow_image = pygame.image.load('icon/left_arrow.png')
        right_arrow_image = pygame.image.load('icon/right_arrow.png')
        left_arrow = surface.Button(self.screen, left_arrow_image, 100, 90, None, self.left_arrow)
        right_arrow = surface.Button(self.screen, right_arrow_image, 435, 90, None, self.right_arrow)
        arrows_list = [left_arrow, right_arrow]
        return arrows_list

    def get_statistics(self):
        """
        get statistics from database
        """
        if self.level_text == "Easy":
            sqlraw.cursor.execute("""
            SELECT player, time, hints FROM statistics
            WHERE level = "easy" ORDER BY time ASC LIMIT 10 
            """)
        elif self.level_text == "Medium":
            sqlraw.cursor.execute("""
            SELECT player, time, hints FROM statistics
            WHERE level = "medium" ORDER BY time ASC LIMIT 10 
            """)
        elif self.level_text == "Hard":
            sqlraw.cursor.execute("""
            SELECT player, time, hints FROM statistics
            WHERE level = "hard" ORDER BY time ASC LIMIT 10 
            """)
        received_statistics = sqlraw.cursor.fetchall()
        statistics = [(stats['player'], stats['time'], stats['hints']) for stats in received_statistics]
        return statistics

    def draw(self):
        self.draw_background()
        self.draw_logo()
        self.draw_level_text()
        self.draw_buttons()
        self.draw_arrows()
        self.draw_grid()
        self.draw_statistics()

    def draw_level_text(self):
        level_text_font = pygame.font.Font(self.font_path, 30)
        self.add_text_on_screen(self.screen, self.level_text, level_text_font, c.white, (300, 110))

    def draw_buttons(self):
        button_font = pygame.font.Font(self.font_path, 15)
        for button in self.buttons_list:
            button.add()
            mouse_on_button = self.mouse_on_button(button, 180, 100)
            self.add_text_on_button(button, button_font, (c.white if mouse_on_button else c.black),
                                    (button.x_start + 90, button.y_start + 50))

    def draw_arrows(self):
        for arrow in self.arrows_list:
            arrow.add()

    def draw_grid(self):
        pygame.draw.rect(self.screen, c.gray, (100, 140, 400, 30))
        pygame.draw.rect(self.screen, c.white, (100, 170, 400, 300))

        line_y = 140
        for i in range(11):
            pygame.draw.line(self.screen, self.color, (100, line_y), (500, line_y), 2)
            line_y += 30

        pygame.draw.line(self.screen, self.color, (150, 140), (150, 470), 2)
        pygame.draw.line(self.screen, self.color, (300, 140), (300, 470), 2)
        pygame.draw.line(self.screen, self.color, (400, 140), (400, 470), 2)

    def draw_statistics(self):
        stats_font = pygame.font.Font(self.font_path, 20)
        statistics = self.get_statistics()

        self.add_text_on_screen(self.screen, "Rank", stats_font, c.red, (125, 155))
        self.add_text_on_screen(self.screen, "Player", stats_font, c.red, (225, 155))
        self.add_text_on_screen(self.screen, "Time", stats_font, c.red, (350, 155))
        self.add_text_on_screen(self.screen, "Hints", stats_font, c.red, (450, 155))

        y_center = 185
        for i in range(len(statistics)):
            self.add_text_on_screen(self.screen, str(i+1), stats_font, c.black, (125, y_center))
            self.add_text_on_screen(self.screen, statistics[i][0], stats_font, c.black, (225, y_center))
            self.add_text_on_screen(self.screen, statistics[i][1], stats_font, c.black, (350, y_center))
            self.add_text_on_screen(self.screen, str(statistics[i][2]), stats_font, c.black, (450, y_center))
            y_center += 30

    def left_arrow(self):
        if self.level_text == "Easy":
            self.level_text = "Hard"
        elif self.level_text == "Medium":
            self.level_text = "Easy"
        elif self.level_text == "Hard":
            self.level_text = "Medium"
        return self.level_text

    def right_arrow(self):
        if self.level_text == "Easy":
            self.level_text = "Medium"
        elif self.level_text == "Medium":
            self.level_text = "Hard"
        elif self.level_text == "Hard":
            self.level_text = "Easy"
        return self.level_text

    @staticmethod
    def reset_statistics():
        sqlraw.cursor.execute("""DELETE FROM statistics""")
        sqlraw.con.commit()

    @staticmethod
    def exit_leaderboards():
        menu.run()

    def handle_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_leaderboards()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons_list:
                        mouse_is_pressed_on_button = self.mouse_is_pressed_on_button(button, 180, 100)
                        if mouse_is_pressed_on_button:
                            button.action()

                    for arrow in self.arrows_list:
                        mouse_is_pressed_on_arrow = self.mouse_is_pressed_on_button(arrow, 65, 45)
                        if mouse_is_pressed_on_arrow:
                            arrow.action()

            self.draw()
            pygame.display.update()


def run():
    leaderboard = Leaderboard()
    leaderboard.handle_events()
