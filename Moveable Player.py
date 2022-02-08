import pygame
from math import *

resolution = [1600, 900]
screen = pygame.display.set_mode(resolution)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def Vector(self):
        return [self.x, self.y]

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def subtract(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def cross(self, v):
        return self.x * v.y - self.y * v.x

    def multiply(self, n):
        return Vector(self.x*n, self.y*n)

    def unit(self):
        vector = self.multiply(1/self.magnitude())
        return vector

    def drawVec(self, start_x, start_y, n, colour):
        pygame.draw.line(screen, colour, [start_x, start_y], [start_x + self.x * n, start_y + self.y * n], 2)


class Ball:
    def __init__(self, center, radius, colour, velocity, controlled):
        self.center = Vector(center[0], center[1])
        self.radius = radius
        self.colour = colour
        self.velocity = Vector(velocity[0], velocity[1])
        self.playerControl = controlled

    def getCenter(self):
        return self.center.Vector()

    def addVelocity(self, velocity):
        self.velocity = self.velocity.add(velocity)

    def addSpeed(self, speed):
        self.velocity = self.velocity.multiply(speed)

    def move(self):
        self.center = self.center.add(self.velocity)

    def draw(self):
        pygame.draw.circle(screen, self.colour, self.center.Vector(), self.radius, 0)
        self.velocity.drawVec(self.center.getX(), self.center.getY(), 100, (255, 0, 0))


def display(objects):
    for item in objects:
        item.draw()
    pygame.display.flip()


def move(objects):
    for item in objects:
        item.move()


def player(objects, v):
    for item in objects:
        if item.playerControl:
            item.addVelocity(v)


def playerInput(objects):
    keys = pygame.key.get_pressed()
    resultant = Vector(0, 0)
    if keys[pygame.K_w]:
        vec = Vector(0, -0.0005)
        vec.drawVec(1500, 800, 100000, (255, 0, 0))
        resultant = resultant.add(vec)
    if keys[pygame.K_s]:
        vec = Vector(0, 0.0005)
        vec.drawVec(1500, 800, 100000, (255, 0, 0))
        resultant = resultant.add(vec)
    if keys[pygame.K_d]:
        vec = Vector(0.0005, 0)
        vec.drawVec(1500, 800, 100000, (0, 0, 255))
        resultant = resultant.add(vec)
    if keys[pygame.K_a]:
        vec = Vector(-0.0005, 0)
        vec.drawVec(1500, 800, 100000, (0, 0, 255))
        resultant = resultant.add(vec)
    resultant.drawVec(1500, 800, 100000, (0, 255, 0))
    player(objects, resultant)


def orbit(obj):
    orbit = obj
    center = obj.getCenter()
    gravity = Vector(800 - center[0], 450 - center[1])
    factor = gravity.magnitude()
    gravity = gravity.unit()
    gravity = gravity.multiply(1/(factor**2))
    gravity = gravity.multiply(3)
    orbit.addVelocity(gravity)


def mainLoop(objects):
    screen.fill((210, 190, 150))
    move(objects)

    orbit(objects[1])
    orbit(objects[2])

    playerInput(objects)

    display(objects)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

    return True


obj = []
b = Ball((800, 450), 50, (255, 0, 0), [0, 0], False)
b1 = Ball((800, 700), 5, (255, 255, 255), [0.075, 0], True)
b2 = Ball((800, 650), 5, (255, 255, 255), [0.125, 0], False)
obj.append(b)
obj.append(b1)
obj.append(b2)
running = True
while running:
    running = mainLoop(obj)

pygame.quit()
