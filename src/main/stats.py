import os.path
import json


def count_languages(files):
    files = [os.path.join(files, file) for file in os.listdir(files)]
    data = {}
    for file in files:
        json_data = json.load(open(file))
        for session_id in json_data:
            messages = json_data[session_id]["chat_sessions"]
            for message in messages:
                key = message["messages"]["input_lang"].lower()
                if key == "typescript":
                    print(file)
                if key not in data:
                    data[key] = 1
                else:
                    data[key] += 1
    print(sorted(data.items(), key=lambda x: x[1], reverse=True))


def count_messages_per_client_id(files):
    files = [os.path.join(files, file) for file in os.listdir(files)]

    message_count_per_client = {}
    for file in files:
        json_data = json.load(open(file))
        # Loop through the data and count messages for each client_id
        for session_id, session_data in json_data.items():
            client_id = session_data['client_id']
            chat_sessions = session_data.get('chat_sessions', [])

            # Count messages in the chat_sessions
            message_count = sum(1 for session in chat_sessions if 'messages' in session)

            # Add to the dictionary
            if client_id in message_count_per_client:
                message_count_per_client[client_id] += message_count
            else:
                message_count_per_client[client_id] = message_count

    with open("message_count_per_client.json", "w") as outfile:
        json.dump(sorted(message_count_per_client.items(), key=lambda x: x[1], reverse=True), outfile)
    print(sorted(message_count_per_client.items(), key=lambda x: x[1], reverse=True))


def count_messages_per_user_id(files):
    files = [os.path.join(files, file) for file in os.listdir(files)]

    message_count_per_user_id = {}
    for file in files:
        json_data = json.load(open(file))
        # Loop through the data and count messages for each client_id
        for session_id, session_data in json_data.items():
            user_id = session_data['user_id']
            chat_sessions = session_data.get('chat_sessions', [])

            # Count messages in the chat_sessions
            message_count = sum(1 for session in chat_sessions if 'messages' in session)

            # Add to the dictionary
            if user_id in message_count_per_user_id:
                message_count_per_user_id[user_id] += message_count
            else:
                message_count_per_user_id[user_id] = message_count

    with open("message_count_per_user_id.json", "w") as outfile:
        json.dump(sorted(message_count_per_user_id.items(), key=lambda x: x[1], reverse=True), outfile)
    print(sorted(message_count_per_user_id.items(), key=lambda x: x[1], reverse=True))


def count_messages_per_name(files):
    files = [os.path.join(files, file) for file in os.listdir(files)]

    message_count_per_user_id = {}
    for file in files:
        json_data = json.load(open(file))
        # Loop through the data and count messages for each client_id
        for session_id, session_data in json_data.items():
            user_id = session_data['name']
            chat_sessions = session_data.get('chat_sessions', [])

            # Count messages in the chat_sessions
            message_count = sum(1 for session in chat_sessions if 'messages' in session)

            # Add to the dictionary
            if user_id in message_count_per_user_id:
                message_count_per_user_id[user_id] += message_count
            else:
                message_count_per_user_id[user_id] = message_count

    with open("message_count_per_name.json", "w") as outfile:
        json.dump(sorted(message_count_per_user_id.items(), key=lambda x: x[1], reverse=True), outfile)
    print(sorted(message_count_per_user_id.items(), key=lambda x: x[1], reverse=True))


def agents_count_per_user_id(files):
    files = [os.path.join(files, file) for file in os.listdir(files)]

    agents_count_per_user_id = {}
    for file in files:
        json_data = json.load(open(file))
        for session_id, session_data in json_data.items():
            if session_data["user_id"] not in agents_count_per_user_id:
                agents_count_per_user_id[session_data["user_id"]] = set()
            agents_count_per_user_id[session_data["user_id"]].add(session_data["client_id"])
    for user_id in agents_count_per_user_id:
        agents_count_per_user_id[user_id] = len(agents_count_per_user_id[user_id])
    with open("agents_count_per_user_id.json", "w") as outfile:
        json.dump(sorted(agents_count_per_user_id.items(), key=lambda x: x[1], reverse=True), outfile)
    print(sorted(agents_count_per_user_id.items(), key=lambda x: x[1], reverse=True))
    print(len(agents_count_per_user_id))

if __name__ == '__main__':
    files = "/Users/mcoslet/PycharmProjects/gigahack_27_09_2024/src/resources/translated/"
    agents_count_per_user_id(files)
