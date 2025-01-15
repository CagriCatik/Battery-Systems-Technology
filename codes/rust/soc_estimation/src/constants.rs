// constants.rs
/// This module defines all the constant values used in the SoC Estimation System.

/// Nominal capacity of the battery in Ampere-hours (Ah).
pub const NOMINAL_CAPACITY: f64 = 100.0; // Example: 100 Ah battery

/// Initial State of Charge (SoC) in percentage.
pub const INITIAL_SOC: f64 = 100.0; // 100% charged

/// Maximum allowable SoC in percentage.
pub const MAX_SOC: f64 = 100.0; // 100% max

/// Minimum allowable SoC in percentage.
pub const MIN_SOC: f64 = 0.0; // 0% min

/// Temperature coefficient for temperature compensation.
/// Adjusts SoC based on temperature deviations.
pub const TEMPERATURE_COEFFICIENT: f64 = 0.05; // Example coefficient

// Additional constants can be added here as needed.
