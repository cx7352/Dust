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
        