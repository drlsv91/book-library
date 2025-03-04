import redis
import json
from app.core.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# Publisher
def publish_event(channel: str, message: dict):
    redis_client.publish(channel, json.dumps(message))


# Listener
def listen_for_events():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("frontend_events")
    for message in pubsub.listen():
        if message["type"] == "message":
            event = json.loads(message["data"])
            print(f"Frontend API received event: {event}")
