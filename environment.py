class Environment:
    """
    Environment class to manage and simulate environmental conditions affecting train adhesion.
    This class allows setting predefined weather conditions and calculates the adhesion factor
    based on rail moisture, temperature, and debris presence.
    """

    def __init__(self):
        self.conditions = {
            'rail_moisture': 0.0,  # 0.0 = dry, 1.0 = standing water
            'temperature': 20.0,    # °C
            'debris': 0.0,          # 0.0 = clean, 1.0 = heavy leaves/snow
        }
    
    def update_conditions(self, weather_type):
        """
        Set predefined environmental presets.

        Arguments:
            weather_type (str): 'dry', 'rain', 'snow', 'autumn', 'heatwave'
        """
        
        presets = {
            'dry':       {'rail_moisture': 0.0,  'temperature': 20, 'debris': 0.0},
            'rain':      {'rail_moisture': 0.4,  'temperature': 15, 'debris': 0.0},  
            'snow':      {'rail_moisture': 0.3,  'temperature': -2, 'debris': 0.6},  
            'autumn':    {'rail_moisture': 0.2,  'temperature': 10, 'debris': 0.4},  
            'heatwave':  {'rail_moisture': 0.0,  'temperature': 40, 'debris': 0.0}
        }

        # Validate input weather type
        if weather_type not in ['dry', 'rain', 'snow', 'autumn', 'heatwave']:
            raise ValueError("Invalid weather type. Choose from: 'dry', 'rain', 'snow', 'autumn', 'heatwave'.")

        # Update conditions based on the selected weather type
        self.conditions.update(presets[weather_type])
    
    def get_adhesion_factor(self):
        """ Calculate combined wheel-rail adhesion (0.0 - 1.0) """

        wet = self.conditions['rail_moisture']
        debris = self.conditions['debris']
        temp = self.conditions['temperature']

        # moisture effect 
        wet_reduction = 0.8 * wet ** 1.1
        
        # debris effect (leaves/snow)
        debris_reduction = min(0.7 * debris ** 1.5, 0.5)
        
        # temperature effect
        temp_deviation = abs(temp - 20)
        temp_factor = 1.0 - 0.001 * temp_deviation
        
        return max(0.15, (1.0 - wet_reduction - debris_reduction) * temp_factor)