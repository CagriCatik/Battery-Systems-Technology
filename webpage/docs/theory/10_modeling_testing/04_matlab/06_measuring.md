# Structural Code Coverage & MC/DC Analysis in Simulink

In the safety certification of automotive Battery Management Systems, showing that a test suite passes is only half the requirement. Under **ISO 26262 Part 6 Table 12**, engineering teams must mathematically prove that the test suite thoroughly exercises the internal structure of the software[^iso26262]. For **ASIL-D** applications, achieving **$100\%$ Modified Condition / Decision Coverage (MC/DC)** is strictly mandatory[^hayhurst2001].

**Simulink Coverage** measures structural test coverage directly on Simulink models, Stateflow state charts, and auto-generated C/C++ code. When coverage gaps occur, **Simulink Design Verifier (SLDV)** uses formal mathematical proof engines to synthesize missing test vectors or prove code deadness[^mathworks_cov2021].

This chapter formalizes the metrics of structural coverage, in-model visual diagnostics, and automated test vector generation with SLDV.

---

## The Hierarchy of Structural Coverage Metrics

ISO 26262-6 defines five distinct structural coverage metrics evaluated during Software-in-the-Loop (SIL) and Model-in-the-Loop (MIL) testing:

```mermaid
flowchart TD
    Metrics["Structural Coverage Hierarchy (ISO 26262-6)"]
    
    Metrics --> M1["1. Execution / Statement Coverage<br/>Every Simulink block and C line executed at least once."]
    Metrics --> M2["2. Decision Coverage (DC)<br/>Every decision branch (True/False) taken at least once."]
    Metrics --> M3["3. Condition Coverage (CC)<br/>Every atomic boolean condition evaluated to True and False."]
    Metrics --> M4["4. Modified Condition / Decision Coverage (MC/DC)<br/>Each condition independently flips the decision outcome."]
    Metrics --> M5["5. Lookup Table & Stateflow Coverage<br/>Every breakpoint interval exercised; all state transitions taken."]
```

### Automotive Safety Integrity Level (ASIL) Recommendations

| Structural Coverage Metric | ASIL-A | ASIL-B | ASIL-C | ASIL-D |
| :--- | :--- | :--- | :--- | :--- |
| **Statement Coverage** | ++ (Highly Rec.) | ++ | ++ | ++ |
| **Branch / Decision Coverage** | + (Recommended) | ++ | ++ | ++ |
| **Modified Condition / Decision Coverage (MC/DC)** | o (Optional) | + | ++ | **++ (Mandatory)** |

---

## Visual Coverage Diagnostics in the Simulink Canvas

When test suites complete execution in Simulink Test, **Simulink Coverage** overlays interactive color-coded visual diagnostics directly on the model canvas[^mathworks_cov2021]:

```
+-------------------------------------------------------------------------------+
| Simulink Coverage Inspector: BMS_Safety_Logic.slx                             |
|                                                                               |
| [ GREEN BLOCK ]  Overvoltage_Comparator: 100% Decision (True: 512, False: 12) |
|                                                                               |
| [ YELLOW BLOCK ] Overtemp_AND_Overcurrent: 75% MC/DC                          |
|                  Expression: (T_cell > 60.0) && (I_pack > 100.0)              |
|                  > Condition 1 (T_cell > 60.0): Fully Covered                 |
|                  > Condition 2 (I_pack > 100.0): False->True Not Observed     |
|                                                                               |
| [ RED BLOCK ]    Unreachable_Fallback_SafeState: 0% Execution (Dead Logic!)   |
+-------------------------------------------------------------------------------+
```

- **Green:** $100\%$ covered across all active metrics (Statement, Decision, MC/DC).
- **Yellow:** Partially covered. The decision was evaluated in one direction, but the alternate branch or an atomic independence condition was never exercised by the test stimuli.
- **Red:** $0\%$ execution. Identifies dead logic or completely untested safety branches.

---

## Resolving Coverage Gaps: Formal Test Synthesis via SLDV

When structural coverage falls below $100\%$, ISO 26262 mandates that the gap must be resolved using a structured engineering workflow[^iso26262]:

```mermaid
flowchart TD
    Gap["Coverage Gap Identified in Simulink Coverage (e.g., 94% MC/DC)"] --> Analysis{"Analyze Uncovered Construct"}
    
    Analysis --> Case1["Case A: Missing Test Scenario<br/>(Algorithmic branch reachable, but test suite omitted it)"]
    Analysis --> Case2["Case B: Unintended / Dead Logic<br/>(Logic can never physically execute under any inputs)"]
    Analysis --> Case3["Case C: Defensive Programming<br/>(Safe fallback for hardware traps that cannot occur in MIL)"]

    Case1 --> SLDV["Run Simulink Design Verifier (SLDV)<br/>Formal solver synthesizes exact test vectors to hit branch"]
    Case2 --> Refactor["Refactor & Remove Dead Blocks from Model"]
    Case3 --> Waiver["Document Formal Safety Waiver / Justification in Safety Case"]

    SLDV --> Merge["Merge Synthesized Test Vectors into Test Manager"]
    Merge --> Target["Achieve 100% MC/DC Target Baseline"]
    Refactor --> Target
    Waiver --> Target
```

### Automated Test Generation with Simulink Design Verifier (SLDV)

**Simulink Design Verifier (SLDV)** uses formal methods (Satisfiability Modulo Theories, SMT solvers, and model checking) to inspect the mathematical state-space of the model:
1. It analyzes the uncovered condition (e.g., Condition 2 in `(T_cell > 60.0) && (I_pack > 100.0)`).
2. It solves for the exact mathematical input vector sequence $[V(t), I(t), T(t)]$ required to force Condition 2 to independently flip the decision outcome.
3. If the solver proves that no mathematical input combination can ever execute the branch, it outputs an **Unsatisfiable / Dead Code Proof**, enabling engineers to safely remove the dead block.
4. If reachable, SLDV exports the synthesized test vectors directly as `.mat` files into the Simulink Test Manager, elevating coverage to **$100\%$ automatically**[^mathworks_cov2021].

---

## References

[^iso26262]: International Organization for Standardization. (2018). *ISO 26262-6: Road vehicles — Functional safety — Part 6: Product development at the software level*. ISO.
[^hayhurst2001]: Hayhurst, K. J., et al. (2001). *A Practical Tutorial on Modified Condition/Decision Coverage*. NASA/TM-2001-210876.
[^mathworks_cov2021]: The MathWorks Inc. (2021). *Simulink Coverage: Measure test completeness in models and generated code*. MathWorks.
