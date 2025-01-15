
# Thermal Management System for Battery Management

The **Thermal Management System for Battery Management** is a Rust-based simulation that monitors the temperature of battery cells and activates cooling or heating systems to maintain optimal operating conditions. This project serves as a foundational framework for understanding and developing more complex Battery Management Systems with thermal regulation capabilities.

- **Temperature Monitoring:** Continuously monitors the temperature of multiple battery cells.
- **Automated Thermal Control:** Activates cooling or heating systems based on predefined temperature thresholds.
- **Modular Design:** Organized into distinct modules for constants, models, and system functionalities, enhancing readability and maintainability.
- **Simulation:** Utilizes randomized temperature changes to simulate real-world scenarios.
- **Scalable:** Easily extendable to accommodate more battery cells or integrate additional features.

## Folder Structure

The project is structured to promote modularity and ease of maintenance. Below is the complete folder structure:

```
thermal_management/
├── Cargo.toml
└── src
    ├── constants.rs
    ├── main.rs
    ├── models
    │   ├── battery_cell.rs
    │   ├── mod.rs
    │   └── thermal_state.rs
    └── systems
        ├── mod.rs
        └── thermal_management_system.rs
```

### Module Breakdown

- **`constants.rs`**
  - Defines constant values such as minimum and maximum temperature thresholds.
  
- **`models/`**
  - **`battery_cell.rs`**
    - Defines the `BatteryCell` struct representing individual battery cells.
  - **`thermal_state.rs`**
    - Defines the `ThermalState` enum representing the system's state (`Cooling`, `Heating`, `Idle`).
  - **`mod.rs`**
    - Re-exports the models for easy access in other modules.
  
- **`systems/`**
  - **`thermal_management_system.rs`**
    - Defines the `ThermalManagementSystem` struct responsible for managing battery cells and controlling thermal states.
  - **`mod.rs`**
    - Re-exports the system functionalities for easy access.
  
- **`main.rs`**
  - Entry point of the application, initializing and running the thermal management simulation.

## Installation

To run this project locally, follow the steps below.

### Prerequisites

- **Rust:** Ensure you have Rust installed. If not, install it using `rustup`.

  ```sh
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```

  Verify the installation:

  ```sh
  rustc --version
  cargo --version
  ```

### Clone the Repository

```sh
git clone https://github.com/yourusername/thermal_management.git
cd thermal_management
```

### Build the Project

Navigate to the project directory and build the project using Cargo:

```sh
cargo build
```

### Run the Project

Execute the simulation:

```sh
cargo run
```

**Note:** Temperatures will vary with each run due to the randomized simulation.

## Usage

Upon running the project, the simulation will initialize a thermal management system with a specified number of battery cells, each starting at an initial temperature. The system will then run through a defined number of cycles, updating each cell's temperature and activating the cooling or heating systems as necessary.
