# ecu.test

In Projekten, die die Komponenten- und Systemtests für Batteriemanagementsysteme (BMS) umfassen, ist **ecu.test** von Tracetronic ein unverzichtbares Werkzeug für die Testautomatisierung und Validierung. Dieses Tool ermöglicht die Spezifikation, Implementierung, Dokumentation, Ausführung und Auswertung von Testfällen für eingebettete Systeme. Es unterstützt verschiedene Teststufen, darunter Model-in-the-Loop (MiL), Software-in-the-Loop (SiL) und Hardware-in-the-Loop (HiL), sowie Tests an realen Systemen.

1. **Testautomatisierung und -ausführung:**
   - Mit ecu.test können Testfälle grafisch erstellt werden, wodurch auch Ingenieure ohne tiefgehende Programmierkenntnisse komplexe Tests für BMS-Systeme entwickeln können.
   - Die Ablaufmaschine von ecu.test führt Testfälle aus, erfasst umfassende Log-Daten und erstellt detaillierte Testberichte. Dies ist besonders nützlich für die Validierung von Funktionen wie Zellspannungsüberwachung, Temperaturmanagement und Laderegelung.

2. **Integration mit verschiedenen Tools und Schnittstellen:**
   - ecu.test bietet Unterstützung für eine Vielzahl von Hard- und Software-Tools, darunter CANoe und CANape von Vector, um Test- und Messaufgaben zu vereinfachen.
   - Durch definierte Schnittstellen können Werkzeuge für das Test- und Anforderungsmanagement eingebunden werden, was die Nachverfolgbarkeit und Effizienz der Tests im BMS-Entwicklungsprozess steigert.

3. **Messdatenerfassung und Analyse:**
   - Während der Testausführung erfasst ecu.test Messdaten wie Zellspannungen, Ströme und Temperaturen, die anschließend analysiert werden können, um das Verhalten des BMS unter verschiedenen Lade- und Entladebedingungen zu bewerten.
   - Die Traceanalyse erlaubt es, Signale effizient zu verarbeiten und Fehler wie Zellimbalancen oder Temperaturabweichungen zu identifizieren.

4. **Diagnose und Fehlersimulation:**
   - ecu.test ermöglicht umfassende Diagnosetests und die Simulation von Fehlern, um die Robustheit des BMS zu überprüfen, beispielsweise durch das Testen von Kommunikationsprotokollen wie UDS oder die gezielte Simulation von Sensorausfällen.
   - Diese Funktionen sind essenziell für die Sicherstellung der funktionalen Sicherheit und Zuverlässigkeit des Systems.

5. **Unterstützung von HiL-Tests:**
   - Durch die Integration mit HiL-Systemen können reale Hardwarekomponenten, wie Batteriemodule oder Steuergeräte, in die Testumgebung eingebunden werden.
   - Dies erlaubt realitätsnahe Tests, beispielsweise zur Validierung des Batteriezustands (State of Charge, SoC) und der Lebensdauerüberwachung (State of Health, SoH).

6. **Berichterstellung und Dokumentation:**
   - Nach Abschluss der Tests erstellt ecu.test detaillierte Berichte mit Testergebnissen, die interaktiv geprüft oder in Datenbanken gespeichert werden können.
   - Diese Berichte unterstützen die Nachvollziehbarkeit und sind entscheidend für Audits im Rahmen der Entwicklungs- und Zulassungsprozesse.

Mit seinen umfangreichen Funktionen und der nahtlosen Integration in verschiedene Testumgebungen ist **ecu.test** ein Schlüsselwerkzeug zur Sicherstellung der Qualität und Zuverlässigkeit von Batteriemanagementsystemen.


## ecu.test vs. EXAM

1. **Grafische Testfallerstellung**: Beide Tools ermöglichen die grafische Entwicklung von Testfällen, wodurch Anwender ohne tiefgehende Programmierkenntnisse Tests erstellen können. 

2. **Unterstützung verschiedener Testumgebungen**: Sowohl ecu.test als auch EXAM sind in unterschiedlichen Teststufen einsetzbar, einschließlich Model-in-the-Loop (MiL), Software-in-the-Loop (SiL) und Hardware-in-the-Loop (HiL). 

3. **Integration von Standardwerkzeugen**: Beide Tools bieten Schnittstellen zu gängigen Testsystemen und -werkzeugen, was eine nahtlose Integration in bestehende Testumgebungen ermöglicht. 

4. **Wiederverwendbarkeit von Testfällen**: Durch generische Testbeschreibungen und einheitliche Testprozesse fördern sowohl ecu.test als auch EXAM die Wiederverwendbarkeit von Testfällen über verschiedene Projekte hinweg. 

5. **Umfassende Testdokumentation**: Beide Werkzeuge bieten Funktionen zur Protokollierung und Auswertung von Testergebnissen, einschließlich der Erstellung detaillierter Testberichte.

---

ecu.test von TraceTronic und EXAM von MicroNova sind beide etablierte Werkzeuge zur Testautomatisierung in der Automobilindustrie, insbesondere für Steuergeräte (ECUs). Nachfolgend ein Vergleich der beiden Tools:

**Entwicklung und Verfügbarkeit:**

- **ecu.test**: Entwickelt von der TraceTronic GmbH in Dresden, ist ecu.test seit 2003 im Einsatz und wurde im Dezember 2023 von ECU-TEST in ecu.test umbenannt. 

- **EXAM**: Seit 2006 wird EXAM gemeinsam von der AUDI AG, der Volkswagen AG und MicroNova entwickelt und hat sich als konzerneinheitlicher Standard im Volkswagen Konzern etabliert. 

**Funktionalität und Methodik:**

