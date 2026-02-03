sessions = {}

def get_session(user_id: str):
    if user_id not in sessions:
        sessions[user_id] = {
            "history": [],
            "state": {}
        }
    return sessions[user_id]
