// utils/data_logger.rs

use std::fs::OpenOptions;
use std::io::Write;

use crate::models::Battery;
use chrono::Local;

/// Logs battery data to a CSV file.
///
/// Each entry includes a timestamp, voltage, current, temperature, and SoC.
///
/// # Arguments
///
/// * `battery` - Reference to the Battery instance.
///
/// # Returns
///
/// * `std::io::Result<()>` - Result indicating success or failure.
///
/// # Example
///
/// ```
/// data_logger::log_data(&battery).expect("Failed to log data");
/// ```
pub fn log_data(battery: &Battery) -> std::io::Result<()> {
    // Get the current timestamp in RFC3339 format
    let timestamp = Local::now().to_rfc3339();

    // Create a CSV-formatted log entry
    let log_entry = format!(
        "{},{:.2},{:.2},{:.2},{:.2}\n",
        timestamp, battery.voltage, battery.current, battery.temperature, battery.soc
    );

    // Open the CSV file in append mode, create it if it doesn't exist
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open("battery_log.csv")?;

    // Write the log entry to the file
    file.write_all(log_entry.as_bytes())?;

    Ok(())
}
