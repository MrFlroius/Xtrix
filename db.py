import time
import sqlite3
from config import DatabaseConfig


__test_mode__ = True
__log_to_file__ = False

# administrator permissions, for admin group
admin = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
             delete_self=1,
             upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=1, delete_files=1,
             create_tags=1, use_service_tags=1, read_logs=1, change_logs=1, change_posts=1, delete_posts=1,
             ban_users=1, permanent_ban_users=1, change_users=1, delete_users=1)
# moderator permissions, for moderator group
moderator = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
                 delete_self=1,
                 upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=1,
                 delete_files=1,
                 create_tags=1, use_service_tags=1, read_logs=0, change_logs=0, change_posts=1, delete_posts=1,
                 ban_users=1, permanent_ban_users=0, change_users=0, delete_users=0)
# senior moderator permissions, for senior moderator group
senior_moderator = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
                        delete_self=1,
                        upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=1,
                        delete_files=1,
                        create_tags=1, use_service_tags=1, read_logs=0, change_logs=0, change_posts=1,
                        delete_posts=1,
                        ban_users=1, permanent_ban_users=0, change_users=0, delete_users=0)
# user permissions, for user group
user = dict(read_posts=1, write_posts=1, change_own_posts=1, delete_own_posts=1, change_self=1,
            delete_self=1,
            upload_files=1, use_files=1, change_own_files=1, delete_own_files=1, change_files=0, delete_files=0,
            create_tags=0, use_service_tags=0, read_logs=0, change_logs=0, change_posts=0, delete_posts=0,
            ban_users=0, permanent_ban_users=0, change_users=0, delete_users=0)


# sql_translate = lambda a: '\"{a}\"'.format(a=a) if type(a) == str elif  str(a)

def sql_translate(a):
    """translate elem for re to paste it in sql request
    a: elem
    return: translated elem"""
    if type(a) == str:
        return '\"{a}\"'.format(a=a)
    elif type(a) == bool:
        return '1' if a else '0'
    else:
        return str(a)


class BaseDBObj:
    """Base class for Users, Groups, etc; NB class Atributes name should be same with db table cols name"""
    __table__ = ''

    def __repr__(self):
        return str(vars(self))

    def __iter__(self):
        for a in vars(self).items():
            yield a

class Group(BaseDBObj): pass
class User(BaseDBObj): pass
class Post(BaseDBObj): pass
class Tag(BaseDBObj): pass
class Image(BaseDBObj): pass
class Ban(BaseDBObj): pass
class Comment(BaseDBObj): pass


class Group(BaseDBObj):
    """Group class
    group_id: id of current group, unique
    group_name: str
    group_author: User
    permissions: dict with keys same with col names in groups"""

    __table__ = 'groups'

    def __init__(self, group_id: int, group_name: str, group_author: User, permissions: dict):
        self.group_id = group_id
        self.group_name = group_name
        self._group_author_user = group_author
        self.group_author = group_author.user_id
        self.group_creation_date = SQLBaseUtil.timestamp()
        for a in permissions.items():
            setattr(self, a[0], a[1])


class User(BaseDBObj):
    """User class
    user_id: telegram user id
    user_name: str
    user_rating: rating of current user, float"""
    __table__ = 'users'

    def __init__(self, user_id: int, user_name: str, user_rating=0.0):
        self.user_id = user_id
        self.user_name = user_name
        self.user_rating = user_rating
        self.user_creation_date = SQLBaseUtil.timestamp()


class Post(BaseDBObj):
    """Post class
    post_id: current post id
    post_name: title of the post
    post_author: user creates the post
    post_rating: rating of current post, float
    post_text: main message"""
    __table__ = 'posts'

    def __init__(self, post_id: int, post_name: str, post_author: User,
                    post_rating: float, post_text: str):
        self.post_id = post_id
        self.post_name = post_name
        self.post_author = post_author
        self.post_rating  = post_rating
        self.post_text = post_text
        self.post_creation_date = SQLBaseUtil.timestamp()


class Tag(BaseDBObj):
    """Tag class
    tag_id: current tag id
    tag_name: displayed tag
    tag_rating: current tag rating, float
    tag_author: author of the tag, User"""
    __table__ = 'tags'

    def __init__(self, tag_id: int, tag_name: str, tag_author: User, tag_rating=0.0):
        self.tag_id = tag_id
        self.tag_name = tag_name
        self._tag_author_user = tag_author
        self.tag_author = tag_author.user_id
        self.tag_rating = tag_rating
        self.tag_creation_date = SQLBaseUtil.timestamp()


