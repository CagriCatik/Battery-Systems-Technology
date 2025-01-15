// src/main.rs

mod constants;
mod models;
mod algorithms;
mod utils;

use models::{Battery, SocCalculator};
use algorithms::estimate_soc;
use utils::{log_data, compensate_temperature};
use algorithms::voltage_correction;
use std::time::{Duration, Instant};
use rand::Rng;
use utils::voltage_curve::voltage_curve;


fn main() {
    // Initialize battery parameters
    let mut battery = Battery::new(4.2, -5.0, 25.0); // Initial voltage, current, temperature
    let mut soc_calculator = SocCalculator::new(constants::INITIAL_SOC);

    // Initialize logging by creating a CSV file with headers
    initialize_logging().expect("Failed to initialize log file");

    // Simulation parameters
    let total_cycles = 10000; // Total number of simulation cycles
    let delta_time = 1.0 / 60.0; // Time interval in hours (1 minute)

    for cycle in 1..=total_cycles {
        let start_time = Instant::now();

        // Simulate battery measurements
        battery.current = simulate_current(&battery);
        battery.temperature = simulate_temperature(&battery);

        // Estimate SoC using Coulomb Counting
        estimate_soc(&mut battery, &mut soc_calculator, delta_time);

        // Simulate voltage based on updated SoC
        battery.voltage = simulate_voltage(&battery);

        // Apply temperature compensation
        let compensated_soc = compensate_temperature(battery.soc, battery.temperature);
        battery.soc = compensated_soc
            .min(constants::MAX_SOC)
            .max(constants::MIN_SOC);

        // Perform voltage-based correction after updating voltage
        voltage_correction(&battery, &mut soc_calculator);

        // Update battery's SoC with the corrected value
        battery.soc = soc_calculator.get_soc();

        // Log data
        if let Err(e) = log_data(&battery) {
            eprintln!("Failed to log data: {}", e);
        }

        // Print current state
        println!(
            "Cycle {}: Voltage: {:.2}V, Current: {:.2}A, Temperature: {:.2}°C, SoC: {:.2}%",
            cycle, battery.voltage, battery.current, battery.temperature, battery.soc
        );

        // Wait for the next cycle (simulate real-time intervals)
        let elapsed = start_time.elapsed();
        let sleep_duration = Duration::from_secs_f64(1.0)
            .checked_sub(elapsed)
            .unwrap_or_else(|| Duration::from_secs(0));
        std::thread::sleep(sleep_duration);
    }
}

/// Initializes the logging by creating the CSV file with headers.
///
/// # Returns
///
/// * `std::io::Result<()>` - Result indicating success or failure.
fn initialize_logging() -> std::io::Result<()> {
    std::fs::write(
        "./log/battery_log.csv",
        "Timestamp,Voltage,Current,Temperature,SoC\n",
    )
}

/// Simulates voltage measurement using a detailed OCV vs SoC curve.
///
/// In a real application, replace this function with actual sensor data acquisition.
///
/// # Arguments
///
/// * `battery` - Reference to the Battery instance.
///
/// # Returns
///
/// * `f64` - Simulated voltage value in volts (V).
fn simulate_voltage(battery: &Battery) -> f64 {
    voltage_curve(battery.soc)
}

/// Simulates current measurement.
///
/// In a real application, replace this function with actual sensor data acquisition.
///
/// # Arguments
///
/// * `_battery` - Reference to the Battery instance (unused).
///
/// # Returns
///
/// * `f64` - Simulated current value in amperes (A).
fn simulate_current(_battery: &Battery) -> f64 {
    // Constant discharge current of -5A
    -5.0
}

/// Simulates temperature measurement.
///
/// In a real application, replace this function with actual sensor data acquisition.
///
/// # Arguments
///
/// * `battery` - Reference to the Battery instance.
///
/// # Returns
///
/// * `f64` - Simulated temperature value in Celsius (°C).
fn simulate_temperature(battery: &Battery) -> f64 {
    let mut rng = rand::thread_rng();
    
    // Simulate temperature fluctuation between -0.5°C to +0.5°C
    battery.temperature + rng.gen_range(-0.5..0.5)
}
