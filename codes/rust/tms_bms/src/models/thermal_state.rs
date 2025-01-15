// models/thermal_state.rs

/// Enum representing the state of the thermal management system.
#[derive(Debug, PartialEq)]
pub enum ThermalState {
    Cooling,
    Heating,
    Idle,
}
