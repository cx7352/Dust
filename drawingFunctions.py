from cmu_graphics import *

def drawParticles(app):
    for particle in app.fluidParticles:
        particleCx, particleCy = particle.cx, particle.cy
        drawCircle(particleCx, particleCy, particle.radius, fill=particle.color)

def drawTargetPointer(app):
    if (app.targetPointerX != None) and (app.targetPointerY != None):
        drawLine(app.mouseX, app.mouseY, app.targetPointerX, app.targetPointerY, fill = 'red', lineWidth = 6)
