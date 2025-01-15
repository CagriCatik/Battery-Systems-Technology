// models/mod.rs

/// This module contains data structures representing the battery and the SoC calculator.

pub mod battery;
pub mod soc_calculator;

pub use battery::Battery;
pub use soc_calculator::SocCalculator;
