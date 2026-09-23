# Scope: adjustable bench power supply (TPS54331 buck)

*Status: Phase 1 (theory) · Last updated 2026-09-22*

## Goal

Design, lay out, build, and characterize a single-channel adjustable bench supply: a non-synchronous buck converter on a custom 2-layer PCB, fed by a 19–20 V laptop brick. Done means a working supply plus a measured-vs-target record solid enough to defend line by line.

Two principles run through every phase:

- **Three-way agreement.** Every key number is worked out three ways (hand calc, Python in `calcs/`, LTspice in `sim/`) before hardware exists, then checked against measurement.
- **Rev 2 is planned.** First boards usually have a mistake. Finding it, fixing it, and writing down how is part of the project.

## Architecture

- **Input:** 19–20 V barrel-jack laptop brick, ≥ 65 W. Deliberately not mains.
- **Controller:** TI TPS54331: 3.5–28 V in, 3 A out, fixed 570 kHz, integrated 80 mΩ high-side MOSFET, current-mode control with external compensation, 0.8 V reference, pulse-skipping Eco-mode at light load.
- **Power stage:** external Schottky catch diode (non-synchronous), inductor, ceramic output capacitors.
- **Adjustment:** feedback-divider pot mounted on the PCB with its shaft through the panel. The feedback node is high-impedance and noise-sensitive, so no wires out to a panel pot.
- **Built-in protection:** cycle-by-cycle current limit, frequency foldback, thermal shutdown, overvoltage transient protection, programmable input UVLO.

## Target spec (provisional until the Phase 2 gate)

IDs match rows in the values ledger ([test-log.md](test-log.md)).

| ID | Quantity | Target | Conditions |
|---|---|---|---|
| T1 | Output range | ~1 V to 15 V (floor set by Q2) | VIN 19.5 V |
| T2 | Output current | 3 A continuous | across T1, within T9 |
| T3 | Output ripple | < 50 mV p-p | 12 V / 3 A; 20 MHz BW limit; ground-spring probe at the output cap |
| T4 | Load regulation | ΔVOUT (DC mean) ≤ 2 % of setpoint | 0.3 → 3 A, at 5 V and 12 V |
| T5 | Line regulation | ΔVOUT (DC mean) ≤ 1 % of setpoint | VIN 17 → 21 V from a bench supply; 12 V / 1.5 A |
| T6 | Efficiency | > 85 % | 12 V / 1.5 A; also log 0.5, 1, 2, 3 A |
| T7 | Load-step response | peak deviation ≤ 5 %, recovery ≤ 200 µs, no sustained ringing | 0.3 → 2 A step at 5 V |
| T8 | Startup overshoot | peak ≤ 5 % above setpoint | power-up into no load |
| T9 | Thermal | every part < 85 °C case | 10 min at 12 V / 3 A and at 3.3 V / 3 A; room ambient |
| T10 | Stability across range | T7 criteria met | at the output floor, 5 V, 12 V, 15 V |

## Phases and gates

A phase is done when its gate passes, with the numbers recorded in `design.md` or the ledger. Dates assume about 3–4 hours a week.

### Phase 0: Setup (Sep 22 – 27)

Repo, seed files, Claude Code scaffold, claude.ai Project.

**Gate:** repo scaffolded and pushed; Project synced to it.

### Phase 1: Theory (Sep 28 – Oct 11)

- Read: the TPS54331 datasheet's application section; TI SLVA477, *Basic Calculation of a Buck Converter's Power Stage*; TI SLVA057, *Understanding Buck Power Stages in Switchmode Power Supplies*.
- Watch: Phil's Lab and GreatScott! buck-converter videos.
- Sort out lab access (Q11).

**Gate** (each done by hand and in Python):

- duty cycle across the T1 range
- inductor value for ~30 % ripple current at the worst-case output voltage (work out which one that is)
- output capacitance for T3
- IC and diode dissipation at 12 V / 3 A and at 3.3 V / 3 A
- answers to Q1 and Q2

### Phase 2: Simulate (Oct 12 – 18)

- Build an ideal-switch buck in LTspice. LTspice ships Analog Devices models, not TI's, so the generic model is the teaching tool.
- Then check the part-specific design in TI WEBENCH Power Designer or PSpice for TI.
- Compensation: follow the datasheet procedure (Q4).
- Do the practice board this week (below).

**Gate:** clean startup (T8); ripple under T3; load step meets T7 at 5 V; stable at every T10 point.

### Practice board (order by Oct 18)

Push a trivial board, such as a TPS54331 breakout, all the way through KiCad → JLCPCB. About two hours of work. It catches footprint, silkscreen, and ordering mistakes on a board you don't care about.

**Gate:** it arrives, and real parts fit its footprints.

### Phase 3: Schematic + BOM (Oct 19 – 30)

- KiCad schematic from the Phase 1–2 values.
- Resolve Q3, Q5–Q8, and Q10 before finalizing the BOM.
- Sanity-check against a WEBENCH auto-design *after* doing your own.

**Gate:** ERC clean; every part in stock at Digi-Key; BOM for three builds within budget.

### Phase 4: Layout (Oct 31 – Nov 9)

Reproduce the datasheet's layout example faithfully; don't invent.

- Read TI's *Five steps to a great PCB layout for a step-down converter* first.
- Keep the hot loop (input cap → high-side switch → diode) tight; solid ground pour; feedback trace and pot far from the switch node.

**Gate:** DRC clean; one outside review (r/PrintedCircuitBoard) addressed. **Order by Mon Nov 9; hard deadline Fri Nov 13**, so boards arrive before Thanksgiving break.

