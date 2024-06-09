from PhysarumSimulation import PhysarumSimulation

filepath = "Physarum/geo_data/dgm_33250-5889.xyz"
grid_size = 450
trail_decay = 1.0
population = 250
rotation_angle = 22.5
step_width = 1.0

simulation = PhysarumSimulation(population, filepath, rotation_angle, step_width, grid_size, trail_decay)
simulation.runSimulation()