// utils/temperature_compensation.rs

use crate::constants::TEMPERATURE_COEFFICIENT;

/// Adjusts the SoC based on temperature.
///
/// This function applies a simple linear compensation based on the deviation from a reference temperature.
///
/// # Arguments
///
/// * `soc` - Current State of Charge in percentage (%).
/// * `temperature` - Current battery temperature in Celsius (°C).
///
/// # Returns
///
/// * `f64` - Adjusted SoC after compensation.
///
/// # Example
///
/// ```
/// let adjusted_soc = temperature_compensation::compensate_temperature(95.0, 30.0);
/// ```
pub fn compensate_temperature(soc: f64, temperature: f64) -> f64 {
    // Reference temperature (e.g., 25°C)
    let reference_temp = 25.0;

    // Calculate temperature deviation
    let temp_deviation = temperature - reference_temp;

    // Apply linear compensation
    soc + TEMPERATURE_COEFFICIENT * temp_deviation
}
