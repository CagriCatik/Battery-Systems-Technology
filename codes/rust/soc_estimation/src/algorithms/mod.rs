// src/algorithms/mod.rs

/// This module contains algorithms used for SoC estimation.

pub mod coulomb_counting;
pub mod voltage_correction;
pub mod soc_algorithm;

pub use coulomb_counting::*;
pub use voltage_correction::*;
pub use soc_algorithm::*;
