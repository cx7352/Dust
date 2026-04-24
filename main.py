"""
Key Features:

a) Smoothed Particle Hydrodynamics, more technical information avaiable within the 'SPH.py' file. It is hard to separate this functionality from
the resolveCollisions logic within 'physics.py' since they are inherently related in nature. However, if you observe closely, or run the simulation
and crank up the values, you can see the effect that the implementation of SPH as opposed to just a bunch of balls bouncing around.

b) 'physics.py' file. This file also contains some math that pretty annoying to actually implement. The coolest feature is by far 'resolveCollisions'
and its accompyning helper function 'resolveParticlePairCollision'. Within the sim, this is one of the most dominant forces and can be seen 
in isolation without any SPH forces on my frst gitHub commit, albeit at a much smaller scale than in the actual simulation. 

c) Resolve Obstacle Collisions, this one took a second to actually implement, but it's fairly simple and I think I could have probably made it more
efficient some how. Spawn an obstacle and watch the fluid collide with it! Partly written by AI.

GRADING SHORTCUTS: 
There are none! There aren't many screens to this projects, so simply run the sim and the motion of the particles is the main thing to look at!

"""
from cmu_graphics import *
from classes import *
from physics import *
from SPH import *
from updaterFunctions import *
import numpy as np
from startScreen import *
from drawingFunctions import *
from creditScreen import *
from tutorialScreen import *

def onAppStart(app):
    url = 'https://od.lk/s/NjhfMTY0NDczNjM2Xw/Intense%20and%20Upbeat%20Electronic%20Trailer%20Music%20-%20Black%20Heat%20%28Copyright%20and%20Royalty%20Free%29.mp3'
    app.bgMusic = Sound(url)
    app.bgMusic.play(restart = True, loop=True)
    
    app.startButtons = [
        Button(app.width/2, app.height/2 - 10,  250, 55, 'Begin Flow', 'start',   'monospace', keepCenterAligned=True),
        Button(app.width/2, app.height/2 + 60, 250, 55, 'Before You Flow', 'tutorial', 'monospace', keepCenterAligned=True),
        Button(app.width/2, app.height/2 + 130, 250, 55, 'Credits',    'credits', 'monospace', keepCenterAligned=True),
        ]
    
    infoButton = Button(260, 30, 40, 40, 'i', 'info', 'monospace')
    app.gameButtons = [infoButton]

def game_onScreenActivate(app):

    # obstacle variables
    app.obstacles = []
    app.obstacleStart = None
    app.obstaclePreview = None
    app.obstacleMode = False

    app.showInfo = False
    app.unlockedFlowParticles = False

    app.keyHoldTimer = 0

    # runtime variables
    app.isPaused = False
    app.mouseIsActive = False
    app.spawnFluidMode = True
    app.fanMode = False
    app.mouseX = None
    app.mouseY = None
    app.targetPointerX = None
    app.targetPointerY = None
    app.fluidParticles = []

    # physical Constants
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

    # AI crap for coloring ###################################################
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
    ##########################################################################

def game_onStep(app):
    if not app.isPaused:
        game_takeStep(app)

def game_takeStep(app):
    if app.spawnFluidMode:
        spawnFluidAtMouse(app)
    if len(app.fluidParticles) != 0: # some fluid particles actually exist
        particles = app.fluidParticles
        positions = np.array([[p.cx, p.cy] for p in particles]) # a 2D array of all the positions of each fluid particle
        tree = KDTree(positions)                                # a KD-tree that automatically maps all the positions, allows for dramatically faster searches 
        computeDensityPressure(particles, positions, tree, app) # Computes the necessary values for all of particles: density and pressure
        computeForces(particles, positions, tree, app)                     
        moveParticles(particles, app)
        resolveObstacleCollisions(app)
        applyFanForce(app)
        resolveCollisions(app, tree)
        updateParticleColorsFromSpeeds(app)
        app.velocities = np.array([[particle.vx, particle.vy] for particle in particles]) # update Our velocity list
    
