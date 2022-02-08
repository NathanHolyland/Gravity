import pygame
import time
from math import *
from random import randrange


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def subtract(self, v):
        return Vector(self.x - v.x, self.y - v.y)

    def multiply(self, n):
        return Vector(self.x*n, self.y*n)

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def unit(self):
        return self.multiply(1/self.magnitude())

    def vec(self):
        return [self.x, self.y]

    def drawVec(self, startPos, colour, n):
        pygame.draw.line(screen, colour, startPos, [startPos[0]+self.x*n, startPos[1]+self.y*n])


class Planet:
    def __init__(self, colour, position, radius, mass, velocity):
        self.colour = colour
        self.position = Vector(position[0], position[1])
        self.radius = radius
        self.mass = mass
        self.velocity = Vector(velocity[0], velocity[1])

    def getPosition(self):
        return self.position

    def getMass(self):
        return self.mass

    def getRadius(self):
        return self.radius

    def getVelocity(self):
        return self.velocity

    def translate(self, vector):
        self.position = self.position.add(vector)

    def move(self, frames):
        self.position = self.position.add(self.velocity.multiply(1/frames))

    def changeVelocity(self, velocity):
        self.velocity = self.velocity.add(velocity)

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.position.vec(), self.radius, 1)

    def gravity(self, planet, constant, frames):
        vector = self.position.subtract(planet.getPosition())
        distance = vector.magnitude()
        unit = vector.unit()
        force = constant * ((self.getMass() * planet.getMass()) / distance**2)
        acceleration = force / self.mass
        velocity = unit.multiply(-acceleration)
        self.velocity = self.velocity.add(velocity.multiply(1/frames))


class Trail:
    def __init__(self, pos, radius, colour, lifespan):
        self.pos = Vector(pos[0], pos[1])
        self.radius = radius
        self.r = colour[0]
        self.g = colour[1]
        self.b = colour[2]
        self.lifespan = lifespan
        self.totalLife = lifespan
        self.opacity = 1
        # lifespan in seconds

    def tickDown(self, elapsed):
        self.lifespan -= elapsed
        self.opacity = self.lifespan/self.totalLife

    def draw(self):
        r = self.r
        g = self.g
        b = self.b
        o = self.opacity
        pygame.draw.circle(screen, (r*o, g*o, b*o), self.pos.vec(), self.radius, 0)

    def translate(self, vector):
        self.pos = self.pos.add(vector)


def collisions(objects):
    for item in objects:
        for item2 in objects:
            if item != item2:
                vector = item.getPosition().subtract(item2.getPosition())
                distance = vector.magnitude()
                bound = item.getRadius() + item2.getRadius()
                if distance < bound:
                    mass = item.getMass() + item2.getMass()
                    newPosition = item.getPosition().subtract(vector.multiply(0.5))
                    momentum1 = item.getVelocity().multiply(item.getMass())
                    momentum2 = item2.getVelocity().multiply(item2.getMass())

                    momentumC = momentum1.add(momentum2)
                    newVelocity = momentumC.multiply(1/mass)
                    radius = mass/10
                    c1 = item.colour
                    c2 = item2.colour
                    mixed = [(c1[0]+c2[0])//2, (c1[1]+c2[1])//2, (c1[2]+c2[2])//2]
                    newPlanet = Planet(mixed, newPosition.vec(), radius, mass, newVelocity.vec())
                    objects.append(newPlanet)
                    objects.remove(item)
                    objects.remove(item2)
                    break


def checkEligibility(p1, p2):
    distance = (p1.getPosition().subtract(p2.getPosition())).magnitude()
    mass = p2.getMass()
    rating = (mass/distance)*10**4
    if rating < 1:
        return False
    return True


def globalGravity(objects, constant, f):
    for item in objects:
        for item2 in objects:
            if item != item2:
                if checkEligibility(item, item2):
                    item.gravity(item2, constant, f)


def globalUpdate(objects, f):
    for item in objects:
        item.move(f)
        item.velocity.drawVec(item.getPosition().vec(), (255, 0, 0), 0.5)
        item.draw()


def renderTrails(objects, p, elapsed):
    for item in objects:
        colour = item.colour
        newParticle = Trail(item.getPosition().vec(), 1, colour, 2)
        p.append(newParticle)

    for particle in p:
        particle.draw()
        particle.tickDown(elapsed)
        if particle.lifespan < 0:
            p.remove(particle)


resolution = [1000, 1000]
screen = pygame.display.set_mode(resolution)

planets = []
sun = Planet((255, 0, 0), (500, 500), 50, 500, [0, 0])
earth = Planet((0, 255, 0), (800, 500), 0.005, 0.05, [300, 200])
mercury = Planet((0, 0, 255), (400, 500), 0.001, 0.01, [300, -600])
jupiter = Planet((255, 0, 0), (900, 500), 0.01, 0.1, [300, 150])

particles = []

planets.append(sun)
planets.append(mercury)
planets.append(earth)
planets.append(jupiter)

rogue_planet = Planet((255, 255, 255), (200, 400), 0.1, 1, [0, 200])
planets.append(rogue_planet)

# rogue_star = Planet((255, 0, 0), (0, 0), 10, 100, [0, 0])
# planets.append(rogue_star)

for i in range(1):
    position = [randrange(0, 1600), randrange(0, 900)]
    velocity = [randrange(-200, 200), randrange(-200, 200)]
    mass = randrange(1, 50)/10
    radius = mass/10
    newplanet = Planet((255, 255, 255), position, radius, mass, velocity)
    planets.append(newplanet)

running = True
fps = 120
conversion = 0
time_elapsed = 0
scale = 1
while running:
    start_time = time.time()
    ignored_time = 0
    screen.fill((0, 0, 0))
    globalGravity(planets, 50000, fps)
    renderTrails(planets, particles, time_elapsed)
    collisions(planets)
    globalUpdate(planets, fps)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        mod = Vector(0, 5)
        for item in planets:
            item.translate(mod)
        for item in particles:
            item.translate(mod)
    if keys[pygame.K_s]:
        mod = Vector(0, -5)
        for item in planets:
            item.translate(mod)
        for item in particles:
            item.translate(mod)
    if keys[pygame.K_a]:
        mod = Vector(5, 0)
        for item in planets:
            item.translate(mod)
        for item in particles:
            item.translate(mod)
    if keys[pygame.K_d]:
        mod = Vector(-5, 0)
        for item in planets:
            item.translate(mod)
        for item in particles:
            item.translate(mod)

    if keys[pygame.K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    end_time = time.time()
    time_elapsed = end_time - start_time
    if time_elapsed != 0:
        fps = 1/(time_elapsed-ignored_time)
pygame.quit()

