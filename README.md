# bench-psu

A single-channel adjustable bench power supply: a TI TPS54331 non-synchronous buck converter on a custom 2-layer PCB, powered by a 19–20 V laptop brick.

**Status:** Phase 1: theory

## Target spec

Provisional until the Phase 2 (simulation) gate. Full plan in [docs/scope.md](docs/scope.md).

| ID | Quantity | Target | Conditions |
|---|---|---|---|
| T1 | Output range | ~1 V to 15 V | VIN 19.5 V |
| T2 | Output current | 3 A continuous | across T1, within T9 |
| T3 | Output ripple | < 50 mV p-p | 12 V / 3 A; 20 MHz BW limit; ground-spring probe at the output cap |
| T4 | Load regulation | ΔVOUT (DC mean) ≤ 2 % of setpoint | 0.3 → 3 A, at 5 V and 12 V |
| T5 | Line regulation | ΔVOUT (DC mean) ≤ 1 % of setpoint | VIN 17 → 21 V from a bench supply; 12 V / 1.5 A |
| T6 | Efficiency | > 85 % | 12 V / 1.5 A; also log 0.5, 1, 2, 3 A |
| T7 | Load-step response | peak deviation ≤ 5 %, recovery ≤ 200 µs, no sustained ringing | 0.3 → 2 A step at 5 V |
| T8 | Startup overshoot | peak ≤ 5 % above setpoint | power-up into no load |
| T9 | Thermal | every part < 85 °C case | 10 min at 12 V / 3 A and at 3.3 V / 3 A; room ambient |
| T10 | Stability across range | T7 criteria met | at the output floor, 5 V, 12 V, 15 V |

## Tools

KiCad (schematic and layout), LTspice (simulation), Python (design calculations).

## Repo map

| Path | Contents |
|---|---|
| [docs/scope.md](docs/scope.md) | spec, phases and gates, timeline, budget, open questions |
| [docs/design.md](docs/design.md) | hand calcs, Python cross-checks, LTspice results |
| [docs/decisions.md](docs/decisions.md) | design decision log |
| [docs/test-log.md](docs/test-log.md) | values ledger and bench-session notes |
| [docs/bom.csv](docs/bom.csv) | bill of materials |
| [calcs/](calcs/) | Python design scripts |
| [sim/](sim/) | LTspice schematics |
| [hardware/](hardware/) | KiCad projects: main board and practice board |
| [media/](media/) | photos and scope captures |
