from cmu_graphics import *
from classes import *
from updaterFunctions import *
from drawingFunctions import *

def start_onScreenActivate(app):
    app.stepsPerSecond = 60
    app.background = 'black'
    app.titleParticles = []
    app.titleParticleSpawnTimer = 0
    app.titleParticleSpawnRate = 3
    app.titleParticleGravity = 0.01

def start_onMouseMove(app, mouseX, mouseY):
    for button in app.startButtons:
        button.isHovered = button.contains(mouseX, mouseY)

def start_onMousePress(app, mouseX, mouseY):
    app.mouseIsActive = True
    app.mouseX = mouseX
    app.mouseY = mouseY

    for button in app.startButtons:
        if button.contains(mouseX, mouseY):
            if button.action == 'start':
                setActiveScreen('game')
            elif button.action == 'credits':
                setActiveScreen('credits')
            elif button.action == 'tutorial':
                setActiveScreen('tutorial')

def start_onStep(app):
    updateTitleParticles(app)

def start_redrawAll(app):
    drawTitleParticles(app)
    drawTitle(app)
    
