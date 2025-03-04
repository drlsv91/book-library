import redis
import json
from sqlmodel import Session, select
from app.api.deps import get_db
from app.core.config import settings
from app.models import User

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# Publisher
def publish_event(channel: str, message: dict):
    redis_client.publish(channel, json.dumps(message))


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
        statement = select(User).where(User.email == payload.get("email"))
        user_exist = session.exec(statement).first()
        if user_exist:
            print(f"User with email {payload.get('email')} already enrolled.")
            return None

        print(f"payload=>{payload}")
        user_create = User.model_validate(payload)
        print(f"create user=>{user_create}")
        session.add(user_create)
        session.commit()
        session.refresh(user_create)
        print(f"User with email {payload.get('email')} enrolled.")
        return user_create
    except Exception as e:
        print(f"Error: {e}")

    finally:
        session.close()
