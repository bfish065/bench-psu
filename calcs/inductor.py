# Inductor sizing and peak current (Phase 1 gate, steps 3a and 3b).
# Ideal V_on and D (switch and diode drops neglected).
# Hand-calc counterpart: docs/design.md, "Inductor value".

Vin = 19.5          # V, brick input
Iout = 3.0          # A, full load (T2)
ripple_frac = 0.30  # ripple target, fraction of Iout
f_typ = 570e3       # Hz, switching frequency typ (TPS54331 datasheet)
f_min = 456e3       # Hz, switching frequency min (datasheet; = 0.8 x typ, Eq. 9)
I_lim_min = 3.5     # A, current-limit threshold min (datasheet, VIN 12 V)


def ripple(Vout, L, f):
    """Peak-to-peak inductor ripple, ideal: dI = (Vin - Vout) * D / (f * L)."""
    D = Vout / Vin
    return (Vin - Vout) * D / (f * L)


def L_required(Vout, dI, f):
    """Inductance that gives ripple dI: L = Vout * (Vin - Vout) / (dI * f * Vin)."""
    return Vout * (Vin - Vout) / (dI * f * Vin)


dI_target = ripple_frac * Iout
print(f"Ripple target: {dI_target:.3f} A p-p ({ripple_frac:.0%} of {Iout} A)")

# 3a: sweep VOUT across T1 to find where the required L peaks
vouts = [v / 100 for v in range(100, 1501, 5)]   # 1.00 V to 15.00 V in 0.05 V steps
worst = max(vouts, key=lambda v: L_required(v, dI_target, f_typ))
L_req = L_required(worst, dI_target, f_typ)
print(f"Worst-case VOUT: {worst:.2f} V")
print(f"Required L at {worst:.2f} V, 570 kHz typ: {L_req * 1e6:.2f} uH")

# 3b: ripple and peak current for candidate standard values, at the worst-case VOUT
print()
print(f"At VOUT = {worst:.2f} V, Vin = {Vin} V, Iout = {Iout} A:")
print("   L      f       ripple (A p-p)   peak (A)   vs 3.5 A min limit")
for L in [10e-6, 15e-6]:
    for f in [f_typ, f_min]:
        dI = ripple(worst, L, f)
        peak = Iout + dI / 2
        verdict = "OVER" if peak > I_lim_min else "under"
        print(f"{L * 1e6:4.0f} uH  {f / 1e3:3.0f} kHz   {dI:.4f}           {peak:.4f}     {verdict}")

# Tolerance check: a 15 uH part at -20 % (12 uH), slow chip, worst-case VOUT
L_low = 15e-6 * 0.8
dI = ripple(worst, L_low, f_min)
peak = Iout + dI / 2
verdict = "OVER" if peak > I_lim_min else "under"
print()
print(f"Tolerance: 15 uH at -20 % = {L_low * 1e6:.0f} uH, {f_min / 1e3:.0f} kHz: "
      f"ripple {dI:.4f} A p-p, peak {peak:.4f} A, {verdict} 3.5 A")
