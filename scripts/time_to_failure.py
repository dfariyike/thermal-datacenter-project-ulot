import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. CONFIGURATION ---
FILE_NAME = 'transient_failure_data.csv'
CRITICAL_THRESHOLD = 35.0  # ASHRAE Allowable Max / Server Trip Point
T_SUPPLY = 22.0            # Nominal supply air temp

try:
    # Load data - handling potential whitespace in headers
    df = pd.read_csv(FILE_NAME, sep=None, engine='python')
    df.columns = [c.strip() for c in df.columns]
    
    # Identify columns: First column is Time, rest are Temperature Monitor Points
    time_col = df.columns[0]
    temp_cols = df.columns[1:]
    
    # Ensure numeric conversion
    df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
    for col in temp_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna()

except Exception as e:
    print(f"File Loading Error: {e}")
    exit()

# --- 2. ANALYSIS & PLOTTING ---
plt.figure(figsize=(12, 7))
plt.style.use('dark_background') # Professional NOC-style look

colors = plt.cm.get_cmap('YlOrRd', len(temp_cols))
ttf_results = {}

print(f"{'Sensor Location':<20} | {'Steady State':<12} | {'Time to Failure':<15}")
print("-" * 55)

for i, col in enumerate(temp_cols):
    # Calculate Time to Failure (TTF)
    # Find the first index where temperature exceeds threshold
    failure_mask = df[col] >= CRITICAL_THRESHOLD
    
    if failure_mask.any():
        ttf_index = df[failure_mask].index[0]
        ttf_seconds = df.loc[ttf_index, time_col]
        steady_state_temp = df[col].iloc[0]
        
        ttf_results[col] = ttf_seconds
        
        # Plotting the line
        plt.plot(df[time_col], df[col], label=f"{col} (TTF: {ttf_seconds:.1f}s)", 
                 color=colors(i), linewidth=2)
        
        # Mark the failure point on the graph
        plt.scatter(ttf_seconds, CRITICAL_THRESHOLD, color='white', zorder=5)
        
        print(f"{col:<20} | {steady_state_temp:>10.1f}°C | {ttf_seconds:>12.1f}s")
    else:
        plt.plot(df[time_col], df[col], label=f"{col} (No Failure)", 
                 color='green', linestyle='--')
        print(f"{col:<20} | {df[col].iloc[0]:>10.1f}°C | {'SAFE':>12}")

# --- 3. FORMATTING THE DASHBOARD ---
plt.axhline(CRITICAL_THRESHOLD, color='red', linestyle='--', linewidth=1.5, label='Shutdown Limit (35°C)')
plt.fill_between(df[time_col], CRITICAL_THRESHOLD, df[temp_cols].max().max() + 5, 
                 color='red', alpha=0.1)

plt.title('Transient Cooling Failure: 50% Fan Speed Scenario', fontsize=14, color='#00b894')
plt.xlabel('Time Since Fan Failure (Seconds)', fontsize=12)
plt.ylabel('Inlet Temperature (°C)', fontsize=12)
plt.grid(True, which='both', linestyle=':', alpha=0.4)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)
plt.tight_layout()

# Save to AWS Dashboard
plt.savefig('time_to_failure.png', dpi=300)
print("-" * 55)
print("Graph saved as 'time_to_failure.png'.")
plt.show()