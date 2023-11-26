import sqlite3

import pytest

import bot_db


@pytest.fixture
def base_connection(tmp_path):
    base_path = tmp_path / "database.db"
    with sqlite3.connect(base_path) as con:
        cur = con.cursor()
        cur.execute(
            "create table users(id integer primary key autoincrement, user_id integer unique, user_join_date datetime not null default (datetime('now')))")
        cur.execute(
            "create table records(id integer primary key autoincrement, user_id integer not null, event text not null, event_time datetime not null, changing_date datetime not null default (datetime('now')), foreign key (user_id) references users (id))")

    base_bot = bot_db.BotDB(base_path)
    return base_bot


def test_add_user(base_connection: bot_db.BotDB):
    base_connection.add_user(2)
    assert base_connection.is_user_in_db(2)


def test_add_user_2(base_connection: bot_db.BotDB):
    base_connection.add_user(2)
    assert base_connection.get_user_id(2) == 1


class Message:
    class FromUser:
        def __init__(self, user_id):
            self.id = user_id

    def __init__(self, user_id, text):
        self.text = text
        self.from_user = self.FromUser(user_id)


def test_event(base_connection: bot_db.BotDB):
    base_connection.add_user(1)
    mes = Message(1, "abc 2024 01 01 00 00")
    base_connection.add_event(mes)
    res = base_connection.get_events(1, "all")
    assert "abc" in [x[2] for x in res]
