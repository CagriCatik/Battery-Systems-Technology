# Mögliche Fragen - 2

---

## **1. Wie würden Sie ein Testkonzept für ein BMS oder HiL-Testsystem entwickeln?**
Ein Testkonzept beginnt mit einer Analyse der Anforderungen, sowohl funktionaler als auch sicherheitsrelevanter Natur. Ich würde folgende Schritte einleiten:

1. **Anforderungsanalyse:** Erstellung eines Anforderungsdokuments basierend auf Spezifikationen und Standards wie ISO 26262.
2. **Teststrategie:** Festlegung der Testarten (z. B. Unit-, Integrations-, Systemtests) und -umgebungen (HiL, MiL, SiL).
3. **Testplanung:** Definieren von Testfällen basierend auf den Anforderungen. Hierbei wird auf Rückverfolgbarkeit zwischen Anforderungen und Tests geachtet.
4. **Implementierung:** Einrichtung der HiL-Systeme und Integration der Simulationsmodelle.
5. **Validierung:** Testdurchführung und Dokumentation der Ergebnisse.
6. **Reporting:** Erstellung eines umfassenden Testberichts mit Fehleranalysen und Optimierungsvorschlägen.

---

## **2. Welche Erfahrungen haben Sie mit der Fehlersuche in sicherheitskritischen Systemen?**
In meiner bisherigen Arbeit habe ich viel Zeit mit der Fehlersuche verbracht, insbesondere in sicherheitskritischen Systemen. Dabei habe ich folgende Methoden verwendet:

- **Protokollanalyse mit Tools wie CANoe:** Hierbei habe ich Kommunikationsfehler in CAN-, LIN- und FlexRay-Netzwerken identifiziert.
- **Debugging auf Software- und Hardware-Ebene:** Mithilfe von Debuggern und Oszilloskopen habe ich Timing-Probleme und Hardware-Störungen gelöst.
- **Root-Cause-Analyse:** Ursachen wurden systematisch isoliert, zum Beispiel durch Hypothesenbildung und gezielte Testszenarien.
- **Simulation in HiL-Umgebungen:** Die Simulation verschiedener Fehlerzustände hat dabei geholfen, Probleme in einem kontrollierten Umfeld zu reproduzieren.

Ein konkretes Beispiel: Während eines Projekts mit einem Steuergerät konnte ich ein sporadisches Problem in der CAN-Kommunikation auf eine fehlerhafte Rückmeldung der Watchdog-Funktion eingrenzen und gemeinsam mit dem Entwicklungsteam beheben.

---

## **3. Können Sie ein Beispiel für ein erfolgreiches Projekt nennen, bei dem Sie eine Herausforderung im Testen von Steuergeräten gelöst haben?**
In einem Projekt für ein elektronisches Lenksystem hatte das Team Schwierigkeiten, sporadische Kommunikationsabbrüche während der Systemtests zu reproduzieren. 

Mein Ansatz:
- Ich habe mithilfe von CAPL-Skripten automatisierte Stresstests für die CAN-Kommunikation implementiert, um die Abbrüche in der HiL-Umgebung nachzustellen.
- Parallel habe ich die Systemlogs analysiert und die Fehler mit den Testprotokollen korreliert.
- Das Problem stellte sich als fehlerhafte Synchronisation eines Timer-Interrupts heraus, der durch eine Aktualisierung der Software behoben wurde.

Ergebnis: Der Fehler wurde erfolgreich behoben, und das Testkonzept wurde als Grundlage für ähnliche Systeme übernommen.

---

## **4. Wie gehen Sie vor, wenn Sie unvollständige Anforderungen in einem Projekt vorfinden?**
Unvollständige Anforderungen sind häufig ein Teil von Entwicklungsprojekten. Mein Ansatz ist:

1. **Klären:** Direkte Abstimmung mit den Stakeholdern (z. B. Produktmanager, Systementwickler), um offene Punkte zu klären.
2. **Dokumentation:** Offene Anforderungen dokumentieren und als "Annahmen" kennzeichnen, um Transparenz zu gewährleisten.
3. **Iteratives Vorgehen:** Das Projekt in kleinen, validierbaren Schritten umsetzen und Feedback einholen.
4. **Risikoanalyse:** Mögliche Risiken durch fehlende Informationen bewerten und priorisieren.

Ein Beispiel aus der Praxis: Bei einem Testprojekt waren die Schnittstellenspezifikationen unvollständig. Ich habe ein Protokoll entwickelt, um die fehlenden Details iterativ mit den Entwicklern zu klären, während der Test planmäßig weiterlief.

---

## **5. Wie schnell können Sie sich in neue Systeme, wie z. B. Battery-Management-Systeme (BMS), einarbeiten?**
Ich habe in der Vergangenheit gezeigt, dass ich mich in neue Systeme schnell und effektiv einarbeiten kann. Mein Ansatz ist strukturiert:

1. **Theorie:** Einarbeitung in relevante technische Dokumentationen und Standards, beispielsweise zur Funktion und Architektur von BMS.
2. **Praxis:** Hands-on-Tests in der Testumgebung oder Simulation, um praktische Einblicke zu gewinnen.
3. **Austausch:** Aktiver Austausch mit Experten und Teammitgliedern, um offene Fragen zu klären.

Ein Beispiel: In einem früheren Projekt musste ich kurzfristig ein Verständnis für FlexRay-Netzwerke entwickeln. Innerhalb von zwei Wochen konnte ich durch Literatur, Schulungen und Praxistests produktiv arbeiten.

---

## **6. Welche Erfahrungen haben Sie mit ISO 26262 oder anderen relevanten Standards?**
Ich habe umfangreiche Erfahrungen mit ISO 26262, insbesondere in den Bereichen:

- **Anforderungsanalyse:** Erstellen von Sicherheitskonzepten und Sicherheitszielen.
- **Testdurchführung:** Entwicklung und Validierung sicherheitskritischer Tests auf System- und Komponentenebene.
- **Funktionale Sicherheit:** Umsetzung von ASIL-relevanten Anforderungen in Testszenarien.
- **Dokumentation:** Rückverfolgbarkeit zwischen Anforderungen, Tests und Fehlerberichten.

Ein konkretes Beispiel ist die Implementierung eines ASIL-C-konformen Tests für ein Bremssystemsteuergerät. Dabei habe ich mithilfe von CAPL-Tests kritische Fehlerfälle simuliert und die Sicherheitsmechanismen evaluiert.

---

## **7. Welche Kompetenzen sind Ihnen für diese Rolle besonders wichtig?**
Die Schlüsselkompetenzen für diese Rolle sind meiner Meinung nach:

1. **Technische Expertise:** Fundierte Kenntnisse in Testmethoden, HiL-Testing und relevanten Tools wie CANoe und CAPL.
2. **Analytische Fähigkeiten:** Systematische Fehlersuche und Problemlösung.
3. **Flexibilität:** Schnelle Einarbeitung in neue Themen wie BMS.
4. **Teamfähigkeit:** Zusammenarbeit mit interdisziplinären Teams.
5. **Normenkonformität:** Verständnis und Umsetzung von Standards wie ISO 26262.
