# Design

Hand calcs, Python cross-checks ([`calcs/`](../calcs/)), and LTspice results ([`sim/`](../sim/)). Each key number shows every method side by side, in separate columns. Python values come from running the script, and LTspice values from the simulation. Measured values go in [test-log.md](test-log.md), not here.

## Phase 1 gate calculations

Each one is done by hand and in Python. See [scope.md](scope.md#phase-1-theory-sep-28--oct-11).

Common inputs unless a section says otherwise: VIN 19.5 V; IOUT 3 A (T2); high-side Rds(on) 80 mΩ typ; switching frequency 456 / 570 / 684 kHz min / typ / max; minimum on-time 130 ns max; current-limit threshold 3.5 A min (all from the [TPS54331 datasheet](https://www.ti.com/lit/ds/symlink/tps54331.pdf), SLVS839H). Catch-diode drop VD 0.5 V is **assumed** until the diode is picked (Q6). Inductor resistance is neglected until the inductor is picked. Hand values are as written on paper; Python values are printed by the named script.

### Duty cycle across the T1 range

Volt-second balance on the inductor, with V_on = VIN − I·Rds − VOUT and V_off = −VD − VOUT:

D = (VOUT + VD) / (VIN − I·Rds + VD)

| VOUT | Ideal D (VOUT/VIN), hand | D with drops, hand | D with drops, Python ([duty_cycle.py](../calcs/duty_cycle.py)) |
|---|---|---|---|
| 1 V | 0.05128 | 0.07591 | 0.0759109 |
| 1.5 V | | | 0.1012146 |
| 3.3 V | 0.16923 | 0.19231 | 0.1923077 |
| 5 V | 0.2564 | 0.27834 | 0.2783401 |
| 12 V | 0.61538 | | 0.6325911 |
| 15 V | 0.76923 | | 0.7844130 |

- The chip's smallest duty is 130 ns × 684 kHz = 0.0889 (hand; Python 0.08892). 1 V at 3 A needs 0.0759, below that, so it is out of reach on a worst-case chip. This led to Q2 below.
- The largest duty, 0.784 at 15 V / 3 A, is under the 0.90 maximum duty.
- The first hand pass left VD out of the 12 V and 15 V numerators; Python caught it and the page was corrected.

### Inductor value (~30 % ripple current at the worst-case output voltage)

ΔI = (VIN − VOUT)·D / (f·L), with ideal D = VOUT/VIN. Required L = VOUT·(VIN − VOUT) / (ΔI·f·VIN). Peak current = IOUT + ΔI/2, checked against the 3.5 A minimum current limit (Q12).

- **Worst-case VOUT is 9.75 V** (VIN/2), where VOUT·(VIN − VOUT) is largest. Hand and Python ([inductor.py](../calcs/inductor.py), 0.05 V sweep from 1 V to 15 V) agree.
- **The slow chip (456 kHz) is the worst case** for ripple and peak. This is the datasheet's Eq. 9 approach (0.8 × typical frequency).
- Ripple target: 0.3 × 3 A = 0.9 A p-p.

All rows at VOUT 9.75 V, VIN 19.5 V, IOUT 3 A:

| Item | f | Hand | Python (inductor.py) |
|---|---|---|---|
| Required L for 0.9 A p-p | 570 kHz typ | rounded to 10 µH | 9.50 µH |
| 10 µH: ripple, peak | 570 kHz typ | 0.855 A p-p | 0.8553 A p-p, 3.4276 A peak |
| 10 µH: ripple, peak | 456 kHz min | 1.069 A p-p, 3.53 A peak | 1.0691 A p-p, 3.5345 A peak (over 3.5 A) |
| 15 µH: ripple, peak | 570 kHz typ | | 0.5702 A p-p, 3.2851 A peak |
| 15 µH: ripple, peak | 456 kHz min | 0.7127 A p-p, 3.356 A peak | 0.7127 A p-p, 3.3564 A peak |
| 15 µH at −20 % tolerance (12 µH): ripple, peak | 456 kHz min | | 0.8909 A p-p, 3.4454 A peak |

**Result: 15 µH** ([D10](decisions.md)). 10 µH peaks above the 3.5 A minimum current limit on a slow chip. 15 µH stays under it, even at −20 % tolerance (Python), though that corner leaves only about 0.05 A of margin. The real part's saturation rating is Q8.

### Output capacitance for T3

**Ripple (T3).** The capacitor carries the inductor's triangle ripple; the charge in each positive half is ΔI·T/8, plus the ESR drop:

ΔV ≈ ΔI / (8·f·C) + ΔI·ESR

Conditions: 15 µH, 456 kHz min, ESR 10 mΩ **assumed** (high side for ceramics), no DC-bias derating (Q7).

| Item | Hand | Python ([output_cap.py](../calcs/output_cap.py)) |
|---|---|---|
| Ripple current at 9.75 V (worst case) | 0.7127 A p-p | 0.7127 A p-p |
| Min C for 50 mV p-p at 9.75 V, no ESR budget | 3.9 µF | 3.91 µF |
| Min C for 50 mV p-p at 9.75 V, after the 7.13 mV ESR drop | | 4.56 µF |
| Chosen C | 4.7 µF (standard value) | |
| Ripple at 9.75 V / 3 A with 4.7 µF | | 48.70 mV p-p |
| Ripple current at 12 V | 0.67476 A p-p | 0.6748 A p-p |
| **T3 ripple at 12 V / 3 A with 4.7 µF** | **46.1 mV p-p** | **46.10 mV p-p** |

T3 is defined at 12 V, but ripple peaks at 9.75 V, so sizing used 9.75 V. Whether T3 should cover the full range is Q21.

**Load step (Q18).** Estimated with a rule of thumb, not a datasheet equation: dip ≈ ΔI_step / (2π·f_c·C), with ΔI_step 1.7 A (T7's 0.3 → 2 A), f_c 25 kHz (the datasheet's maximum crossover), and an allowed dip of 5 % of VOUT. Second check: datasheet Eq. 12, C_O(min) = 1 / (2π·R_O·f_CO(max)) with R_O = VOUT / 2 A. That's a stability minimum, not a dip estimate.

| Point | Allowed dip | C needed, hand (rule of thumb) | C needed, Python (rule of thumb) | Eq. 12 minimum, Python |
|---|---|---|---|---|
| 5 V (T7) | 250 mV | 43.3 µF | 43.3 µF | 2.55 µF |
| 1.5 V (T1 floor, T10) | 75 mV | | 144.3 µF | 8.49 µF |
| 1 V (former floor) | 50 mV | 216.45 µF | 216.5 µF | 12.73 µF |

**Result:** the load step sets the output capacitance, needing roughly 9× (5 V) to 31× (1.5 V) the 4.7 µF that ripple needs ([D14](decisions.md)). Both estimates assume 25 kHz crossover at every point; one fixed compensation network can't do that across the range (Q4). The real values come from Phase 2 simulation. The tension at the floor is Q23.

### IC and diode dissipation (12 V / 3 A and 3.3 V / 3 A)

IC loss from the datasheet's power-dissipation estimate (§8.2.2.11): P_con = I²·Rds·VOUT/VIN, P_sw = 0.5×10⁻⁹·VIN²·I·f, P_gc = 22.8×10⁻⁹·f, P_q = 0.11×10⁻³·VIN. Diode loss: P_D = VD·I·(1 − D), since the diode conducts during the off time.

Typical chip (570 kHz), Rds 80 mΩ typ:

| Point | IC total, hand | IC total, Python ([dissipation.py](../calcs/dissipation.py)) | Diode (ideal D), hand | Diode (ideal D), Python | Diode (D with drops), Python |
|---|---|---|---|---|---|
| 12 V / 3 A | 0.7833 W (P_con 0.443, P_sw 0.325, P_gc 0.01299, P_q 0.002) | 0.7833 W | 0.5769 W | 0.5769 W | 0.5511 W |
| 3.3 V / 3 A | 0.462 W (P_con 0.1218) | 0.4621 W | 1.246 W | 1.2462 W | 1.2115 W |
| 15 V / 3 A | 0.89 W | 0.8941 W | | | |
| 1.5 V / 3 A (floor) | | | | 1.3846 W | 1.3482 W |

Worst-case chip (684 kHz) for the IC: 0.96 W at 15 V / 3 A (hand; 0.9617 W unrounded), 0.9617 W (Python); 0.8510 W at 12 V / 3 A (Python).

- The IC runs hottest at high VOUT: the switch is closed for a larger share of each cycle, so P_con grows with VOUT/VIN. The diode runs hottest at low VOUT, where the switch is open most of the cycle and the diode carries the current.
- Ideal D slightly overstates diode loss compared with D with drops, so it's the conservative number.
- T9 tests 12 V and 3.3 V. Neither is the IC's hottest point (15 V) nor the diode's (the floor). See Q13.

### Q1: package choice (SOIC-8 D vs PowerPAD DDA junction temperature)

TJ = TA + RθJA·P_tot; case top ≈ TJ − ψJT·P_tot. From datasheet Table 6.4: RθJA 116.3 °C/W (D), 48.7 °C/W (DDA); ψJT 12.9 °C/W (D), 8.4 °C/W (DDA). TA 25 °C. These are TI's standard-test-board figures; this 2-layer board will differ, so T9's bench test is the real check.

At 15 V / 3 A, worst-case chip (684 kHz):

| Package | TJ, hand | Case, hand | TJ, Python | Case, Python |
|---|---|---|---|---|
| D (SOIC-8) | 136.848 °C | 124.44 °C | 136.85 °C | 124.44 °C |
| DDA (PowerPAD) | 71.75 °C | 63.67 °C | 71.84 °C | 63.76 °C |

The hand DDA lines used P_tot rounded to 0.96 W; the D lines and Python used 0.9617 W.

Python also covers T9's own points with DDA: case 59.29 °C at 12 V / 3 A (684 kHz) and 43.62 °C at 3.3 V / 3 A (570 kHz).

**Result: DDA** ([D12](decisions.md)). D's case is over T9's 85 °C limit, and its junction sits only about 13 °C under the 150 °C maximum at 25 °C ambient.

### Q2: output floor at 19.5 V in

Datasheet Eq. 33: VO(MIN) = 0.0889·(VIN(MAX) − IO(MIN)·Rds + VD) − IO(MIN)·RL − VD, where 0.0889 = 130 ns max on-time × 684 kHz max frequency. The worst corner is high VIN and light load: smaller drops mean the same minimum duty gives a higher VOUT. RL neglected.

| VIN | Load | Floor, hand | Floor, Python ([floor.py](../calcs/floor.py)) |
|---|---|---|---|
| 21 V (top of T5) | 0 A | 1.41178 V | 1.4118 V |
| 21 V | 3 A | 1.39 V | 1.3904 V |
| 19.5 V | 0 A | 1.2784 V | 1.2784 V |
| 19.5 V | 3 A | 1.2571 V | 1.2571 V |

**Result:** the floor a worst-case chip can guarantee is about 1.41 V, so T1's floor becomes 1.5 V ([D13](decisions.md)). At 0 A the converter is in discontinuous mode and pulse-skips, where Eq. 33 (a continuous-mode formula) is only approximate. Phase 2 simulation and the bench pin down the real floor.
