// main.rs
mod constants;
mod models;
mod systems;

use systems::ThermalManagementSystem;

fn main() {
    // Initialize the Thermal Management System with 5 cells, each starting at 30°C.
    let mut tms = ThermalManagementSystem::new(5, 30.0);

    // Run the simulation for 10 cycles with a 1-second interval between cycles.
    tms.run(10, 1);
}
