from cmu_graphics import *

def drawParticles(app):
    for particle in app.fluidParticles:
        particleCx, particleCy = particle.cx, particle.cy
        drawCircle(particleCx, particleCy, particle.radius, fill=particle.color)

def drawTargetPointer(app):
    if (app.targetPointerX != None) and (app.targetPointerY != None):
        drawLine(app.mouseX, app.mouseY, app.targetPointerX, app.targetPointerY, fill = 'red', lineWidth = 4, arrowEnd = True)

def drawMouseDot(app):
    drawCircle(app.mouseX, app.mouseY, 6, fill = 'yellow', opacity = 60)

def drawTitleParticles(app):
    for particle in app.titleParticles:
        normalizedSpeed = min(particle.speed / 5, 1.0)
        r = int(30  + normalizedSpeed * 225)
        g = int(144 - normalizedSpeed * 100)
        b = int(255 - normalizedSpeed * 100)
        drawCircle(particle.x, particle.y, particle.radius, fill=rgb(r, g, b))

def drawTitle(app):
    drawLabel('Flow', app.width/2, app.height/2 - 180,
              size=256, bold=True, fill='white', font='monospace')
    drawLabel('An Exploration of Smoothed Particle Hydrodynamics', app.width/2, app.height/2 - 40,
              size = 24, bold = True, fill = 'white', font = 'monospace')
    for button in app.startButtons:
        button.drawButton(app)
    
def drawPropertiesBox(app):
    drawRect(10, 10, 220, 110, fill=rgb(15, 20, 40), 
             border=rgb(50, 100, 200), borderWidth=2, opacity= 60)
    drawLabel('Properties', 120, 28, 
              fill=rgb(150, 200, 255), size=24, bold=True, font='monospace')
    drawLabel(f'Stiffness:    {app.stiffness:.4f}',  120, 52,
              fill='white', size=16, font='monospace')
    drawLabel(f'Rest Density: {app.restDensity:.4f}', 120, 72,
              fill='white', size=16, font='monospace')
    drawLabel(f'Viscosity:    {app.viscosity:.4f}',   120, 92,
              fill='white', size=16, font='monospace')


def drawControlsPanel(app):
    drawRect(app.width - 242, 10, 235, 375, fill=rgb(15, 20, 40),
             border=rgb(50, 100, 200), borderWidth=2, opacity = 60)
    drawLabel('Controls', app.width - 120, 28,
              fill=rgb(150, 200, 255), size=24, bold=True, font='monospace')

    flowLockStr = 'LOCKED' if not app.unlockedFlowParticles else 'UNLOCKED'
    controls = [
        '1 - FLOW',
        '2 - FAN',
        '3 - OBSTACLE',
        '4 - JET',
        'Z - UNDO OBSTACLE',
        'R — FULL RESET',
        'T - PARTICLE RESET',
        'P - PAUSE',
        'L - STEP',
        'Q/A — STIFFNESS ±5%',
        'W/S — DENSITY ±5%',
        'E/D — VISCOSITY ±5%',
        '← → ↑ ↓ — GRAVITY',
        f'U — FLOW IS {flowLockStr}',
        'ESC - RETURN HOME'
    ]
    for i, line in enumerate(controls):
        drawLabel(line, app.width - 210, 52 + i * 22,
                  fill='white', size=16, font='monospace', align = 'left')
        
def drawInfoBox(app):
    drawRect(app.width/2, app.height/2, 1000, 200,
            fill=rgb(15, 20, 40), border=rgb(50, 100, 200), borderWidth=2, opacity = 60, align = 'center')
    drawLabel('Stiffness: controls how hard particles bounce apart — higher makes fluid more explosive',
            app.width/2, app.height/2 - 50,
            fill='white', size=18, font='monospace')
    drawLabel('Rest Density: controls cohesion — higher pulls particles together into a tighter blob',
            app.width/2, app.height/2,
            fill='white', size=18, font='monospace')
    drawLabel('Viscosity: controls thickness — higher makes it flow like honey, lower like water',
            app.width/2, app.height/2 + 50,
            fill='white', size=18, font='monospace')
    
def drawObstacles(app):
    for obs in app.obstacles:
        drawRect(obs.left, obs.top,
                 obs.right - obs.left,
                 obs.bottom - obs.top,
                 fill=rgb(40, 40, 60), border=rgb(100, 150, 255), borderWidth=2)

    if app.obstaclePreview is not None:
        x1, y1, x2, y2 = app.obstaclePreview
        left, top = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)
        if w < 2 or h < 2:  # ← skip if too small to draw
            return
        drawRect(left, top, w, h,
                 fill=None, border=rgb(100, 150, 255), borderWidth=2, opacity=60)

def drawHUD(app):
    drawPropertiesBox(app)
    drawControlsPanel(app)
    drawLabel(f'Flow Particles: {len(app.fluidParticles)}', 10, 150,
                fill='white', size=24, font='monospace', align = 'left')
    if app.showInfo:
        drawInfoBox(app)


