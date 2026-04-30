import pandas as pd

# --- 1. CONFIGURATION (ASHRAE Class A1) ---
FILE_NAME = 'server_rack_mean_inlet.csv'
T_REC_MAX = 27.0  # Recommended Max
T_REC_MIN = 18.0  # Recommended Min
T_ALLOW_MAX = 32.0  # Allowable Max (Used as the denominator for RCI_HI)
T_ALLOW_MIN = 15.0  # Allowable Min (Used as the denominator for RCI_LO)

# --- 2. LOAD DATA ---
try:
    df = pd.read_csv(FILE_NAME, sep=None, engine='python')
    df.columns = [c.strip() for c in df.columns]
    temp_col = df.columns[1]
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df = df.dropna(subset=[temp_col])
    inlet_temps = df[temp_col].tolist()
except Exception as e:
    print(f"Error: {e}")
    exit()

# --- 3. RCI CALCULATION LOGIC ---
def calculate_rci(temps):
    # RCI High (Overheating)
    over_limit_sum = sum([max(0, T - T_REC_MAX) for T in temps])
    max_allowable_excess = len(temps) * (T_ALLOW_MAX - T_REC_MAX)
    rci_hi = 100 * (1 - (over_limit_sum / max_allowable_excess))

    # RCI Low (Overcooling)
    under_limit_sum = sum([max(0, T_REC_MIN - T) for T in temps])
    max_allowable_deficit = len(temps) * (T_REC_MIN - T_ALLOW_MIN)
    rci_lo = 100 * (1 - (under_limit_sum / max_allowable_deficit))

    return rci_hi, rci_lo

rci_hi, rci_lo = calculate_rci(inlet_temps)

# --- 4. DISPLAY RESULTS ---
print("-" * 30)
print(f"RACK COOLING INDEX REPORT")
print("-" * 30)
print(f"RCI High (Protection from Heat): {rci_hi:.1f}%")
print(f"RCI Low  (Protection from Cold): {rci_lo:.1f}%")
print("-" * 30)

# Interpretation of Results:
if rci_hi >= 95:
    print("Status: Excellent Cooling Performance")
elif rci_hi >= 80:
    print("Status: Good (Minor Hot Spots)")
else:
    print("Status: Poor (Significant Recirculation detected)")