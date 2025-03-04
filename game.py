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

    def get_direcrion(self):
        return self.location[0] + self.direction[0]*7, self.location[1] + self.direction[1]*7

class Lake:
    def __init__(self, width, height) -> None:
        self.location = np.array([width/2, height/3])
        self.radius = 200
    
    def colision(self, point: list[int, int]) -> bool:
        return (point[0] - self.location[0] ) ** 2 + (point[1] - self.location[1]) ** 2 <= self.radius ** 2 and point[1] > self.location[1]

    def colision_with_rock(self, point, r):
        return (self.location[0] - point[0])**2 + (self.location[1] - point[1])**2 <= (self.radius + r)**2

class Button:
    def __init__(self):
        self.location = np.array([20, 20])
        self.size = np.array([100, 50])
        self.text = 'Change direction'
        self.dark_color = (155, 155, 155)
        self.light_color = (255, 255, 255)

    def button_click(self, a_drill: Drill, mouse):
        if 20 <= mouse[0] <= 120 and 20 <= mouse[1] <= 70:
            a_drill.change_direction()

class Block_square:
    def __init__(self, left, top, right, bottom):
        self.point1 = [left, top]
        self.point2 = [right, bottom]

    def colision(self, point, r):
        closest_x = max(self.point1[0], min(point[0], self.point2[0]))
        closest_y = max(self.point1[1], min(point[1], self.point2[1]))
        return (point[0] - closest_x)**2 + (point[1] - closest_y)**2 <= r**2

class Rock:
    def __init__(self, left: int, right: int, top: int, bottom: int, start_square_block, win_square_block, lake):
        while True:
            x, y, r = randint(left, right), randint(bottom, top), randint(30, 100)
            if start_square_block.colision([x,y], r):
                continue
            if win_square_block.colision([x,y], r):
                continue
            if lake.colision_with_rock([x,y], r):
                continue
            break
        self.location = [x, y]
        self.radius = r
        self.color = (0, 0, 0)

    def colision(self, point: list[int, int]) -> bool:
        return (point[0] - self.location[0]) ** 2 + (point[1] - self.location[1]) ** 2 <= self.radius ** 2

    def draw_rock(self, screen):
        pygame.draw.circle(screen, self.color, (self.location[0], self.location[1]), self.radius, self.radius)

class Win_square:
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
    a_win_square = Win_square(height)
    start_square_block = Block_square(0, height/3, 280, height/3+150)
    win_square_block = Block_square(900, height/3, 900+300, height/3+110)
    rocks = [Rock(0, width, int(height*(2/3)), int(height/3), start_square_block, win_square_block, a_lake) for _ in range(5)]
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Horizontal drilling")

    # Main game loop
    win = False
    lose = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                a_button.button_click(a_drill, mouse)

                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()
            pygame.quit()

        # Clear the screen
        screen.fill((0,0,0))

        if not win and not lose:
            # Ground
            pygame.draw.rect(screen, (160,82,45), (0, height/3, width, height*(2/3)))   
            for rock in rocks:
                rock.draw_rock(screen)
            # Lake
            pygame.draw.circle(screen, (0, 0, 255), (a_lake.location[0], a_lake.location[1]), a_lake.radius, a_lake.radius, draw_bottom_left=True, draw_bottom_right=True)
            # Sky
            pygame.draw.rect(screen, (125, 191, 221), (0, 0, width, height/3))
            # Drill
            start_point = a_drill.get_location()
            end_point = a_drill.get_direcrion()
            pygame.draw.line(screen, (255,0,0), start_point, end_point, 2)
            # Win square
            pygame.draw.rect(screen, (0, 255, 0), (1000, height//3, 100, 20))
            # Path
            pygame.draw.lines(screen, (0,0,0), False, a_drill.path, 2)

            a_drill.drill()
            mouse = pygame.mouse.get_pos()
            if 20 <= mouse[0] <= 120 and 20 <= mouse[1] <= 70: 
                pygame.draw.rect(screen, a_button.light_color, (a_button.location[0], a_button.location[1], a_button.size[0], a_button.size[1])) 
                font = pygame.font.Font(None, 16)
                button_text = font.render("Change driection", True, (0,0,0))
                button_rect = button_text.get_rect(center=(a_button.location[0] + a_button.size[0]/2, a_button.location[1] + a_button.size[1]/2))
                screen.blit(button_text, button_rect)
            else: 
                pygame.draw.rect(screen, a_button.dark_color, (a_button.location[0], a_button.location[1], a_button.size[0], a_button.size[1])) 
                font = pygame.font.Font(None, 16)
                button_text = font.render("Change driection", True, (0,0,0))
                button_rect = button_text.get_rect(center=(a_button.location[0] + a_button.size[0]/2, a_button.location[1] + a_button.size[1]/2))
                screen.blit(button_text, button_rect)
        elif win:
            font = pygame.font.Font(None, 48)
            win_text = font.render("You`ve won!\nPress 'r' to restart", True, (0,255,0))
            win_rect = win_text.get_rect(center=(width // 2, height // 2))
            screen.blit(win_text, win_rect)
        else:
            font = pygame.font.Font(None, 48)
            lose_text = font.render("You`ve lost!\nPress 'r' to restart", True, (255,0,0))
            lose_rect = lose_text.get_rect(center=(width // 2, height // 2))
            screen.blit(lose_text, lose_rect)
        

        # Update the display
        pygame.display.flip()

        if a_lake.colision(a_drill.get_location()):
            lose = True
        for rock in rocks:
            if rock.colision(a_drill.get_location()):
                lose = True
        if a_win_square.colision(a_drill.get_location()):
            win = True
        x, y = a_drill.get_location()
        if x < 0 or width < x or y > height or y < height//3:
            lose = True

        # Control the frame rate
        pygame.time.Clock().tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
    
