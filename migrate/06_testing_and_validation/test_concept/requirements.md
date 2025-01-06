# Anforderungen

## Funktionale Anforderungen

### Spannungsüberwachung

#### Anforderung
- Das BMS muss die Zellspannungen jeder einzelnen Zelle mit einer Genauigkeit von ±0,01 V messen.
- Es muss eine Warnung ausgegeben werden, wenn die Zellspannung unter 2,5 V oder über 4,2 V liegt.

#### Testspezifikation

- Testfall 1.1: Überprüfen Sie die Genauigkeit der Zellspannungsmessung durch Einspeisen von Spannungen im Bereich von 2,5 V bis 4,2 V in 0,01 V-Schritten. Validieren Sie die Messwerte.
- Testfall 1.2: Simulieren Sie eine Zellspannung unter 2,5 V und prüfen Sie, ob eine Warnung generiert wird.
- Testfall 1.3: Simulieren Sie eine Zellspannung über 4,2 V und prüfen Sie, ob eine Warnung generiert wird.

---

### Stromüberwachung

#### Anforderung
- Das BMS muss den Lade- und Entladestrom der Batterie kontinuierlich überwachen und sicherstellen, dass der Strom innerhalb des spezifizierten Bereichs bleibt (z. B. -50 A bis +50 A).

#### Testspezifikation
- Testfall 2.1: Speisen Sie Lade- und Entladeströme im Bereich von -50 A bis +50 A in 5 A-Schritten ein und überprüfen Sie die gemessenen Werte auf Genauigkeit.
- Testfall 2.2: Überschreiten Sie den spezifizierten Strombereich und überprüfen Sie, ob das BMS Schutzmaßnahmen einleitet.

---

### Temperaturmanagement

#### Anforderung

- Das BMS muss die Temperatur jeder Batteriezelle sowie der gesamten Batterie mit einer Genauigkeit von ±2 °C messen.
- Das System muss eine Abschaltung einleiten, wenn die Temperatur einer Zelle 60 °C übersteigt oder unter -20 °C fällt.

#### Testspezifikation

- Testfall 3.1: Simulieren Sie Temperaturen zwischen -20 °C und 60 °C und überprüfen Sie die Messgenauigkeit (±2 °C).
- Testfall 3.2: Überschreiten Sie die Temperaturschwellen (-20 °C und 60 °C) und prüfen Sie, ob das BMS eine Abschaltung einleitet.

---

4. State of Charge (SoC) Berechnung  
   - Das BMS muss den Ladezustand der Batterie in Prozent mit einer Genauigkeit von ±5 % berechnen und an das Fahrzeugsteuergerät kommunizieren.

5. State of Health (SoH) Berechnung  
   - Das BMS muss den Gesundheitszustand der Batterie (SoH) basierend auf Ladezyklen, Zellalterung und Kapazitätsverlust ermitteln und regelmäßig aktualisieren.

6. Fehlererkennung und Schutzmechanismen  
   - Das BMS muss Zellbalancing durchführen, wenn der Spannungsunterschied zwischen Zellen ≥ 0,1 V beträgt.
   - Das BMS muss Überspannung, Überstrom, Übertemperatur und Tiefentladung erkennen und entsprechende Schutzmaßnahmen aktivieren.

7. Kommunikation  
   - Das BMS muss über CAN und LIN-Protokolle mit anderen Fahrzeugsteuergeräten kommunizieren.
   - Fehler und Warnungen müssen in einem standardisierten Format (z. B. DTC gemäß ISO 14229) gesendet werden.

---

## Sicherheitsanforderungen (ISO 26262-konform)
8. Sicherer Zustand  
   - Bei Erkennung eines kritischen Fehlers muss das BMS die Batterie innerhalb von ≤ 10 ms in einen sicheren Zustand versetzen.

9. Redundanz  
   - Das BMS muss redundante Messpfade für Spannung und Temperatur enthalten, um Ausfälle zu kompensieren.

10. ASIL-B Konformität  
    - Das BMS muss alle Anforderungen an ASIL-B-Systeme erfüllen, einschließlich Diagnose- und Sicherheitsmechanismen.

---

## Test- und Verifikationsanforderungen
11. HiL-Testumgebung  
    - Das BMS muss so ausgelegt sein, dass es in einer HiL-Testumgebung getestet werden kann, um alle Funktionen und Sicherheitsmechanismen zu validieren.

12. Testabdeckung  
    - Alle sicherheitskritischen Funktionen des BMS müssen durch automatisierte Testfälle zu mindestens 90 % abgedeckt sein.

13. Diagnosefähigkeit  
    - Das BMS muss alle erkannten Fehlercodes (DTCs) speichern und über ein Diagnosewerkzeug wie CANoe oder INCA auslesbar machen.

---

## Umgebungs- und Systemanforderungen
14. Temperaturbereich  
    - Das BMS muss innerhalb eines Temperaturbereichs von -40 °C bis +85 °C betriebsbereit sein.

15. Mechanische Belastung  
    - Das BMS muss Vibrationen gemäß ISO 16750-3 (Testbedingungen für Kraftfahrzeugelektronik) standhalten.

16. EMV  
    - Das BMS muss die elektromagnetische Verträglichkeit gemäß ISO 11452 sicherstellen.

---

## Leistungsanforderungen
17. Reaktionszeit  
    - Das BMS muss auf externe Steuerbefehle und interne Fehlermeldungen innerhalb von ≤ 5 ms reagieren.

18. Energieverbrauch  
    - Der Energieverbrauch des BMS im Standby-Modus darf 10 mW nicht überschreiten.

---

Diese Anforderungen sind klar, präzise, testbar und mit den geltenden Automotive-Standards kompatibel.