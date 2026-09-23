# CLAUDE.md — bench-psu

Standing rules for Claude Code in this repo. The repo is public, so everything here should read well to a recruiter or reviewer.

The full plan (spec, phases, gates, timeline, open questions) is in @docs/scope.md.

## What this project is

A single-channel adjustable bench power supply: a non-synchronous buck converter built around the TI TPS54331 on a custom 2-layer PCB, powered by a 19–20 V laptop brick.

Fish, the builder, is a second-year EE student working at a Circuits I level (KVL/KCL, RC/RL transients) who hasn't taken control theory yet. Explain things from that level. Loop compensation follows the datasheet's step-by-step procedure; go deeper into loop theory only if he asks.

## Where things live

| Path | Holds | Rule |
|---|---|---|
| `README.md` | status line, target spec, results, photos | recruiter-facing; no internal notes |
| `docs/scope.md` | spec (T1–T10), phases, gates, timeline, budget, open questions (Q1–Q11) | targets change only through a logged decision |
| `docs/design.md` | hand calcs, Python cross-checks, LTspice results | each key number shows every method side by side |
| `docs/decisions.md` | one entry per decision | append-only; supersede, never delete |
| `docs/test-log.md` | values ledger + dated bench-session notes | the only home of measured values |
| `docs/bom.csv` | ref, value, manufacturer PN, Digi-Key PN, qty per board, unit price, link | quantities for three builds |
| `calcs/` | Python scripts behind design.md numbers | each script prints the values it backs |
| `sim/` | LTspice schematics (`.asc`) | don't commit `.raw`, `.log`, or `.net` outputs |
| `hardware/` | KiCad projects: `main/` and `practice/` | no backup, lock, or cache files |
| `media/` | photos and scope captures | name as `YYYY-MM-DD_r1-u1_what.png` |

- Update files in place. Never create versioned copies (`scope_v2.md`, `design-final.md`); git is the history.
- Use standard markdown links, not Obsidian `[[wikilinks]]`, so GitHub renders them.
- Link to vendor datasheets and app notes; don't commit the PDFs.

## Number rules

1. No bare numbers and no bare ±. Name the statistic and the conditions: "28 mV p-p, 20 MHz BW limit, 12 V / 3 A out, ground-spring probe," not "28 mV ripple."
2. Hand-calc, Python, LTspice, and measured values never share a column, and one never overwrites another.
3. Python values come from actually running the script in `calcs/`. LTspice and measured values come from Fish. Never fill a cell with an estimate or a number carried forward from an earlier session; leave it blank and ask.
4. At every gate, ask Fish for the values the gate needs before calling it passed.
5. Tag every measurement with a board ID (`r1-u1` = rev 1, unit 1) and a date. Data from a board with a known defect is marked **quarantined**: kept, but excluded from pass/fail.
6. Keep one consolidated values ledger in `docs/test-log.md`: one row per target ID, with columns for target, hand calc, Python, LTspice, measured, board ID, and status.

## Decisions

Log each decision in `docs/decisions.md`: date, decision, why, and what was rejected. If a decision changes a target, update `docs/scope.md` and that ledger row in the same commit. When an open question gets answered, remove it from the scope's table and log the answer as a decision.

## Handoffs from the claude.ai Project

Fish works through problems in a claude.ai Project and brings the results here as a note starting with `HANDOFF:`. When you get one:

1. File each item where it belongs: decisions → `decisions.md`, calcs → `design.md`, values → the ledger, open questions → `scope.md`.
2. If an item contradicts what's already in the repo, stop and ask before changing anything.
3. Reply with a short list of what changed, commit as `handoff: <topic>`, and push.

## Gates

Each phase in `docs/scope.md` ends with a gate. When Fish says a phase is done, check its gate against the ledger and `design.md`, then list anything missing or unmeasured. When a gate passes, update the status line in `README.md` and `docs/scope.md`.

## Safety

- Low-voltage DC only; nothing mains-powered in this project.
- The first power-up of any new or reworked board comes from a current-limited bench supply, not the brick.
- Flag anything that could push VIN past the TPS54331's 28 V rating, such as hot-plug ringing on the input.

## Git

Small commits with plain messages (`docs: inductor calc`, `sim: 5 V load step`). Push after every handoff.
