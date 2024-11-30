# Gute Anforderungen an Anforderungen

Im Automotivebereich sind präzise und gut strukturierte Anforderungen essenziell, insbesondere wenn sie den strengen Sicherheitsstandards wie ISO 26262 entsprechen sollen. Im Folgenden werden die **guten Anforderungen an Anforderungen im Automotivebereich** sowie die **wichtigen Aspekte bei der Spezifikation von ISO 26262 Anforderungen und der Erstellung von Testfall-Automatisierungsskripten** erläutert.

---

## **Gute Anforderungen im Automotivebereich**

### **Klar und Präzise**
- **Eindeutige Sprache:** Vermeiden Sie Mehrdeutigkeiten. Jede Anforderung sollte so formuliert sein, dass sie nur eine Interpretation zulässt.
- **Keine Fachjargon ohne Definition:** Falls technische Begriffe verwendet werden, sollten diese klar definiert sein.

### **Vollständig und Konsistent**
- **Vollständigkeit:** Alle notwendigen Aspekte des Systems sollten durch Anforderungen abgedeckt sein.
- **Konsistenz:** Anforderungen sollten sich nicht widersprechen und in Einklang miteinander stehen.

### **Nachvollziehbarkeit (Traceability)**
- **Rückverfolgbarkeit:** Jede Anforderung sollte auf ihre Herkunft zurückführbar sein (z.B. Kundenanforderungen, gesetzliche Vorgaben) und in den späteren Entwicklungsphasen nachvollzogen werden können.

### **Testbarkeit**
- **Messbar und Überprüfbar:** Anforderungen müssen so formuliert sein, dass sie durch Tests überprüft werden können. Klare Akzeptanzkriterien sind hierbei wichtig.

### **Realistisch und Erreichbar**
- **Machbarkeit:** Die Anforderungen sollten unter den gegebenen technischen, zeitlichen und finanziellen Rahmenbedingungen realisierbar sein.

### **Modularität**
- **Strukturierung:** Anforderungen sollten in überschaubare, modularisierte Einheiten gegliedert sein, um die Handhabung und Wartung zu erleichtern.


### Anforderungen für ein Battery Management System (BMS)

Basierend auf den Prinzipien für gute Anforderungen im Automotivebereich und unter Berücksichtigung der Sicherheitsstandards wie ISO 26262, sind folgende Anforderungen für ein Battery Management System formuliert:

---

#### **1. Klar und Präzise**
- Das BMS **muss** den Lade- und Entladevorgang der Batterie innerhalb der spezifizierten Grenzwerte (z. B. Spannung und Strom) steuern.
- Die **Temperaturüberwachung** der Batterie **muss** mit einer Genauigkeit von ±2 °C erfolgen.
- Das System **muss** eine Warnung ausgeben, wenn der Ladezustand (State of Charge, SoC) unter 20 % fällt.

---

#### **2. Vollständig und Konsistent**
- Das BMS **muss** alle Zellspannungen, Zellströme und Zelltemperaturen in einem Intervall von maximal 100 ms messen.
- Es **muss** möglich sein, die Batterie sicher in den Ruhezustand zu versetzen, falls ein kritischer Fehler erkannt wird.
- Alle Kommunikationsanforderungen **müssen** mit den Protokollen CAN und LIN kompatibel sein und dürfen sich nicht gegenseitig widersprechen.

---

#### **3. Nachvollziehbarkeit (Traceability)**
- Jede Anforderung **muss** eindeutig auf die zugehörige Sicherheitsanalyse nach ISO 26262 zurückführbar sein.
- Anforderungen an die Ladeprotokolle **müssen** auf internationalen Standards wie IEC 62133 basieren.

---

#### **4. Testbarkeit**
- Die maximale Spannungsabweichung zwischen gemessener und tatsächlicher Zellspannung **muss** in Tests ≤ 0,01 V betragen.
- Das BMS **muss** bei einem simulierten Kurzschluss innerhalb von ≤ 10 ms in den Sicherheitsmodus wechseln.
- Jede Sicherheitsanforderung **muss** durch Testfall-Skripte validiert werden, die auf einer HiL-Umgebung (Hardware-in-the-Loop) basieren.

---

#### **5. Realistisch und Erreichbar**
- Das BMS **sollte** für den Einsatz in kommerziellen Fahrzeugen optimiert sein, mit einer Produktionskostenobergrenze von 200 EUR pro Einheit.
- Die Implementierung des Sicherheitsmechanismus **muss** mit handelsüblichen Mikrocontrollern (z. B. ARM Cortex-M-Serie) möglich sein.

---

#### **6. Modularität**
- Das BMS **muss** aus folgenden klar definierten Modulen bestehen:
  - **Spannungs- und Stromüberwachung**: Überwacht die elektrischen Parameter aller Zellen.
  - **Fehlerdiagnosemodul**: Erfasst und protokolliert Fehler wie Überspannung oder Übertemperatur.
  - **Kommunikationsmodul**: Stellt die Verbindung zu Fahrzeugsteuergeräten über CAN/LIN sicher.

---

#### **7. Zusätzliche Anforderungen an die ISO 26262-Konformität**
- Das BMS **muss** eine ASIL-B-Konformität (Automotive Safety Integrity Level) erfüllen, einschließlich redundanter Schutzmechanismen gegen Zellüberladung.
- Das System **muss** Fail-Safe-Mechanismen implementieren, um den Betrieb bei Hardwarefehlern sicherzustellen.
- Softwareänderungen **müssen** mit einem versionierten Change-Management-System dokumentiert und validiert werden.

---

Diese Anforderungen bilden eine solide Grundlage, die sowohl den Entwicklungsprozess erleichtert als auch die Sicherheit und Zuverlässigkeit eines Battery Management Systems gewährleistet.