### Phase 5: Order + assemble (Nov 9 – 24)

- JLCPCB with expedited shipping; check import fees at checkout. Parts for three builds from Digi-Key, because something will smoke.
- Build unit 1 alone first.

**Gate:** unit 1 assembled; no short from VIN or VOUT to GND.

If boards slip past the break, assemble Nov 30 and compress Phase 6.

### Phase 6: Bring-up + characterize (Nov 30 – Dec 11, before finals)

- First power-up from a current-limited bench supply set low, no load. The brick comes after.
- Measure every T-row; save ripple and load-step captures to `media/`.

**Gate:** ledger complete for T1–T10, each pass/fail with board ID; README results filled in.

### Stretch (winter break)

Enclosure (3D-printed), banana jacks, panel meter. Or v2 with adjustable current limiting, making it a true CC/CV supply. Rev 2 of the board if rev 1 needs fixes.

## Open questions

Each answer becomes an entry in [decisions.md](decisions.md).

| # | Question | By | Notes |
|---|---|---|---|
| Q1 | Package: plain SOIC-8 (D) or PowerPAD (DDA)? | Phase 1 | D is easiest to hand-solder, but third-party data puts the PowerPAD's junction-to-board thermal resistance at less than half of D's (≈ 25 vs ≈ 57 °C/W; confirm in the datasheet). With IC loss on the order of 1 W at 12 V / 3 A, compute junction temperature for both. DDA means soldering the thermal pad: hot air, or a via under the pad soldered from the back. |
| Q2 | Output floor at 19.5 V in? | Phase 1 | Minimum on-time (up to ~130 ns per third-party data) at 570 kHz caps the duty cycle near 7 %. With the diode drop, the full-load floor lands around 1 V, not the 0.8 V reference. Confirm. |
| Q3 | Pot wiring that fails *low* | Phase 3 | If the pot sits in the divider's top leg and its wiper opens, VSENSE drops to 0 V and the controller drives the output toward VIN, putting up to ~19 V into whatever's connected. The IC's overvoltage protection won't catch it. Wire it so an open wiper drives the output down. |
| Q4 | Compensation stable over the whole range | Phase 2 | Loop gain scales with VREF/VOUT, so crossover moves as the knob turns. Design at one end, verify at every T10 point. |
| Q5 | Input hot-plug protection | Phase 3 | Plugging a brick into ceramic-only input caps can ring to ~2× VIN, past the IC's 28 V rating. Add a bulk electrolytic for damping; consider a TVS. See LT AN88. |
| Q6 | Catch-diode package | Phase 3 | Worst-case diode loss is at low VOUT and 3 A, where it conducts most of each cycle: ~1.2–1.4 W. SMA packages run too hot there; look at SMB/SMC. Rate it ≥ 40 V and ≥ 3 A. |
| Q7 | Output capacitors | Phase 3 | Ceramic capacitors lose a large share of their capacitance under DC bias. At 15 V out, use 35–50 V parts and check the derated value on the manufacturer's curve. |
| Q8 | Inductor saturation | Phase 3 | Saturation current must exceed the IC's maximum current limit, not just 3 A plus ripple. |
| Q9 | Test load for 3 A | Phase 5 | Lab electronic load, power resistors (15 V / 3 A is 45 W), or a cheap DC load module? |
| Q10 | Brick and connector | Phase 3 | Which brick (≥ 65 W; 15 V × 3 A is 45 W out), and which barrel size; the PCB jack must match. |
| Q11 | Lab access | Phase 1 | PKI open-lab hours; a bench supply with current limit; a scope with a 20 MHz BW limit and a ground-spring probe tip. |

## Measurement notes

- **Ripple:** 20 MHz bandwidth limit, ground-spring (tip-and-barrel) probing right at the output capacitor. A long ground lead picks up switching spikes that aren't really there.
- **Light load:** below ~160 mA peak inductor current the chip enters Eco-mode and skips pulses. Bursty ripple there is normal, not instability.
- **Efficiency:** measure VIN, IIN, VOUT, and IOUT at the board terminals, not from the supply's front panel.
- **Every value:** statistic, conditions, board ID, date.

## Budget (estimates; verify at checkout)

| Item | Est. |
|---|---|
| PCBs: practice + main, with expedited shipping and any import fees | $30–60 |
| Parts for three builds (Digi-Key) | ~$40 |
| Laptop brick, 19–20 V, ≥ 65 W (used or generic) | $15–25 |
| Pot, knob, jacks, standoffs | ~$15 |
| Test load, if the lab can't lend one (Q9) | $0–40 |
| Soldering iron (e.g., Pinecil), optional | $0–40 |
| **Total** | **~$100–220** |

## Resources

- [TPS54331 datasheet](https://www.ti.com/lit/ds/symlink/tps54331.pdf): application section, compensation procedure, layout example, thermal data
- TI SLVA477, *Basic Calculation of a Buck Converter's Power Stage*
- TI SLVA057, *Understanding Buck Power Stages in Switchmode Power Supplies*
- TI Analog Applications Journal, *Five steps to a great PCB layout for a step-down converter*
- Linear Technology AN88, *Ceramic Input Capacitors Can Cause Overvoltage Transients*
- Phil's Lab (YouTube): KiCad and buck-converter design
- GreatScott! (YouTube): buck-converter basics
- Tools: KiCad, LTspice, TI WEBENCH Power Designer, PSpice for TI, JLCPCB, Digi-Key

## Decisions

All decisions are logged in [decisions.md](decisions.md).
