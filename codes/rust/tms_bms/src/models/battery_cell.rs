// models/battery_cell.rs
use rand::Rng;

/// Struct representing a single battery cell.
#[derive(Debug)]
pub struct BatteryCell {
    pub id: usize,
    pub temperature: f64,
}

impl BatteryCell {
    /// Creates a new BatteryCell with a given ID and initial temperature.
    pub fn new(id: usize, initial_temp: f64) -> Self {
        BatteryCell {
            id,
            temperature: initial_temp,
        }
    }

    /// Simulates temperature changes for the cell.
    pub fn update_temperature(&mut self) {
        // For simulation purposes, randomly adjust the temperature.
        let mut rng = rand::thread_rng();
        let temp_change: f64 = rng.gen_range(-5.0..5.0);
        self.temperature += temp_change;
        println!(
            "Cell {} temperature updated to {:.2}°C",
            self.id, self.temperature
        );
    }
}
