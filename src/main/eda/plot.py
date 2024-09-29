import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.main.utils.commons import PathUtils


def client_inquiries(data, file_path):
    data['weekday'] = data['chat_sessions'].apply(lambda x: x[0]['messages']['weekday'])
    data['hour'] = data['chat_sessions'].apply(lambda x: x[0]['messages']['hour'])

    heatmap_data = pd.crosstab(data['hour'], data['weekday'])

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt="d")
    plt.title('Client Inquiries: Heatmap by Weekday and Hour')
    plt.xlabel('Day of the Week (0=Monday, 6=Sunday)')
    plt.ylabel('Hour of Day')
    plt.tight_layout()
    plt.savefig(PathUtils.RESOURCES / "plots" / f"{file_path.stem}.png")




if __name__ == '__main__':
    data_folder = [PathUtils.RESOURCES / "topics_with_time" / file for file in
                   os.listdir(PathUtils.RESOURCES / "topics_with_time")]

    for file_path in data_folder:
        data = pd.read_json(file_path, orient='index')
        client_inquiries(data, file_path)