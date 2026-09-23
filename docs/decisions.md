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

Revise the output floor from 0.8 V to ~1 V, pending Q2.

- *Why:* minimum on-time at 19.5 V in.
- *Rejected:* 0.8 V floor (the reference voltage).

### D9 · 2026-09-22 · Rev 2

Plan for a rev 2 from the start.

- *Why:* first boards usually need a fix.
- *Rejected:* none recorded.
