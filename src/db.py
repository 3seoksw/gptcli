import os
import icons
from tinydb import TinyDB, Query


def init_db(chat_log):
    db = TinyDB(chat_log)
    counter = max([row["_id"] for row in db], default=0)
    DB_info = {"db": db, "counter": counter}
    return DB_info


def generate_unique_ID(counter):
    counter += 1
    return counter


def init_chat_log(DB_info, preset, messages):
    db = DB_info["db"]
    counter = DB_info["counter"]

    _id = generate_unique_ID(counter)

    db.insert(
        {
            "_id": _id,
            "title": "Untitled",
            "preset": preset,
            "messages": messages,
        }
    )

    return _id


def db_message_append(db, _id, messages):
    db.update({"messages": messages}, Query()._id == _id)


def db_update_title(db, _id, title):
    db.update({"title": title}, Query()._id == _id)


def db_get_messages(db, _id):
    return db.search(Query()._id == _id)[0]["messages"]


def db_get_title(db, _id):
    return db.search(Query()._id == _id)[0]["title"]


def db_get_all_chats(db):
    return db.all()


def db_get_db_by_id(db, _id):
    return db.search(Query()._id == _id)[0]
