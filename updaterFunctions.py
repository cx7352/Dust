import numpy as np
from particleClasses import *
import random
from cmu_graphics import rgb
import math


################################################# EXEMPT CODE, LINEAR COLOR INTERPOLATION DONE BY AI

def updateParticleColorsFromSpeeds(app):
    speeds = np.linalg.norm(app.velocities, axis=1)
    weightedSpeeds = np.clip((speeds) / 15.0, 0.0, 1.0)
    indices = np.clip(np.searchsorted(app.speedGradient, weightedSpeeds, side='right') - 1, 0, len(app.speedGradient) - 2)
    t0 = app.speedGradient[indices]
    t1 = app.speedGradient[indices + 1]
    alpha = ((weightedSpeeds - t0) / (t1 - t0))[:, None]
    colors = (app.speedToColorIndices[indices] + alpha * (app.speedToColorIndices[indices + 1] - app.speedToColorIndices[indices])).astype(int)
    for index, particle in enumerate(app.fluidParticles):
        particle.color = rgb(int(colors[index, 0]), int(colors[index, 1]), int(colors[index, 2]))

#################################################

def updateTargetPointer(app, mouseX, mouseY):
    targetPointerLength = 40
    if (app.mouseX != None) and (app.mouseY != None):
            prevMouseXY = np.array([app.mouseX, app.mouseY])
            app.mouseX, app.mouseY = mouseX, mouseY
            currMouseXY = np.array([app.mouseX, app.mouseY])
            deltaXYVector = currMouseXY - prevMouseXY
            magn = np.linalg.norm(deltaXYVector)
            if magn > 0.5:
                deltaXYUnitVector = deltaXYVector / magn
                scaledDeltaXYVector = deltaXYUnitVector * targetPointerLength
                endPoint = currMouseXY + scaledDeltaXYVector
                app.targetPointerX = int(endPoint[0])
                app.targetPointerY = int(endPoint[1])
    else:
            app.mouseX, app.mouseY = mouseX, mouseY

def resetParticlesToGrid(app):
    app.fluidParticles = []
    spaceBetweenParticles = 20
    rows, cols = 20, 20
    startX = (app.width - cols * spaceBetweenParticles) / 2
    startY = 100
    for row in range(rows):
        for col in range(cols):
            x = startX + col * spaceBetweenParticles
            y = startY + row * spaceBetweenParticles
            app.fluidParticles.append(FluidParticle(
                x, y,
                random.uniform(-0.5, 0.5),
                random.uniform(0, 0.5),
                6,
                rgb(30, 100, 255)
            ))
    app.densities = np.zeros(len(app.fluidParticles))
    app.pressures = np.zeros(len(app.fluidParticles))
    app.velocities = np.array([[particle.vx, particle.vy] for particle in app.fluidParticles])

def moveParticles(particles, app):
    for particle in particles:
        # applying the forces derived from SPH operators
        particle.vx += particle.fx
        particle.vy += particle.fy

        # gravity!
        particle.vx += app.gravityX
        particle.vy += app.gravityY

    
        particle.cx += particle.vx
        particle.cy += particle.vy

        # Bounding Box Code
        if (particle.cy + particle.radius >= app.height):
            particle.cy = app.height - particle.radius
            particle.vy *= -app.coefficientOfRestitution
        if (particle.cx + particle.radius >= app.width):
            particle.cx = app.width - particle.radius 
            particle.vx *= -app.coefficientOfRestitution
        if (particle.cx - particle.radius <= 0):
            particle.cx = particle.radius  
            particle.vx *= -app.coefficientOfRestitution
        if (particle.cy - particle.radius <= 0):
            particle.cy = particle.radius
            particle.vy *= -app.coefficientOfRestitution



