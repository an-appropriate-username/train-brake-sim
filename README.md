# Train Braking Performance Simulator

A physics-based simulator for evaluating train braking performance under various environmental and operational conditions.

## Table of Contents
- [Physics Model](#physics-model)
- [Component Architecture](#component-architecture)
- [Parameter Configuration](#parameter-configuration)
- [Output Metrics](#output-metrics)
- [Installation](#installation-and-usage)

## Physics Model

### Core Calculations
1. **Brake Force Calculation**
  > Force = (Pressure × 100,000) × Piston Area × μ_effective 
  > μ_effective = Friction Coefficient × (Brake Pad Wear)^2

  - Converts hydraulic pressure to mechanical force

2. **Deceleration Dynamics**
  > a = (Total Force × Adhesion Factor) / Mass

  - Adhesion factors: Dry rail, rain, autumn and snow.
  - Accounts for pad wear, weather and debris

3. **Stopping Distance**
  > Total Distance = (Initial Speed × Brake Delay) + (Speed² / (2 × a))

  - Includes dynamic system response delay
  - Accounts for brake delay

## Component Architecture

| Component         | Key Functions | Parameters |
|-------------------|--------------|------------|
| **Train**         | Tracks mass, speed, and motion state | `mass_kg`, `initial_speed_kmh` |
| **BrakeSystem**   | Models hydraulic brakes and wear | `piston_area`, `num_cylinders`, `friction_coeff`, `brake_pad_wear` |
| **Environment**   | Simulates weather effects | `rail_moisture`, `temperature`, `debris` |
| **BCU**           | Preforms brake test, calculates stopping distance and deceleration | `min_deceleration = 0.8 m/s²` |

## Parameter Configuration

### Operational Parameters
  - SPEED
  - MASS

### Brake System Configuration
  - PISTON AREA
  - NUMBER OF CYLINDERS
  - BRAKE PAD FRICTION COFFECIENT
  - BRAKE PAD WEAR
  - LEAK CHANCE

### Environmental Settings
  - ENV_CONDITION

## Output Metrics

### Terminal Output
  - Effective Pressure
  - Total Force
  - Effective Deceleration
  - Braking Distance
  - Slip Test
  - TSI Test

### Graphical Output 

1. Bar Chart
  - Deceleration against brake pressure demand
  - Blue to indicate TSI standard
  - Orange line to indicate desired deceleration in undesirable conditions

2. Line Graph
  - Stopping distance against brake pressure demand
  - 50m safety thresold marker

## Installation and Usage

- Clone train-brake-sim
- Install 'requirements.txt'
- Set parameters in 'main.py'
- Run 'python main.py'
