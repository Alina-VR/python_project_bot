import sqlite3
import datetime

DELTA_UTC = datetime.timedelta(hours=3)


class BotDB:
    """A class for connecting telegram bot with database sqlite3
    """

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        """A function that add user that write message to bot to database

        :param user_id: int
        :return: None
        """
        self.cursor.execute('INSERT INTO "users" ("user_id") VALUES(?)', (user_id,))
        self.connection.commit()

    def is_user_in_db(self, user_id):
        """A function that checks is this user in database

        :param user_id: int
        :return: bool
        """
        result = self.cursor.execute('SELECT "id" FROM "users" WHERE "user_id" = ?', (user_id,))
        self.connection.commit()
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """A function that takes user id of this user from telegram and gives id of this user from database
        (that is less and simpler)

        :param user_id: int
        :return: int
        """
        result = self.cursor.execute('SELECT "id" FROM "users" WHERE "user_id" = ?', (user_id,))
        self.connection.commit()
        return result.fetchone()[0]

    def add_event(self, message):
        """A function that add event and event time from user's message to the database

        :param message: Message
        :return: None
        """
        user_id = message.from_user.id
        text = message.text.split()
        event = ' '.join(text[:-5])
        event_time = datetime.datetime(int(text[-5]), int(text[-4]), int(text[-3]), int(text[-2]),
                                       int(text[-1])) - DELTA_UTC
        self.cursor.execute('INSERT INTO "records" ("user_id", "event", "event_time") VALUES (?,?,?)',
                            (self.get_user_id(user_id), event, event_time))
        self.connection.commit()

    def get_events(self, user_id, within):
        """A function that get events that user has recorded and that take place within specified period of time

        :param user_id: int
        :param within: str
        :return: list
        """
        if within == 'day':
            result = self.cursor.execute('SELECT * FROM "records" WHERE "user_id" = ?  AND "event_time" '
                                         "BETWEEN DATETIME('now') AND DATETIME('now','start of day', '1 days', "
                                         "'-3 hours') ORDER BY 'event_time'",
                                         (self.get_user_id(user_id),))
            self.connection.commit()
        elif within == 'month':
            result = self.cursor.execute('SELECT * FROM "records" WHERE "user_id" = ?  AND "event_time" '
                                         "BETWEEN DATETIME('now') AND DATETIME('now','start of month', '1 months', "
                                         "'-3 hours') ORDER BY 'event_time'",
                                         (self.get_user_id(user_id),))
            self.connection.commit()
        else:
            result = self.cursor.execute('SELECT * FROM "records" WHERE "user_id" = ? order by "event_time"',
                                         (self.get_user_id(user_id),))
            self.connection.commit()
        return result.fetchall()

    def close(self):
        """A function that close connection with database

        :return: None
        """
        self.connection.close()
