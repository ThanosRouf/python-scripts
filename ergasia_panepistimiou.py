import math
# Η βιβλιοθήκη pandas αφαιρέθηκε

BR = 1.0
SIGMA = 20.0
W = 32.0
M = 5
DELTA = 1.0
SIFS = 10.0
DIFS = 50.0

EP = 8224.0
ACK = 304.0
RTS = 352.0
CTS = 304.0
H = 224.0 + 192.0

Ts_bas = H + EP + SIFS + DELTA + ACK + DIFS + DELTA
Tc_bas = H + EP + DIFS + DELTA

Ts_rts = RTS + DELTA + SIFS + CTS + DELTA + SIFS + H + EP + DELTA + SIFS + ACK + DELTA + DIFS
Tc_rts = RTS + DELTA + DIFS

def solve_tau_p(n, W, M):
    p1 = 0.00001
    p_step = 0.000001
    
    while p1 <= 1.0:
        denom_tau = (1.0 - 2.0 * p1) * (W + 1.0) + p1 * W * (1.0 - (2.0 * p1)**M)
        if denom_tau <= 0:
            p1 += p_step
            continue
            
        tau = (2.0 * (1.0 - 2.0 * p1)) / denom_tau

        if not 0 < tau < 1:
            p1 += p_step
            continue

        p_new = 1.0 - (1.0 - tau)**(n - 1)

        if abs(p_new - p1) < 0.00002 and 0 < p1 < 1:
            return tau, p1
        
        p1 += p_step
            
    return -1, -1

def calculate_S(tau, n, Ts, Tc):
    if tau <= 0:
        return 0.0
        
    Ptr = 1.0 - (1.0 - tau)**n
    if Ptr <= 0:
        return 0.0
        
    Ps = (n * tau * (1.0 - tau)**(n - 1)) / Ptr

    numerator = Ps * Ptr * EP
    denominator = (1.0 - Ptr) * SIGMA + Ptr * Ps * Ts + Ptr * (1.0 - Ps) * Tc
    
    return numerator / denominator * BR

n_values = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

print("--- ΑΠΟΤΕΛΕΣΜΑΤΑ ΥΠΟΛΟΓΙΣΜΩΝ ---")
print(f"Ts (Basic): {Ts_bas:.0f} μs | Tc (Basic): {Tc_bas:.0f} μs")
print(f"Ts (RTS/CTS): {Ts_rts:.0f} μs | Tc (RTS/CTS): {Tc_rts:.0f} μs")

# Εκτύπωση Κεφαλίδας Πίνακα
print("\n----------------------------------------------------------------------------------")
print("n |  tau  |    p    | S (Basic) Mbps | S (RTS/CTS) Mbps")
print("----------------------------------------------------------------------------------")

for n in n_values:
    tau, p = solve_tau_p(n, W, M)
    
    if tau == -1:
        # Χειρισμός περιπτώσεων που δεν βρέθηκε λύση (n >= 40)
        output = f"{n:<2} | --.---- | --.---- | ---.---- | ---.----"
    else:
        S_basic = calculate_S(tau, n, Ts_bas, Tc_bas)
        S_rts_cts = calculate_S(tau, n, Ts_rts, Tc_rts)
        
        output = f"{n:<2} | {tau:.5f} | {p:.5f} | {S_basic:.6f} | {S_rts_cts:.6f}"
    
    print(output)
print("----------------------------------------------------------------------------------")