from cmu_graphics import *
from classes import *
from drawingFunctions import *

##################################### THIS ENTIRE THING IS AI GENERATED #####################################
# Just wanted a tutorial screen but I am not typing all that out, hell no!

def tutorial_onScreenActivate(app):
    app.tutorialBackButton = Button(app.width/2, app.height - 60, 200, 50, 'Back', 'back', 'monospace')
    app.tutorialScroll = 0
    numLines = 57 
    contentHeight = numLines * 28
    app.tutorialMaxScroll = max(0, contentHeight - (app.height - 200))

def tutorial_onMouseMove(app, mouseX, mouseY):
    app.tutorialBackButton.isHovered = app.tutorialBackButton.contains(mouseX, mouseY)

def tutorial_onMousePress(app, mouseX, mouseY):
    if app.tutorialBackButton.contains(mouseX, mouseY):
        setActiveScreen('start')

def tutorial_onKeyPress(app, key):
    if key == 'up':
        app.tutorialScroll = max(0, app.tutorialScroll - 20)
    if key == 'down':
        app.tutorialScroll = min(app.tutorialMaxScroll, app.tutorialScroll + 40)
    if key == 'escape':
        setActiveScreen('start')

def tutorial_redrawAll(app):

    # title
    drawLabel('How to Use Flow', app.width/2, 60,
              size=52, bold=True, fill='white', font='monospace')
    drawLine(app.width/2 - 400, 100, app.width/2 + 400, 100,
             fill=rgb(50, 100, 200), lineWidth=2)

    lines = [
        ('-GETTING STARTED-', True),
        ('', False),
        ('When you enter the sim, the screen starts empty', False),
        ('Hold down the mouse to pour fluid onto the screen', False),
        ('Fluid spawns at your cursor and falls with gravity', False),
        ('', False),
        ('-MODES-', True),
        ('', False),
        ('Press 1, 2, 3, and 4 to toggle between spawn, fan, obstacle, and jet modes', False),
        ('Spawn Mode: hold mouse to pour fluid at cursor', False),
        ('Fan Mode: hold mouse to blow fluid in cursor direction', False),
        ('Obstalce Mode: click and drag to create an obstalce for the fluid', False),
        ('Jet Mode: the child of spawn and fan modes, aim a jet of fluid', False),    
        ('', False),
        ('-GRAVITY-', True),
        ('', False),
        ('Arrow keys change the direction of gravity', False),
        ('Right arrow — gravity pulls right', False),
        ('Left arrow  — gravity pulls left', False),
        ('Up arrow    — gravity pulls upward', False),
        ('Down arrow  — gravity pulls down (default)', False),
        ('', False),
        ('-TUNING THE FLUID-', True),
        ('', False),
        ('Q / A — increase / decrease Stiffness', False),
        ('Higher stiffness makes fluid more explosive and bouncy', False),
        ('Lower stiffness makes fluid sluggish and clumpy', False),
        ('', False),
        ('W / S — increase / decrease Rest Density', False),
        ('Higher rest density pulls particles together into a blob', False),
        ('Lower rest density lets particles spread out freely', False),
        ('', False),
        ('E / D — increase / decrease Viscosity', False),
        ('Higher viscosity makes the fluid thick like honey', False),
        ('Lower viscosity makes it flow fast like water', False),
        ('Hold any tuning key to continuously adjust the value', False),
        ('', False),
        ('-OTHER CONTROLS-', True),
        ('', False),
        ('Z  — undo the most recent obstacle created', False),
        ('P  — pause and unpause the simulation', False),
        ('L  — step forward one frame while paused', False),
        ('R  — reset all fluid particles and properties, relock fluid cap', False),
        ('T  — reset all fluid particles, properties and fluid cap remain unchanged', False), 
        ('U - Uncaps the 400 particle limit, once uncapped, cannot be capped again unless particles are reset', False),
        ('', False),
        ('-GOOD TO KNOWS-', True),
        ('', False),
        ('We recommend you do not go past 400 flow particles, but feel free to unlock this if you wish,', False),
        ('However, expect a very dramatic drop in performance due to the increased computational load', False),
        ('Flow particles will traverse a color gradient as they accelerate and gain more velocity and speed', False),
        ('Blue indicates particles at a lower speed while deep red indicates particles at a higher velocity', False),
        ('We also recommend that you play on a relatively large window size, full screen if possible', False)
    ]

    startY = 130 - app.tutorialScroll
    lineHeight = 28

    for i, (text, isHeader) in enumerate(lines):
        y = startY + i * lineHeight
        if y < 110 or y > app.height - 80:
            continue
        if isHeader:
            drawLabel(text, app.width/2, y,
                      size=24, bold=True, fill=rgb(100, 180, 255), font='monospace')
        else:
            drawLabel(text, app.width/2, y,
                      size=18, fill=rgb(180, 210, 255), font='monospace')

    # back button
    drawRect(0, app.height - 90, app.width, 90, fill='black')
    app.tutorialBackButton.drawButton(app)

    drawLabel('↑ ↓ to scroll', app.width - 100, app.height - 70,
              size=13, fill=rgb(80, 120, 180), font='monospace')
    
###############################################################################################################