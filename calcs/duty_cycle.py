# Duty cycle across the T1 range (Phase 1 gate, step 2).
# Volt-second balance with the switch and diode drops; inductor resistance neglected:
#   D = (VOUT + VD) / (VIN - I * Rds + VD)
# Hand-calc counterpart: docs/design.md, "Duty cycle across the T1 range".

Vin = 19.5      # V, brick input
I = 3.0         # A, full load (T2)
Rds = 0.080     # ohm, high-side switch on-resistance, typ (TPS54331 datasheet)
VD = 0.5        # V, catch-diode forward drop, ASSUMED until the diode is picked (Q6)
D_min = 130e-9 * 684e3   # max min on-time x max frequency (datasheet Eq. 33)
D_max = 0.90             # max duty, datasheet

print(f"VIN {Vin} V, {I} A, Rds {Rds * 1e3:.0f} mohm typ, VD {VD} V assumed")
print(f"Chip limits: min duty {D_min:.4f}, max duty {D_max:.2f}")
print(" VOUT   ideal D    D with drops   within chip limits?")
for Vout in [1.0, 1.5, 3.3, 5.0, 12.0, 15.0]:
    D_ideal = Vout / Vin
    D = (Vout + VD) / (Vin - I * Rds + VD)
    ok = "yes" if D_min <= D <= D_max else "NO"
    print(f"{Vout:5.1f}   {D_ideal:.7f}  {D:.7f}      {ok}")
