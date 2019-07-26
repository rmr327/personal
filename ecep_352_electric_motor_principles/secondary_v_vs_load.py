import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# These calculations are done using an equivalent
# circuit referred to the primary side.
# Define values for this transformer

vp = 15000  # Primary voltage (V)
amps = list(range(0, 12501, 125))  # Current values (A)
req = 0.018  # Equivalent R (ohms)
xeq = 0.075  # Equivalent X (ohms)

# Calculate the current values for the three
# power factors. The first row of I contains
# the lagging currents, the second row contains
# the unity currents, and the third row contains
# the leading currents.
i = pd.DataFrame(np.zeros((3, len(amps))))

i.iloc[0, :] = [amps[o] * complex(0.8, -0.6) for o in range(len(amps))]  # Lagging
i.iloc[1, :] = amps * 1  # Unity
i.iloc[2, :] = [amps[o] * complex(0.8, 0.6) for o in range(len(amps))]   # Leading

# Calculate VS referred to the primary side
# for each current and power factor.
a_vs = pd.DataFrame(np.zeros((3, len(amps))))
a_vs.iloc[0, :] = [vp - complex(req*i.iloc[0, o], xeq*i.iloc[0, o]) for o in range(len(amps))]  # Lagging
a_vs.iloc[1, :] = [vp - complex(req*i.iloc[1, o], xeq*i.iloc[1, o]) for o in range(len(amps))]  # Unity
a_vs.iloc[2, :] = [vp - complex(req*i.iloc[2, o], xeq*i.iloc[2, o]) for o in range(len(amps))]   # Leading


# Refer the secondary voltages back to the
# secondary side using the turns ratio.
vs = a_vs.multiply(200/15)

# Plot the secondary voltage (in kV!) versus load
plt.plot(amps, abs(vs.iloc[0, :]/1000), 'r-')
plt.plot(amps, abs(vs.iloc[1, :]/1000), 'k--')
plt.plot(amps, abs(vs.iloc[2, :]/1000), 'b-.')

plt.title('fSecondary Voltage Versus Load')
plt.xlabel('Load (A)')
plt.ylabel('Secondary Voltage (kV)')
plt.legend(('0.8 PF lagging', '1.0 PF', '0.8 PF leading'))

plt.ylim(190, 206)
plt.xlim(0, 14000)
plt.grid(True)
plt.show()
