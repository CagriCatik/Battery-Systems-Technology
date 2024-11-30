# State Machine - Batteriemanagementsystem

In der Fahrzeugtechnik fungiert das Batteriemanagementsystem (BMS) als zentrale Schnittstelle zwischen dem Fahrzeug und den in der Batterie integrierten elektronischen Komponenten. Ein wesentliches Merkmal des BMS ist seine State Machine, die die verschiedenen Betriebszustände und Übergänge des Systems steuert. Diese strukturierte Zustandsverwaltung gewährleistet eine effiziente, sichere und zuverlässige Steuerung der Batterie im gesamten Fahrzeugbetrieb.

## **State Machine des BMS**

Die State Machine des BMS gliedert sich in mehrere klar definierte Zustände, die jeweils spezifische Funktionen und Übergangsbedingungen aufweisen. Die Hauptzustände umfassen:

1. **Schlafmodus (Sleep Mode)**
2. **Wachmodus (Active Mode)**
3. **Startmodus (Start Mode)**
4. **Betriebsmodus (Operational Mode)**
5. **Fehlerzustand (Fault Mode)**
6. **Sicherheitsmodus (Safety Mode)**

### **1. Schlafmodus (Sleep Mode)**
- **Beschreibung:** Aktiviert, wenn das Fahrzeug ausgeschaltet ist.
- **Funktionen:**
  - Minimierung des Energieverbrauchs durch das Batteriesystem.
  - Periodisches Aufwachen des BMS gemäß einer programmierten Zykluszeit.
- **Übergangsbedingungen:**
  - Fahrzeug wird eingeschaltet → Übergang zu Startmodus.

### **2. Wachmodus (Active Mode)**
- **Beschreibung:** Kurzzeitiger Zustand während der regelmäßigen Überprüfungen im Schlafmodus.
- **Funktionen:**
  - Durchführung von Systemprüfungen (Spannungen, Temperaturen etc.).
  - Fehlererkennung und -protokollierung.
  - Steuerung von Kühl- und Heizfunktionen zur Temperaturregelung.
- **Übergangsbedingungen:**
  - Abschluss der Prüfungen → Rückkehr zum Schlafmodus.

### **3. Startmodus (Start Mode)**
- **Beschreibung:** Aktiviert beim Starten des Fahrzeugs.
- **Funktionen:**
  - Überprüfung des Fahrakkuzustands.
  - Aktivierung der Schütze des Batteriesystems zur Stromversorgung des Motors.
- **Übergangsbedingungen:**
  - Erfolgreiche Überprüfung → Übergang zum Betriebsmodus.
  - Fehler erkannt → Übergang zum Fehlerzustand.

### **4. Betriebsmodus (Operational Mode)**
- **Beschreibung:** Hauptbetriebszustand während der Fahrzeugnutzung.
- **Funktionen:**
  - Kontinuierliche Überwachung der Batterieparameter.
  - Dynamische Anpassung der Kühl- und Heizmaßnahmen zur Optimierung der Batterieleistung und -lebensdauer.
- **Übergangsbedingungen:**
  - Fahrzeug wird ausgeschaltet → Übergang zum Schlafmodus.
  - Fehler erkannt → Übergang zum Fehlerzustand.

### **5. Fehlerzustand (Fault Mode)**
- **Beschreibung:** Aktiviert bei Erkennung eines Fehlers im Batteriesystem.
- **Funktionen:**
  - Analyse und Kategorisierung des Fehlers.
  - Speicherung des Fehlers für zukünftige Wartungsarbeiten.
  - Anzeige des Fehlers an den Fahrer.
- **Übergangsbedingungen:**
  - Kritischer Fehler → Übergang zum Sicherheitsmodus.
  - Fehler behoben → Rückkehr zum Betriebsmodus.

### **6. Sicherheitsmodus (Safety Mode)**
- **Beschreibung:** Letzter Schutzzustand bei kritischen Fehlern.
- **Funktionen:**
  - Unterbrechung des Fahrstroms oder vollständige Abschaltung der Batterie.
  - Gewährleistung der Sicherheit des Fahrzeugs und der Insassen.
- **Übergangsbedingungen:**
  - Fehler behoben → Rückkehr zum Betriebsmodus nach Überprüfung.

## **Interaktion der Zustände im Fahrzeugbetrieb**

Beim Starten des Fahrzeugs initiiert das Steuergerät einen Übergang vom Schlafmodus in den Startmodus. Das BMS prüft den Zustand des Fahrakkus und aktiviert die notwendigen Schütze, um den Motor mit Strom zu versorgen. Während des Betriebs überwacht das BMS kontinuierlich die Batterieparameter und passt die Kühl- bzw. Heizmaßnahmen an, um optimale Bedingungen aufrechtzuerhalten.

Tritt ein Fehler während des Betriebs auf, wechselt das BMS in den Fehlerzustand, analysiert und kategorisiert den Fehler und informiert den Fahrer. Bei kritischen Fehlern erfolgt ein Übergang in den Sicherheitsmodus, um die Batterie zu schützen und potenzielle Gefahren zu vermeiden.

## **Vorteile der State Machine im BMS**

- **Strukturierte Zustandsverwaltung:** Klare Definition von Zuständen und Übergängen erleichtert die Fehlerdiagnose und Systemwartung.
- **Erhöhte Sicherheit:** Schnelle Reaktion auf Fehler durch definierte Sicherheitszustände schützt Fahrzeug und Insassen.
- **Optimierte Batterieleistung:** Dynamische Anpassung der Betriebszustände zur Maximierung der Effizienz und Lebensdauer der Batterie.
- **Zuverlässigkeit:** Kontinuierliche Überwachung und systematische Zustandswechsel gewährleisten einen stabilen Fahrzeugbetrieb.

Durch die Implementierung einer State Machine im BMS wird eine robuste und effiziente Steuerung der Fahrzeugbatterie realisiert, die sowohl die Leistung als auch die Sicherheit des Fahrzeugs signifikant verbessert.


```plantuml
@startuml
!define RECTANGLE class

[*] --> Sleep_Mode

Sleep_Mode --> Start_Mode : Fahrzeug eingeschaltet
Sleep_Mode : Minimiert Energieverbrauch
Sleep_Mode : Periodisches Aufwachen gemäß Zykluszeit

Start_Mode --> Operational_Mode : Erfolgreiche Überprüfung
Start_Mode --> Fault_Mode : Fehler erkannt
Start_Mode : Überprüfung des Fahrakkuzustands
Start_Mode : Aktivierung der Schütze für Motorstrom

Operational_Mode --> Sleep_Mode : Fahrzeug ausgeschaltet
Operational_Mode --> Fault_Mode : Fehler erkannt
Operational_Mode : Kontinuierliche Überwachung der Batterie
Operational_Mode : Dynamische Anpassung der Kühl-/Heizmaßnahmen

Fault_Mode --> Safety_Mode : Kritischer Fehler
Fault_Mode --> Operational_Mode : Fehler behoben
Fault_Mode : Analyse und Kategorisierung des Fehlers
Fault_Mode : Speicherung und Anzeige des Fehlers

Safety_Mode --> Operational_Mode : Fehler behoben und überprüft
Safety_Mode : Unterbrechung des Fahrstroms
Safety_Mode : Vollständige Abschaltung der Batterie

Sleep_Mode --> Active_Mode : Kurzzeitige Aktivierung
Active_Mode --> Sleep_Mode : Abschluss der Prüfungen
Active_Mode : Durchführung von Systemprüfungen
Active_Mode : Fehlererkennung und -protokollierung
Active_Mode : Steuerung von Kühl- und Heizfunktionen

@enduml
