# plot_results.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("benchmark_results.json", lines=True)

plt.figure(figsize=(10, 5))
plt.bar(df["model"], df["avg_tps"], color="skyblue")
plt.title("Average TPS by Model")
plt.ylabel("Tokens Per Second (TPS)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("tps_by_model.png")
plt.show()
