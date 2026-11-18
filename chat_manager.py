import uuid
from datetime import datetime


def create_thread():

    thread_id = str(uuid.uuid4())

    return {
        "thread_id": thread_id,
        "title": "New Chat",
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M"),
    }


def generate_title(message):

    return " ".join(message.strip().split()[:5]).capitalize()