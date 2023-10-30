import pygame
import math

# Constants
TILE_SIZE = 32
MAP_NUM_ROWS =15
MAP_NUM_COLS =20
WINDOW_WIDTH =MAP_NUM_COLS*2 * TILE_SIZE
WINDOW_HEIGHT = MAP_NUM_ROWS * TILE_SIZE
screen  = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
BRICK_IMG = pygame.image.load('wall1001.png')
CEILING_IMG = pygame.image.load("Metal.png").convert_alpha()
BRICK_IMG = pygame.transform.scale(BRICK_IMG, (TILE_SIZE, TILE_SIZE))

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED= (255, 0, 0)

# Initialize pygame
pygame.init()

# Game Map
grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation_speed = 5
        self.turn_direction = 0 
        self.walk_direction = 0 
        self.rotation_angle = math.pi / 2 #This means the player is initially facing a direction equivalent to 90 degrees
        self.move_speed = 0.5
        self.rotation_speed = math.pi / 100

        
    def player_one(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), radius=5, width=5)
        pygame.draw.line(screen, RED, (self.x, self.y), 
        (self.x + math.cos(self.rotation_angle) * 1, 
        self.y + math.sin(self.rotation_angle) * 1),
        width=5)


        
    def render(self, screen):
        # Draw the player on the screen
        pass

class RayCaster:
    def __init__(self, player, grid, screen, TILE_SIZE):
        self.distances = []
        self.player = player
        self.TILE_SIZE = TILE_SIZE
        self.grid = grid
        self.screen = screen 
        self.max_depth = MAP_NUM_COLS * TILE_SIZE
        self.FOV = 110
        self.closest_wall_x = 0
        self.closest_wall_y = 0
        self.MAP_WIDTH = len(self.grid[0]) * TILE_SIZE
        self.WINDOW_WIDTH=WINDOW_WIDTH
        self.WINDOW_HEIGHT=WINDOW_HEIGHT
        # You can initialize other attributes here as needed

    def cast_rays2(self):
        
        self.distances.clear()
        #print("Casting rays...")
        distances = []
        #Fov_rad=(math.pi)/360# it gives the angle in radiants
        left_ray_angle = self.player.rotation_angle - (self.FOV / 2 * math.pi)#calculates the leftmost angle
        
        
        for rays in range (self.FOV):
          smallest_distance = 1000000
        
          for depth in range (self.max_depth):
                            
                            wall_x_pos=self.player.x + math.cos(left_ray_angle)*depth
                            wall_y_pos=self.player.y + math.sin(left_ray_angle)*depth
                                            

                            row=int(wall_y_pos/TILE_SIZE)
                            col=int(wall_x_pos/TILE_SIZE)
                    

                            if col<15 and col>=0 and row<11 and row>=0:

                                if self.grid[row][col]==1:
                                    my_distance = math.sqrt((self.player.x - wall_x_pos)**2 + (self.player.y - wall_y_pos)**2)
                                    
                                    
                                            
                                    if my_distance<smallest_distance:
                                        
                                        smallest_distance=my_distance
                                        self.closest_wall_x = wall_x_pos
                                        self.closest_wall_y = wall_y_pos                        
                                    
                                    #print(f"Ray at angle {left_ray_angle} hit wall at ({self.closest_wall_x}, {self.closest_wall_y}) with distance {smallest_distance}")
                                    #print(f"player x pos {self.player.x} player y pos ({self.player.y}")
                                    pygame.draw.line(self.screen, RED, (self.player.x, self.player.y), (self.closest_wall_x, self.closest_wall_y))
                                    #pygame.draw.line(self.win, (255, 0, 0), (self.player_xpos, self.player_ypos), (self.closest_wall_x, self.closest_wall_y), 2)

                                    break

          self.distances.append(smallest_distance)
          #print (distances)
          left_ray_angle += math.pi/360 # increment left_ray_angle by 1 degree
       
        #pygame.draw.line(self.win, RED, (100, 100), (200, 200), 5)
        return distances
    # Calculate MAP_WIDTH outside the function
    
    
    def draw_walls(self):
         
        stripe_width = self.WINDOW_WIDTH // len(self.distances)


        ####

        FLOOR_COLOR_NEAR = (100, 100, 100)  # Darker gray for nearer parts
        FLOOR_COLOR_FAR = (200, 200, 200)  # Lighter gray for farther parts
        
        

        # Define ceiling and floor colors
        CEILING_COLOR = (60, 60, 60)

        FLOOR_COLOR = (169, 169, 169)  # For example, a dark shade of gray

        for idx, distance in enumerate(self.distances):
            # Your existing code for drawing wall stripe
            wall_height = 10000 / (distance if distance else 1)
            offset = (self.WINDOW_HEIGHT - wall_height) / 2 #to make sure that the walls are centered
            #color = (255 - min(int(distance * 1), 255), 255 - min(int(distance * 1), 255), 255 - min(int(distance * 1), 255))

            blend_factor = min(1, distance / 500.0)  # Adjust the 1000.0 for more or less aggressive blending
            # 3. Blend the two colors
            blended_red = int(FLOOR_COLOR_NEAR[0] * (1 - blend_factor) + FLOOR_COLOR_FAR[0] * blend_factor)
            blended_green = int(FLOOR_COLOR_NEAR[1] * (1 - blend_factor) + FLOOR_COLOR_FAR[1] * blend_factor)
            blended_blue = int(FLOOR_COLOR_NEAR[2] * (1 - blend_factor) + FLOOR_COLOR_FAR[2] * blend_factor)

            blended_color = (blended_red, blended_green, blended_blue)
            
             # Only draw the brick texture for the walls
            scaled_img = pygame.transform.scale(BRICK_IMG, (stripe_width, int(wall_height)))
            #print (stripe_width, wall_height)
            
            self.screen.blit(scaled_img, (self.MAP_WIDTH + idx * stripe_width, offset))
            #print ("stripe",stripe_width, "wall",wall_height)

            #pygame.draw.rect(self.screen, color, (self.MAP_WIDTH + idx * stripe_width, offset, stripe_width, wall_height))

            # Draw ceiling
            pygame.draw.rect(self.screen, CEILING_COLOR, (self.MAP_WIDTH + idx * stripe_width, 0, stripe_width, offset))
            

            # Draw floor
            #pygame.draw.rect(self.screen, FLOOR_COLOR, (self.MAP_WIDTH + idx * stripe_width, offset + wall_height, stripe_width, self.WINDOW_HEIGHT))
            pygame.draw.rect(self.screen, blended_color, (self.MAP_WIDTH + idx * stripe_width, offset + wall_height, stripe_width, self.WINDOW_HEIGHT))




    
