from cmu_graphics import *
import numpy as np
import math
import random

class FluidParticle:
    def __init__(self, cx, cy, vx, vy, radius, color):
        self.cx = cx
        self.cy  = cy
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color


def onAppStart(app):
    app.isPaused = False
    app.height, app.width = 1000, 1000
    app.fluidParticles = []
    app.colors = ['blue','red','green','orange','black','purple']
    for i in range(0,500,10):
        app.fluidParticles.append(FluidParticle(10 + i, 50, 2, random.random(), 7, random.choice(app.colors)))
    app.gravity = 0.06
    app.stepsPerSecond = 200
    app.coefficientOfRestitution = 0.85 # The amount of energy that a particle loses on a collision

def onStep(app):
    if app.isPaused:
        return
    takeStep(app)

def takeStep(app):
    for i in range(len(app.fluidParticles)):
        currFluidParticle = app.fluidParticles[i]
        currFluidParticle.vy += app.gravity
        currFluidParticle.cx += currFluidParticle.vx
        currFluidParticle.cy += currFluidParticle.vy
        if (currFluidParticle.cy + currFluidParticle.radius >= app.height):
            currFluidParticle.cy = app.height - currFluidParticle.radius
            currFluidParticle.vy *= -app.coefficientOfRestitution
        if (currFluidParticle.cx + currFluidParticle.radius >= app.width):
            currFluidParticle.cx = app.width - currFluidParticle.radius 
            currFluidParticle.vx *= -app.coefficientOfRestitution
        if (currFluidParticle.cx - currFluidParticle.radius <= 0):
            currFluidParticle.cx = currFluidParticle.radius  
            currFluidParticle.vx *= -app.coefficientOfRestitution
        if (currFluidParticle.cy - currFluidParticle.radius <= 0):
            currFluidParticle.cy = currFluidParticle.radius
            currFluidParticle.vy *= -app.coefficientOfRestitution
    resolveCollisions(app)

def onKeyPress(app, key):
    if key == 'p':
        app.isPaused = not app.isPaused
    if key == 's' and app.isPaused:
        takeStep(app)


def redrawAll(app):
    for particle in app.fluidParticles:
        particleCx, particleCy = particle.cx, particle.cy
        drawCircle(particleCx, particleCy, particle.radius, fill=particle.color)

def resolveCollisions(app):
    particles = app.fluidParticles
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):  # i+1 avoids checking pairs twice
            resolveParticlePairCollision(particles[i], particles[j])

def resolveParticlePairCollision(particle1, particle2):
    particle1Pos = np.array([particle1.cx, particle1.cy], dtype=float)
    particle2Pos = np.array([particle2.cx, particle2.cy], dtype=float)
    particle1Vel = np.array([particle1.vx, particle1.vy], dtype=float)
    particle2Vel = np.array([particle2.vx, particle2.vy], dtype=float)

    delta = particle2Pos - particle1Pos # A vector that points FROM particle 1 TO particle 2
    dist = np.linalg.norm(delta)
    minDist = particle1.radius + particle2.radius
    if (dist < minDist) and (dist != 0): # They are colliding
        deltaUnitVector = delta / dist # A unit vector that points from P1 to P2, in particle dynamics, changes in velocities only happen along the line of impact, I.E. this vector
        overlap = minDist - dist
        particle1Pos -= (deltaUnitVector * overlap) / 2
        particle2Pos += (deltaUnitVector * overlap) / 2

        p1DotN = np.dot(particle1Vel, deltaUnitVector) #component of particle's velocity along line of impact
        p2DotN = np.dot(particle2Vel, deltaUnitVector)
        particle1Vel += (p2DotN - p1DotN) * deltaUnitVector # The relative difference of their velocities along the ling of impact, essentially swapping their vels along the line of impact
        particle2Vel += (p1DotN - p2DotN) * deltaUnitVector # We are assuming a perfectly elastic collision where energy is conserved, e = 1

       
        particle1.cx, particle1.cy = particle1Pos
        particle1.vx, particle1.vy = particle1Vel
        particle2.cx, particle2.cy = particle2Pos
        particle2.vx, particle2.vy = particle2Vel

def main():
    runApp()

main()