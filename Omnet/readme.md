# Omnet++ Experiment: Veins Simulation

## How to Run

### Prerequisites
- Linux OS
- Install Omnet++: Open a terminal and start Omnet++ with the command "omnetpp".
- Build Veins: Import and build Veins if not done previously.
- Navigate to the home/src directory.

### Simulation Execution
1. Open a terminal at home/src.
2. Run the following command to launch Veins:
   ```bash
   ./veins-5.2/veins-veins-5.2/bin/veins_launchd -vv -c sumo
   ```
3. Open the Omnet++ interface and run the Veins example.

## Experiment Customization

### Changes Needed
1. Modify the NED file to incorporate the experimental settings.
2. Ensure proper feeding of SUMO files for the experiment.

### Running the Experiment
- Execute the experiment with the specified time step and experimental duration.

## Reading Result Files in Omnet++

### Using Pandas
1. Open a terminal in the result folder.
2. Run the following command to convert SCA files to CSV:
   ```bash
   scavetool x *.sca -o xxx.csv
   ```

For detailed information on reading and analyzing result files in Omnet++, refer to the [Omnet++ Pandas Tutorial](https://docs.omnetpp.org/tutorials/pandas/).

Feel free to adjust these instructions based on your specific experimental setup. Happy simulating!