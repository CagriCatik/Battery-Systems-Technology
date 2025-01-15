// algorithms/coulomb_counting.rs

use crate::models::soc_calculator::SocCalculator;

/// Updates SoC using the Coulomb Counting method.
///
/// # Arguments
///
/// * `calculator` - Mutable reference to the SocCalculator instance.
/// * `current` - Current flowing into/out of the battery in amperes (A).
/// * `delta_time` - Time interval over which the current was measured in hours (h).
///
/// # Example
///
/// ```
/// coulomb_counting(&mut soc_calculator, -5.0, 1.0);
/// ```
pub fn coulomb_counting(calculator: &mut SocCalculator, current: f64, delta_time: f64) {
    calculator.update_soc(current, delta_time);
}
