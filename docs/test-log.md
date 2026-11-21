# Test log

This file is the only home of measured values. Targets and conditions are defined in [scope.md](scope.md#target-spec-provisional-until-the-phase-2-gate).

## Values ledger

One row per target. Hand-calc, Python, LTspice, and measured values each keep their own column, and one never overwrites another. Every cell names its statistic and conditions (for example, "28 mV p-p, 20 MHz BW limit, 12 V / 3 A out, ground-spring probe"). Measured values carry a board ID (`r1-u1` = rev 1, unit 1). Data from a board with a known defect is marked **quarantined** and excluded from pass/fail.

| ID | Target | Hand calc | Python | LTspice | Measured | Board ID | Status |
|---|---|---|---|---|---|---|---|
| T1 | Output range 1.5 V to 15 V, VIN 19.5 V | worst-case floor 1.41178 V (datasheet Eq. 33, VIN 21 V, 0 A, VD 0.5 V assumed) | worst-case floor 1.4118 V (same conditions, floor.py); D 0.7844130 at 15 V / 3 A, under 0.90 max (duty_cycle.py) | | | | |
| T2 | Output current 3 A continuous, across T1, within T9 | peak inductor current 3.356 A, under the 3.5 A min current limit (15 µH, 9.75 V out, 456 kHz) | peak 3.3564 A (same conditions); 3.4454 A at 12 µH, −20 % tolerance (inductor.py) | | | | |
| T3 | Output ripple < 50 mV p-p, 12 V / 3 A, 20 MHz BW limit, ground-spring probe at output cap | 46.1 mV p-p (12 V / 3 A, 4.7 µF, 15 µH, 456 kHz, ESR 10 mΩ assumed, no DC-bias derating) | 46.10 mV p-p (same conditions, output_cap.py) | | | | |
| T4 | Load regulation ΔVOUT (DC mean) ≤ 2 % of setpoint, 0.3 → 3 A, at 5 V and 12 V | | | | | | |
| T5 | Line regulation ΔVOUT (DC mean) ≤ 1 % of setpoint, VIN 17 → 21 V, 12 V / 1.5 A | | | | | | |
| T6 | Efficiency > 85 %, 12 V / 1.5 A (also log 0.5, 1, 2, 3 A) | | | | | | |
| T7 | Load step 0.3 → 2 A at 5 V: peak deviation ≤ 5 %, recovery ≤ 200 µs, no sustained ringing | | | | | | |
| T8 | Startup overshoot peak ≤ 5 % above setpoint, power-up into no load | | | | | | |
| T9 | Every part < 85 °C case, 10 min at 12 V / 3 A and at 3.3 V / 3 A, room ambient | IC case estimate 63.67 °C (DDA, 15 V / 3 A, 684 kHz, TA 25 °C, datasheet ψJT) | IC case estimate, DDA, TA 25 °C: 59.29 °C at 12 V / 3 A (684 kHz), 43.62 °C at 3.3 V / 3 A (570 kHz), 63.76 °C at 15 V / 3 A (684 kHz) (dissipation.py); diode not estimated until the part is picked | | | | |
| T10 | T7 criteria met at the output floor, 5 V, 12 V, 15 V | | | | | | |

## Bench sessions

Dated notes, newest last. Each session lists the date, board ID, equipment, setup, and results, with captures saved to [`media/`](../media/).
