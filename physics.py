import numpy as np
from scipy.spatial import KDTree

def resolveCollisions(app, tree):
    particles = app.fluidParticles
    maxPasses = 8
    for _ in range(maxPasses):
        positions = np.array([[p.cx, p.cy] for p in particles])
        tree = KDTree(positions)
        pairs = tree.query_pairs(r=2 * particles[0].radius)
        if len(pairs) == 0:
            break
        for i, j in pairs:
            resolveParticlePairCollision(particles[i], particles[j], app)

def resolveParticlePairCollision(particle1, particle2, app):
    particle1Pos = np.array([particle1.cx, particle1.cy], dtype=float)
    particle2Pos = np.array([particle2.cx, particle2.cy], dtype=float)
    particle1Vel = np.array([particle1.vx, particle1.vy], dtype=float)
    particle2Vel = np.array([particle2.vx, particle2.vy], dtype=float)

    delta = particle2Pos - particle1Pos
    dist = np.linalg.norm(delta)
    minDist = particle1.radius + particle2.radius
    if (dist < minDist) and (dist != 0):
        deltaUnitVector = delta / dist
        overlap = minDist - dist
        particle1Pos -= (deltaUnitVector * overlap) / 2
        particle2Pos += (deltaUnitVector * overlap) / 2

        p1DotN = np.dot(particle1Vel, deltaUnitVector)
        p2DotN = np.dot(particle2Vel, deltaUnitVector)
        particle1Vel += (p2DotN - p1DotN) * deltaUnitVector
        particle2Vel += (p1DotN - p2DotN) * deltaUnitVector

        particle1.cx, particle1.cy = particle1Pos
        particle1.vx, particle1.vy = particle1Vel
        particle2.cx, particle2.cy = particle2Pos
        particle2.vx, particle2.vy = particle2Vel

def resolveObstacleCollisions(app):
    for particle in app.fluidParticles:
        for obs in app.obstacles:
            particlePos = np.array([particle.cx, particle.cy], dtype=float)
            particleVel = np.array([particle.vx, particle.vy], dtype=float)

            if (obs.left <= particlePos[0] <= obs.right and
                obs.top  <= particlePos[1] <= obs.bottom):

                distLeft   = particlePos[0] - obs.left
                distRight  = obs.right  - particlePos[0]
                distTop    = particlePos[1] - obs.top
                distBottom = obs.bottom - particlePos[1]
                minDist = min(distLeft, distRight, distTop, distBottom)

                if minDist == distLeft:
                    particlePos[0] = obs.left - particle.radius
                    particleVel[0] = -abs(particleVel[0]) * app.coefficientOfRestitution
                elif minDist == distRight:
                    particlePos[0] = obs.right + particle.radius
                    particleVel[0] = abs(particleVel[0]) * app.coefficientOfRestitution
                elif minDist == distTop:
                    particlePos[1] = obs.top - particle.radius
                    particleVel[1] = -abs(particleVel[1]) * app.coefficientOfRestitution
                else:
                    particlePos[1] = obs.bottom + particle.radius
                    particleVel[1] = abs(particleVel[1]) * app.coefficientOfRestitution

                particle.cx, particle.cy = particlePos
                particle.vx, particle.vy = particleVel
                continue

#############################  WRITTEN BY AI, EXEMPT #####################################
            # check edge proximity
            closest = np.array([
                np.clip(particlePos[0], obs.left, obs.right),
                np.clip(particlePos[1], obs.top,  obs.bottom)
            ])
            diff = particlePos - closest
            dist = np.linalg.norm(diff)
            if dist < particle.radius and dist > 0:
                normal = diff / dist
                overlap = particle.radius - dist
                particlePos += normal * overlap
                dot = np.dot(particleVel, normal)
                particleVel -= 2 * dot * normal * app.coefficientOfRestitution
                particle.cx, particle.cy = particlePos
                particle.vx, particle.vy = particleVel

##########################################################################################

def applyFanForce(app):
    if not (app.fanMode) or not (app.mouseIsActive):
        return
    if app.targetPointerX is None or app.targetPointerY is None:
        return
    if app.mouseX is None or app.mouseY is None:
        return
    
    windStrength = 10.0
    mouseRadius = 150

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
    mask = dists < mouseRadius

    # strength falls off linearly with distance
    strength = windStrength * (1 - dists[mask] / mouseRadius)

    # apply force in fan direction to all masked particles at once
    app.velocities[mask, 0] += fanDir[0] * strength
    app.velocities[mask, 1] += fanDir[1] * strength

    # write back to particles
    for i in np.where(mask)[0]:
        app.fluidParticles[i].vx = float(app.velocities[i, 0])
        app.fluidParticles[i].vy = float(app.velocities[i, 1])

#################################################