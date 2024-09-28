import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

from dotenv import load_dotenv

from src.main.utils.commons import PathUtils, LLMUtils
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


def add_translate(file_path: Path):
    print(f"Working on {file_path}")
    df = pd.read_json(file_path, orient="index")
    for index in df["chat_sessions"].index:
        second_df = pd.DataFrame(df["chat_sessions"][index])
        first_msg = second_df.messages[0]["message"]
        input_lang = {"input_lang": LLMUtils.identify_language(first_msg)}
        for i, message_metadata in enumerate(second_df["messages"]):
            if not input_lang["input_lang"].lower().startswith("eng"):
                translated_msg = LLMUtils.translate_text(message_metadata["message"], **input_lang)
            else:
                translated_msg = message_metadata["message"]
            message_metadata["message_en"] = translated_msg
            message_metadata["input_lang"] = input_lang["input_lang"]
        df["chat_sessions"][index] = second_df.to_dict("records")
    file_name = file_path.stem
    output_path = PathUtils.RESOURCES / "translated" / f"{file_name}.json"
    df.to_json(output_path, orient="index")


if __name__ == '__main__':
    load_dotenv(dotenv_path=PathUtils.ENV_FILE)
    data_folder = [PathUtils.OUTPUT / file for file in os.listdir(PathUtils.OUTPUT)]
    # for file_path in data_folder:
    #     transform_raw_data(file_path)
    # print("All done")

    # Determine the number of processes to use (use 75% of available CPUs)
    num_processes = max(1, int(cpu_count() * 0.75))

    # Create a pool of worker processes
    with Pool(num_processes) as pool:
        pool.map(add_translate, [(file_path) for file_path in data_folder])
