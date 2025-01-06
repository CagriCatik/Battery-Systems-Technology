# Test Concept

# Testkonzept

## Was ist ein Testkonzept?

Ein **Testkonzept** ist ein strukturierter Plan, der alle relevanten Informationen und Strategien für die Durchführung von Tests beschreibt. Es dient als Leitfaden, um sicherzustellen, dass die Tests zielgerichtet, nachvollziehbar und effizient durchgeführt werden. Das Testkonzept deckt folgende Aspekte ab:

1. **Ziel des Tests**: Warum wird getestet? Welche Anforderungen sollen geprüft werden?
2. **Testgegenstand**: Was wird getestet? (z. B. Komponenten, Systeme, Funktionen)
3. **Teststrategie**: Wie wird getestet? (z. B. manuell, automatisiert, Simulationen)
4. **Testumgebung**: Wo und unter welchen Bedingungen wird getestet? (z. B. HiL, Prüfstände, reale Fahrzeuge)
5. **Testmittel**: Welche Tools, Hardware und Software werden verwendet? 
6. **Rollen und Verantwortlichkeiten**: Wer führt die Tests durch?
7. **Kriterien**: Was sind die Abbruchkriterien, Erfolgskriterien und Abnahmekriterien?
8. **Testzeitplan**: Wann werden welche Tests durchgeführt?

---

## Wie entwickelt man ein Testkonzept?

### Schritt 1: **Anforderungen analysieren**
- Sammeln Sie alle relevanten Anforderungen aus Lastenheften, Spezifikationen und Normen (z. B. ISO 26262 für Funktionale Sicherheit).
- Definieren Sie die zu prüfenden Funktionen und Komponenten des Batteriemanagementsystems (BMS).

### Schritt 2: **Ziele und Teststrategie definieren**
- Ziel: Überprüfen, ob das BMS im Gesamtfahrzeug ordnungsgemäß funktioniert.
- Strategie: Festlegen, welche Testmethoden eingesetzt werden:
  - **Komponententests**: Überprüfung einzelner Funktionen des BMS.
  - **Integrationstests**: Sicherstellen, dass das BMS mit anderen Fahrzeugsystemen kompatibel ist.
  - **Systemtests**: Testen der Gesamtfunktionalität im HiL und Fahrzeug.

### Schritt 3: **Testgegenstand und Testfälle beschreiben**
- Definieren Sie den Testgegenstand (z. B. Batteriesteuergerät, Sensoren, Schnittstellen wie CAN/LIN/FlexRay).
- Entwickeln Sie Testfälle basierend auf den Anforderungen:
  - Lade-/Entladezyklen
  - Temperaturmanagement
  - Zellbalancing
  - Fehlererkennung und -management
  - Kommunikation mit dem Fahrzeugnetzwerk

### Schritt 4: **Testumgebung definieren**
- **HiL-Umgebung**:
  - Simulieren Sie das Fahrzeugverhalten, um das BMS zu testen.
  - Verwenden Sie spezifische Modelle für Batterie, Ladung, Temperatur und Stromverbrauch.
- **Gesamtfahrzeug**:
  - Validierung des BMS unter realen Bedingungen (z. B. Testfahrten).
- Tools: CANape, dSPACE, Vector CANoe, NI Veristand, ECU-Test.

### Schritt 5: **Testmittel und Automatisierung planen**
- Automatisieren Sie Testfälle, um Wiederholbarkeit und Effizienz zu steigern.
- Tools:
  - Testautomatisierung mit **ecu.test** oder **CAPL**.
  - Datenauswertung mit **CANape**.
  - Versionsverwaltung und Testmanagement mit **DOORS** oder **Polarion**.

### Schritt 6: **Kriterien festlegen**
- **Abnahmekriterien**: Das BMS erfüllt alle funktionalen Anforderungen.
- **Abbruchkriterien**: Tests werden abgebrochen, wenn wesentliche Hardware- oder Softwarefehler auftreten.
- **Erfolgskriterien**: Alle definierten Testfälle wurden bestanden.

### Schritt 7: **Zeitplan und Ressourcen abstimmen**
- Entwickeln Sie einen Zeitplan, der Testphasen, Deadlines und Ressourcen berücksichtigt.
- Weisen Sie Rollen und Verantwortlichkeiten zu.

### Schritt 8: **Dokumentation und Freigabe**
- Halten Sie das Konzept in einem **Testkonzept-Dokument** fest und lassen Sie es von den relevanten Stakeholdern genehmigen.

---

## Beispiel: Testkonzept für ein BMS im Automotive-Umfeld

### **Anforderungen**
- Temperaturüberwachung der Batteriezellen (Sensoren)
- Kommunikation über CAN und FlexRay
- Sicherheitsfunktionen (ISO 26262)

### **Teststrategie**
- HiL-Tests zur Simulation von Fahrzeugbedingungen.
- Integrationstests mit dem Antriebsstrang-Steuergerät.
- Systemtests im Fahrzeug.

### **Testumgebung**
- HiL-Prüfstand:
  - Batterie-Modell simuliert mit **Simulink**.
  - Fehlerszenarien: Ausfall eines Sensors, Überhitzung.
- Fahrzeugtests:
  - Testfahrten bei unterschiedlichen Temperaturen (Winter/Sommer).

### **Testfälle**
1. Überprüfen, ob das BMS den Ladezustand (SOC) korrekt berechnet.
2. Simulation eines Temperatursensors mit Überhitzungswert.
3. Kommunikationsprüfung zwischen BMS und Fahrzeugsteuergerät.

### **Testtools**
- **CANoe**: Kommunikationstest.
- **DOORS**: Anforderungsmanagement.
- **dSPACE**: HiL-Simulation.

