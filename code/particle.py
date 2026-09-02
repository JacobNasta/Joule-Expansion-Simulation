import numpy as np
import pygame
from numpy.random import uniform
from wall import Wall

u = 1.67e-27
mass = 1
epsilon = 1
sigma = 8.0
scaling_factor = 1

class Particle:
    def __init__(self, position, velocity, radius = 5, mass = mass):
        self.position = self.screen_to_position(position).astype(float)
        self.velocity = self.screen_to_position(velocity).astype(float)
        self.acceleration = np.array([0.0,0.0])
        self.radius = self.screen_to_position(radius)
        self.mass = mass

    def compute_particle_forces(self, particles):
        self.acceleration[:] = 0.0
        for particle in particles:
            if particle is self:
                continue
            self.particle_interaction(particle)

    def wall_interaction(self, wall):
        dis = distance(wall.start[0],wall.start[1], wall.end[0],wall.end[1], self.position[0],self.position[1])
        if abs(dis) < self.radius + wall.width / 2:
            vec = wall.start - wall.end
            n = normal(vec[0], vec[1], dis)
            v = self.velocity
            self.velocity = v - 2*(float(v@n)/float(n@n))*n

    @staticmethod
    def create_particles(number, co1,co2):
        particle_list = []
        for i in range (number):
            pos = np.array([uniform(co1[0], co2[0]), uniform(co1[1], co2[1])])
            vel = np.array([uniform(-200, 200), uniform(-200,200)])
            particle = Particle(pos,vel)
            particle_list.append(particle)
        return particle_list

    def particle_interaction(self, particle):
        r_vec = particle.position - self.position
        r = np.linalg.norm(r_vec)
        if r == 0:
            return
        r = max(r, 0.6 * sigma) # particles can get too close due to the rate at which the code updates so a clamp is used  
        n = r_vec / r
        f_mag = -48 * epsilon / self.mass * ((sigma / r) ** 12 / r - (sigma / r) ** 6 / (2 * r))
        self.acceleration += f_mag * n

    def kinetic_energy(self):
        return 0.5 * self.mass * float(self.velocity @ self.velocity)

    def screen_to_position(self,vec):
        return vec * scaling_factor

    def position_to_screen(self,vec):
        return vec / scaling_factor

    def draw(self,screen):
        pos = self.position_to_screen(self.position)
        pygame.draw.circle(screen, "black", (pos[0],pos[1]), self.position_to_screen(self.radius))


def distance(x1,y1,x2,y2,x0,y0):
    return ((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1) / np.sqrt((y2-y1)**2 + (x2-x1)**2)

def normal(x, y, distance):
    if distance > 0:
        return np.array([y, -x])
    else:
        return np.array([-y, x])
