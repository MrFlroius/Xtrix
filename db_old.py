import time
import sqlite3
from config import DatabaseConfig

admin = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
             delete_self=1,
             upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=1, delete_files=1,
             create_tags=1, use_service_tags=1, read_logs=1, change_logs=1, change_posts=1, delete_posts=1,
             ban_users=1, permanent_ban_users=1, change_users=1, delete_users=1)

moderator = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
                 delete_self=1,
                 upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=1,
                 delete_files=1,
                 create_tags=1, use_service_tags=1, read_logs=0, change_logs=0, change_posts=1, delete_posts=1,
                 ban_users=1, permanent_ban_users=0, change_users=0, delete_users=0)

senior_moderator = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
                        delete_self=1,
                        upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=1,
                        delete_files=1,
                        create_tags=1, use_service_tags=1, read_logs=0, change_logs=0, change_posts=1,
                        delete_posts=1,
                        ban_users=1, permanent_ban_users=0, change_users=0, delete_users=0)

user = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
            delete_self=1,
            upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=0, delete_files=0,
            create_tags=0, use_service_tags=0, read_logs=0, change_logs=0, change_posts=0, delete_posts=0,
            ban_users=0, permanent_ban_users=0, change_users=0, delete_users=0)

class Logger(object):
    """docstring for Logger."""
    def __init__(self, fname:str):
        self.fname = str

    def is_sql_request(s: str):
        pass

    def log(s: str):
        pass


class SQLBaseUtil:
    def __init__(self, db: str):
        self.connection = sqlite3.connect(db, check_same_thread=False, isolation_level='EXCLUSIVE')
        self.cursor = self.connection.cursor()

    def drop_all(self):
        with self.connection:
            script = ""
            for command in self.cursor.execute("SELECT 'DROP TABLE ' || name || ';\n' "
                                               "FROM sqlite_master WHERE type = 'table'"):
                script += (command[0]) if 'sqlite_sequence' not in command[0] else ''
            self.cursor.executescript(script)
        self.connection.commit()

    def reset(self):
        self.drop_all()
        with self.connection:
            self.cursor.executescript(DatabaseConfig.reset_request)
            self.connection.commit()

    @staticmethod
    def timestamp():
        """return: current timestamp in unix format"""
        return int(time.time())

class SQLUtil(SQLBaseUtil):
    """piece of shit, not to use"""

    def new_user(self, user_id: int, user_name: str, user_rating=0):
        """creates new user
        user_id: telegram user_id
        user_name: custom user name, up to user_name_limit"""
        if len(user_name) < self.user_name_limit:
            try:
                with self.connection:
                    self.cursor.execute("INSERT INTO users (user_id, user_name, user_rating, user_creation_date) "
                                        "VALUES (?, ?, ?, ?)", (user_id, user_name, user_rating,))
            except sqlite3.Error as e:
                if e.args == ('UNIQUE constraint failed: users.user_id',):
                    raise ValueError('User with user_id {user_id} already exist'.format(user_id=user_id))
        else:
            raise ValueError('User_name \'{user_name}\' is too long(len(user_name) > {limit}'.
                             format(user_name=user_name, limit=self.user_name_limit))

    def bind_user_to_group(self, user_id, group_id):
        with self.connection:
            self.cursor.execute("INSERT INTO users_gropups (user_id, group_id) VALUES (?, ?)", (user_id, group_id,))
        self.connection.commit()

    def get_user(self, user_id: int):
        return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()[0]

    def is_allowed(self, permission, user_id):
        with self.connection:
            return True if self.cursor.execute(
                "SELECT {permission} FROM groups INNER JOIN users_gropups WHERE user_id = ?".format(
                    permission=permission),
                (user_id,)) else False

    def insert_permissions(self, name, group_author, permission: dict):
        with self.connection:
            try:
                script = "INSERT INTO groups ({column}, group_creation_date, group_name, group_author) " \
                         "VALUES ({value}, ?, ?, ?)". \
                    format(column=", ".join(list(permission.keys())),
                           value=" ,".join(map(str, list(permission.values()))))
                self.cursor.execute(script, (self.timestamp(), name, group_author))
                self.connection.commit()
            except sqlite3.Error as e:
                self.connection.rollback()
                raise e

    def new_post(self, name, author, text, rating=0):
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO main.posts (post_name, post_author, post_rating, post_text, post_creation_date) "
                    "VALUES (?, ?, ?, ?, ?)", (name, author, rating, text, self.timestamp()))
                self.connection.commit()
            except sqlite3.Error as e:
                self.connection.rollback()
                raise e

    def new_tag(self, name, author, rating=0):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO tags (tag_name, tag_author, tag_rating, tag_creation_date) "
                                    "VALUES (?, ?, ?, ?)", (name, author, rating, self.timestamp()))
                self.connection.commit()
            except sqlite3.Error as e:
                self.connection.rollback()
                raise e

    def bind_tag_to_post(self, tag_id, post_id):
        with self.connection:
            try:
                self.cursor.execute("INSERT INTO tags_posts (tag_id, post_id) VALUES (?, ?)", (tag_id, post_id))
                self.connection.commit()
            except sqlite3.Error as e:
                self.connection.rollback()
                raise e

    def get_post(self, post_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM posts")
