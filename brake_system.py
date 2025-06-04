import random

class BrakeSystem:
    def __init__(self, piston_area, num_cylinders, friction_coeff, brake_pad_wear, leak_chance, brake_delay):
        self.piston_area = piston_area  # m² (area of brake cylinder piston)
        self.num_cylinders = num_cylinders  # number of brake cylinders
        self.friction_coeff = friction_coeff # coefficient of friction (depending on brake type)
        self.brake_pipe_pressure = 5.0 # initialize brake pressures (in bar)
        self.brake_cylinder_pressure = 0.0
        self.deceleration_sensor = 0.0
        self.brake_pad_wear = brake_pad_wear  # 0-100% efficiency
        self.leak_chance = leak_chance  # chance of brake leak (0-1)
        self.brake_delay = brake_delay  # delay in seconds for brake response

    def apply_brake(self, demanded_pressure, train_mass_kg):
        # simulate random chance for brake leak
        if random.random() < self.leak_chance: 
            print("Brake leak detected! Pressure reduced.")
            demanded_pressure *= 0.7  # leak reduces pressure by 30%

        # set demanded pressure (0-5 bar)
        self.brake_cylinder_pressure = demanded_pressure

        # calculate force per cylinder based on pressure and piston area
        force_per_cylinder = self.calculate_brake_force()
        total_force = force_per_cylinder * self.num_cylinders

        # calculate deceleration (m/s²) using force = mass * acceleration (a = f/m)
        self.deceleration_sensor = total_force / train_mass_kg
        return self.deceleration_sensor 

    def release_brake(self):
        """Release brakes (pressure drop)."""
        self.brake_cylinder_pressure = 0.0
        self.deceleration_sensor = 0.0

    def get_wear_factor(self):
        """Scale friction based on pad wear."""
        return self.brake_pad_wear ** 2

    def calculate_brake_force(self):
        """Convert pressure (bar) to force (N)."""
        # effective friction force considering wear
        effective_friction = self.friction_coeff * self.get_wear_factor()

        # convert pressure from bar to pascal and calculate force
        pressure_pa = self.brake_cylinder_pressure * 100000  
        return pressure_pa * self.piston_area * effective_friction  # F = P*A*μ