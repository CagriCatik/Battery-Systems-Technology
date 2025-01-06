# Battery Thermal Management System
---

## Overview

This code models a Battery Thermal Management System (BTMS), simulating how a battery pack’s temperature evolves over time under different types of thermal management strategies. It includes:

1. A **BatteryPack** class to represent the battery’s physical properties.  
2. A **BTMS** class that handles cooling or heating mechanisms depending on the selected system type.  
3. A **simulate_btms** function to run the simulation for a specified period.  
4. A **plot_results** function to visualize the simulation output.  
5. A **main** function to demonstrate running simulations for multiple BTMS types.

The code uses NumPy for numerical operations and Matplotlib for plotting.

---

## Code Structure

The code is organized into the following main sections:

1. **Imports**  
2. **BatteryPack Class**  
3. **BTMS Class**  
4. **Simulation Function** (`simulate_btms`)  
5. **Plotting Function** (`plot_results`)  
6. **Main Function** (`main`)

---

## 1. Imports

```python
import matplotlib.pyplot as plt
import numpy as np
```

- **matplotlib.pyplot**: for creating plots and visualizations.  
- **numpy**: for array manipulation, numerical computations, and simulation time array generation.