class Train:
    '''Train class represents a train with mass and speed attributes.'''

    def __init__(self, mass_kg, initial_speed_kmh):
        self.mass_kg = mass_kg  
        self.speed_kmh = initial_speed_kmh  # km/h 
        self.speed_mps = initial_speed_kmh / 3.6  # convert to m/s
        self.wheel_slip = False  
        self.brake_temp = 20.0

    
    def update_speed(self, effective_deceleration, dt):
        """Apply deceleration in m/s² over a given time step, update speed in km/h.

        Arguments:
            effective_deceleration (float): Effective deceleration in m/s².
            dt (float): Time step in seconds.
            
        Returns:
            speed_kmh (float): Speed of the train.
            """ 
        self.speed_mps = max(self.speed_mps - effective_deceleration * dt, 0)
        self.speed_kmh = self.speed_mps * 3.6  # convert to km/h

        return self.speed_kmh
    
        