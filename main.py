import pygame
import requests
from enum import Enum

from pygame.locals import *



pygame.font.init()

font = pygame.font.SysFont('Arial', 20)

LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameState(Enum):
    Desert = 1
    Turbines = 2


class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, text1, text2, text3):
        super().__init__()

        self.text1 = text1
        self.text2 = text2
        self.text3 = text3
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), pygame.rect.Rect(660, -10, 400, 100), border_radius=5)
        text1_surface = font.render(self.text1, False, (255,255,255))
        text2_surface = font.render(self.text2, False, (255,255,255))
        text3_surface = font.render(self.text3, False, (255,255,255))

        textx = 670

        screen.blit(text1_surface, (textx,5))
        screen.blit(text2_surface, (textx,32))
        screen.blit(text3_surface, (textx,60))

    def update(self, text1, text2, text3):
        self.text1 = text1
        self.text2 = text2
        self.text3 = text3





class Windmill(pygame.sprite.Sprite):
    def __init__(self, x, y, windmill_list, num):
        super().__init__()

        windmill_list.add(self)
        self.center_x, self.center_y = x, y
        self.offset = num
        self.angle = 0
 
    def draw(self):
        # Draw Tower
        screen.blit(pygame.transform.scale(pygame.image.load("assets/pole.png"), (300, 800)), (self.center_x - 152, self.center_y - 20))  # Adjusted for new size
 
        # Rotate and draw blades
        rotated_blades = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("assets/blades.png"), (400,400)), -self.angle - self.offset)
        blade_rect = rotated_blades.get_rect(center=(self.center_x, self.center_y))
        screen.blit(rotated_blades, blade_rect.topleft)

    def update(windmill, degrees):
        windmill.angle = degrees

class Panel(pygame.sprite.Sprite):
    def __init__(self, x, y, panel_list):
        super().__init__()
        panel_list.add(self)

        self.image = pygame.transform.scale(pygame.image.load("assets/solar-panel.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def solar_panel_data(solar_panel_amount, stored_joules):
    joules_per_secondpanel = 350 / 50 * solar_panel_amount
    stored_joules += joules_per_secondpanel
    # print( "You're making " + str(joules_per_secondpanel) + " joules per second from your solar panels!")
    return  stored_joules
 
 
def wind_turbine_data(wind_turbine_amount, stored_joules, wind_speed_ratio):
    print(wind_speed_ratio)
    turbine_joules_per_second = 2750000 / 50 * wind_turbine_amount * wind_speed_ratio
    stored_joules += turbine_joules_per_second
    # print( "You're making " + str(turbine_joules_per_second) + " joules per second from your wind turbines!")
    return stored_joules


def get_wind_speed(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=wind_speed_10m"
    response = requests.get(url)
    data = response.json()
 
    if "current" in data and "wind_speed_10m" in data["current"]:
        return data['current']['wind_speed_10m']

 
def get_location():
    response = requests.get("https://ipinfo.io/json")
    data = response.json()
    if "loc" in data:
        lat, lon = data["loc"].split(",")
        return float(lat), float(lon)

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set the window dimensions
width = 1000
height = 700

# Create the window
screen = pygame.display.set_mode((width, height))


# Set the window title
pygame.display.set_caption("Climate Game")

text = TextDisplay("Hello", " Hi", " Hah")

panel_list = pygame.sprite.Group()
windmill_list = pygame.sprite.Group()

windimll0 = Windmill(250, 300, windmill_list, 180)
windmill1 = Windmill(500, 250, windmill_list, 90)
windmill2 = Windmill(750, 400, windmill_list, 253)

wind_turbine_joules = 0
wind_turbine_joules_per_second = 3 * 2750000
panel_joules = 0
panel_joules_per_second = 0

panel = Panel(100, 100, panel_list)
game_state = GameState.Desert

live_mode = True;

lat, lon = get_location()
wind_turbine_ratio = get_wind_speed(lat, lon) / 9

# Game loop
running = True
while running:
    keys = pygame.key.get_pressed()



    if keys[pygame.K_RIGHT] and (game_state == GameState.Turbines):
        game_state = GameState.Desert
        panel_joules = 0

        
    if keys[pygame.K_LEFT] and (game_state == GameState.Desert):
        game_state = GameState.Turbines
        wind_turbine_joules = 0

    if keys[pygame.K_a]:
        print("Live Mode")
        live_mode = True

    if keys[pygame.K_s]:
        live_mode = False
    
    screen.fill((255, 255, 255))
    
    if game_state == GameState.Desert:

        panel_joules = solar_panel_data(panel_list.__len__(), panel_joules)

        text.update("Energy per solar panel: 350" ,"Joules per second: " + str(panel_joules_per_second), "Total joules: " + str(panel_joules))

        panel_joules_per_second = panel_list.__len__() * 350
        
        screen.blit(pygame.transform.scale(pygame.image.load("assets/background-sand.png"), (width, height)).convert(), [0,0])


        for panel in panel_list:
            panel.draw(screen)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                panel = Panel(mouseX - 50, mouseY - 50, panel_list)

                print("Drew solar panel")
                print(panel_list.__len__())
    elif game_state == GameState.Turbines:
        
        energy_per_turbine = 2750000

        num = 0

        if live_mode:
            energy_per_turbine *= wind_turbine_ratio
            print(wind_turbine_ratio)
            wind_turbine_joules = wind_turbine_data(3, wind_turbine_joules, wind_turbine_ratio)
            num = wind_turbine_joules_per_second * wind_turbine_ratio
        else:
            num = wind_turbine_joules_per_second
            wind_turbine_joules = wind_turbine_data(3, wind_turbine_joules, 1)



        text.update("Energy per wind turbine: " + str(int(energy_per_turbine)) ,"Joules per second: " + str(int(num)), "Total joules: " + str(int(wind_turbine_joules)))


        screen.blit(pygame.transform.scale(pygame.image.load("assets/turbine_background.png"), (width, height)).convert(), [0,0])

        for turbine in windmill_list:
            if live_mode:
                turbine.update(wind_turbine_joules/150000 * wind_turbine_ratio)
            else:
                turbine.update(wind_turbine_joules / 150000)
            turbine.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

    text.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(50)

# Quit Pygame
pygame.quit()
