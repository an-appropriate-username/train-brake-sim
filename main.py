from train import Train
from brake_system import BrakeSystem
from bcu import BCU
from environment import Environment
from graph_manager import GraphManager

def simulate_dynamic_brake_test():

    """
    Set up the brake test simulation variables, including train parameters,
    brake system characteristics, and environmental conditions.

    The Brake Control Unit (BCU) will run a series of brake tests at different pressure demands, 
    checking for compliance with TSI standards and visualizes the results.
    """

    # ----------------------------- #
    # --- SIMULATION PARAMETERS --- #
    # ----------------------------- #

    # initalize simulation constants
    SPEED = 36   # km/h
    MASS = 40000  # kg 

    PISTON_AREA = 0.05  # m²
    NUM_CYLINDERS = 4  # number of brake cylinders
    FRICTION_COEFF = 0.6  # friction coefficient for type of pads
    BRAKE_PAD_WEAR = 1.0  # efficiency %
    LEAK_CHANCE = 0.1  # chance % of brake leak
    BRAKE_DELAY = 1.2  # seconds delay for brake response (pneumatic avg = 1.2s)
    
    ENV_CONDITION = 'snow'  # dry, rain, snow, autumn, heatwave
    
    # initialize components
    train = Train(MASS, SPEED)
    brake_system = BrakeSystem(PISTON_AREA, NUM_CYLINDERS, FRICTION_COEFF, BRAKE_PAD_WEAR, LEAK_CHANCE, BRAKE_DELAY)  
    bcu = BCU()

    # initialize environment conditions
    env = Environment()
    env.update_conditions(ENV_CONDITION)
    adhesion_factor = env.get_adhesion_factor()

    # initailze graph manager
    graph_manager = GraphManager()
    graph_manager.initialize_graphs({
        'mass': MASS/1000,
        'speed': SPEED,
        'env': ENV_CONDITION,
        'adhesion': adhesion_factor,
        'cylinders': NUM_CYLINDERS,
        'piston_area': PISTON_AREA,
        'friction': FRICTION_COEFF,
        'wear': BRAKE_PAD_WEAR*100
    })
    decels, distances, passes, phases = [], [], [], []

    # test phases (brake demand: 0-5 bar)
    test_phases = [
        {"demand": 1.5, "name": "30% (1.5 bar)"},
        {"demand": 2.5, "name": "50% (2.5 bar)"},
        {"demand": 3.5, "name": "70% (3.5 bar)"},
        {"demand": 5.0, "name": "100% (5.0 bar)"}
    ]
    results = []

    # --------------------- #
    # --- DISPLAY & RUN --- #
    # --------------------- #

    # print initial conditions
    print("\n=== BRAKE TEST SIMULATION ===")
    print(f"Train Mass: {train.mass_kg/1000} tonnes | Initial Speed: {train.speed_kmh} km/h")
    print(f"Brake System: {brake_system.num_cylinders} cylinders | Piston Area: {brake_system.piston_area} m²")
    print(f"Friction Coefficient: {brake_system.friction_coeff} | Pad Wear: {brake_system.brake_pad_wear*100}% efficiency")
    print(f"Current Adhesion: {adhesion_factor:.2f} | Environment: {ENV_CONDITION.capitalize()}")

    for phase in test_phases:
        test_name = phase["name"]
        test_demand = phase["demand"]

        print(f"\n--- Testing {test_name} ---")
        
        passed, effective_deceleration, slip, data = bcu.perform_brake_test(train, brake_system, test_demand, adhesion_factor)

        # store results
        phases.append(phase["name"])
        distances.append(data['braking_distance'])
        decels.append(effective_deceleration)
        passes.append(passed)
        results.append((test_name, effective_deceleration, passed))
        
        # print detailed report for each phase
        print(f"\nTEST {test_name}:")
        print(f"Effective Pressure: {data['applied_pressure']:.2f} bar")
        print(f"Force per Cylinder: {data['force_per_cylinder']:.0f} N | Total Force: {data['total_force']:.0f} N")
        print(f"Theoretical Deceleration: {data['theoretical_deceleration']:.2f} m/s²")
        print(f"Effective Deceleration: {effective_deceleration:.2f} m/s²")
        print(f"Braking Distance: {data['braking_distance']:.1f} meters")
        print(f"Slip: {'YES' if slip else 'NO'} | TSI: {'PASS' if passed else 'FAIL'}")

        # reset for next test
        brake_system.release_brake()
        train.speed_kmh = SPEED

    # -------------------- #
    # --- PLOT RESULTS --- #
    # -------------------- #

    graph_manager.plot_deceleration(phases, decels, passes, ENV_CONDITION)
    graph_manager.plot_stopping_distances(phases, distances)
    graph_manager.finalize()

if __name__ == "__main__":
    simulate_dynamic_brake_test()