### **Abnahmekriterien**
- Das BMS erkennt und meldet alle Fehler korrekt.
- Kommunikation funktioniert gemäß Spezifikation.

---

## **Muster-Testkonzept für ein Batteriemanagementsystem (BMS) im Automotive-Umfeld (ASPICE-konform)**

---

### **1. Einleitung**
Dieses Testkonzept beschreibt die geplante Vorgehensweise zur Verifikation und Validierung eines Batteriemanagementsystems (BMS) im Automotive-Umfeld. Ziel ist die Sicherstellung der korrekten Funktionalität gemäß den System- und Softwareanforderungen sowie die Einhaltung relevanter Normen wie ISO 26262 und ASPICE.

---

### **2. Ziele des Testkonzepts**
- **Verifikation**: Sicherstellen, dass das BMS die spezifizierten Anforderungen erfüllt.
- **Validierung**: Prüfen, ob das BMS im realen Fahrzeugbetrieb zuverlässig arbeitet.
- **Rückverfolgbarkeit**: Lückenlose Nachverfolgbarkeit von Anforderungen zu den Testfällen.
- **Fehleridentifikation und -behebung**: Aufdecken und Dokumentieren von Fehlern zur Prozessoptimierung.

---

### **3. Testgegenstand**
Der Testgegenstand ist das Batteriemanagementsystem (BMS), bestehend aus:
- **Hardware**: Steuergerät, Sensoren (Temperatur, Spannung, Strom).
- **Software**: Steuerungs- und Regelungsalgorithmen (z. B. Zell-Balancing, Sicherheitsfunktionen).
- **Schnittstellen**: CAN-Bus, FlexRay, LIN.

---

### **4. Teststrategie**
Die Teststrategie umfasst drei Hauptbereiche, abgestimmt auf ASPICE-Prozesse:

#### **4.1 Systemtests (SYS.4)**
- Ziel: Sicherstellen, dass das BMS korrekt in das Fahrzeug integriert ist.
- Testumgebung:
  - HiL-Prüfstand (Hardware-in-the-Loop).
  - Realfahrzeugtests unter verschiedenen Betriebsbedingungen.
- Testfälle:
  1. **Kommunikationstest**: Prüfen der CAN/FlexRay-Kommunikation zwischen BMS und anderen Steuergeräten.
  2. **Fehlerhandling**: Simulieren von Zellenausfall und Überhitzung.

#### **4.2 Softwareintegrationstests (SWE.5)**
- Ziel: Überprüfung der Interaktion zwischen Softwaremodulen.
- Testumgebung:
  - SIL-Prüfstand (Software-in-the-Loop).
- Testfälle:
  1. **Balancing-Algorithmus**: Validierung des Zellenausgleichs unter verschiedenen Ladezuständen.
  2. **Laderegler**: Simulation von Lade- und Entladezyklen.

#### **4.3 Softwareunitverifikation (SWE.4)**
- Ziel: Verifikation einzelner Softwaremodule.
- Testumgebung:
  - White-Box-Tests.
- Testfälle:
  1. **SOC-Berechnung**: Testen der Berechnung des Ladezustands (State of Charge).
  2. **Fehlererkennung**: Prüfung des Algorithmus zur Erkennung fehlerhafter Sensoren.

---

### **5. Testumgebung**
Die Testumgebungen werden je nach Testphase und Ziel definiert:

- **HiL-Prüfstand**:
  - Werkzeuge: dSPACE, Vector CANoe.
  - Simulation von Batterieparametern, Umwelteinflüssen und Fahrzeugverhalten.
  
- **SIL-Prüfstand**:
  - Werkzeuge: MATLAB/Simulink, Jenkins (für Automatisierung).
  - Testen von Softwaremodulen ohne Hardware.
  
- **Realfahrzeug**:
  - Testfahrten mit verschiedenen Temperaturszenarien (-20 °C bis +50 °C).
  - Überwachung mit Datenloggern (z. B. CANalyzer).

---

### **6. Testmittel**
- **Tools für Testautomatisierung**:
  - ECU-Test: Automatisierte Testfälle am HiL.
  - CANoe: Tests der Kommunikation.
  - Jenkins: Automatisierung von Regressionstests.
  
- **Tools für Anforderungsmanagement**:
  - DOORS: Verwaltung der Anforderungen.
  - Polarion: Rückverfolgbarkeit von Anforderungen und Tests.

- **Simulationswerkzeuge**:
  - MATLAB/Simulink: Modellbasierte Entwicklung.
  - NI Veristand: Echtzeitsimulation.

---

### **7. Rollen und Verantwortlichkeiten**
- **Testmanager**: Koordiniert das Testkonzept und überwacht die Durchführung.
- **Systemtestingenieur**: Führt System- und Integrationstests durch.
- **Softwareentwickler**: Entwickelt und testet die Softwaremodule.
- **Qualitätsmanager**: Überwacht die Einhaltung der ASPICE-Prozesse.

---

### **8. Testmetriken**
- **Anforderungsabdeckung**: Sicherstellen, dass alle Anforderungen getestet sind (z. B. 95% Abdeckung).
- **Fehlerdichte**: Anzahl gefundener Fehler pro Testfall.
- **Testabdeckung**: Überprüfung aller Softwarepfade (z. B. durch Code Coverage).

---

### **9. Testkriterien**
- **Abnahmekriterien**:
  - Alle Tests wurden erfolgreich durchgeführt.
  - Alle kritischen Fehler wurden behoben.
  
- **Abbruchkriterien**:
  - Kritische Fehler, die eine Weiterführung der Tests verhindern.

- **Erfolgskriterien**:
  - Anforderungen und Sicherheitsziele (ISO 26262) wurden vollständig erfüllt.

