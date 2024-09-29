import json
import os
from multiprocessing import Pool, cpu_count
from pathlib import Path

from dotenv import load_dotenv
from wordllama import WordLlama

from src.main.utils.commons import PathUtils, LLMUtils
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
        message_df["minute"] = message_df["timestamp"].dt.minute
        message_df["second"] = message_df["timestamp"].dt.second
        message_df["microsecond"] = message_df["timestamp"].dt.microsecond
        message_df["quarter"] = message_df["timestamp"].dt.quarter
        message_df.drop(["timestamp"], axis=1, inplace=True)

        second_df["year"] = second_df["timestamp"].dt.year
        second_df["month"] = second_df["timestamp"].dt.month
        second_df["day"] = second_df["timestamp"].dt.day
        second_df["weekday"] = second_df["timestamp"].dt.weekday
        second_df["hour"] = second_df["timestamp"].dt.hour
        second_df["minute"] = second_df["timestamp"].dt.minute
        second_df["second"] = second_df["timestamp"].dt.second
        second_df["microsecond"] = second_df["timestamp"].dt.microsecond
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
    return df


def add_topic_info(file_path: Path):
    file_name = file_path.stem
    output_path = PathUtils.RESOURCES / "topics" / f"{file_name}.json"
    if output_path.exists():
        return
    print(f"Working on {file_path}")

    # Load the dataframe
    df = pd.read_json(file_path, orient="index")
    print(f"df shape 0: {df.shape[0]}")
    print(f"df len: {len(df)}")
    print(f"df shape 1: {df.shape[1]}")

    # Ensure 'topic_data' column exists and is initialized with None
    if "topic_data" not in df.columns:
        df["topic_data"] = None

    for index in df["chat_sessions"].index:
        print(f"Parsing topic data for index {index}, full index: {len(df['chat_sessions'][index])}")
        messages = "".join(json.dumps(df["chat_sessions"][index]))

        topic_data = LLMUtils.extract_topic(messages)

        if topic_data.startswith("```json"):
            topic_data_json = topic_data[7:-3]
        else:
            topic_data_json = topic_data

        try:
            topic_data_json = json.loads(topic_data_json)
        except ValueError as e:
            print(f"ERROR: {e}")
            topic_data_json = None

        # Assign the extracted topic data back to the dataframe
        df.at[index, "topic_data"] = topic_data_json

    df.to_json(output_path, orient="index")
    return df


def cluster_topics(file_path: Path, k: int = 130):
    wl = WordLlama.load()
    docs = []
    data = pd.read_json(file_path, orient='index')
    data['topic'] = data['topic_data'].apply(lambda x: x['topic'] if 'topic' in x else None)
    topics = data['topic'].dropna().unique()
    topics_str = [str(topic) for topic in topics]
    docs.extend(topics_str)
    labels, inertia = wl.cluster(docs, k=k, max_iterations=100, tolerance=1e-4)

    # Create a dictionary to store topics for each cluster
    cluster_topics = {i: [] for i in range(k)}

    # Assign each topic to its corresponding cluster
    for topic, label in zip(docs, labels):
        cluster_topics[label].append(topic)

    # Print topics for each cluster
    for cluster, topics in cluster_topics.items():
        print(f"Cluster {cluster}:")
        for topic in topics:
            print(f"  - {topic}")
        print()

    print("Inertia:", inertia)
    return labels, cluster_topics, inertia


def pipeline(file_path: Path):
    transform_raw_data(file_path)
    add_translate(file_path)
    add_topic_info(file_path)


if __name__ == '__main__':
    load_dotenv(dotenv_path=PathUtils.ENV_FILE)
    data_folder = [PathUtils.RESOURCES / "topics_with_time" / file for file in
                   os.listdir(PathUtils.RESOURCES / "topics_with_time")]
    num_processes = max(1, int(cpu_count() * 0.70))

    # with Pool(num_processes) as pool:
    #     pool.map(add_topic_info, [(file_path) for file_path in data_folder])
