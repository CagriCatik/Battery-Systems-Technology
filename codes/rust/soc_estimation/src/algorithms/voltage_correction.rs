// src/algorithms/voltage_correction.rs

use crate::models::battery::Battery;
use crate::models::soc_calculator::SocCalculator;

/// Corrects SoC estimation based on Open Circuit Voltage (OCV).
///
/// **Note:** This is a simplistic implementation. In real-world applications,
/// a detailed OCV vs SoC curve should be used.
///
/// # Arguments
///
/// * `battery` - Reference to the Battery instance.
/// * `calculator` - Mutable reference to the SocCalculator instance.
///
/// # Example
///
/// ```rust
/// voltage_correction(&battery, &mut soc_calculator);
/// ```
pub fn voltage_correction(battery: &Battery, calculator: &mut SocCalculator) {
    // Placeholder formula: linear relationship between voltage and SoC
    // In practice, use the actual OCV vs SoC curve for the specific battery.
    let soc_from_voltage = (battery.voltage - 3.0) / 1.2 * 100.0; // Example formula

    // Clamp the calculated SoC within [MIN_SOC, MAX_SOC]
    let soc_clamped = soc_from_voltage.min(crate::constants::MAX_SOC).max(crate::constants::MIN_SOC);

    // Update the SocCalculator with the corrected SoC
    calculator.set_soc(soc_clamped);
}
