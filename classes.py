import random, math
from cmu_graphics import drawRect, drawLabel, rgb, drawImage

class FluidParticle:
    def __init__(self, cx, cy, vx, vy, radius, color):
        self.cx = cx
        self.cy  = cy
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.density = 0
        self.pressure = 0
        self.fx = 0
        self.fy = 0
        
class TitleParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(0, 1)
        self.radius = random.randint(3, 8)
        self.speed = math.sqrt(self.vx**2 + self.vy**2)

class Button:
    def __init__(self, cx, cy, width, height, label, action, font, keepCenterAligned=False):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.label = label
        self.action = action  # string identifier for what this button does
        self.font = font
        self.isHovered = False
        self.keepCenterAligned = keepCenterAligned

    def contains(self, mouseX, mouseY):
        return (abs(mouseX - self.cx) < (self.width / 2) and
                abs(mouseY - self.cy) < (self.height / 2))
    
    def drawButton(self, app):
        if self.isHovered:
            fillColor = rgb(80, 160, 255)   # bright blue when hovered
            borderColor = 'white'
            textColor = 'white'
        else:
            fillColor = rgb(20, 40, 80)     # dark blue
            borderColor = rgb(80, 120, 200)
            textColor = rgb(150, 200, 255)

        if self.keepCenterAligned and (self.cx != app.width/2):
            self.cx = app.width / 2
        
        drawRect(self.cx, self.cy,
                self.width, self.height,
                fill=fillColor, border=borderColor, borderWidth=2, align = 'center')
        drawLabel(self.label, self.cx, self.cy,
                fill=textColor, size=20, bold=True, font=self.font, align = 'center')
        
class RectObstacle:
    def __init__(self, x1, y1, x2, y2):
        self.left   = min(x1, x2)
        self.right  = max(x1, x2)
        self.top    = min(y1, y2)
        self.bottom = max(y1, y2)


