# OCV vs SOC for Chemistries

## Introduction

Batteries are a cornerstone of modern energy storage solutions, powering applications ranging from electric vehicles (EVs) to renewable energy systems and consumer electronics. Their operation is governed by complex electrochemical and physical principles, necessitating detailed study and precise management through Battery Management Systems (BMS). Key aspects like open circuit voltage (OCV), state of charge (SOC), and degradation trends are critical for designing efficient, reliable systems.

This document delves into the relationship between OCV and SOC across different chemistries, the impact of temperature, aging mechanisms, and degradation trends. It also discusses hysteresis effects, internal resistance, and their implications for BMS design.

---

## Open Circuit Voltage (OCV) and State of Charge (SOC)

The relationship between OCV and SOC is fundamental to battery management. It forms the basis for determining a battery’s remaining capacity and helps optimize its performance. OCV is defined as the voltage of a battery when it is not under load, while SOC represents the percentage of remaining charge relative to the battery’s maximum capacity.

For most lithium-ion chemistries, the OCV-SOC curve provides a reliable method for estimating SOC. However, this relationship varies significantly with the type of battery chemistry. Chemistries such as Lithium Nickel Manganese Cobalt Oxide (NMC) and Lithium Cobalt Oxide (LCO) exhibit a relatively consistent curve with a gradual slope, making SOC estimation straightforward. On the other hand, Lithium Iron Phosphate (LFP) batteries have a unique flat OCV-SOC profile, where voltage changes minimally over a broad SOC range. This characteristic complicates SOC estimation and demands sophisticated algorithms in the BMS.

Temperature significantly influences OCV-SOC characteristics. At higher temperatures, OCV decreases more gradually for a given SOC, causing the entire curve to shift downward. This effect must be accounted for in BMS algorithms to ensure accurate SOC estimation under varying environmental conditions. Accurate modeling of this behavior is vital for robust battery system design.

---

## Battery Chemistries and Their Characteristics

Battery performance and management requirements are heavily influenced by the specific chemistry. Among the commonly used lithium-ion chemistries, NMC and NCA (Nickel Cobalt Aluminum Oxide) are notable for their high energy density and consistent OCV-SOC relationship. These chemistries are widely adopted in electric vehicles due to their favorable energy-to-weight ratio and manageable thermal properties.

LFP batteries, despite their lower energy density, are valued for their superior thermal stability and extended cycle life. However, their flat OCV-SOC curve poses a unique challenge for SOC estimation. To accurately predict the SOC of LFP batteries, BMS algorithms must rely on additional parameters such as coulomb counting or temperature-adjusted voltage references.

Other chemistries like Lithium Manganese Oxide (LMO) and Lithium Cobalt Oxide (LCO) are employed in specific applications such as power tools and consumer electronics. Each chemistry requires tailored management strategies to optimize performance, ensure safety, and prolong life.

---

## Battery Aging and Degradation

Battery aging refers to the gradual decline in performance over time, manifesting as capacity loss, power fade, and increased resistance. Aging mechanisms are categorized as either calendar aging, which occurs due to chemical reactions over time, or cyclic aging, caused by repeated charge and discharge cycles.

### Capacity Degradation

Capacity degradation is the reduction in the maximum charge a battery can store. This process follows a characteristic pattern across all lithium-ion chemistries. Initially, there is a slight but rapid capacity drop following the manufacturing process. This is followed by a long period of relatively linear degradation during regular use. Eventually, the degradation rate accelerates, leading to a sharp decline in capacity, often referred to as the “final drop” phase.

The 80% threshold is critical in electric vehicle applications. Once a battery's capacity falls below 80% of its original value, it is deemed unsuitable for further use in EVs due to the increased risk of rapid performance decline. This threshold is determined by the steep acceleration in capacity loss beyond this point.

### Power Fade

Power fade, distinct from capacity degradation, refers to the battery's reduced ability to deliver current at a given voltage. This phenomenon is particularly prominent in two-wheelers and small-capacity applications. Over time, the internal resistance of the battery increases, leading to a drop in the voltage available for discharge. Consequently, the vehicle's performance, such as acceleration or maximum speed, deteriorates even if the total range remains unaffected.

---

## Hysteresis Effects

Hysteresis in batteries describes the difference between the voltage profiles during charging and discharging. This effect arises due to the chemical and structural changes within the electrodes during operation. Although hysteresis is negligible in high-voltage systems like electric vehicles, it becomes significant in low-voltage applications such as mobile phones and laptops.

In these systems, even minor differences in the voltage profiles can lead to inaccuracies in SOC estimation. To address this, BMS algorithms are designed to follow separate voltage profiles for charging and discharging, ensuring accurate tracking despite the hysteresis effect.

---

## Degradation Mechanisms

Battery degradation is influenced by various factors, including temperature, usage patterns, and internal resistance. Internal resistance increases with age, impacting both voltage and SOC. This non-linear behavior is critical to understand, as it affects power delivery and efficiency.

Temperature also plays a pivotal role in degradation. Prolonged exposure to high temperatures accelerates chemical reactions that degrade the electrodes and electrolyte. Similarly, extreme cycling conditions exacerbate wear and tear on the battery components, shortening its operational lifespan.

---

## Conclusion

Battery systems are complex, requiring detailed understanding and precise management to optimize performance and longevity. By understanding the relationships between OCV, SOC, temperature, and aging, engineers can design effective BMS algorithms tailored to specific applications. The interplay of these factors, coupled with advancements in battery chemistry and modeling, will continue to enhance the reliability and efficiency of modern battery systems.

---

## Appendix: Key Parameters
| **Parameter**         | **Definition**                                           |
|------------------------|---------------------------------------------------------|
| OCV                   | Open Circuit Voltage                                    |
| SOC                   | State of Charge                                         |
| Hysteresis            | Voltage difference during charge/discharge cycles       |
| Capacity Degradation  | Loss of maximum charge capacity                         |
| Power Fade            | Reduction in power delivery capability                  |


