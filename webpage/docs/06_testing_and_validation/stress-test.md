# StressTests

Die Implementierung eines **Stresstests mit CAPL** ist ein effektiver Ansatz, um sporadische Kommunikationsabbrüche in einem elektronischen Lenksystem zu untersuchen. Hier ist eine strukturierte Beschreibung, wie ein solcher Test umgesetzt werden kann:

---

### **1. Testanforderungen definieren**
- Ziel: Reproduzieren und Identifizieren von Kommunikationsabbrüchen.
- Umfang:
  - Belastung der CAN-Kommunikation durch hohe Datenlast und sporadische Nachrichtenmuster.
  - Beobachtung der Reaktion des Systems unter stressigen Bedingungen.

---

### **2. Testumgebung vorbereiten**
- **Hardware**: HiL-System, Steuergerät (ECU), CAN-Bus mit notwendiger Peripherie.
- **Software**: CAPL-Skript für CANalyzer oder CANoe.
- Sicherstellen, dass:
  - Die Kommunikationsschnittstellen überwacht werden können.
  - Log-Daten erfasst und gespeichert werden.
  - Fehlerdetektionsmechanismen wie ACK-Fehler, Bus-Off-Zustände oder Frame-Drops aktiviert sind.

---

### **3. CAPL-Skript für Stresstest entwickeln**

#### **Schritte im Skript:**
1. **Initialisierung**: 
   - Definiere CAN-Kanäle, zu testende Nachrichten und Prioritäten.
   - Initialisiere Timer für zeitgesteuerte Nachrichtenübertragung.

   ```capl
   variables {
       message 0x100 msgHighPriority;
       message 0x200 msgLowPriority;
       timer stressTimer;
   }

   on start {
       setTimer(stressTimer, 10); // Starte den Timer für Stress-Simulation.
   }
   ```

2. **Stress-Szenarien erzeugen**:
   - Sende Nachrichten mit hoher Frequenz.
   - Variiere Botschaftsintervallen (z. B. von 1 ms bis 100 ms).
   - Integriere zufällige Dateninhalte, um die Datenlast zu erhöhen.

   ```capl
   on timer stressTimer {
       // Sende Nachrichten mit hoher Frequenz
       msgHighPriority.Data[0] = rand(0, 255); // Zufallsdaten
       output(msgHighPriority);
       
       msgLowPriority.Data[0] = rand(0, 255); 
       output(msgLowPriority);
       
       setTimer(stressTimer, 1 + rand(0, 10)); // Zufällige Zeitintervalle
   }
   ```

3. **Fehler provozieren**:
   - Simuliere Bus-Störungen (z. B. Bus-Off-Szenarien).
   - Teste Grenzbedingungen wie vollständige Busüberlastung.

   ```capl
   on key 'F1' { // Manuelle Störung aktivieren
       output(msgHighPriority); 
       overload(10); // Simuliere hohe Last für 10 ms
   }
   ```

4. **Loggen von Daten und Fehlern**:
   - Erfasse CAN-Fehler wie Frame-Drops, ACK-Fehler oder Bus-Off-Zustände.
   - Log-Daten speichern und mit Zeitstempeln versehen.

   ```capl
   on busError {
       write("BusError: %d", this.errorCode);
   }
   ```

---

### **4. Durchführung des Tests**
- Test mit verschiedenen Konfigurationen wiederholen:
  - Unterschiedliche Nachrichtenprioritäten.
  - Variierende Buslast (50 %, 80 %, 100 %).
- Simuliere reale Fahrsituationen, um zu prüfen, ob Fehler reproduziert werden können.

---

### **5. Analyse und Korrelation**
- **Logs analysieren**: Fehler und Zeitstempel mit Testprotokollen korrelieren.
- **Fehlerursache eingrenzen**: 
  - Identifiziere, welche Nachricht (ID, Frequenz, Priorität) zu den Kommunikationsabbrüchen führt.
  - Prüfe Timer-Synchronisation oder andere softwarebedingte Fehlerquellen.

---

### **6. Optimierung und Fehlerbehebung**
- Auf Basis der Testergebnisse:
  - Software-Updates einspielen (z. B. Timer-Interrupt-Synchronisation anpassen).
  - Systemintegrität durch erneute Tests validieren.

---

### **Ergebnis**
- Erfolgreiche Reproduktion der sporadischen Fehler.
- Optimiertes CAPL-Testkonzept, das als Basis für ähnliche Projekte dient.

Dieses Vorgehen zeigt ein systematisches und strukturiertes Vorgehen bei der Implementierung von Stresstests, das zuverlässig sporadische Fehler aufdecken kann.

