import os
from src.main.utils.commons import PathUtils
import pandas as pd

def translate(text_to_translate: str, input_lang, output_lang="English") -> str:
    pass

if __name__ == '__main__':
    data_folder = [PathUtils.DATA / file for file in os.listdir(PathUtils.DATA)]
    for file_path in data_folder:
        print(f"Working on {file_path}")
        df = pd.read_json(file_path, orient="records")
        for index in df["chat_sessions"].index:
            second_df = pd.DataFrame(df["chat_sessions"][index])
            second_df["timestamp"] = pd.to_datetime(second_df["timestamp"])

            # Process 'timestamp' in second_df
            second_df["year"] = second_df["timestamp"].dt.year
            second_df["month"] = second_df["timestamp"].dt.month
            second_df["day"] = second_df["timestamp"].dt.day
            second_df["hour"] = second_df["timestamp"].dt.hour
            second_df["quarter"] = second_df["timestamp"].dt.quarter
            second_df.drop(["timestamp"], axis=1, inplace=True)

            # Explode the 'messages' column
            second_df = second_df.explode('messages').reset_index(drop=True)
            print(second_df.info())

            # # Normalize the 'messages' data
            # messages_normalized = pd.json_normalize(second_df["messages"])
            # print(messages_normalized.head())
            # print(messages_normalized.info())
            # messages_normalized["timestamp"] = pd.to_datetime(messages_normalized["timestamp"])
            #
            # # Process 'timestamp' in messages_normalized
            # messages_normalized["year"] = messages_normalized["timestamp"].dt.year
            # messages_normalized["month"] = messages_normalized["timestamp"].dt.month
            # messages_normalized["day"] = messages_normalized["timestamp"].dt.day
            # messages_normalized["hour"] = messages_normalized["timestamp"].dt.hour
            # messages_normalized["quarter"] = messages_normalized["timestamp"].dt.quarter
            # messages_normalized.drop(["timestamp"], axis=1, inplace=True)
            #
            # # Concatenate second_df and messages_normalized
            # second_df = second_df.drop(columns=['messages']).reset_index(drop=True)
            # second_df = pd.concat([second_df, messages_normalized], axis=1)
            #
            # print(second_df.info())
            #
            # # Update the original DataFrame
            # df.at[index, "chat_sessions"] = second_df.to_dict(orient='records')
            #
            # # Save to JSON
            # df["chat_sessions"].head().to_json("test.json")
            break
        break