- **ecu.test**: Bietet eine grafische Benutzeroberfläche zur Erstellung von Testfällen und unterstützt verschiedene Teststufen wie Model-in-the-Loop, Software-in-the-Loop und Hardware-in-the-Loop. Die Tests können mit Python angepasst werden, was Flexibilität bei der Testentwicklung ermöglicht. 

- **EXAM**: Setzt auf eine grafische Entwicklung von Testfällen basierend auf der Unified Modeling Language (UML). Es ermöglicht die Erstellung von Testabläufen in Sequenzdiagrammen und unterstützt die Wiederverwendbarkeit von Testfällen. 

**Schnittstellen und Integration:**

- **ecu.test**: Unterstützt eine Vielzahl von Hard- und Softwarekomponenten, darunter dSPACE ControlDesk, ETAS INCA, Vector CANoe und viele mehr. Es bietet klar definierte Schnittstellen für Erweiterungen und die Integration in bestehende Test- und Absicherungsprozesse. 

- **EXAM**: Bietet offene Schnittstellen, die die Anbindung zusätzlicher Hard- und Software ermöglichen, z. B. in Form von Plug-ins und als Erweiterung der EXAM-Bibliotheken. Es unterstützt zahlreiche Hard- und Softwarekomponenten, darunter ASAM XiL API, dSPACE ControlDesk, ETAS INCA und Vector CANoe. 

**Lizenzierung und Verfügbarkeit:**

- **ecu.test**: Ist ein proprietäres Softwarewerkzeug, das von TraceTronic vertrieben wird. Es bietet verschiedene Lizenzmodelle, die auf die Bedürfnisse der Kunden zugeschnitten sind. 

- **EXAM**: Steht unter einer Freeware-Lizenz zur Verfügung, wobei das Tooling kostenfrei ist und die Core-Bibliotheken als Open Source erhältlich sind. Zusätzlich gibt es lizenzpflichtige Erweiterungen, die den Funktionsumfang erweitern. 

**Zusammenfassung:**

Beide Tools bieten umfangreiche Möglichkeiten zur Testautomatisierung von Steuergeräten und unterstützen verschiedene Testumgebungen. Die Wahl zwischen ecu.test und EXAM hängt von spezifischen Anforderungen, bestehenden Systemen und Präferenzen hinsichtlich Methodik und Integration ab. 

---

Sowohl **SCALEXIO** von dSPACE als auch **NovaCarts** von MicroNova sind fortschrittliche Hardware-in-the-Loop (HiL)-Simulationsplattformen, die in der Automobilindustrie zur Entwicklung und Validierung von Steuergeräten (ECUs) eingesetzt werden. Nachfolgend ein Vergleich der beiden Systeme:

**Modularität und Skalierbarkeit:**

- **SCALEXIO**: Bietet eine modulare und skalierbare Echtzeitplattform, die sich flexibel an verschiedene Projektanforderungen anpassen lässt. Sie unterstützt sowohl stationäre als auch mobile Anwendungen und ermöglicht die nahtlose Integration von I/O-Schnittstellen sowie Bus- und Netzwerkschnittstellen. 

- **NovaCarts**: Steht für leistungsstarke und zukunftsfähige HiL-Simulatoren mit hoher Modularität und Skalierbarkeit. Die Plattform deckt alle Testanforderungen des gesamten V-Modells ab und ermöglicht die Anpassung an spezifische Kundenbedürfnisse. 

**Echtzeitfähigkeiten und Rechenleistung:**

- **SCALEXIO**: Verfügt über leistungsstarke Prozessortechnologie, die die Echtzeitberechnung großer und komplexer Simulationsmodelle ermöglicht. Die Plattform unterstützt umfassende, präzise und schnelle I/O-Fähigkeiten, basierend auf FPGA-Technologie. 

- **NovaCarts**: Setzt auf eine offene und leistungsstarke Modellplattform mit Zykluszeiten ab wenigen Mikrosekunden und hochdynamischen I/Os. Dies ermöglicht die Entwicklung neuer BMS-Algorithmen und die genaue Abbildung dynamischer Zellverhalten. 

**Anwendungsbereiche:**

- **SCALEXIO**: Eignet sich für eine Vielzahl von Anwendungen, darunter Rapid-Control-Prototyping, HiL-Tests auf Signal- und Leistungsebene sowie mechanische Prüfstände. Die Plattform unterstützt alle gängigen Busnetzwerke und bietet umfangreiche I/O-Fähigkeiten. 

- **NovaCarts**: Deckt alle Testanforderungen des gesamten V-Modells ab – von der Überprüfung einzelner Steuergeräte sowie Software- oder Hardware-Funktionen bis hin zur gesamten Fahrzeugelektronik. Die Plattform ist besonders geeignet für anspruchsvolle Testing-Anwendungen in technologisch anspruchsvollen Bereichen. 

**Integration und Offenheit:**

- **SCALEXIO**: Bietet Offenheit für mehrere Simulationsumgebungen von Drittanbietern über das Functional Mock-up Interface (FMI) und unterstützt die neuesten Kommunikationsstandards im Automobilbereich, einschließlich Sicherheit. 

- **NovaCarts**: Verfügt über offene und standardisierte Schnittstellen, die die Vernetzung mit Fremdsystemen und die nahtlose Integration in heterogene Prüffelder ermöglichen. Die Plattform unterstützt die Funktionalitäten des Standards „XIL API 2.0.2“. 

**Zusammenfassung:**

Beide Plattformen bieten leistungsstarke und flexible Lösungen für HiL-Simulationen in der Automobilindustrie. Die Wahl zwischen SCALEXIO und NovaCarts hängt von spezifischen Projektanforderungen, bestehenden Systemen und Präferenzen hinsichtlich Modularität, Echtzeitfähigkeiten und Integrationsmöglichkeiten ab. 