import numpy as np
from scipy.spatial import KDTree
import math

def resolveCollisions(app, tree):
    particles = app.fluidParticles
    MAX_PASSES = 8  # safety cap to prevent infinite loop
    for _ in range(MAX_PASSES):
        positions = np.array([[p.cx, p.cy] for p in particles])
        tree = KDTree(positions)
        pairs = tree.query_pairs(r=2 * particles[0].radius)
        if len(pairs) == 0:  
            break
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
        deltaUnitVector = delta / dist # A uni                                                                                                      t vector that points from P1 to P2, in particle dynamics, changes in velocities only happen along the line of impact, I.E. this vector
        overlap = minDist - dist
        particle1Pos -= (deltaUnitVector * overlap) / 2
        particle2Pos += (deltaUnitVector * overlap) / 2

        p1DotN = np.dot(particle1Vel, deltaUnitVector) #component of particle's velocity along line of impact
        p2DotN = np.dot(particle2Vel, deltaUnitVector)
        particle1Vel += (p2DotN - p1DotN) * deltaUnitVector # The relative difference of their velocities along the ling of impact, essentially swapping their vels along the line of impact
        particle2Vel += (p1DotN - p2DotN) * deltaUnitVector # We are assuming a perfectly elastic collision where energy is conserved, e = 1, equal masses as well

       
        particle1.cx, particle1.cy = particle1Pos
        particle1.vx, particle1.vy = particle1Vel
        particle2.cx, particle2.cy = particle2Pos
        particle2.vx, particle2.vy = particle2Vel

def applyFanForce(app):
    if not app.mouseIsActive:
        return
    if app.targetPointerX is None or app.targetPointerY is None:
        return
    if app.mouseX is None or app.mouseY is None:
        return

    # compute fan direction from mouse to target pointer
    fanDir = np.array([app.targetPointerX - app.mouseX, 
                       app.targetPointerY - app.mouseY], dtype=float)
    fanDirMag = np.linalg.norm(fanDir)
    if fanDirMag == 0:
        return
    fanDir /= fanDirMag  # unit vector

    # vectorized distance from mouse to every particle
    positions = np.array([[p.cx, p.cy] for p in app.fluidParticles])
    mousePos = np.array([app.mouseX, app.mouseY])
    deltas = positions - mousePos
    dists = np.linalg.norm(deltas, axis=1)

################################################# EXEMPT CODE, WAS ORIGINALLY WRITTEN USING LISTS, BUT AI CONVERTED TO VECTORIZED NUMPY OPERATIONS

    # mask of particles within fan radius
    mask = dists < app.mouseRadius

    # strength falls off linearly with distance
    strength = app.windStrength * (1 - dists[mask] / app.mouseRadius)

    # apply force in fan direction to all masked particles at once
    app.velocities[mask, 0] += fanDir[0] * strength
    app.velocities[mask, 1] += fanDir[1] * strength

    # write back to particles
    for i in np.where(mask)[0]:
        app.fluidParticles[i].vx = float(app.velocities[i, 0])
        app.fluidParticles[i].vy = float(app.velocities[i, 1])

#################################################