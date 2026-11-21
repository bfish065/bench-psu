# Output capacitor sizing (Phase 1 gate, step 3c).
# Part 1: ripple (T3). Part 2: load step (T7 / T10, Q18).
# Hand-calc counterpart: docs/design.md, "Output capacitance for T3".
from math import pi

Vin = 19.5          # V, brick input
Iout = 3.0          # A, full load (T2)
L = 15e-6           # H, chosen inductor (15 uH)
f_min = 456e3       # Hz, switching frequency min (TPS54331 datasheet)
ESR = 0.010         # ohm, output cap ESR, ASSUMED (high side for ceramics)
ripple_max = 0.050  # V p-p, T3 limit
C_chosen = 4.7e-6   # F, chosen standard value (no DC-bias derating)

f_c = 25e3          # Hz, max crossover (datasheet, Compensation Components)
I_step = 2.0 - 0.3  # A, T7 load step 0.3 -> 2 A
dip_frac = 0.05     # T7: peak deviation <= 5 % of setpoint


def ripple_current(Vout):
    """Inductor ripple, ideal: dI = (Vin - Vout) * D / (f * L)."""
    D = Vout / Vin
    return (Vin - Vout) * D / (f_min * L)


def ripple_voltage(dI, C):
    """Capacitance term + ESR term: dV = dI / (8 f C) + dI * ESR."""
    return dI / (8 * f_min * C) + dI * ESR


# Part 1: size C at the worst-case VOUT (ripple current peaks at Vin / 2)
V_worst = Vin / 2
dI_worst = ripple_current(V_worst)
budget = ripple_max - dI_worst * ESR             # what's left after the ESR drop
C_min_no_esr = dI_worst / (8 * f_min * ripple_max)
C_min = dI_worst / (8 * f_min * budget)
print(f"Part 1: ripple, {L * 1e6:.0f} uH, {f_min / 1e3:.0f} kHz, ESR {ESR * 1e3:.0f} mohm assumed")
print(f"  Ripple current at {V_worst:.2f} V: {dI_worst:.4f} A p-p")
print(f"  Min C, no ESR budget:   {C_min_no_esr * 1e6:.2f} uF")
print(f"  ESR drop: {dI_worst * ESR * 1e3:.2f} mV, leaves {budget * 1e3:.2f} mV")
print(f"  Min C, with ESR budget: {C_min * 1e6:.2f} uF")
for Vout in [V_worst, 12.0]:
    dI = ripple_current(Vout)
    dV = ripple_voltage(dI, C_chosen)
    print(f"  {Vout:5.2f} V / 3 A with {C_chosen * 1e6:.1f} uF: dI {dI:.4f} A p-p, ripple {dV * 1e3:.2f} mV p-p")

# Part 2: load step, rule of thumb dip = I_step / (2 pi f_c C), NOT from the datasheet
# Second check: datasheet Eq. 12, C_O(min) = 1 / (2 pi R_O f_CO(max)), R_O = VO / IO
print()
print(f"Part 2: load step {I_step:.1f} A, f_c {f_c / 1e3:.0f} kHz (rule of thumb)")
for Vout in [5.0, 1.5, 1.0]:   # 1.5 V = T1 floor (D10); 1.0 V = old floor
    dip = dip_frac * Vout
    C_step = I_step / (2 * pi * f_c * dip)
    R_O = Vout / 2.0                              # at the 2 A end of the step
    C_eq12 = 1 / (2 * pi * R_O * f_c)
    print(f"  {Vout:3.1f} V: allowed dip {dip * 1e3:.0f} mV -> C >= {C_step * 1e6:.1f} uF; "
          f"Eq. 12 min (R_O {R_O:.2f} ohm) {C_eq12 * 1e6:.2f} uF")
