import os
from pathlib import Path

from src.main.utils.commons import PathUtils
import json
import pandas as pd


def transform_raw_data(file_path: Path):
    print(f"Working on {file_path}")
    df = pd.read_json(file_path, orient="records")
    for index in df["chat_sessions"].index:
        second_df = pd.DataFrame(df["chat_sessions"][index])
        second_df["timestamp"] = pd.to_datetime(second_df["timestamp"])
        message_data = []
        for message in second_df["messages"]:
            message_data.append(message)
        message_df = pd.DataFrame(message_data)

        message_df["timestamp"] = pd.to_datetime(message_df["timestamp"])
        message_df["year"] = message_df["timestamp"].dt.year
        message_df["month"] = message_df["timestamp"].dt.month
        message_df["day"] = message_df["timestamp"].dt.day
        message_df["weekday"] = message_df["timestamp"].dt.weekday
        message_df["hour"] = message_df["timestamp"].dt.hour
        message_df["quarter"] = message_df["timestamp"].dt.quarter
        message_df.drop(["timestamp"], axis=1, inplace=True)

        second_df["year"] = second_df["timestamp"].dt.year
        second_df["month"] = second_df["timestamp"].dt.month
        second_df["day"] = second_df["timestamp"].dt.day
        second_df["weekday"] = second_df["timestamp"].dt.weekday
        second_df["hour"] = second_df["timestamp"].dt.hour
        second_df["quarter"] = second_df["timestamp"].dt.quarter
        second_df.drop(["timestamp"], axis=1, inplace=True)

        second_df["messages"] = message_df.to_dict("records")
        df["chat_sessions"][index] = second_df.to_dict("records")
    file_name = file_path.stem
    output_path = PathUtils.OUTPUT / f"{file_name}.json"
    df.to_json(output_path, orient="index")


def translate(text_to_translate: str, input_lang, output_lang="English") -> str:
    pass


if __name__ == '__main__':
    data_folder = [PathUtils.DATA / file for file in os.listdir(PathUtils.DATA)]
    for file_path in data_folder:
        transform_raw_data(file_path)
    print("All done")
