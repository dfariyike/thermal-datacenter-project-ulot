import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
FILE_NAME = 'server_rack_mean_inlet.csv'
T_SUPPLY = 22.0  # The temperature of the air leaving the floor tiles (Celsius)
T_EXHAUST_AVG = 45.0 # Estimated or modeled average exhaust temp for SHI calculation

# --- 2. LOAD DATA ---
try:
    df = pd.read_csv(FILE_NAME, sep=None, engine='python')
    df.columns = [c.strip() for c in df.columns]
    name_col, temp_col = df.columns[0], df.columns[1]
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df = df.dropna(subset=[temp_col])
except Exception as e:
    print(f"Error: {e}"); exit()

# --- 3. RECIRCULATION CALCULATIONS ---
# Calculate the temperature rise at the intake (Recirculation Delta)
df['Recirc_Delta'] = df[temp_col] - T_SUPPLY

# Supply Heat Index (SHI) Calculation
# SHI = (T_inlet - T_supply) / (T_exhaust - T_supply)
df['SHI'] = (df[temp_col] - T_SUPPLY) / (T_EXHAUST_AVG - T_SUPPLY)

# --- 4. VISUALIZATION ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8), sharey=True)

# Plot 1: Recirculation Magnitude
bars1 = ax1.barh(df[name_col], df['Recirc_Delta'], color='orangered', edgecolor='black')
ax1.set_title(f'Recirculation Delta (Inlet - {T_SUPPLY}°C Supply)', fontweight='bold')
ax1.set_xlabel('Temperature Rise at Intake (°C)')
ax1.axvline(2.0, color='red', linestyle='--', label='High Risk (>2°C)')
ax1.legend()

# Plot 2: Supply Heat Index (Efficiency Score)
# SHI closer to 0 is perfect; closer to 1 is total failure.
bars2 = ax2.barh(df[name_col], df['SHI'], color='mediumslateblue', edgecolor='black')
ax2.set_title('Supply Heat Index (SHI)', fontweight='bold')
ax2.set_xlabel('Index Score (0.0 to 1.0)')
ax2.set_xlim(0, 0.5) # Zoomed in for typical rack performance

# Annotate with the specific Delta T
for bar in bars1:
    ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
             f'+{bar.get_width():.1f}°C', va='center', fontsize=9)

ax1.invert_yaxis()
plt.tight_layout()
plt.savefig('recirculation_report.png', dpi=300)
plt.show()

# --- 5. SUMMARY ---
total_recirc_loss = df['Recirc_Delta'].mean()
print(f"Average Recirculation Magnitude: {total_recirc_loss:.2f}°C")
print(f"Max SHI: {df['SHI'].max():.2f} at {df.loc[df['SHI'].idxmax(), name_col]}")