class Image(BaseDBObj):
    """Image class
    image_id: current img id
    image_title: displayed image title
    image_fname: path to file with image"""
    __table__ = 'images'

    def __init__(self, image_id: int, image_title: str, image_fname: str,
            image_author: User):
        self.image_id = image_id
        self.image_title = image_title
        self.image_fname  = image_fname
        self.image_creation_date = SQLBaseUtil.timestamp()


class Ban(BaseDBObj):
    """Ban class
    suspect: banned User
    creator: moderator and higher"""
    __table__ = 'bans'

    def __init__(self, suspect: User, creator: User, duration, permanent=False):
        self._suspect = suspect
        self._creator = creator
        self.user_id = suspect.user_id
        self.creator_id = creator.user_id
        self.duration = duration
        self.is_permanent = permanent
        self.ban_creation_date = SQLBaseUtil.timestamp()


class Comment(BaseDBObj):
    """Comment class
    comment_author: User, created comment
    post:
    comment_text: displayed comment_text"""
    __table__ = 'comments'

    def __init__(self, comment_author: User, post: Post, comment_text: str):
        self._comment_author = comment_author
        self.comment_author_id = comment_author.user_id
        self._post = post
        self.post_id = post.post_id
        self.comment_text = comment_text
        self.comment_creation_date = SQLBaseUtil.timestamp()


class SQLBaseUtil:
    """Base helpfull functions to work with db"""
    def __init__(self, db: str):
        self.connection = sqlite3.connect(db, check_same_thread=False, isolation_level='EXCLUSIVE')
        self.cursor = self.connection.cursor()

    def drop_all(self):
        """drop all tables"""
        with self.connection:
            script = ""
            for command in self.cursor.execute("SELECT 'DROP TABLE ' || name || ';\n' "
                                               "FROM sqlite_master WHERE type = 'table'"):
                script += (command[0]) if 'sqlite_sequence' not in command[0] else ''
            self.cursor.executescript(script)
        self.connection.commit()

    def reset(self):
        """reset db struct"""
        self.drop_all()
        with self.connection:
            self.cursor.executescript(DatabaseConfig.reset_request)
            self.connection.commit()

    @staticmethod
    def timestamp():
        """return: current timestamp in unix format"""
        return int(time.time())


