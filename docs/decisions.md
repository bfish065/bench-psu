# Decisions

Append-only log. Each entry gives the date, the decision, why, and what was rejected. To change a decision, add a new entry that supersedes the old one and mark the old one *Superseded by D#*. Never edit or delete an entry.

Open questions (Q#) live in [scope.md](scope.md#open-questions) until they're answered here.

---

### D1 · 2026-09-22 · Project

Build an adjustable buck bench supply.

- *Why:* exercises analog circuit analysis end to end: design, simulation, layout, measurement.
- *Rejected:* none recorded.

### D2 · 2026-09-22 · Input

19–20 V laptop brick.

- *Why:* a first power-electronics project stays low-voltage DC.
- *Rejected:* mains input.

### D3 · 2026-09-22 · Controller

TI TPS54331. Package still open (Q1).

- *Why:* 3 A / 28 V, cheap, and external compensation forces learning the loop.
- *Rejected:* none recorded.

### D4 · 2026-09-22 · Simulation

Ideal-switch buck in LTspice, plus a part-specific check in TI WEBENCH or PSpice for TI.

- *Why:* LTspice doesn't ship TI models, and the generic model teaches the physics.
- *Rejected:* none recorded.

### D5 · 2026-09-22 · Practice board

Build a practice board before the main board.

- *Why:* catches footprint and ordering mistakes cheaply.
- *Rejected:* none recorded.

### D6 · 2026-09-22 · Pot placement

Put the pot on the PCB, with its shaft through the panel.

- *Why:* the feedback node is high-impedance and noise-sensitive.
- *Rejected:* a panel pot wired back to the board.

### D7 · 2026-09-22 · Compensation

Use the datasheet procedure; deep loop theory optional.

- *Why:* control theory not yet taken.
- *Rejected:* none recorded.

### D8 · 2026-09-22 · Output floor

*Superseded by D13.*

Revise the output floor from 0.8 V to ~1 V, pending Q2.

- *Why:* minimum on-time at 19.5 V in.
- *Rejected:* 0.8 V floor (the reference voltage).

### D9 · 2026-09-22 · Rev 2

Plan for a rev 2 from the start.

- *Why:* first boards usually need a fix.
- *Rejected:* none recorded.

### D10 · 2026-11-21 · Inductor value

15 µH. Answers Q12.

- *Why:* at the worst-case output (9.75 V) on a slow chip (456 kHz), 10 µH ripples 1.069 A p-p and peaks at 3.53 A, over the 3.5 A minimum current limit (hand calc). 15 µH ripples 0.7127 A p-p and peaks at 3.356 A (hand calc). Python agrees, and puts the −20 % corner (12 µH) at 3.4454 A, still under 3.5 A. See [design.md](design.md#inductor-value-30--ripple-current-at-the-worst-case-output-voltage).
- *Rejected:* 10 µH (peak over the limit on a slow chip); derating T2 below 3 A.

### D11 · 2026-11-21 · Python cross-checks

Claude writes and runs the `calcs/` scripts. Each script mirrors the hand formulas, and Fish checks its output against the paper.

- *Why:* keeps the Phase 1 rule of every key number by hand and in Python. Python already caught a real hand slip (the duty-cycle numerator).
- *Rejected:* dropping Python from the gate; Fish writing every script from scratch.

### D12 · 2026-11-21 · IC package

PowerPAD (DDA). Answers Q1.

- *Why:* at 15 V / 3 A on a worst-case chip (684 kHz), the SOIC-8's case reaches 124.44 °C, over T9's 85 °C limit, while the DDA's reaches 63.67 °C (hand calc, TA 25 °C, datasheet Table 6.4 thermal figures). See [design.md](design.md#q1-package-choice-soic-8-d-vs-powerpad-dda-junction-temperature).
- *Rejected:* SOIC-8 (D). It's easier to hand-solder, but it fails T9 and leaves only about 13 °C of junction margin at 25 °C ambient.
- *Cost:* the thermal pad must be soldered (hot air, or a via under the pad soldered from the back), and the layout needs copper and vias under it.

### D13 · 2026-11-21 · Output floor

T1's floor is 1.5 V. Answers Q2; supersedes D8.

- *Why:* datasheet Eq. 33 puts the worst-case floor at 1.41 V (21 V in, 0 A, VD 0.5 V assumed; hand and Python). 1.5 V adds margin for the assumed input and diode drop. See [design.md](design.md#q2-output-floor-at-195-v-in).
- *Rejected:* 1.4 V (no margin); keeping ~1 V as a typical-only value (not guaranteed on every chip).

### D14 · 2026-11-21 · Output capacitance

Size the output capacitance for the load step, not for ripple. Answers Q18.

- *Why:* 4.7 µF meets T3 (46.1 mV p-p at 12 V / 3 A, hand calc), but T7's 5 % dip needs about 43 µF at 5 V and about 144 µF at the 1.5 V floor (rule-of-thumb estimate, 25 kHz crossover; Python). Final values come from Phase 2 simulation.
- *Rejected:* sizing for T3 ripple alone (4.7 µF).

### D15 · 2026-11-21 · Lab access

Lab access confirmed. Answers Q11.

- *Why:* Fish has access to the lab's bench equipment for Phase 6.
- *Rejected:* none recorded.

### D16 · 2026-11-21 · Revised schedule

Reschedule Phases 2–6 and the practice board: Phase 2 Nov 22 – Dec 6; practice board ordered by Dec 6; finals pause about Dec 7 – 18; Phase 3 Dec 19 – 31; Phase 4 Jan 1 – 14, 2027, boards and parts ordered by Jan 14; Phase 5 about Jan 25 – Feb 7; Phase 6 Feb 8 – 28. Still about 3–4 hours a week.

- *Why:* Phase 1 passed 2026-11-21, about six weeks after its Oct 11 date, so the Nov 13 board-order deadline had already passed. Schematic and layout move into winter break, and bring-up moves after it.
- *Rejected:* keeping the old dates (already past).
