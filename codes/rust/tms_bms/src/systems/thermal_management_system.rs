// systems/thermal_management_system.rs
use std::thread;
use std::time::Duration;

use crate::constants::{MAX_TEMPERATURE, MIN_TEMPERATURE};
use crate::models::{BatteryCell, ThermalState};

/// Struct representing the Thermal Management System.
pub struct ThermalManagementSystem {
    pub cells: Vec<BatteryCell>,
    pub state: ThermalState,
}

impl ThermalManagementSystem {
    /// Creates a new ThermalManagementSystem with a given number of cells.
    pub fn new(num_cells: usize, initial_temp: f64) -> Self {
        let mut cells = Vec::with_capacity(num_cells);
        for id in 1..=num_cells {
            cells.push(BatteryCell::new(id, initial_temp));
        }
        ThermalManagementSystem {
            cells,
            state: ThermalState::Idle,
        }
    }

    /// Monitors the temperatures of all cells and activates cooling/heating if necessary.
    pub fn monitor_temperatures(&mut self) {
        let mut need_cooling = false;
        let mut need_heating = false;

        for cell in &self.cells {
            if cell.temperature > MAX_TEMPERATURE {
                need_cooling = true;
            } else if cell.temperature < MIN_TEMPERATURE {
                need_heating = true;
            }
        }

        match (need_cooling, need_heating) {
            (true, _) => {
                if self.state != ThermalState::Cooling {
                    self.activate_cooling();
                }
            }
            (_, true) => {
                if self.state != ThermalState::Heating {
                    self.activate_heating();
                }
            }
            _ => {
                if self.state != ThermalState::Idle {
                    self.deactivate_systems();
                }
            }
        }
    }

    /// Activates the cooling system.
    fn activate_cooling(&mut self) {
        self.state = ThermalState::Cooling;
        println!("Cooling system activated.");
        // Here you would add code to activate actual cooling hardware.
    }

    /// Activates the heating system.
    fn activate_heating(&mut self) {
        self.state = ThermalState::Heating;
        println!("Heating system activated.");
        // Here you would add code to activate actual heating hardware.
    }

    /// Deactivates any active thermal management systems.
    fn deactivate_systems(&mut self) {
        self.state = ThermalState::Idle;
        println!("Thermal systems deactivated. All cells within optimal temperature range.");
        // Here you would add code to deactivate heating/cooling hardware.
    }

    /// Simulates the thermal management process over a period of time.
    pub fn run(&mut self, cycles: usize, interval_secs: u64) {
        for cycle in 1..=cycles {
            println!("\n--- Cycle {} ---", cycle);
            for cell in &mut self.cells {
                cell.update_temperature();
            }
            self.monitor_temperatures();
            thread::sleep(Duration::from_secs(interval_secs));
        }
    }
}
