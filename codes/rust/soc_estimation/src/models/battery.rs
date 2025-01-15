// models/battery.rs

use serde::{Deserialize, Serialize};

/// Struct representing the battery's state.
#[derive(Debug, Serialize, Deserialize)]
pub struct Battery {
    /// Current voltage of the battery in volts (V).
    pub voltage: f64,

    /// Current flowing into or out of the battery in amperes (A).
    /// Negative for discharge, positive for charge.
    pub current: f64,

    /// Current temperature of the battery in Celsius (°C).
    pub temperature: f64,

    /// Current State of Charge (SoC) in percentage (%).
    pub soc: f64,
}

impl Battery {
    /// Creates a new Battery instance with initial values.
    ///
    /// # Arguments
    ///
    /// * `voltage` - Initial voltage in volts.
    /// * `current` - Initial current in amperes.
    /// * `temperature` - Initial temperature in Celsius.
    ///
    /// # Example
    ///
    /// ```
    /// let battery = Battery::new(4.2, -5.0, 25.0);
    /// ```
    pub fn new(voltage: f64, current: f64, temperature: f64) -> Self {
        Battery {
            voltage,
            current,
            temperature,
            soc: crate::constants::INITIAL_SOC,
        }
    }
}
