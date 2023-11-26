import sqlite3
import datetime

DELTA_UTC = datetime.timedelta(hours=3)


class BotDB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        self.cursor.execute('INSERT INTO "users" ("user_id") VALUES(?)', (user_id,))
        self.connection.commit()

    def is_user_in_db(self, user_id):
        result = self.cursor.execute('SELECT "id" FROM "users" WHERE "user_id" = ?', (user_id,))
        self.connection.commit()
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute('SELECT "id" FROM "users" WHERE "user_id" = ?', (user_id,))
        self.connection.commit()
        return result.fetchone()[0]

    def add_event(self, message):
        user_id = message.from_user.id
        text = message.text.split()
        event = ' '.join(text[:-5])
        event_time = datetime.datetime(int(text[-5]), int(text[-4]), int(text[-3]), int(text[-2]),
                                       int(text[-1])) - DELTA_UTC
        self.cursor.execute('INSERT INTO "records" ("user_id", "event", "event_time") VALUES (?,?,?)',
                            (self.get_user_id(user_id), event, event_time))
        self.connection.commit()

    def get_events(self, user_id, within):
        if within == 'day':
            result = self.cursor.execute('SELECT * FROM "records" WHERE "user_id" = ?  AND "event_time" '
                                         "BETWEEN datetime('now') AND datetime('now','start of day', '1 days', '-3 hours') order by 'event_time'",
                                         (self.get_user_id(user_id),))
            self.connection.commit()
        elif within == 'month':
            result = self.cursor.execute('SELECT * FROM "records" WHERE "user_id" = ?  AND "event_time" '
                                         "BETWEEN datetime('now') AND datetime('now','start of month', '1 months', '-3 hours') order by 'event_time'",
                                         (self.get_user_id(user_id),))
            self.connection.commit()
        else:
            result = self.cursor.execute('SELECT * FROM "records" WHERE "user_id" = ? order by "event_time"', (self.get_user_id(user_id),))
            self.connection.commit()
        return result.fetchall()

    def close(self):
        self.connection.close()
