# Terminals

## 1. Access

| **Use-Case** | **Mechanical Key (Insert-Turn)**   | **Keyless-Start / Keyless-Go**        |
|--------------|--------------------------------------|---------------------------------------|
| **Unlock**   | Key button: Lock UNLOCK              | Key button: Lock UNLOCK               |
| **Lock**     | Key button: Lock LOCK                | Key button: Lock LOCK                 |

---

## 2. Terminal Status

| **Use-Case**                           | **Mechanical Key (Insert-Turn)**               | **Keyless-Start / Keyless-Go**                         |
|----------------------------------------|------------------------------------------------|--------------------------------------------------------|
| **Terminal 15c** "Key Inserted"        | Key inserted into the EZS                      | After door lock, toggle the start button multiple times |
| **Terminal 15R**                       | Key in the 1st notch                           | Toggle the start button                                 |
| **Terminal 15**                        | Key in the 2nd notch                           | Toggle the start button                                 |
| **Terminal 50 (Engine Start)**         | Turn the key further past the 2nd notch        | Press the brake and toggle the start button             |

---

## 3. Definition of Ignition States

| **State**     | **Description**       | **Terminal** |
|---------------|-----------------------|--------------|
| **IGN_LOCK**  | Ignition Lock         | 0            |
| **IGN_OFF**   | Ignition Off          | 15c          |
| **IGN_ACC**   | Ignition Accessory    | 15R          |
| **IGN_ON**    | Ignition On           | 15           |
| **IGN_START** | Ignition Start        | 50           |

---