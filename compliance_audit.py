import pandas as pd
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
FILE_NAME = 'server_rack_mean_inlet.csv'
ASHRAE_REC_MAX = 27.0
ASHRAE_ALLOW_MAX = 32.0

# --- 2. LOAD AND CLEAN DATA ---
try:
    # sep=None with engine='python' tells pandas to guess the delimiter (tab or comma)
    df = pd.read_csv(FILE_NAME, sep=None, engine='python')
    
    # Strip any whitespace from the column headers themselves
    df.columns = [c.strip() for c in df.columns]

    # POSITIONAL SELECTION: 
    # This ignores the exact 'Object Name' text and just grabs the columns by index
    name_col = df.columns[0]   # Usually 'Object Name'
    target_col = df.columns[1] # Usually 'Region Mean Temp'
    
    print(f"Successfully identified columns: '{name_col}' and '{target_col}'")

except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# --- 3. COMPLIANCE LOGIC ---
def get_status(temp):
    if temp > ASHRAE_ALLOW_MAX:
        return 'CRITICAL'
    elif temp > ASHRAE_REC_MAX:
        return 'WARNING'
    else:
        return 'OPTIMAL'

# Ensure the temp column is treated as a number
df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
df = df.dropna(subset=[target_col]) # Remove any empty rows

df['Compliance_Status'] = df[target_col].apply(get_status)

# --- 4. VISUALIZATION ---
plt.style.use('ggplot') # ggplot is built-in and very clean for LinkedIn
fig, ax = plt.subplots(figsize=(12, 8))

color_map = {'CRITICAL': '#d63031', 'WARNING': '#fdcb6e', 'OPTIMAL': '#00b894'}
colors = [color_map[status] for status in df['Compliance_Status']]

# Using the position-based column names here
bars = ax.barh(df[name_col], df[target_col], color=colors, edgecolor='black', alpha=0.9)

# Add ASHRAE Guideline Lines
ax.axvline(ASHRAE_REC_MAX, color='orange', linestyle='--', label=f'ASHRAE Rec Max ({ASHRAE_REC_MAX}°C)')
ax.axvline(ASHRAE_ALLOW_MAX, color='red', linestyle='-', linewidth=2, label=f'ASHRAE Allowable Max ({ASHRAE_ALLOW_MAX}°C)')

# Annotate values
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
            f'{width:.2f}°C', va='center', fontsize=10, fontweight='bold')

ax.set_title('Thermal Compliance Audit: Cabinet Inlet Temperatures', fontsize=16, pad=15)
ax.set_xlabel('Temperature (°C)', fontsize=12)
ax.invert_yaxis() 
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()

# --- 5. EXPORT ---
df.to_excel('Thermal_Audit_Summary.xlsx', index=False)
print("Audit complete and saved to Excel.")