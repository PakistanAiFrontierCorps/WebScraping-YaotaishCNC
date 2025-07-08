#Step 2
import pandas as pd

df = pd.read_csv("fanuc_link.csv")

df["Link"] = "https://www.yaotaishcnc.com/" + df["Link"]

df.to_csv("input_urls.csv", index=False)