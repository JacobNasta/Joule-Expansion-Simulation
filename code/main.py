import pygame
import numpy as np
import matplotlib.pyplot as plt
from particle import Particle
from wall import Wall


def Pos(x, y):
    return np.array([x, y])


def total_kinetic_energy(particles):
    return sum(p.kinetic_energy() for p in particles)


def plot_kinetic_energy(time_array, ke_array, removal_time=None, filename="kinetic_energy.png"):
    fig, ax = plt.subplots()
    ax.plot(time_array, ke_array)
    if removal_time is not None:
        ax.axvline(removal_time, linestyle="--", color="red", label="wall removed")
        ax.legend()
    ax.set_xlabel("Simulated time (s)")
    ax.set_ylabel("Total kinetic energy")
    ax.set_title("Kinetic energy during Joule expansion")
    fig.tight_layout()
    fig.savefig(filename, bbox_inches="tight")
    plt.show()


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

left_wall = 80
right_wall = 800
top_wall = 60
bottom_wall = 400

middle_x = (left_wall + right_wall) / 2
joule_wall = Wall(Pos(middle_x, top_wall), Pos(middle_x, bottom_wall))

start_ticks = pygame.time.get_ticks()

particles = Particle.create_particles(50, Pos(left_wall + 6, top_wall + 6), Pos(middle_x - 6, bottom_wall - 6))

walls = Wall.create_box(Pos(left_wall, top_wall), Pos(right_wall, top_wall),
                         Pos(right_wall, bottom_wall), Pos(left_wall, bottom_wall)) + [joule_wall]

for p in particles:
    p.compute_particle_forces(particles)

dt = 1 / 60
time_array = []
ke_array = []
removal_time = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    if elapsed_time > 10 and joule_wall in walls:
        walls.remove(joule_wall)
        removal_time = elapsed_time
        pygame.image.save(screen, "joulevid.tga")

    for p in particles:
        p.position += p.velocity * dt + 0.5 * p.acceleration * dt ** 2

    for p in particles:
        for w in walls:
            p.wall_interaction(w)

    old_acceleration = {id(p): p.acceleration.copy() for p in particles}
    for p in particles:
        p.compute_particle_forces(particles)

    for p in particles:
        p.velocity += 0.5 * (old_acceleration[id(p)] + p.acceleration) * dt

    screen.fill("white")
    for p in particles:
        p.draw(screen)
    for w in walls:
        w.draw(screen)
    pygame.display.flip()

    time_array.append(elapsed_time)
    ke_array.append(total_kinetic_energy(particles))

    clock.tick(60)

pygame.quit()
plot_kinetic_energy(np.array(time_array), np.array(ke_array), removal_time)