def render_walls(self, screen):
        # Render the walls based on the ray distances
        pass

class GameMap:
    def __init__(self, map_data):
        self.map_data = map_data

    def draw_grid(self, screen):
        boundary_of_grid = []
        for i in range(len(self.map_data)):
            for j in range(len(self.map_data[0])):
                if self.map_data[i][j] == 0:
                    pygame.draw.rect(screen, WHITE, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, BLACK, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    cell_rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    boundary_of_grid.append(cell_rect)
        return boundary_of_grid



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(WINDOW_WIDTH / 2 / 2, WINDOW_HEIGHT / 2)
        self.ray_caster = RayCaster(self.player, grid, self.screen, TILE_SIZE)
        self.map = GameMap(grid)

    
    
    def check_for_collision(self):
         boundaries = self.map.draw_grid(self.screen) 
         circle_bounding_box = pygame.Rect(self.player.x - 5, self.player.y - 5, 10, 10)
         for rectangle in boundaries:
            if circle_bounding_box.colliderect(rectangle):
                # Collision detected
                
                return True

        # No collision detected
         return False
         
       
        

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            prev_x, prev_y = self.player.x, self.player.y    
            #if keys[pygame.K_LEFT]:
            self.player.turn_direction = -1
            self.player.rotation_angle += self.player.turn_direction * self.player.rotation_speed
            if self.check_for_collision():
                self.player.x, self.player.y = prev_x, prev_y

        elif keys[pygame.K_RIGHT]:
            prev_x, prev_y = self.player.x, self.player.y
            self.player.turn_direction=1
            self.player.rotation_angle =self.player.rotation_angle + self.player.turn_direction*self.player.rotation_speed
            if self.check_for_collision():
                self.player.x, self.player.y = prev_x, prev_y


        elif keys[pygame.K_UP]:
                # temporarily save the player's current position
                prev_x, prev_y = self.player.x, self.player.y
                self.player.walk_direction=1
                move_step=self.player.walk_direction*self.player.move_speed#makes it positive or negative
                #print (walk_direction)
                self.player.x += math.cos(self.player.rotation_angle)*move_step
                self.player.y += math.sin(self.player.rotation_angle)*move_step
                if self.check_for_collision():
                    self.player.x, self.player.y = prev_x, prev_y

        elif keys[pygame.K_DOWN]:
            prev_x, prev_y = self.player.x, self.player.y
            self.player.walk_direction=-1
            move_step=self.player.walk_direction*self.player.move_speed#makes it positive or negative
            self.player.x += math.cos(self.player.rotation_angle)*move_step
            self.player.y += math.sin(self.player.rotation_angle)*move_step   
            if self.check_for_collision():
                    self.player.x, self.player.y = prev_x, prev_y

    def render(self):
        self.screen.fill(WHITE)
        self.map.draw_grid(self.screen)
        self.ray_caster.cast_rays2()  # Call the ray-casting method
        self.ray_caster.draw_walls()
        self.player.player_one(self.screen)  # This line renders the player now after the map.
    
        
        pygame.display.flip()


    def run(self):
        while True:
            self.handle_input()
            
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
