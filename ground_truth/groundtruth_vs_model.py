import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('path/to/your/clean/groundtruth/file')
df2 = pd.read_csv('path/to/your/modelprediciton/file')

df2_distress = df2[df2['Prediction'] == 'Distress']

max_time_full = df1[['Column1', 'Column2']].max().max()
full_timeline = pd.DataFrame({'Time': range(0, max_time_full)})
full_timeline['Distress_Label'] = 0  # default label

# Label timepoints with 1 if Distress_Status == "Distress"
for _, row in df1.iterrows():
    if row['Distress_Status'] == 'Distress':
        full_timeline.loc[row['Column1']:row['Column2'] - 1, 'Distress_Label'] = 1

distress_times_only = full_timeline[full_timeline['Distress_Label'] == 1]['Time']

tick_interval = 5000
x_ticks = list(range(0, max_time_full + tick_interval, tick_interval))

fig, axs = plt.subplots(2, 1, figsize=(20, 6), sharex=True)

# Top plot: Ground truth (only distress points)
axs[0].scatter(distress_times_only, [1] * len(distress_times_only), color='red', s=10)
axs[0].set_title('Distress Events (Ground Truth)', fontsize=14)
axs[0].set_yticks([])
axs[0].set_xticks(x_ticks)
axs[0].grid(True)

# Bottom plot: Model predictions (only distress points)
axs[1].scatter(df2_distress['Second'], [1] * len(df2_distress), color='blue', s=10)
axs[1].set_title('Distress Events (Model Predictions)', fontsize=14)
axs[1].set_xlabel('Time (seconds)', fontsize=12)
axs[1].set_yticks([])
axs[1].set_xticks(x_ticks)
axs[1].grid(True)

plt.tight_layout()
plt.show()
