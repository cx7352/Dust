from cmu_graphics import *
from particleClasses import *
from physics import *
from SPH import *
from updaterFunctions import *
import numpy as np
from drawingFunctions import *

def onAppStart(app):



    app.background = 'gray'
    app.isPaused = False
    app.mouseIsActive = False
    app.mouseX = None
    app.mouseY = None
    app.targetPointerX = None
    app.targetPointerY = None
    app.windStrength = 10.0
    app.mouseRadius = 150


    app.fluidParticles = []
    resetParticlesToGrid(app)

    # Physical Constants
    app.accelDueToGravity = 0.25 # g/stepsPerSecond
    app.gravityX = 0
    app.gravityY = app.accelDueToGravity  # default downward
    app.stepsPerSecond = 60
    app.coefficientOfRestitution = 0.60 # The amount of energy that a particle loses on a collision with a wall (0 = all energy is lost, 1 = no energy is lost)

    # SPH constants
    app.stiffness = 0.014
    app.restDensity = 1.0
    app.viscosity = 0.01

    # arrays of all the particles' important values so we don't have to calculate them every time within helper functions
    app.densities = np.zeros(len(app.fluidParticles))
    app.pressures = np.zeros(len(app.fluidParticles))
    app.velocities = np.array([[particle.vx, particle.vy] for particle in app.fluidParticles])


    app.speedGradient = np.array([0.00, 0.07, 0.14, 0.21, 0.28, 0.35,
                                0.42, 0.50, 0.58, 0.65, 0.72, 0.79,
                                0.86, 0.93, 1.00])
    app.speedToColorIndices = np.array([
        (30,  144, 255),   # dodger blue — at rest
        (0,   120, 230),   # ocean blue
        (0,   100, 200),   # deep ocean
        (0,   80,  180),   # dark ocean
        (0,   180, 220),   # shallow water
        (0,   210, 210),   # turquoise
        (0,   220, 170),   # cyan teal
        (0,   210, 100),   # teal green
        (50,  200, 30),    # green
        (150, 210, 0),     # yellow green
        (220, 200, 0),     # yellow
        (255, 150, 0),     # amber
        (255, 80,  0),     # orange
        (255, 20,  20),    # red
        (200, 0,   80),    # deep red — max speed
    ], dtype=float)

def onStep(app):
    if not app.isPaused:
        takeStep(app)

def takeStep(app):
    particles = app.fluidParticles
    positions = np.array([[p.cx, p.cy] for p in particles]) # a 2D array of all the positions of each fluid particle
    tree = KDTree(positions)                                # a KD-tree that automatically maps all the positions, allows for dramatically faster searches 
    computeDensityPressure(particles, positions, tree, app) # Computes the necessary values for all of particles: density and pressure
    computeForces(particles, positions, tree, app)                     
    moveParticles(particles, app)
    applyFanForce(app)
    resolveCollisions(app, tree)
    updateParticleColorsFromSpeeds(app)
    app.velocities = np.array([[particle.vx, particle.vy] for particle in particles]) # update Our velocity list

def onKeyPress(app, key):
    if key == 'l' and app.isPaused:
        takeStep(app)
    if key == 'p':
        app.isPaused = not app.isPaused
    # Stiffness
    if key == 'r':
        resetParticlesToGrid(app)
    if key == 'q':
        app.stiffness *= 1.05
    if key == 'a':
        app.stiffness *= 0.95
    if key == 'w':
        app.restDensity *= 1.05
    if key == 's':
        app.restDensity *= 0.95
    # Viscosity
    if key == 'e':
        app.viscosity *= 1.05
    if key == 'd':
        app.viscosity *= 0.95
    if key == 'right':
        app.gravityX = app.accelDueToGravity
        app.gravityY = 0
    if key == 'left':
        app.gravityX = -app.accelDueToGravity
        app.gravityY = 0
    if key == 'up':
        app.gravityX = 0
        app.gravityY = -app.accelDueToGravity
    if key == 'down':
        app.gravityX = 0
        app.gravityY = app.accelDueToGravity

def redrawAll(app):
    drawLabel(f'viscosity {app.viscosity}', app.width/2,app.height/2)
    drawLabel(f'stiffness {app.stiffness}', app.width/2,app.height/2 + 50)
    drawLabel(f'density {app.restDensity}', app.width/2,app.height/2 + 100)
    drawParticles(app)
    drawTargetPointer(app)

def onMousePress(app, mouseX, mouseY):
    app.mouseIsActive = True

def onMouseDrag(app, mouseX, mouseY):
    updateTargetPointer(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    updateTargetPointer(app, mouseX, mouseY)


def onMouseRelease(app, mouseX, mouseY):
    app.mouseIsActive = False


def main():
    runApp(width = 1000, height = 1000)

main()