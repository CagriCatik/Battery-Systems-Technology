// src/utils/voltage_curve.rs

/// Returns the voltage based on the SoC using a piecewise linear approximation.
///
/// # Arguments
///
/// * `soc` - State of Charge in percentage (%).
///
/// # Returns
///
/// * `f64` - Corresponding voltage in volts (V).
pub fn voltage_curve(soc: f64) -> f64 {
    match soc {
        0.0..=25.0 => 3.0 + (soc / 25.0) * 0.4,       // 3.0V to 3.4V
        25.0..=50.0 => 3.4 + ((soc - 25.0) / 25.0) * 0.3, // 3.4V to 3.7V
        50.0..=75.0 => 3.7 + ((soc - 50.0) / 25.0) * 0.3, // 3.7V to 4.0V
        75.0..=100.0 => 4.0 + ((soc - 75.0) / 25.0) * 0.2, // 4.0V to 4.2V
        _ => 3.0, // Default fallback
    }
}
