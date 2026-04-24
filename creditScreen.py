from cmu_graphics import *
from classes import *
from drawingFunctions import *

def credits_onScreenActivate(app):
    app.creditsBackButton = Button(app.width/2, app.height - 80, 200, 50, 'Back', 'back', 'monospace')

def credits_onMouseMove(app, mouseX, mouseY):
    app.creditsBackButton.isHovered = app.creditsBackButton.contains(mouseX, mouseY)

def credits_onMousePress(app, mouseX, mouseY):
    if app.creditsBackButton.contains(mouseX, mouseY):
        setActiveScreen('start')

def credits_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    drawLabel('Credits', app.width/2, 100,
              size=72, bold=True, fill='white', font='monospace')

    drawLine(app.width/2 - 300, 140, app.width/2 + 300, 140,
             fill=rgb(50, 100, 200), lineWidth=2)

    drawLabel('Flow — A 2D SPH Fluid Simulation',
              app.width/2, 200,
              size=24, bold=True, fill=rgb(150, 200, 255), font='monospace')
    drawLabel('15-112 Final Project  |  Spring 2026',
              app.width/2, 240,
              size=18, fill=rgb(100, 150, 200), font='monospace')

    drawLine(app.width/2 - 300, 280, app.width/2 + 300, 280,
             fill=rgb(50, 100, 200), lineWidth=1)

    drawLabel('Created by', app.width/2, 330,
              size=20, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('Caleb Xie', app.width/2, 370,
              size=36, bold=True, fill='white', font='monospace')

    drawLine(app.width/2 - 300, 420, app.width/2 + 300, 420,
             fill=rgb(50, 100, 200), lineWidth=1)

    drawLabel('References', app.width/2, 465,
              size=16, bold=True, fill=rgb(150, 200, 255), font='monospace')
    drawLabel('Muller et al. 2003 — Particle-Based Fluid Simulation',
              app.width/2, 505,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('for Interactive Applications',
              app.width/2, 530,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('scipy.spatial.KDTree — Neighbor Search',
              app.width/2, 570,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('numpy — Vectorized Physics Computation',
              app.width/2, 600,
              size=15, fill=rgb(100, 150, 200), font='monospace')

    drawLine(app.width/2 - 300, 640, app.width/2 + 300, 640,
             fill=rgb(50, 100, 200), lineWidth=1)

    drawLabel('Built with Python, CMU Graphics, numpy, scipy',
              app.width/2, 680,
              size=15, fill=rgb(80, 120, 180), font='monospace')

    app.creditsBackButton.drawButton(app)