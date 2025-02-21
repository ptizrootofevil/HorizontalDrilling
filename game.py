import pygame
import numpy as np
from random import randint


class Drill:
    def __init__(self, height: int) -> None:
        self.location = np.array([0, height/3])
        self.direction = np.array([1, 0])
        self.bias = 1 # 1 - clochwise -1 - counterclockwise
        self.speed = 5
        self.rotation = np.radians(1.1)
        self.path = [self.location, self.location]
    
    def drill(self) -> None:
        cos, sin = np.cos(self.rotation * self.bias), np.sin(self.rotation * self.bias)
        R = np.array(((cos,-sin), (sin, cos)))
        self.direction = np.dot(R, self.direction)

        self.location = self.location + self.direction * self.speed
        self.path.append(self.location)

    def change_direction(self) -> None:
        self.bias *= -1

    def get_location(self) -> list[int, int]:
        return self.location

class Lake:
    def __init__(self, width, height) -> None:
        self.location = np.array([width/2, height/3])
        self.radius = 200
    
    def colision(self, point: list[int, int]) -> bool:
        return (point[0] - self.location[0]) ** 2 + (point[1] - self.location[1]) ** 2 <= self.radius ** 2 and point[1] > self.location[1]


class Button:
    def __init__(self):
        self.location = np.array([20, 20])
        self.size = np.array([100, 50])
        self.text = 'Change direction'
        self.dark_color = (155, 155, 155)
        self.light_color = (255, 255, 255)

    def draw_button(self, screen, mouse):
        if 20 <= mouse[0] <= 120 and 20 <= mouse[1] <= 70: 
            pygame.draw.rect(screen, self.light_color, (self.location[0], self.location[1], self.size[0], self.size[1])) 
        else: 
            pygame.draw.rect(screen, self.dark_color, (self.location[0], self.location[1], self.size[0], self.size[1])) 

    def button_click(self, a_drill: Drill, mouse):
        if 20 <= mouse[0] <= 120 and 20 <= mouse[1] <= 70:
            a_drill.change_direction()

class Rock:
    def __init__(self, left, right, top, bottom):
        self.location = (randint(left, right), randint(bottom, top))
        self.radius = randint(30, 100)
        self.color = (0, 0, 0)

    def colision(self, point: list[int, int]) -> bool:
        return (point[0] - self.location[0]) ** 2 + (point[1] - self.location[1]) ** 2 <= self.radius ** 2

    def draw_rock(self, screen):
        pygame.draw.circle(screen, self.color, (self.location[0], self.location[1]), self.radius, self.radius)

class Win_screen:
    def __init__(self, height):
        self.location = [1000, height//3]
        self.size = [100, 20]

    def colision(self, drill):
        return 1000 <= drill[0] <= 1100 and 240 <= drill[1] <= 260




def main():
    width, height = 1280, 720
    a_drill = Drill(height)
    a_lake = Lake(width, height)
    a_button = Button()
    a_win_screen = Win_screen(height)
    rocks = [Rock(0, width, int(height*(2/3)), int(height/3)) for _ in range(3)]
    pygame.init()
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Triangle")

    # Main game loop
    win = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                a_button.button_click(a_drill, mouse)
                
        # Clear the screen
        screen.fill((0,0,0))

        # Ground
        pygame.draw.rect(screen, (160,82,45), (0, height/3, width, height*(2/3))) 
        
        for rock in rocks:
            rock.draw_rock(screen)
        # Lake
        pygame.draw.circle(screen, (0, 0, 255), (a_lake.location[0], a_lake.location[1]), a_lake.radius, a_lake.radius, draw_bottom_left=True, draw_bottom_right=True)
        # Sky
        pygame.draw.rect(screen, (125, 191, 221), (0, 0, width, height/3))
        # Drill
        pygame.draw.rect(screen, (255, 0, 0), (a_drill.location[0], a_drill.location[1], 5, 5))
        # Win square
        pygame.draw.rect(screen, (0, 255, 0), (1000, height//3, 100, 20))
        # Draw the lines
        pygame.draw.lines(screen, (0,0,0), False, a_drill.path, 2)
        
        a_drill.drill()

        mouse = pygame.mouse.get_pos()

        a_button.draw_button(screen, mouse)

        # Update the display
        pygame.display.flip()

        if a_lake.colision(a_drill.get_location()):
            break
        for rock in rocks:
            if rock.colision(a_drill.get_location()):
                running = False
        if a_win_screen.colision(a_drill.get_location()):
            win = True




        # Control the frame rate
        pygame.time.Clock().tick(10)

    # Quit Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
    
