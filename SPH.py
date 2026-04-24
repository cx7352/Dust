import numpy as np

H = 30 # The smoothing radius, particles that are distance greater than this away from a given particle have no influence on said particle
particleMass = 1.0 #Assumed constant for a uniform fluid

"""
Within Smoothed paticle Hydrodynamics, there is something always used called a 'smoothing kernel,' which essentially, for a given particle, looks at the immediate neighbors of that
particle and obtains values for those particles' contributions to 3 main things, density, pressure, and viscosity. I'll admit, the math for this is pretty difficult and I don't fully
understand it, but the smoothing kernal looks something like: ρᵢ = Σ m · W(|rᵢ - rⱼ|, h)
What this is basically saying is that function "w" takes in the distance between the two particles and a user-defined smoothing radius 'h' and returns the three values previously mentioned
of density, pressure, and viscosity all weighted by the particles separation distance.

Taken from the internet, these are the mathematical functions that need to be returned:
W(r, h)   = (1 - (r/h)²)²          for density
∇W(r, h)  = -4r/h² · (1 - (r/h)²)  for pressure
∇²W(r, h) = (1 - r/h)              for viscosity 
"""

################################################# EXEMPT CODE, ALL MATH DONE BY AI

def W_density(r, h):
    comparator = r < h
    result = np.zeros_like(r)
    result[comparator] = (1 - (r[comparator]/h)**2)**2
    return result

def W_pressure_gradient(r_vecs, r_mags, h):
    comparator = (r_mags < h) & (r_mags > 0)
    result = np.zeros_like(r_vecs)
    scalar = np.zeros_like(r_mags)
    scalar[comparator] = -4 * r_mags[comparator] / h**2 * (1 - (r_mags[comparator]/h)**2)
    result[comparator] = scalar[comparator, None] * (r_vecs[comparator] / r_mags[comparator, None])
    return result

def W_viscosity_laplacian(r, h):
    comparator = r < h
    result = np.zeros_like(r)
    result[comparator] = 1 - r[comparator]/h
    return result

#################################################

def computeDensityPressure(particles, positions, tree, app):
    pairs = tree.query_pairs(r=H)
    if len(pairs) == 0:
        for particle in particles:
            particle.density = 0.0
            particle.pressure = 0.0
        app.densities = np.zeros(len(particles))
        app.pressures = np.zeros(len(particles))
        return
    
    pairs = list(pairs) # tree.query returns a set, so we must convert it into a list so that we can index into it, contains tuples of point pairs that are close enough to interact (i, j)
    iIndices, jIndices, r_vecs, r_mags = getijIndicesRVecMags(pairs, positions)
    
    # Accumulate density, each pair contributes to both particles
    densityKernelValues = particleMass * W_density(r_mags, H)
    
    # each particle contributes to its density value, we basically evalute each particle at a distance zero from itself
    densities = np.zeros(len(particles))
    np.add.at(densities, iIndices, densityKernelValues)
    np.add.at(densities, jIndices, densityKernelValues)
    densities += particleMass * W_density(np.zeros(len(particles)), H)
    pressures = app.stiffness * (densities - app.restDensity)       #From equation of state P = mu *(rho_curr - rho_rest)

    # Store on app so that computeForces can access them
    app.densities = densities
    app.pressures = pressures

    for index, particle in enumerate(particles):
        particle.density = densities[index]
        particle.pressure = pressures[index]
    
def computeForces(particles, positions, tree, app):
    velocities = app.velocities
    densities = app.densities   
    pressures = app.pressures    
    
    pairs = list(tree.query_pairs(r=H))
    if len(pairs) == 0:
        for particle in particles:
            particle.fx = 0.0
            particle.fy = 0.0
        return
    
    forces = np.zeros((len(particles), 2))
    iIndices, jIndices, r_vecs, r_mags = getijIndicesRVecMags(pairs, positions)
    
    # Pressure Forces
    avg_pressure = (pressures[iIndices] + pressures[jIndices]) / 2         
    particleDensity = np.maximum(densities[jIndices], 1e-6)
    pressure_scalar = -(particleMass * avg_pressure / particleDensity)
    pressure_grad = W_pressure_gradient(r_vecs, r_mags, H)
    pressure_force = pressure_scalar[:, None] * pressure_grad

    # Viscous Forces
    vel_diff = velocities[jIndices] - velocities[iIndices]
    visc_scalar = app.viscosity * particleMass / particleDensity
    visc_weight = W_viscosity_laplacian(r_mags, H)
    viscosity_force = visc_scalar[:, None] * vel_diff * visc_weight[:, None]

    total_force = pressure_force + viscosity_force

    np.add.at(forces, iIndices, total_force)
    np.add.at(forces, jIndices, -total_force)
    
    for index, particle in enumerate(particles):
        particle.fx = forces[index, 0]
        particle.fy = forces[index, 1]

def getijIndicesRVecMags(pairs, positions):
    iIndices = np.array([particle[0] for particle in pairs])
    jIndices = np.array([particle[1] for particle in pairs])
    
    r_vecs = positions[iIndices] - positions[jIndices]
    r_mags = np.linalg.norm(r_vecs, axis=1)

    return iIndices, jIndices, r_vecs, r_mags  # Given pairs of points and their positions, returns two arrays containing each half of the particle pair (i, j)
        