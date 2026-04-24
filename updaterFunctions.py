import numpy as np
from classes import *
import random
from cmu_graphics import drawCircle, rgb
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

def applyTuning(app, key):
    if key == 'q':
        app.stiffness = min(app.stiffness * 1.05, 200)
    if key == 'a':
        app.stiffness = max(app.stiffness * 0.95, 0.0001)
    if key == 'w':
        app.restDensity = min(app.restDensity * 1.05, 10000)
    if key == 's':
        app.restDensity = max(app.restDensity * 0.95, 0.0001)
    if key == 'e':
        app.viscosity = min(app.viscosity * 1.05, 2)
    if key == 'd':
        app.viscosity = max(app.viscosity * 0.95, 0.005)

def updateTargetPointer(app, mouseX, mouseY):
    targetPointerLength = 60
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

def updateMouseDot(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY


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

def spawnFluidAtMouse(app):
    if ((app.mouseX == None) or
        (app.mouseY == None) or (len(app.fluidParticles) >= 400) or
        (not app.mouseIsActive)):
        if not app.unlockedFlowParticles or not app.mouseIsActive:
            return
    
    particlesSpawnedPerStep = 2
    fluidParticleRadius = 9

    for _ in range(particlesSpawnedPerStep):
        x = app.mouseX + random.uniform(-15, 15)
        y = app.mouseY + random.uniform(-15, 15)
        app.fluidParticles.append(FluidParticle(
            x, y,
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            fluidParticleRadius,
            rgb(30, 144, 255) # particle with no velocity, gets updated immediately after spawning
        ))

    # update our numpy aarrays
    app.densities  = np.zeros(len(app.fluidParticles))
    app.pressures  = np.zeros(len(app.fluidParticles))
    app.velocities = np.array([[particle.vx, particle.vy] for particle in app.fluidParticles])

def updateTitleParticles(app):
     # spawn new particles
    app.titleParticleSpawnTimer += 1
    if app.titleParticleSpawnTimer >= app.titleParticleSpawnRate:
        app.titleParticleSpawnTimer = 0
        for _ in range(3):
            x = random.randint(0, app.width)
            app.titleParticles.append(TitleParticle(x, -20))

    # update positions
    for particle in app.titleParticles:
        particle.vy += app.titleParticleGravity
        particle.x += particle.vx
        particle.y += particle.vy
        particle.speed = math.sqrt(particle.vx**2 + particle.vy**2)

    # remove particles that fall off bottom
    app.titleParticles = [particle for particle in app.titleParticles if particle.y < app.height]


