import numpy as np
import pygame
from physics_engine import PhysicsEngine


def rotate_y(theta):
    return np.array([
        [np.cos(theta), 0, -np.sin(theta)],
        [0, 1, 0],
        [np.sin(theta), 0, np.cos(theta)]
    ])
    

def get_window_coordinates(point_array):
    """point array : [x, y, z]
        Returns [x+1920//2, y+1080//2, z]
    """
    if point_array.ndim == 1:
        point_array = [point_array[0] + 1920//2, point_array[1] + 1080//2, point_array[2]]
        return np.array(point_array)
    
    elif point_array.ndim == 2:
        x = point_array[:, 0] + 1920//2
        y = point_array[:, 1] + 1080//2
        z = point_array[:, 2]
        return np.array([x,y,z]).T


class Body:
    """Body Class"""
    def __init__(self, position, mass, color=np.random.randint(0, 255, 3), radius=10, TIME_DELAY=0.005):
        self.position = position
        self.mass = mass
        self.color = color
        self.radius = radius
        self.TIME_DELAY = TIME_DELAY
        self.velocity = np.zeros(3)
        self.force = np.zeros(3)
        self.position_history = np.array([self.position])
    
    def add_velocity(self, velocity_array):
        self.velocity += velocity_array
        
    def add_force(self, force_array):
        self.force += force_array
        
    def move(self):
        self.velocity = self.velocity + (self.force / self.mass) * self.TIME_DELAY
        self.position = self.position + self.velocity * self.TIME_DELAY
    
    def append_position(self, position):
        self.position_history = np.append(self.position_history, np.array([position]), axis=0)
        


class RenderEngine:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.angle = 0
        self.font = pygame.font.Font('freesansbold.ttf', 15)
        
        self.rotate_y = False
        
    def check_events(self):
        [exit() for event in pygame.event.get() if event.type==pygame.QUIT]
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
            
        if keys[pygame.K_y]:
            self.rotate_y = not self.rotate_y
        
    def rotate(self, angle):
        bodies_position = np.array([body.position for body in bodies])
        rotated_points = np.dot(rotate_y(angle), bodies_position.T)
        rotated_points = rotated_points.T
        
        for i, body in enumerate(bodies):
            window_coordinate = get_window_coordinates(rotated_points[i])
            if (window_coordinate[0] >= 0 and window_coordinate[0] <= 1920) and (window_coordinate[1] >= 0 and window_coordinate[1] <= 1080):
                pygame.draw.circle(self.screen, body.color, window_coordinate[:2], body.radius)
            
            orbit_points = body.position_history
            rotated_orbit_points = np.dot(rotate_y(angle), orbit_points.T)
            rotated_orbit_points = rotated_orbit_points.T
            rotated_orbit_points = get_window_coordinates(rotated_orbit_points)[:, :2]
            
            pygame.draw.lines(self.screen, body.color, False, rotated_orbit_points, 1)

            
        self.angle += 0.001
        if angle >= 2* np.pi:
            angle = 0
    
    def update(self):
        net_force = engine.compute_force_vectors(bodies=bodies)
        for i, body in enumerate(bodies):
            body.force = net_force[i]
            body.move()
            
        
        
    
    def draw(self):
        for i, body in enumerate(bodies):
            window_coordinate = get_window_coordinates(body.position)
            
            pygame.draw.circle(
                self.screen,
                body.color,
                window_coordinate[:2],
                body.radius
            )
            
            body.append_position(body.position)
        
        if self.rotate_y:
            self.rotate(self.angle)
            
    
    def run(self):
        while True:
            self.screen.fill((0,0,0))
            self.clock.tick(self.FPS)
            self.check_events()        
            self.update()
            self.draw()
            bodies[-1].position = np.zeros(3)
            text = self.font.render("FPS: %f"%(self.clock.get_fps()), True, (255, 255, 255))
            self.screen.blit(text, (1920//2, 20))
            
            pygame.display.flip()
    



# ------------------------- Parameters ----------------------------
bodies = [Body(
    position=np.random.randint(-500, 500, 3),
    mass=np.random.randint(5, 20) * 6e15,
    color=np.random.randint(0, 256, 3)
) for i in range(8)]

bodies.append(Body(
    position=np.zeros(3),
    mass= 6e15 * 1000,
    radius=40,
    color=np.array([255, 255, 255])
))

for body in bodies:
    body.add_velocity(np.random.randint(-500, 500, 3))




# -------------------------- Run --------------------------------

if __name__ == "__main__":
    bodies = np.array(bodies, dtype=object)
    engine = PhysicsEngine()
    app = RenderEngine()
    app.run()