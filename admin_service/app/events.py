import redis
import json
from sqlmodel import Session, select
from app.core.db import engine
from app.core.config import settings
from app.models import User
from typing import List
from app.models import Book, BorrowedBook, BorrowedBookCreate

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
            if event_data["event"] == "new_borrowed_book":

                borrow_book(event_data["data"])


def enroll_user(payload: dict):

    with Session(engine) as session:
        statement = select(User).where(User.email == payload.get("email"))
        user_exist = session.exec(statement).first()
        if user_exist:
            print(f"User with email {payload.get('email')} already enrolled.")
            return None

        user_create = User.model_validate(payload)

        session.add(user_create)
        session.commit()
        session.refresh(user_create)
        print(f"User with email {payload.get('email')} enrolled.")
        return user_create


def borrow_book(payload: List[dict]):
    print(f"New borrowed book: {payload}")
    with Session(engine) as session:
        create_data = []
        for item in payload:
            statement = select(Book).where(Book.id == item["book_id"])
            book = session.exec(statement).first()
            if not book:
                print(f"Book with id {item['book_id']} not found.")
                continue
            borrow_book_data = BorrowedBookCreate(**item)
            db_borrowed_book = BorrowedBook.model_validate(
                borrow_book_data,
                update={
                    "user_id": item["user_id"],
                    "return_date": item["return_date"],
                    "book_id": book.id,
                    "period_in_days": item["period_in_days"],
                },
            )

            book.sqlmodel_update(
                {"is_available": False, "available_date": item["return_date"]}
            )
            create_data.append(db_borrowed_book)

        session.add_all(create_data)
        session.commit()
        print(f"NEW books({len(create_data)}) uploaded")
