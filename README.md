# Complex Systems 270 Final Project
By: Matthew Drutis (did the coding portion), Logan Hayner, Stevie Port

## Multi-lane Highway Simulation 🛣️:

There are 3 different agents that can spawn, each with their own individual driving characteristics.
- **Reckless** 🏎️
- **Cautious** 👵
- **Normal** 🚙

> We hope you test this simulation for yourself with different parameters, and adjust your real-life driving patterns accordingly.
## To run the simulation yourself:
### Clone the repository:
With SSH:
`git clone git@github.com:madrutis/cmplxsys_finalproj.git`<br>
With HTTPS:
`git clone https://github.com/madrutis/cmplxsys_finalproj.git`

### Getting Started
Run the script `setup.sh` in your preferred unix/linux terminal which will:
- make a new virtual environment
- download the requirements
<br>
* If the requirements download doesn't work, you can just pip install <package> for the package imported at the top of simulation.py

### Running the simulation:
Take a look around simulation.py, and adjust the initial parameters to the `Simulation` class.<br>
Initalize a dataset with `python3 init_df.py <test.csv>` even if you don't plan to store the data from the run.
In VS Code or your preferred IDE, right click on the code in simulation.py, and click `Run in Interactive Window` ➡️ `Run Current File in Interactive Window`<br>
And Voila 🪄

### Running a parameter sweep:
- Initialize a new dataset with `python3 init_df.py <dataset_name.csv>`
- Run a parameter sweep with `python3 param_sweep.py <dataset_name.csv>`
- Feel free to adjust the initalization of the simulation in `para_sweep.py` to your liking
- The csv files are saved in data/

### Visualize the data:
- The preliminary visualizations are in visualize_data.ipynb
