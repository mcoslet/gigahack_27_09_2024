import json
from collections import defaultdict


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def analyze_users(data):
    users = set()
    clients = set()
    user_sessions = defaultdict(set)
    user_messages = defaultdict(int)

    for session_id, session_data in data.items():
        user_id = session_data['user_id']
        client_id = session_data['client_id']

        users.add(user_id)
        clients.add(client_id)
        user_sessions[user_id].add(session_id)

        for message in session_data['chat_sessions']:
            if message['messages']['role'] == 'user':
                user_messages[user_id] += 1

    return {
        'unique_users': len(users),
        'unique_clients': len(clients),
        'sessions_per_user': {user: len(sessions) for user, sessions in user_sessions.items()},
        'messages_per_user': dict(user_messages)
    }


def print_analysis(analysis):
    print(f"Number of unique users: {analysis['unique_users']}")
    print(f"Number of unique clients: {analysis['unique_clients']}")

    print("\nSessions per user:")
    for user, sessions in analysis['sessions_per_user'].items():
        print(f"User {user}: {sessions} sessions")

    print("\nMessages per user:")
    for user, messages in analysis['messages_per_user'].items():
        print(f"User {user}: {messages} messages")

    avg_sessions = sum(analysis['sessions_per_user'].values()) / len(analysis['sessions_per_user'])
    print(f"\nAverage sessions per user: {avg_sessions:.2f}")

    avg_messages = sum(analysis['messages_per_user'].values()) / len(analysis['messages_per_user'])
    print(f"Average messages per user: {avg_messages:.2f}")


if __name__ == "__main__":
    file_path = 'your_json_file.json'  # Replace with your actual file path
    data = load_json_data(file_path)
    analysis_results = analyze_users(data)
    print_analysis(analysis_results)
