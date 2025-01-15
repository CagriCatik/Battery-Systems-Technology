// src/algorithms/soc_algorithm.rs

use crate::algorithms::coulomb_counting;
use crate::models::{Battery, SocCalculator};

/// Performs the SoC estimation algorithm.
///
/// This function uses Coulomb Counting to estimate the State of Charge.
///
/// # Arguments
///
/// * `battery` - Mutable reference to the Battery instance.
/// * `calculator` - Mutable reference to the SocCalculator instance.
/// * `delta_time` - Time interval over which the measurements were taken in hours (h).
///
/// # Example
///
/// ```rust
/// soc_algorithm::estimate_soc(&mut battery, &mut soc_calculator, 1.0);
/// ```
pub fn estimate_soc(
    battery: &mut Battery,
    calculator: &mut SocCalculator,
    delta_time: f64,
) {
    // Update SoC using Coulomb Counting
    coulomb_counting(calculator, battery.current, delta_time);

    // Update the battery's SoC with the calculated value
    battery.soc = calculator.get_soc();
}
