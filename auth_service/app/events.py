import redis
import json
from app.core.config import settings
from sqlmodel import select
from app.crud import get_user_by_email, create_user
from app.api.deps import get_db
from app.models import UserCreate

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# Listener
def listen_for_events():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("frontend_events")
    for message in pubsub.listen():
        print(message)
        if message["type"] == "message":
            event_data = json.loads(message["data"])
            print(f"Admin API received event: {event_data}")
            if event_data["event"] == "user_enrolled":
                print(f"User with email {event_data['user']['email']} enrolled.")
                enroll_user(event_data["user"])


def enroll_user(payload: dict):
    session = next(get_db())
    try:

        user_exist = get_user_by_email(session=session, email=payload.get("email"))
        if user_exist:
            print(f"User with email {payload.get('email')} already enrolled.")
            return None

        print(f"payload=>{payload}")
        create_payload = UserCreate(**payload)
        user_create = create_user(session=session, user_create=create_payload)
        print(f"User with email {payload.get('email')} enrolled.")
        return user_create
    except Exception as e:
        print(f"Error: {e}")

    finally:
        session.close()
