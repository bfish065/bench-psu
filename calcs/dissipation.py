# Step 4a/4b: TPS54331 loss (datasheet SLVS839H section 8.2.2.11) and package temperatures.
# Hand-calc formulas, typ = 570 kHz, worst = 684 kHz. Rds 80 mOhm typ (no max in the datasheet).
Vin = 19.5      # V, brick nominal
Iout = 3.0      # A
Rds = 0.080     # ohm, typ
TA = 25.0       # deg C, room ambient
TJ_max = 150.0  # deg C, datasheet
T_case_max = 85.0  # deg C, target T9

# Table 6.4 thermal metrics, deg C/W
packages = {"D (SOIC-8)": {"RthJA": 116.3, "psiJT": 12.9},
            "DDA (PowerPAD)": {"RthJA": 48.7, "psiJT": 8.4}}

def ic_loss(Vout, f):
    Pcon = Iout**2 * Rds * Vout / Vin
    Psw = 0.5e-9 * Vin**2 * Iout * f
    Pgc = 22.8e-9 * f
    Pq = 0.11e-3 * Vin
    return Pcon, Psw, Pgc, Pq, Pcon + Psw + Pgc + Pq

for label, Vout, f in [("typ 15 V", 15.0, 570e3), ("worst 15 V", 15.0, 684e3),
                       ("typ 12 V", 12.0, 570e3), ("worst 12 V", 12.0, 684e3),
                       ("typ 3.3 V", 3.3, 570e3)]:
    Pcon, Psw, Pgc, Pq, Ptot = ic_loss(Vout, f)
    print(f"{label}: Pcon {Pcon:.4f} W, Psw {Psw:.4f} W, Pgc {Pgc:.4f} W, Pq {Pq:.4f} W, Ptot {Ptot:.4f} W")
    for name, p in packages.items():
        TJ = TA + p["RthJA"] * Ptot
        Tc = TJ - p["psiJT"] * Ptot
        ok = "PASS" if (TJ < TJ_max and Tc < T_case_max) else "FAIL"
        print(f"    {name}: TJ {TJ:.2f} C, case {Tc:.2f} C -> {ok}")

# Diode loss: P_D = VD * I * (1 - D). Ideal D = Vout/Vin; D with drops from step 2.
VD = 0.5  # V, assumed until the diode is picked (Q6)
print()
for Vout in [12.0, 3.3, 1.5]:
    D_ideal = Vout / Vin
    D_drops = (Vout + VD) / (Vin - Iout * Rds + VD)
    print(f"diode at {Vout} V / 3 A: ideal D {VD*Iout*(1-D_ideal):.4f} W, D with drops {VD*Iout*(1-D_drops):.4f} W")
