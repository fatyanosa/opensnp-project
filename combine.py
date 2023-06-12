import pathlib
import pandas as pd
import os
import subprocess

root_dir = pathlib.Path("data/")
data = {}
output_dir = "results/"

num_cols = 0
df = pd.DataFrame()
output = ""

if any(os.scandir(output_dir)):
    output = subprocess.check_output(
        "head -n1 -q " + output_dir + "*", shell=True
    ).decode("utf-8")
    num_cols = output.count(",")
for pth in root_dir.glob("*"):
    if pth.name in output:
        continue
    print(pth.name)
    data[pth.name] = pd.read_csv(pth, sep=",", header=0, names=["rsid", pth.name])
    if df.size == 0:
        df = data[pth.name]
    else:
        df = pd.merge(df, data[pth.name], on="rsid", how="outer")

    num_cols += 1
    if len(df.columns) - 1 == 100:
        df.to_csv(output_dir + "rs699_" + str(num_cols) + ".csv", index=False)
        df = pd.DataFrame()

    print(num_cols)

root_dir = pathlib.Path("results/")
data = {}
df = pd.DataFrame()
num_data = 0

for pth in root_dir.glob("*"):
    data[pth.name] = pd.read_csv(pth, sep=",")
    if df.size == 0:
        df = data[pth.name]
    else:
        df = pd.merge(df, data[pth.name], on="rsid", how="outer")

    num_data += 1
    print(num_data)

df.to_csv("data.csv", index=False)
