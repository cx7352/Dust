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

    drawLabel('Credits', app.width/2, 80,
              size=72, bold=True, fill='white', font='monospace')
    drawLine(app.width/2 - 300, 120, app.width/2 + 300, 120,
             fill=rgb(50, 100, 200), lineWidth=2)

    # project
    drawLabel('Flow — A 2D SPH Fluid Simulation',
              app.width/2, 170,
              size=24, bold=True, fill=rgb(150, 200, 255), font='monospace')
    drawLabel('15-112 Final Project  |  Spring 2026',
              app.width/2, 205,
              size=18, fill=rgb(100, 150, 200), font='monospace')
    drawLine(app.width/2 - 300, 235, app.width/2 + 300, 235,
             fill=rgb(50, 100, 200), lineWidth=1)

    # creator
    drawLabel('Created by', app.width/2, 270,
              size=20, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('Caleb Xie', app.width/2, 310,
              size=36, bold=True, fill='white', font='monospace')
    drawLine(app.width/2 - 300, 350, app.width/2 + 300, 350,
             fill=rgb(50, 100, 200), lineWidth=1)

    # references
    drawLabel('References', app.width/2, 385,
              size=18, bold=True, fill=rgb(150, 200, 255), font='monospace')
    drawLabel('Muller et al. 2003 — Particle-Based Fluid Simulation',
              app.width/2, 415,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('for Interactive Applications',
              app.width/2, 438,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('scipy.spatial.KDTree — Neighbor Search',
              app.width/2, 465,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('numpy — Vectorized Physics Computation',
              app.width/2, 490,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLine(app.width/2 - 300, 520, app.width/2 + 300, 520,
             fill=rgb(50, 100, 200), lineWidth=1)

    # music
    drawLabel('Music', app.width/2, 555,
              size=18, bold=True, fill=rgb(150, 200, 255), font='monospace')
    drawLabel('Ross Bugden - Black Heat',
              app.width/2, 585,
              size=15, fill=rgb(100, 150, 200), font='monospace')
    drawLabel('https://soundcloud.com/rossbugden', app.width/2, 608,
              size=15, fill=rgb(80, 120, 180), font='monospace')
    drawLine(app.width/2 - 300, 638, app.width/2 + 300, 638,
             fill=rgb(50, 100, 200), lineWidth=1)

    # tools
    drawLabel('Built with Python, CMU Graphics, numpy, scipy',
              app.width/2, 668,
              size=15, fill=rgb(80, 120, 180), font='monospace')

    app.creditsBackButton.drawButton(app)