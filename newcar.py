# This Code is Heavily Inspired By The YouTuber: Cheesy AI
# Code Changed, Optimized And Commented By: NeuralNine (Florian Dedov)
# This code has again been hoisted by the CGS Digital Innovation Department
# giving credit to the above authors for the benfit of our education in ML

import math
import random
import sys
import os

import neat
import pygame

# Constants
# WIDTH = 1600
# HEIGHT = 880

WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 60
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255)  # Color To Crash on Hit

current_generation = 0  # Generation counter

"""
The Car Class 

Throughout this section, you will need to explore each function
and provide extenive comments in the spaces denoted by the 
triple quotes(block quotes) """ """.
Your comments should describe each function and what it is doing, 
why it is necessary and where it is being used in the rest of the program.

"""


class Car:
    """1. This Function:

    Firstly the program starts by loading an image from a file named "car.png".
    Once the image has been loaded the program converts and scales it based on the stated size and format.
    This will improve the program's performance and speed when performed.

    Secondly the program sets various attributes for the car suchs as the position, angle and speed around the race track. 
    The starting position will equal (830, 920), the angle will be initially set to 0 degress and the speed to 0.

    Thirdly the speed will not be set so that the variable will be able to be changed depeding on the generations of the cars and selective breeding.

    Fourthly the function  calculates the center of the cars position and then placing the car size ontop of that to initialise the car.

    Next the function will draw the radars which act as the senses for the car which will find where the walls of the track are and move so that the 
    car will turn to avoid whatever is in its direct line of sight. The amount of radars that the cars posses can be changed to reflect the amout of input
    that you want the car to have.

    Lastly the function defines 2 variables and a boolean to verify the cars performance and fitness on the track. Firstly a boolean is created to verify that
    the car has not been crashed. Furthermore two more variables are created which hold the distance traveled and the time on track.
    
    """

    def __init__(self):
        # Load Car Sprite and Rotate
        self.sprite = pygame.image.load("car.png").convert()  # Convert Speeds Up A Lot
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite

        # self.position = [690, 740] # Starting Position
        self.position = [830, 920]  # Starting Position
        self.angle = 0
        self.speed = 0

        self.speed_set = False  # Flag For Default Speed Later on

        self.center = [
            self.position[0] + CAR_SIZE_X / 2,
            self.position[1] + CAR_SIZE_Y / 2,
        ]  # Calculate Center

        self.radars = []  # List For Sensors / Radars
        self.drawing_radars = []  # Radars To Be Drawn

        self.alive = True  # Boolean To Check If Car is Crashed

        self.distance = 0  # Distance Driven
        self.time = 0  # Time Passed

    """ 2. This Function:

    Screen is being drawn through the use of pygame.
    Sprite positions are being placed onto the screen at the current location.
    Furthermore it optionaly draws the radars for the sensors.
    
    """

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)  # Draw Sprite
        self.draw_radar(screen)  # OPTIONAL FOR SENSORS

    """ 3. This Function:
    
    Firstly this is a function that defines and draws the radars. This is done through the use of self and screen, which are passed in.
    The first variable self is the location of each of the individual cars, while the screen is the location relative to the wider viewing panel.
    
    Secondly the function runs a for loop which for each radar in the self of each car runs the following instructions.
    Next the function extracts the position of the radar center.
    
    Then two Pygame drawing functions are used for visualization:

    pygame.draw.line: This function draws a line from the center of the screen to the position of the radar sensor. 
    The line color is green (RGB: 0, 255, 0), and it has a thickness of 1 pixel.

    pygame.draw.circle: This function draws a small green circle at the position of the radar sensor. The circle has a radius of 5 pixels.
    """

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    """ 4. This Function:
    
    The function then iterates through each corner of the object, represented by the variable 'point'.
    It checks whether any of these corners touch the border color on the game map.
    If the pixel at the current 'point' coordinates on the game map matches the 'BORDER_COLOR', it signifies a collision.

    If a collision is detected at any corner, the 'self.alive' flag is set to 'False' to indicate that the object has crashed,
    and the loop is broken to prevent further checks. This function essentially determines the collision status of the object
    with the border color on the game map.

    """

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    """ 5. This Function:
    
    In this function, `check_radar`, the first step is to initialize a variable `length` to zero. 
    Then, the function calculates the x and y coordinates based on the given `degree` and `game_map`. 
    It uses trigonometric functions to determine the new coordinates.

    Next, there's a `while` loop that continues as long as two conditions are met: first, the color at the current `(x, y)` 
    position on the `game_map` is not equal to `BORDER_COLOR`, and second, `length` is less than 300. Inside this loop, the `length` 
    is incremented by 1, and the new `(x, y)` coordinates are recalculated using trigonometric functions.

    Once the loop exits, the function calculates the distance `dist` between the final `(x, y)` coordinates and the center of the object. 
    This distance is calculated using the Euclidean distance formula. Finally, the calculated `(x, y)` coordinates and `dist` are appended to 
    the `self.radars` list as a sub-list, forming a radar reading.

    """

    def check_radar(self, degree, game_map):
        length = 0
        x = int(
            self.center[0]
            + math.cos(math.radians(360 - (self.angle + degree))) * length
        )
        y = int(
            self.center[1]
            + math.sin(math.radians(360 - (self.angle + degree))) * length
        )

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(
                self.center[0]
                + math.cos(math.radians(360 - (self.angle + degree))) * length
            )
            y = int(
                self.center[1]
                + math.sin(math.radians(360 - (self.angle + degree))) * length
            )

        # Calculate Distance To Border And Append To Radars List
        dist = int(
            math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))
        )
        self.radars.append([(x, y), dist])

    """ 6. This Function:
    
    The function checks if the car's speed has been set before. If not, it sets the speed to 20 and marks the speed as set.
    The function rotates the car's sprite based on its current angle and moves it in the right X-direction.
    It ensures that the car stays at least 20 pixels away from the edge of the game map.

    The distance traveled by the car is increased by its current speed, and the time is incremented by 1.
    Similar to the X-position update, the function also updates the Y-position of the car, ensuring it stays within the boundaries of the game map.
    The center of the car is recalculated based on its new position.

    Four corner points of the car are calculated, considering its angle and size.
    The function checks for collisions between the car and the game map and clears the car's radar data.
    It then iterates through a range of angles from -90 to 120 with a step size of 45 and checks the radar for each angle in relation to the game map.

    """

    def update(self, game_map):
        # Set The Speed To 20 For The First Time
        # Only When Having 4 Output Nodes With Speed Up and Down
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1

        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Calculate New Center
        self.center = [
            int(self.position[0]) + CAR_SIZE_X / 2,
            int(self.position[1]) + CAR_SIZE_Y / 2,
        ]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * CAR_SIZE_X
        left_top = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length,
        ]
        right_top = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length,
        ]
        left_bottom = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length,
        ]
        right_bottom = [
            self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
            self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length,
        ]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    """ 7. This Function:
    
    In this function, `get_data`, the first step is to obtain the radar data and store it in the variable `radars`.
    Then, a list called `return_values` is initialized with five zeros. The function proceeds to iterate through the `radars` list,
    using a for loop with the `enumerate` function to provide both the index `i` and the radar data `radar` in each iteration.
    Inside the loop, it calculates the integer division of the second element of each radar data by 30 and assigns the result to the corresponding position
    in the `return_values` list.
    This step effectively computes distances to the border for each radar and stores them in the `return_values` list.

    """

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    """ 8. This Function:
    
    This function is a function that checks if the car is alive through returning the self object.

    """

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    """ 9. This Function:
    
    In the given function, "get_reward," the first step involves calculating the reward.
    This is done by taking the value of "self.distance" and dividing it by half of the constant "CAR_SIZE_X." 
    It appears that the division is used to determine the reward, and the comment
    suggests that this calculation might be subject to change in the future.
    Finally, the calculated reward is returned as the function's output.

    """

    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        # return self.distance / 50.0
        return self.distance / (CAR_SIZE_X / 2)

    """ 10. This Function:
    
    In the rotate_center function, the code first obtains the rectangle that encloses the input image using image.get_rect().
    It then rotates the image by the specified angle using pygame.transform.rotate, resulting in the rotated_image.
    To ensure that the rotated image stays centered properly, a copy of the original rectangle is created as rotated_rectangle,
    and its center is updated to match the center of the rotated image.
    Finally, the code extracts the subsurface of the rotated image based on the updated rectangle and returns this modified image.

    In the draw_radar function, the code iterates through a list of radar positions stored in self.radars.
    For each radar position, it draws a green line from the center of the screen to that radar position using pygame.draw.line.
    Additionally, it draws a green circle at the radar position using pygame.draw.circle. These actions are performed for each radar position in the list,
    allowing the radar points to be visualized on the screen.
    
    """

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    """ This Function:

    Firstly the function is defined as run_simulation and it takes two arguments (genomes and config).
    Next there are two lists which are emptied namely nets and cars.
    Once this is complete the function creates a fullscreen window using the newly initialized pygame.

    Next the function runs a for loop which iterates over each item in genomes through the use of the tracker i.
    During the loop, a feed forward neat neural network is created and the net is appended to "nets".
    Futhermore each genome's fitness is set to 0 before simulation is run.

    Next a clock is created using the pygame library, the fonts are created and the game map is loaded from the files using the convert functionality
    which speeds up the performance of the program.

    Fifth the generation counter is incremetented displaying to the user how many generations of the cars have been trialed, and the counter is set to limit
    the simulation time.

    Next an infinite loop is created that constantly runs a for loop. This for loop will check for user interactions with the program and subsequently quit
    the program if it is found that the user has clicked the exit button.

    After this is completed the program runs a for loop which is responsible for making decisions for each car in the simulation.
    It uses the i placeholder and the car object to iterate through the list of cars through the method 'enumerate(cars)'.

    Then for each car it activates the neural network through using the neural net's activation function and passing the get_data from the car.
    It then determines the action to be taken by the car based on the neural network's output (output). The action is determined by finding the index
    of the maximum value in the output array (choice = output.index(max(output))).
    Depending on the value of choice, the car's behavior is adjusted:

    If choice is 0, the car's angle is increased by 10 degrees, simulating a left turn.
    If choice is 1, the car's angle is decreased by 10 degrees, simulating a right turn.
    If choice is 2 and the car's speed minus 2 is greater than or equal to 12, the car's speed is decreased by 2, simulating slowing down.

    After all of this is completed the a check will be created which will make sure that the car is still alive:
    If the car is still alive then the fitness level of the car will be increased due to the proficiency of its genes.
    If the car is dead then the loop will be broken not allowing the car to continue with its genome.

    Furthermore the counter will count up to around 20 seconds at which point the alive checking function above will be run.

    Next the program uses the "blit" method of pygame inorder to draw the screen at position (0,0).
    A for loop is then run that for each car in the "cars" list will check if the car is alive:
    If it is then only the alive cars will be drawn ensuring that the dead cars are not re rendered.

    Next the program displays the generation number which represents the amount of genome recombinations that have occured during the run time.
    Furthermore the program creates a rectangle around the text, aswell as positioningthe text.

    Next the code "blits" (draws) the rendered text onto the Pygame screen. It uses the text surface (the rendered text)
    and the text_rect to determine where to display the text on the screen.
    After this the code repeats the process seen above, however this time it shows the amount of cars that are still alive.

    Next the program uses pygame.display.flip to show the changes made to the screen. 
    It effectively renders the text onto the screen after the blit operations.

    Finally the program uses the clock.tick functionality to set the animation frames per second to 60 ensuring that the simulation runs consistently.

    """

def run_simulation(genomes, config):
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load("map2.png").convert()  # Convert Speeds Up A Lot

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10  # Left
            elif choice == 1:
                car.angle -= 10  # Right
            elif choice == 2:
                if car.speed - 2 >= 12:
                    car.speed -= 2  # Slow Down
            else:
                car.speed += 2  # Speed Up

        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40:  # Stop After About 20 Seconds
            break

        # Draw Map And All Cars That Are Alive
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)

        # Display Info
        text = generation_font.render(
            "Generation: " + str(current_generation), True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS


""" 1. This Section:
    
Firstly the code checks whether the program is being run as a main program and not as an imported module.

Next the program procedes by loading the config:

    It starts by setting the config's path to the config.txt path which contains settings for NEAT algorithm.
    Next it creates a population and adds reporters and finally it runs the program for a max of 1000 generations and recombinations of genomes.

"""
if __name__ == "__main__":
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)
