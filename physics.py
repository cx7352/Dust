import numpy as np
from scipy.spatial import KDTree

def resolveCollisions(app, tree):
    particles = app.fluidParticles
    pairs = tree.query_pairs(r=2 * particles[0].radius)
    for i, j in pairs:
        resolveParticlePairCollision(particles[i], particles[j])

def resolveParticlePairCollision(particle1, particle2):
    particle1Pos = np.array([particle1.cx, particle1.cy], dtype=float)
    particle2Pos = np.array([particle2.cx, particle2.cy], dtype=float)
    particle1Vel = np.array([particle1.vx, particle1.vy], dtype=float)
    particle2Vel = np.array([particle2.vx, particle2.vy], dtype=float)

    delta = particle2Pos - particle1Pos # A vector that points FROM particle 1 TO particle 2
    dist = np.linalg.norm(delta)
    minDist = particle1.radius + particle2.radius
    if (dist < minDist) and (dist != 0): # They are colliding
        deltaUnitVector = delta / dist # A unit vector that points from P1 to P2, in particle dynamics, changes in velocities only happen along the line of impact, I.E. this vector
        overlap = minDist - dist
        particle1Pos -= (deltaUnitVector * overlap) / 2
        particle2Pos += (deltaUnitVector * overlap) / 2

        p1DotN = np.dot(particle1Vel, deltaUnitVector) #component of particle's velocity along line of impact
        p2DotN = np.dot(particle2Vel, deltaUnitVector)
        particle1Vel += (p2DotN - p1DotN) * deltaUnitVector # The relative difference of their velocities along the ling of impact, essentially swapping their vels along the line of impact
        particle2Vel += (p1DotN - p2DotN) * deltaUnitVector # We are assuming a perfectly elastic collision where energy is conserved, e = 1

       
        particle1.cx, particle1.cy = particle1Pos
        particle1.vx, particle1.vy = particle1Vel
        particle2.cx, particle2.cy = particle2Pos
        particle2.vx, particle2.vy = particle2Vel