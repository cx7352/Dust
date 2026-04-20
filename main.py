from cmu_graphics import *
import math
import random
from particleClasses import *
from physics import *
from SPH import *

def onAppStart(app):
    app.isPaused = False
    app.height, app.width = 1000, 1000
    app.fluidParticles = []
    app.colors = ['blue','red','green','orange','black','purple']
    resetParticles(app)
    app.gravity = 0.16 # g/stepsPerSecond
    app.stepsPerSecond = 60
    app.coefficientOfRestitution = 0.60 # The amount of energy that a particle loses on a collision with a wall (0 = all energy is lost, 1 = no energy is lost)
    app.stiffness = 0.017
    app.restDensity = 4
    app.viscosity = 0.035

def onStep(app):
    if app.isPaused:
        return
    takeStep(app)

def takeStep(app):
    particles = app.fluidParticles
    positions = np.array([[p.cx, p.cy] for p in particles])
    tree = KDTree(positions)

    computeDensityPressure(particles, tree, app)
    computeForces(particles, tree, app)

    for p in particles:
        p.color = rgb(*densityToColor(p.density, app.restDensity))

    for particle in particles:
        # applying the forces derived from SPH operators
        particle.vx += particle.fx
        particle.vy += particle.fy

        # gravity!
        particle.vy += app.gravity

    
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
    resolveCollisions(app, tree)

def resetParticles(app):
    app.fluidParticles = []
    for i in range(150):
        app.fluidParticles.append(FluidParticle(10 + i*5, 50, 2, random.random(), 10, 'cyan'))

def onKeyPress(app, key):
    if key == 'p':
        app.isPaused = not app.isPaused
    # Stiffness
    if key == 'r':
        resetParticles(app)
    if key == 'q':
        app.stiffness *= 1.05
        print(f'STIFFNESS: {app.stiffness:.4f}')
    if key == 'a':
        app.stiffness *= 0.95
        print(f'STIFFNESS: {app.stiffness:.4f}')
    # Rest density
    if key == 'w':
        app.restDensity *= 1.05
        print(f'REST_DENSITY: {app.restDensity:.4f}')
    if key == 's':
        app.restDensity *= 0.95
        print(f'REST_DENSITY: {app.restDensity:.4f}')
    # Viscosity
    if key == 'e':
        app.viscosity *= 1.05
        print(f'VISCOSITY: {app.viscosity:.4f}')
    if key == 'd':
        app.viscosity *= 0.95
        print(f'VISCOSITY: {app.viscosity:.4f}')

def redrawAll(app):
    drawLabel(f'viscosity {app.viscosity}', app.width/2,app.height/2)
    drawLabel(f'stiffness {app.stiffness}', app.width/2,app.height/2 + 50)
    drawLabel(f'density {app.restDensity}', app.width/2,app.height/2 + 100)
    for particle in app.fluidParticles:
        particleCx, particleCy = particle.cx, particle.cy
        drawCircle(particleCx, particleCy, particle.radius, fill=particle.color)


def main():
    runApp()

main()