import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

new_dict = {
    "A1-075" : [1,2,3,344,35,4,4565,76,7],
    "B" : 1
}

# new_dict.keys()
# list_keys = ["A", "B"]

# for list_value in list_keys:
#     print(list_value)

# new_dict.values()
# list_values = [0, 1]

# new_dict["A"] # = 0
# string = "test"
# int = 0
# float = 0.0
# char = 'a'
# list = []
# dict = {}
# boolean = True oder False

data = pd.ExcelFile("Karbonatisierungstiefen_20%-CO2_20160714.xlsx")
data_sheets = pd.read_excel(data, sheet_name=None)
probe_sheet_keys = list(data_sheets.keys())[3:]

dataMod = pd.ExcelFile("xc_results-modelling_20250130.xlsx")
a1Mod = pd.read_excel(dataMod, "Results")
x = a1Mod.iloc[:,66]
y = a1Mod.iloc[:,67] * 1000

for probe_key in probe_sheet_keys:
    plt.figure()
    fig, ax = plt.subplots(figsize=(10, 6))

    plt.plot(x,y, zorder=3)
    carb_depth_of_sheet = data_sheets[probe_key].values[2:, 7]
    time_days = pd.Series(data_sheets[probe_key].values[2:, 3])
    time_days = time_days.dropna().values
    
    carb_depth_of_sheet_chunked = [carb_depth_of_sheet[i:i + 20] for i in range(0, len(carb_depth_of_sheet), 20)]
    
    check_all_nan = np.array(carb_depth_of_sheet_chunked)
    rows_all_nan = np.all(np.isnan(check_all_nan.astype(float)), axis=1)
    time_days_selected = time_days[~rows_all_nan]

    
    flattened_carb_depths =  [value for sublist in carb_depth_of_sheet_chunked for value in sublist]
    # jitter = np.random.normal(0, 0.2, size=len(flattened_carb_depths))
    flattened_time_values = np.repeat(time_days, 20) # + jitter
    
    sns.boxplot(carb_depth_of_sheet_chunked, positions=time_days_selected, color='grey', medianprops={'color': 'red', 'linewidth': 2},ax=ax, zorder=1)
    ax.scatter(y=flattened_carb_depths, x=flattened_time_values, color='black', alpha=0.5, zorder=2)
    ax.set_xticks([str(i) for i in np.arange(0, time_days_selected[-1] + 1, 1)])
    plt.title("Plots of all times in sheet " + probe_key)
    os.makedirs(name="plots_20CO2", exist_ok=True)
    plt.savefig("plots_20CO2/plots_for_"+probe_key+"-20CO2.png")