class SQLUtil(SQLBaseUtil):
    _binding_tables = {(Group, User): ('group_id', 'user_id',  'users_groups') ,
                       (User, Group): ('user_id',  'group_id', 'users_groups') ,
                       (Image, Post): ('image_id', 'post_id',  'images_posts'),
                       (Post, Image): ('post_id',  'image_id', 'images_posts'),
                       (Tag,   Post): ('tag_id',   'post_id',  'tags_posts'),
                       (Post,   Tag): ('post_id',  'tag_id',   'tags_posts')}

    __insert_template__ = 'INSERT INTO {table} ({cols}) VALUES ({val})'
    __binding_exist_template__ = 'SELECT {binding_table[0]}, {binding_table[1]} FROM {binding_table[2]} WHERE {binding_table[0]}={vals[0]} AND {binding_table[0]}={vals[1]}'
    __binding_delete_template__ = 'DELETE FROM {binding_table[2]} WHERE {binding_table[0]}={vals[0]} AND {binding_table[1]}={vals[1]}'
    __delete_template__ = 'DELETE FROM {table} WHERE {obj_id}={obj_id_val}'
    __select_template__ = 'SELECT ({cols}) FROM {table} WHERE {obj_id[0]}={obj_id[1]}'

    def _execute(self, script):
        with self.connection:
            print(script)
            if __log_to_file__:
                # TODO: Replace with log
                pass
            if not __test_mode__:
                return self.cursor.execute(script)

    def add(self, obj: BaseDBObj):
        """add BaseDBObj obj to db
        (work with piece of magic, thats why obj public fielfs should be same with its table's columns name)"""
        scripts = []
        with self.connection:
            _obj = dict(obj)
            script = self.__insert_template__.format(table=obj.__table__, cols=', '.join(_obj.keys()),
                                                        val=', '.join(map(sql_translate, _obj.values())))
            self._execute(script)

    def _bind_by_id(self, ids, binding_table):
        """INSERT INTO binding_table[2] (binding_table[0], binding_table[1]) VALUES (ids[0], ids[1])"""
        with self.connection:
            script = self.__insert_template__.format(
                table=binding_table[2], cols=', '.join(binding_table[:2]), val=', '.join(map(str, ids)))
            self._execute(script)

    def _get_bindable_ids(self, *obj, binding_table=None):
        """return 2 ids if it possible, types of elements of obj may be int or BaseDBObj
        (DARK MAGIC)"""
        if len(obj) > 2:
            raise Warning("Only 2 first objects would be binded")
        _obj = list(obj[:2])
        ids = [None] * 2
        if all(isinstance(x, (int, BaseDBObj)) for x in _obj):
            # if binding table not definef and one of obj is int rais ValueError
            if any(isinstance(x, int) for x in _obj):
                if binding_table == None:
                    raise ValueError('binding_table not defined')
            # check if obj are bindable
            if binding_table not in self._binding_tables.values():
                raise ValueError('Objects are unbindble')
            # if all obj are BaseDBObj
            if all(isinstance(x, BaseDBObj) for x in _obj):
                # try to ge ids from obj, if obj hasnt field defined in _binding_tables raise ValueError
                try:
                    binding_table = self._binding_tables[_obj]
                    ids = list(map(getattr, _obj, binding_table))
                except KeyError:
                    raise ValueError('Objects are unbindble')
            # if obj are ints just copy it into ids
            elif all(isinstance(x, int) for x in _obj):
                ids = _obj
            # if one of obj is int, another is BaseDBObj
            else:
                # get indexes of raw id and BaseDBObj
                id_idx = list(map(type, _obj)).index(int)
                BaseDBObj_idx = list(map(lambda a: type(a).__base__, _obj)).index(BaseDBObj)
                try:
                    ids[id_idx] = _obj.pop(id_idx)
                    # check binding_table
                    if list(self._binding_tables.keys())[list(self._binding_tables.values()).index(binding_table)].index(type(obj[0])) == BaseDBObj_idx:
                        ids[BaseDBObj_idx] = getattr(_obj.pop(), binding_table[BaseDBObj_idx])
                    else:
                        raise ValueError('Objects are unbindble')
                except ValueError:
                    raise ValueError('Objects are unbindble')
        else:
            raise ValueError('Objects are of unsupported types')

        return ids, binding_table

    def _unbind_by_ids(self, ids, binding_table):
        if self._is_binding_exist(ids, binding_table):
            script = self.__binding_delete_template__.format(binding_table=binding_table, vals=ids)
            self._execute(script)
        else:
            raise ValueError('Binding is not exist')

    def _is_binding_exist(self, ids, binding_table):
        with self.connection:
            return self.cursor.execute(self.__binding_exist_template__.format(binding_table=binding_table, vals=ids)).fetchall() != []

    def bind(self, *obj, binding_table=None):
        """bind 2 obj if it possible, types of elements of obj may be int or BaseDBObj"""
        ids, _binding_table = self._get_bindable_ids(*obj, binding_table=binding_table)
        # bind by ids and binding table
        self._bind_by_id(ids, _binding_table)

    def unbind(self, *obj, binding_table=None):
        ids, _binding_table = self._get_bindable_ids(*obj, binding_table=binding_table)
        self._unbind_by_ids(ids, _binding_table)

    def delete(self, obj: BaseDBObj):
        pass

    def push(self, obj: BaseDBObj):
        pass

    def pull(self, obj: BaseDBObj):
        _obj = dict(obj)
        script = self.__select_template__.format(table=obj.__table__, cols=', '.join(_obj.keys()), obj_id=[(k, v) for k, v in _obj.items() if '_id' in k][0])
        vals = self._execute(script)
        if vals is not None:
            map(labda k, v: setattr(obj, k, v), _obj.keys(), vals)
        else:
            raise ValueError('No object in db')



if __name__ == '__main__':
    database = SQLUtil('xtrix_test.db')
    # database.reset()
    database.add(User(1, 'MrFlorius', user_rating=100500))
    bt = database._binding_tables[(User, Group)]
    database.bind(1, 2, binding_table=bt)
    database.pull(User(1, 'MrFlorius', user_rating=100500))
