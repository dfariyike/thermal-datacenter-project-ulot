# 42U High-Density Rack: Thermal Safety & Failure Audit
**Lead Engineer:** David Fariyike  
**Tools:** Simcenter FloTherm 2021, Python (Data Analysis), AWS (Cloud Infrastructure Context)

---

## Project Overview
This project involves a comprehensive thermal audit of a 42U server rack operating at a high power density of **12,758.6 W**. Using CFD (Computational Fluid Dynamics), I simulated steady-state performance and transient "cooling degradation" scenarios to determine the operational safety margins of critical IT infrastructure. The objective was to evaluate compliance with ASHRAE TC 9.9 (Class A1) standards and identify the **Time-to-Failure (TTF)** during a partial fan failure event.

## Key Engineering Findings
*   **Thermal Exceedance:** Even at 100% fan capacity, 100% of server inlets exceeded ASHRAE recommended limits, with a peak exceedance of ~1.6°C.
*   **Recirculation Risks:** Supply Heat Index (SHI) analysis confirmed moderate-to-high hot-air recirculation, driven by the high power dissipation overcoming local airflow.
*   **Critical Status:** The rack was assigned a **'Marginal'** status as steady-state temperatures exceeded ASHRAE Recommended limits, leaving insufficient thermal headroom to sustain 50% cooling failure transients.

## Methodology
1.  **Steady-State Baseline:** 
    *   **Configuration:** All internal fans set to 100% duty cycle.
    *   **Result:** Established the initial flow field and identified that the high density (~12.8 kW) creates localized hot spots despite maximum cooling.
2.  **Transient "Fan-Down" Analysis:** 
    *   **Scenario:** Initialized from the 100% steady-state results, the fans were dropped to a 50% failure state at $t = 0s$.
    *   **Goal:** Isolate the thermal "soak" and measure the speed of temperature rise at the top-tier inlets.
    *   **Numerical Stability:** To ensure accuracy, the model utilized a high-fidelity mesh with a 0.01s time step to resolve turbulent exhaust mixing.

## Repository Structure
*   **/visualizations:** Dashboard `index.html` and high-resolution thermal plots (Compliance, SHI, and TTF).
*   **/data:** CSV exports of transient monitor points (Temperature vs. Time).
*   **/scripts:** Python scripts used to calculate RCI (Rack Cooling Index) and SHI (Supply Heat Index).
*   **Note:** FloTherm source model files (`.pdml`/`.pack`) are excluded from this repository due to file size constraints.

## Professional Context
This audit bridges the gap between Mechanical/Thermal Engineering and System Administration. By quantifying how long a system can survive a cooling failure, I provide actionable data for:
*   Configuring automated hardware throttling thresholds.
*   Developing disaster recovery timelines for data center floor managers.
*   Optimizing Cloud Infrastructure layout for ASHRAE-certified environments.

## How to Use the Dashboard
1.  Clone the repository.
2.  Open `visualizations/index.html` in any modern browser to view the **Critical Infrastructure Thermal Audit** dashboard.
