# Wissensbasierte und knifflige Fragen

---

## **1. Grundlagen- und Fachwissen**

### **ISO 26262 und Funktionale Sicherheit**
1. Was sind die wichtigsten Anforderungen der ISO 26262 im Zusammenhang mit Softwaretests?
2. Wie unterscheidet sich ein sicherheitskritischer Test (z. B. ASIL-D) von einem Standardtest?  
3. Wie validieren Sie Sicherheitsmechanismen wie Watchdogs oder CRC-Prüfungen?

### **HiL-Testing**
4. Wie simulieren Sie ein Steuergerät-Timeout an einem HiL-System? 
5. Welche Vorteile bietet ein HiL-Test gegenüber einem realen Fahrzeugtest? 
6. Wie würden Sie testen, ob ein Steuergerät korrekt auf Busfehler (z. B. CAN-Error-Frames) reagiert?

### **Vector Tools**
7. Wie würden Sie in CANoe einen Testfall für eine Gateway-Funktion erstellen, die Nachrichten von CAN nach LIN weiterleitet?  
8. Wie gehen Sie vor, wenn CANape während der Kalibrierung unerwartet keine Verbindung zum Steuergerät aufbauen kann?

### **ECU-Test**
9. Welche Arten von Testfällen können mit ECU-Test automatisiert werden?  
10. Wie debuggen Sie ein fehlschlagendes Testskript in ECU-Test?  

### **BMS-spezifisches Wissen**
11. Wie überwacht ein BMS das Gleichgewicht (Balancing) der Zellen, und warum ist dies wichtig?  
12. Wie würden Sie die Funktionalität eines Tiefentladungsschutzes testen?

---

## **2. Testmethoden und Strategien**
### **Testkonzepte**
13. Welche Schritte führen Sie aus, um ein Testkonzept für ein neues Steuergerät zu erstellen?  
14. Wie stellen Sie sicher, dass ein Testkonzept vollständig ist und alle Anforderungen abdeckt?

### **Fehleranalyse**
15. Ein Fehler tritt nur sporadisch auf und ist schwer reproduzierbar. Wie würden Sie vorgehen, um diesen zu analysieren?  
16. Welche Tools oder Techniken verwenden Sie, um Protokolldaten aus einem HiL-Test effizient auszuwerten?

### **Black-Box-Testing**
17. Sie kennen die interne Logik eines Steuergeräts nicht. Wie würden Sie sicherstellen, dass Ihr Testfall die Anforderungen abdeckt?  
18. Welche Herausforderungen gibt es beim Black-Box-Testen sicherheitskritischer Systeme?

---

## **3. Knifflige Szenarien**
### **Edge Cases und Fehlerfälle**
19. Sie testen ein Steuergerät, das bei einem Spannungsausfall korrekt herunterfahren soll. Wie würden Sie diesen Test am HiL umsetzen?  
20. Wie testen Sie, ob das Steuergerät auf ein fehlerhaftes Signal korrekt reagiert (z. B. ein unsinniger Temperaturwert von -100°C)?

### **Timing und Performance**
21. Wie prüfen Sie, ob ein Steuergerät alle CAN-Nachrichten innerhalb der spezifizierten Zeit versendet?  
22. Sie stellen fest, dass ein Steuergerät gelegentlich Nachrichten doppelt sendet. Wie gehen Sie vor, um die Ursache zu identifizieren?

### **Fehler beim Testen selbst**
23. Was machen Sie, wenn Sie feststellen, dass der Test selbst fehlerhaft ist? (z. B. ein falscher Prüfalgorithmus im Testskript)
24. Wie stellen Sie sicher, dass die Ergebnisse eines automatisierten Tests zuverlässig sind?

---

## **4. Prozess- und Soft-Skill-Fragen**
### **Testplanung**
25. Ein Projekt hat plötzlich eine Änderung im Lieferzeitpunkt. Wie priorisieren Sie Ihre Tests, um die wichtigsten Punkte termingerecht zu liefern?  
26. Wie gehen Sie vor, wenn eine Anforderung unklar formuliert ist, aber ein Testkonzept erstellt werden muss?

### **Teamarbeit und Kommunikation**
27. Ein Entwickler behauptet, dass der von Ihnen gefundene Fehler kein Softwareproblem ist. Wie klären Sie das?  
28. Sie haben begrenzte Ressourcen (z. B. nur ein HiL-System für mehrere Tester). Wie planen Sie Ihre Tests, um alle Anforderungen zu erfüllen?

---

## **5. Theoretische Fragen zu Technologien**
### **CAN-Bus und Kommunikation**
29. Was ist der Unterschied zwischen einer Standard-CAN-ID und einer Extended-CAN-ID?  
30. Wie erkennen Sie eine Busüberlastung (Bus-Off), und welche Auswirkungen hat dies auf das Steuergerät?

### **Diagnose (UDS/OBD)**
31. Was ist der Unterschied zwischen einem OBD-Fehlercode (DTC) und einem herstellerspezifischen DTC?  
32. Wie testen Sie die Implementierung eines Diagnose-Service, z. B. "Read DTCs"?

### **Energie- und Batteriemanagement**
33. Was passiert, wenn ein BMS-Temperatursensor falsche Werte liefert? Wie könnten Sie das testen?  
34. Welche Rolle spielt der SoC (State of Charge) in einem BMS, und wie würden Sie ihn verifizieren?

---

Diese Fragen sind darauf ausgelegt, Ihr Fachwissen, Ihre Problemlösungsfähigkeiten und Ihre Fähigkeit zur praktischen Anwendung von Wissen zu testen. Eine strukturierte und präzise Beantwortung wird hier entscheidend sein. Möchten Sie Beispielantworten für einige der kniffligeren Fragen?