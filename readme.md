# Co-Simulation Study: Impact of Connected and Autonomous Vehicles on Traffic Flow Stability during Hurricane Evacuation

## Overview
Hurricane evacuation poses significant challenges for coastal residents, and this project aims to enhance traffic management during such events. The study utilizes a co-simulation approach, combining SUMO (a microscopic traffic simulation model) with vehicular ad-hoc network (VANET) simulations to assess the impact of Connected and Autonomous Vehicles (CAVs) and Autonomous Vehicles (AVs) on evacuation traffic.

## Simulation Setup
- **Simulation Model:** SUMO
- **Focus:** Evaluate CAVs and AVs using car-following models and VANET simulations.
- **Scenarios:** Mixed traffic scenarios with varying percentages (25%, 50%, 75%, 100%) of CAVs, AVs, and human-driven vehicles (HDVs) on I-75 in Florida.

  SOME MAIN FILES ARE HIDDEN DUE TO CONFIDENTIALITY

## Key Findings
1. **Car-Following Models:**
   - CACC model (CAVs) exhibits instability, while ACC model (AVs) produces more stable results.
   - With 25% AV market penetration, potential collisions can be reduced by 65.9%.

2. **Connectivity Impact:**
   - Introducing 10% CAVs with vehicle-to-vehicle communication reduces potential conflicts by 75%.
   - Connectivity enhances road safety by facilitating informed maneuvers in congested evacuation traffic.

## Python Simulation
- **Executable File:** main.py
- 
- **Output Files:**  *.xml files and csv files

## Traffic Parameter Analysis
- **CACC Model Gain Parameters:** Table 5
- **Simulation Runs:** 10 runs for each set of parameters
- **Results Compilation:** Tables 7 and 8
  - Scenario column indicates the percentage of vehicle types in each scenario (e.g., CACC-25).
  - Standard deviation (std) recorded to assess result stability across runs.

## Observations
- **CACC Model Reliability:** Caution advised due to high fluctuations; results from CACC scenarios should be interpreted carefully.
- **Effect of CAV Percentage:** General decrease in potential conflicts with an increase in CAV percentage.
- **Optimal Results:** Literature parameter set yields the least conflicts and stable traffic flow.

## Speed Deviation Analysis
- **Parameter Adjusted:** Speed deviation (0.1 to 0.05) for CAVs.
- **Impact:** About 15% decrease in total TTC count at CACC-25 scenario; limited impact in other scenarios.
- **Results:** See Table 9 for detailed findings.

### Conclusion
The study emphasizes the potential of AVs and CAVs in improving evacuation traffic stability. Connectivity proves crucial in reducing conflicts, while careful consideration of simulation parameters is necessary for reliable results.

