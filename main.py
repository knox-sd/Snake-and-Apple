import pygame
from pygame.locals import *  #import globle ceruin veriable for hold background(event)
import time
import random

SIZE = 40  #size of block
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resoures/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):  # apple moving area
        self.x = random.randint(1, 20 - 1) * SIZE
        self.y = random.randint(1, 15 - 1) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resoures/block2.jpg").convert()
        self.direction = "down"

        self.length = 1
        self.x = [40]
        self.y = [40]

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SD Snake and Apple Game")

        pygame.mixer.init()  # sound module
        self.play_background_music()

        self.surface = pygame.display.set_mode(
            (1000, 700)
        )  ## Create display and backgroung color
        self.snake = Snake(self.surface, 1)  # increase or decrease the block
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resoures/new_music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resoures/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resoures/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(
                self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y
        ):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(
                    self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                self.play_sound("crash")
                raise "Collision Occured"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(
            f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255)
        )
        self.surface.blit(line1, (200, 300))
        line2 = font.render(
            "To play again press Enter. To exit press Escape!", True, (255, 255, 255)
        )
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.play_background_music()

    def run(self):
        ## Show display until you close or ESC
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  ## close using ESC key
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        ## moving block using key
                        if event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()

                        if event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()

                        if event.key == K_UP and self.snake.direction != "down":
                            self.snake.move_up()

                        if event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()

                elif event.type == QUIT:  ## clicking close icon X
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.25)


if __name__ == "__main__":
    game = Game()
    game.run()
