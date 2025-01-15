// models/soc_calculator.rs

use crate::constants::{MAX_SOC, MIN_SOC, NOMINAL_CAPACITY};

/// Struct responsible for calculating the State of Charge (SoC) of the battery.
pub struct SocCalculator {
    /// Nominal capacity of the battery in Ampere-hours (Ah).
    nominal_capacity: f64,

    /// Current State of Charge (SoC) in percentage (%).
    current_soc: f64,
}

impl SocCalculator {
    /// Creates a new SocCalculator instance.
    ///
    /// # Arguments
    ///
    /// * `initial_soc` - Initial SoC in percentage.
    ///
    /// # Example
    ///
    /// ```
    /// let soc_calculator = SocCalculator::new(100.0);
    /// ```
    pub fn new(initial_soc: f64) -> Self {
        SocCalculator {
            nominal_capacity: NOMINAL_CAPACITY,
            current_soc: initial_soc.min(MAX_SOC).max(MIN_SOC),
        }
    }

    /// Updates the SoC based on the current measurement using Coulomb Counting.
    ///
    /// # Arguments
    ///
    /// * `current` - Current flowing into/out of the battery in amperes (A).
    /// * `delta_time` - Time interval over which the current was measured in hours (h).
    ///
    /// # Formula
    ///
    /// ΔSoC = (I * Δt) / C * 100%
    ///
    /// Where:
    /// - I = Current (A)
    /// - Δt = Time interval (h)
    /// - C = Nominal Capacity (Ah)
    ///
    /// # Example
    ///
    /// ```
    /// soc_calculator.update_soc(-5.0, 1.0);
    /// ```
    pub fn update_soc(&mut self, current: f64, delta_time: f64) {
        // Coulomb Counting: ΔSoC = (I * Δt) / C * 100%
        let delta_soc = (current * delta_time) / self.nominal_capacity * 100.0;
        self.current_soc += delta_soc;

        // Ensure SoC stays within [MIN_SOC, MAX_SOC]
        self.current_soc = self.current_soc.min(MAX_SOC).max(MIN_SOC);
    }

    /// Sets the SoC to a specific value (used for voltage correction).
    ///
    /// # Arguments
    ///
    /// * `soc` - New SoC value in percentage (%).
    ///
    /// # Example
    ///
    /// ```
    /// soc_calculator.set_soc(95.0);
    /// ```
    pub fn set_soc(&mut self, soc: f64) {
        self.current_soc = soc.min(MAX_SOC).max(MIN_SOC);
    }

    /// Retrieves the current SoC.
    ///
    /// # Returns
    ///
    /// * `f64` - Current SoC in percentage (%).
    ///
    /// # Example
    ///
    /// ```
    /// let current_soc = soc_calculator.get_soc();
    /// ```
    pub fn get_soc(&self) -> f64 {
        self.current_soc
    }
}
