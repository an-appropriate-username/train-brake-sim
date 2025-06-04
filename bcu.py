class BCU:
    def __init__(self):
        self.min_deceleration = 0.8  # m/s² (TSI standard)

    def perform_brake_test(self, train, brake_system, brake_demand, adhesion_factor):
        # apply brake and calculate force
        deceleration = brake_system.apply_brake(brake_demand, train.mass_kg)
        
        # calculate forces
        force_per_cylinder = (brake_system.brake_cylinder_pressure * 100000) * brake_system.piston_area * brake_system.friction_coeff
        total_force = force_per_cylinder * brake_system.num_cylinders * brake_system.brake_pad_wear
        
        # calculate effective deceleration
        effective_deceleration = deceleration * adhesion_factor

        # calculate stopping distance
        braking_distance = self.calculate_braking_distance(train.speed_mps, effective_deceleration, brake_system.brake_delay)
        
        # check for wheel slip
        slip = self.detect_wheel_slip(deceleration, adhesion_factor)
        
        # check TSI compliance
        passed = effective_deceleration >= self.min_deceleration
        
        # package all test data
        data = {
            'applied_pressure': brake_system.brake_cylinder_pressure,
            'force_per_cylinder': force_per_cylinder,
            'total_force': total_force,
            'theoretical_deceleration': deceleration,
            'braking_distance': braking_distance
        }
        
        return passed, effective_deceleration, slip, data

    def detect_wheel_slip(self, deceleration, adhesion_factor):
        """ Simple slip detection based on deceleration threshold. """
        slip_threshold = 0.5 * self.min_deceleration * adhesion_factor
        return deceleration < slip_threshold
    
    def calculate_braking_distance(self, initial_speed_mps, effective_deceleration_mps2, brake_delay):
        """
        Calculate stopping distance using v² = u² + 2as
            v = final speed (0)
            u = initial speed
            a = deceleration (-value)
            s = distance
        """
        if effective_deceleration_mps2 <= 0:
            return float('inf')  # prevent division by zero
        
        # get the distance during brake delay
        delay_distance = initial_speed_mps * brake_delay

        # stopping distance = s = (u²) / (2a)
        stopping_distance = (initial_speed_mps ** 2) / (2 * effective_deceleration_mps2)
        
        return delay_distance + stopping_distance