# Scope: adjustable bench power supply (TPS54331 buck)

*Status: Phase 2 (simulate); Phase 1 gate passed 2026-11-21 · Last updated 2026-11-21*

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
| T1 | Output range | 1.5 V to 15 V (floor from D13) | VIN 19.5 V |
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

**Gate passed 2026-11-21.** Results in [design.md](design.md#phase-1-gate-calculations); decisions D10–D15.

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
| Q3 | Pot wiring that fails *low* | Phase 3 | If the pot sits in the divider's top leg and its wiper opens, VSENSE drops to 0 V and the controller drives the output toward VIN, putting up to ~19 V into whatever's connected. The IC's overvoltage protection won't catch it. Wire it so an open wiper drives the output down. Datasheet: VSENSE absolute maximum is 3 V, so the fail-low wiring must never leave VSENSE connected only to VOUT (up to 15 V) through the top resistor. |
| Q4 | Compensation stable over the whole range | Phase 2 | Loop gain scales with VREF/VOUT, so crossover moves as the knob turns. Design at one end, verify at every T10 point. Across 1.5–15 V (T1, D13) that gain spreads by about 10×. Tuning at the low-VOUT end is the stable choice, but the loop is then slow at 12–15 V, so T7's ≤ 200 µs recovery may fail there. Decide whether T10 needs relaxing at the ends of the range (a target change, so log it). Datasheet (Compensation Components): keep crossover below 1/8 of the minimum switching frequency and not above 25 kHz; Eq. 26 sets the compensation resistor in proportion to VO × CO, so with fixed parts the crossover moves with 1/VOUT (and with the output capacitance, which drops under DC bias, Q7). The datasheet's table of typical designs (Table 7-1) uses different compensation parts for each output voltage. |
| Q5 | Input hot-plug protection | Phase 3 | Plugging a brick into ceramic-only input caps can ring to ~2× VIN, past the IC's 30 V absolute-maximum VIN (datasheet; 28 V is the recommended maximum). Add a bulk electrolytic for damping; consider a TVS. A TVS whose standoff clears the highest brick voltage typically clamps well above 30 V, so check its clamping voltage against 30 V; the electrolytic likely does most of the work. See LT AN88. |
| Q6 | Catch-diode package | Phase 3 | Worst-case diode loss is at low VOUT and 3 A, where it conducts most of each cycle: ~1.2–1.4 W. SMA packages run too hot there; look at SMB/SMC. Rate it ≥ 40 V and ≥ 3 A. |
| Q7 | Output capacitors | Phase 3 | Ceramic capacitors lose a large share of their capacitance under DC bias. At 15 V out, use 35–50 V parts and check the derated value on the manufacturer's curve. |
| Q8 | Inductor saturation | Phase 3 | Saturation current must cover the IC's current limit, not just 3 A plus ripple. Datasheet: current-limit threshold 3.5 A min, 5.8 A typ at VIN 12 V; no maximum is given, so the rating needs margin above 5.8 A. How much? |
| Q9 | Test load for 3 A | Phase 5 | Lab electronic load, power resistors (15 V / 3 A is 45 W), or a cheap DC load module? |
| Q10 | Brick and connector | Phase 3 | Which brick (≥ 65 W; 15 V × 3 A is 45 W out), and which barrel size; the PCB jack must match. |
| Q13 | T9 coverage at the hottest diode and IC points | Phase 2 | T9 tests 12 V / 3 A and 3.3 V / 3 A, but diode loss peaks at the output floor and 3 A (Q6; 1.3482 W at 1.5 V / 3 A, Python, VD 0.5 V assumed) and IC loss peaks at 15 V / 3 A (0.9617 W on a 684 kHz chip, hand and Python). Add one or both points to T9? |
| Q14 | DCM at the 0.3 A load-step points | Phase 2 | A non-synchronous buck goes discontinuous when load current falls below half the inductor ripple. Check whether 0.3 A (T4, T7, T10) starts in DCM at each setpoint; the loop behaves differently there. |
| Q15 | Sustained output short or overload | Phase 3 | Bench supplies get shorted and overloaded. Nothing enforces T2's 3 A: the current-limit threshold is 3.5 A min, 5.8 A typ, no maximum given (datasheet, VIN 12 V), so a load can draw well above 3 A. The datasheet describes cycle-by-cycle limiting and frequency foldback but no hiccup mode, and thermal shutdown protects the IC, not the catch diode or inductor. In a short the diode carries the limit current for most of each cycle. Can the diode and inductor survive sustained overload, and is that a requirement? |
| Q16 | Back-feed from the output | Phase 3 | With a battery or another supply on the output and the brick unplugged, current flows backward through the high-side MOSFET's body diode into VIN. Protect against it? |
| Q17 | Input reverse polarity | Phase 3 | A wrong-polarity barrel plug. Add reverse-polarity protection, and at what cost in efficiency (T6)? |
| Q19 | Which simulation decides the Phase 2 gate? | Phase 2 | An ideal-switch LTspice model does not include the IC's minimum on-time, Eco-mode pulse skipping, or internal slope compensation. Slope compensation matters above 50 % duty (12 V and 15 V out), and the datasheet gives no value for its ramp. Should the T10 stability call rest on TI's model (WEBENCH or PSpice for TI), with LTspice kept as the teaching model? |
| Q20 | Input UVLO thresholds | Phase 3 | The datasheet recommends an external UVLO divider on EN unless VIN stays more than 2 V above VOUT. Pick start and stop voltages for a 19–20 V brick with up to 15 V out. |
| Q21 | Should T3 cover the whole output range? | Phase 2 | T3 is defined at 12 V / 3 A, but ripple current peaks at VIN/2 = 9.75 V. The 4.7 µF ripple sizing was done at 9.75 V (48.70 mV p-p, Python), so the design covers it; the target text doesn't. Widen T3's conditions? |
| Q22 | Why is T3 50 mV? | Phase 2 | T3's < 50 mV p-p has no recorded reason. Log one, or change it, before the Phase 2 gate makes the spec final. |
| Q23 | Load-step capacitance at the output floor | Phase 2 | T7's 5 % at the 1.5 V floor (T10) allows a 75 mV dip, which by the rule-of-thumb estimate needs about 144 µF, versus about 43 µF at 5 V (D14). Options: more ceramics, a bulk polymer cap, or relaxing T10's deviation limit at the floor (a target change). Ties to Q4. |

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
