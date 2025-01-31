import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.ExcelFile("Karbonatisierungstiefen_20%-CO2_20160714.xlsx")
a1 = pd.read_excel(data, "A1-0,75")

carb_depth_a1 = a1.values[2:, 7]
carb_depth_a1_in_time_chunks = [carb_depth_a1[i:i + 20] for i in range(0, len(carb_depth_a1), 20)]

sns.boxplot(carb_depth_a1_in_time_chunks[0])
sns.swarmplot(carb_depth_a1_in_time_chunks[0])

plt.show()
