# Klemmen

---

## **Zugang**
| **Use-Case**       | **Serienschlüssel (Stecken-Drehen)** | **Keyless-Start / Keyless-Go**           |
|--------------------|-------------------------------------|------------------------------------------|
| **Entriegeln**     | Taste Schlüssel: Schloss-AUF       | Taste Schlüssel: Schloss-AUF            |
| **Verriegeln**     | Taste Schlüssel: Schloss-ZU        | Taste Schlüssel: Schloss-ZU             |

---

## **Klemmen-Status**
| **Use-Case**                    | **Serienschlüssel (Stecken-Drehen)**          | **Keyless-Start / Keyless-Go**                 |
|---------------------------------|----------------------------------------------|-----------------------------------------------|
| **Klemme 15c** "Schlüssel steckt" | Schlüssel ins EZS                            | Nach Tür-ZU, mehrfach Start-Taster togglen    |
| **Klemme 15R**                  | Schlüssel in 1. Raste                        | Start-Taster togglen                          |
| **Klemme 15**                   | Schlüssel in 2. Raste                        | Start-Taster togglen                          |
| **Klemme 50** Motorstart        | Schlüssel über 2. Raste weiterdrehen         | Bremse treten und Start-Taster togglen        |

---

## **Definition der Ignitions-States**
| **Zustand**      | **Beschreibung**            | **Klemme** |
|------------------|----------------------------|------------|
| **IGN_LOCK**     | Ignition Lock              | 0          |
| **IGN_OFF**      | Ignition Off               | 15c        |
| **IGN_ACC**      | Ignition Accessory         | 15R        |
| **IGN_ON**       | Ignition On                | 15         |
| **IGN_START**    | Ignition Start             | 50         |

--- 