Hier ist ein vollständiges Beispiel für ein **CAPL-Skript**, das einen **Stresstest für ein elektronisches Lenksystem** implementiert. Dieses Skript simuliert eine hohe CAN-Buslast, zufällige Nachrichtenintervalle und loggt auftretende Fehler:

### **Vollständiger CAPL-Code**
```capl
/* Stresstest für CAN-Kommunikation
   Ziel: Sporadische Kommunikationsabbrüche reproduzieren */

variables {
    // Definiere Nachrichten (IDs und Daten)
    message 0x100 msgHighPriority;  // Hohe Priorität
    message 0x200 msgLowPriority;   // Niedrige Priorität

    timer stressTimer;              // Timer für Stress-Simulation
    timer errorInjectionTimer;      // Timer für Fehlersimulation
    int overloadCounter = 0;        // Zähler für Overload-Simulation
}

// Initialisierung beim Start des Skripts
on start {
    // Initialisiere Nachrichten-Daten
    msgHighPriority.DataLength = 8; // Nachrichtenlänge 8 Bytes
    msgLowPriority.DataLength = 8;

    // Timer starten
    setTimer(stressTimer, 10);      // Start mit 10 ms Intervall
    write("Stresstest gestartet...");
}

// Haupttimer: Simuliert hohe Buslast mit zufälligen Daten
on timer stressTimer {
    // Zufallsdaten für Nachricht mit hoher Priorität
    msgHighPriority.Data[0] = rand(0, 255);
    msgHighPriority.Data[1] = rand(0, 255);
    msgHighPriority.Data[2] = rand(0, 255);
    msgHighPriority.Data[3] = rand(0, 255);
    output(msgHighPriority);

    // Zufallsdaten für Nachricht mit niedriger Priorität
    msgLowPriority.Data[0] = rand(0, 255);
    msgLowPriority.Data[1] = rand(0, 255);
    msgLowPriority.Data[2] = rand(0, 255);
    msgLowPriority.Data[3] = rand(0, 255);
    output(msgLowPriority);

    // Timer erneut setzen (zufälliges Intervall zwischen 1 ms und 10 ms)
    setTimer(stressTimer, 1 + rand(0, 10));
}

// Tastensteuerung: Manuelle Störung simulieren
on key 'F1' {
    write("Manuelle Überlastung aktiviert...");
    overloadCounter = 10;  // Simuliere 10 Zyklen hoher Buslast
    setTimer(errorInjectionTimer, 1);  // Timer für Fehler-Simulation
}

// Fehler-Simulation: Überlastung des Busses
on timer errorInjectionTimer {
    if (overloadCounter > 0) {
        msgHighPriority.Data[0] = rand(0, 255);
        output(msgHighPriority);  // Nachricht senden
        setTimer(errorInjectionTimer, 1);  // Nächstes Intervall (1 ms)
        overloadCounter--;
    } else {
        write("Manuelle Überlastung beendet.");
    }
}

// Fehlerbehandlung: Bus-Fehler loggen
on busError {
    write("Busfehler erkannt: ErrorCode=%d", this.errorCode);
}

// Aufzeichnung von CAN-Nachrichten
on message * {
    write("Empfangene Nachricht: ID=%x, Data=[%x %x %x %x %x %x %x %x]",
        this.id,
        this.data[0], this.data[1], this.data[2], this.data[3],
        this.data[4], this.data[5], this.data[6], this.data[7]);
}
```

---

### **Erläuterungen zum Code**

1. **Hauptfunktionen**:
   - **Stress-Simulation**: Der `stressTimer` erzeugt Nachrichten mit zufälligen Daten und zufälligen Intervallen, um den CAN-Bus zu belasten.
   - **Manuelle Überlastung**: Mit der `F1`-Taste wird eine simulierte Überlastung des Busses für 10 Zyklen ausgelöst.
   - **Fehlerprotokollierung**: `on busError` loggt auftretende Busfehler wie ACK-Fehler oder Bus-Off-Zustände.

2. **Variablen**:
   - Nachrichten (`message`) werden definiert, um gezielt hohe und niedrige Prioritäten zu testen.
   - Timer (`timer`) steuern zeitliche Abläufe für die Simulation.

3. **Logging**:
   - Nachrichten und Fehler werden in der CANoe-Konsole ausgegeben.

4. **Flexibilität**:
   - Die Intervalle und Datenmuster können leicht angepasst werden.
   - Die Fehlersimulation ist flexibel über die `F1`-Taste aktivierbar.

---

### **Erweiterungen**
- **Statistische Analyse**: Log-Dateien analysieren, um zeitliche Muster von Fehlern zu erkennen.
- **Automatische Trigger**: Simuliere zusätzliche Bedingungen (z. B. Bus-Auslastung über 90 %).

Dieses Skript bildet eine solide Grundlage für Stresstests und kann je nach Systemanforderungen erweitert werden.