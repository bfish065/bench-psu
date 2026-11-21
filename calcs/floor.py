# Step 4c: output floor, datasheet Eq. 33 (SLVS839H section 8.2.2.10).
t_on_min = 130e-9   # s, max min on-time
f_max = 684e3       # Hz, fastest chip
D_min = t_on_min * f_max
Rds = 0.080         # ohm, typ
VD = 0.5            # V, assumed
RL = 0.0            # ohm, neglected until the inductor is picked
print(f"minimum duty {D_min:.5f}")
for Vin in [21.0, 19.5]:      # 21 V = top of T5's input range
    for Io in [0.0, 3.0]:
        Vo_min = D_min * (Vin - Io * Rds + VD) - Io * RL - VD
        print(f"VIN {Vin} V, {Io} A: floor {Vo_min:.4f} V")