def game_onKeyPress(app, key):
    key = key.lower()  # ignore case
    
    if key == 'z':
        if len(app.obstacles) != 0:
            app.obstacles.pop()
    if key == 'l' and app.isPaused:
        game_takeStep(app)
    if key == '1':
        app.spawnFluidMode = True
        app.fanMode = app.obstacleMode = False
        app.targetPointerX = None
        app.targetPointerY = None
        app.obstacleStart = None  
        app.obstaclePreview = None
    if key == '2':
        app.fanMode = True
        app.spawnFluidMode = app.obstacleMode = False
        app.targetPointerX = None
        app.targetPointerY = None
        app.obstacleStart = None  
        app.obstaclePreview = None
    if key == '3':
        app.obstacleMode = True
        app.spawnFluidMode = app.fanMode = False
        app.targetPointerX = None
        app.targetPointerY = None
    if key == '4':
        app.spawnFluidMode = app.fanMode = True
        app.obstacleMode = False
        app.targetPointerX = None
        app.targetPointerY = None
        app.obstacleStart = None  
        app.obstaclePreview = None
    if key == 'p':
        app.isPaused = not app.isPaused
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
    if key == 'r':
        app.fluidParticles = []
        app.stiffness = 0.014
        app.restDensity = 1.0
        app.viscosity = 0.01
        app.unlockedFlowParticles = False
    if key == 't':
        app.fluidParticles = []
    if key == 'u':
        app.unlockedFlowParticles = True
    if key == 'escape':
        setActiveScreen('start')
    applyTuning(app, key)

def game_onKeyHold(app, keys):
    app.keyHoldTimer += 1
    keyHoldDelay = 30
    if app.keyHoldTimer < keyHoldDelay:  # wait before starting repeat
        return
    if app.keyHoldTimer % 3 != 0:  
        return
    for key in keys: #only runs every fifth frame
        applyTuning(app, key.lower())

def game_onKeyRelease(app, key):
    app.keyHoldTimer = 0

def game_redrawAll(app):
    drawParticles(app)
    drawObstacles(app)
    drawHUD(app)
    for button in app.gameButtons:
        button.drawButton(app)
    if (app.mouseX != None) and (app.mouseY != None):
        if app.fanMode:
            drawTargetPointer(app)
        else:
            drawMouseDot(app)

def game_onMousePress(app, mouseX, mouseY):
    for button in app.gameButtons:
        if button.contains(mouseX, mouseY):
            if button.action == 'info':
                app.showInfo = not app.showInfo
            return
        
    if app.obstacleMode:
        app.obstacleStart = (mouseX, mouseY)
        return

    app.mouseX, app.mouseY = mouseX, mouseY
    app.mouseIsActive = True

def game_onMouseDrag(app, mouseX, mouseY):
    if app.obstacleMode and app.obstacleStart is not None:
        updateMouseDot(app, mouseX, mouseY)
        app.obstaclePreview = (app.obstacleStart[0], app.obstacleStart[1], mouseX, mouseY)
        return
    
    if app.fanMode:
        updateTargetPointer(app, mouseX, mouseY)
    else:
        updateMouseDot(app, mouseX, mouseY)

def game_onMouseMove(app, mouseX, mouseY):
    for button in app.gameButtons:
        button.isHovered = button.contains(mouseX, mouseY)
    if app.fanMode:
        updateTargetPointer(app, mouseX, mouseY)
    else:
        updateMouseDot(app, mouseX, mouseY)

def game_onMouseRelease(app, mouseX, mouseY):
    if app.obstacleMode and app.obstacleStart is not None:
        x1, y1 = app.obstacleStart
        w = abs(mouseX - x1)
        h = abs(mouseY - y1)
        if w > 5 and h > 5:  # only create if big enough
            app.obstacles.append(RectObstacle(x1, y1, mouseX, mouseY))
        app.obstacleStart = None
        app.obstaclePreview = None
        updateMouseDot(app, mouseX, mouseY)
        return
    app.mouseX, app.mouseY = mouseX, mouseY
    app.mouseIsActive = False

def main():
    runAppWithScreens(initialScreen="start", width = 1200, height = 1200)

main()