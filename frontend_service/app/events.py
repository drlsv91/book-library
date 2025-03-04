import redis
import json
from app.core.config import settings
from app.core.db import engine
from sqlmodel import Session, select
from app.models import Book

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# Publisher
def publish_event(channel: str, message: dict):
    redis_client.publish(channel, json.dumps(message))


# Listener
def listen_for_events():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("admin_events")
    for message in pubsub.listen():
        if message["type"] == "message":
            event_data = json.loads(message["data"])
            print(f"Frontend API received event: {event_data}")
            if event_data["event"] == "new_book":
                add_new_book(event_data["data"])
            if event_data["event"] == "delete_book":
                delete_book(event_data["data"])


def add_new_book(payload: dict):

    with Session(engine) as session:
        print(payload)

        book_create = Book.model_validate(payload)

        session.add(book_create)
        session.commit()
        session.refresh(book_create)
        print(f"book with title {payload.get('title')} added.")
        return book_create


def delete_book(payload: dict):
    with Session(engine) as session:
        statement = select(Book).where(Book.id == payload["id"])
        book = session.exec(statement).first()
        title = payload.get("title")
        if not book:
            print(f"book({title}) does not exist")
            return None

        session.delete(book)
        session.commit()
        print(f"book({title}) has been deleted succesfully")
        return 1
