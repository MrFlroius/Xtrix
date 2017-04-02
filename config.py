import datetime

token = '310714083:AAGKqM34frZyvXRE_d80fuEOuI892__7qbo'
database = 'xtrix.db'
log = 'log.txt'


class DatabaseConfig:
    database = 'xtrix.db'
    test_database = 'xtrix_test.db'
    reset_request = '''
            CREATE TABLE bans
            (
                user_id INT NOT NULL,
                creator_id INT NOT NULL,
                duration INT,
                is_permanent BOOLEAN DEFAULT FALSE NOT NULL,
                CONSTRAINT bans_users_user_id_user_id_fk FOREIGN KEY (user_id, creator_id) REFERENCES users (user_id, user_id)
            );
            CREATE TABLE comments
            (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                comment_author INT NOT NULL,
                post_id INT NOT NULL,
                comment_text TEXT NOT NULL,
                comment_creation_date INT NOT NULL,
                CONSTRAINT comments_users_user_id_fk FOREIGN KEY (comment_author) REFERENCES users (user_id),
                CONSTRAINT comments_posts_post_id_fk FOREIGN KEY (post_id) REFERENCES posts (post_id)
            );
            CREATE TABLE groups
            (
                group_id INTEGER PRIMARY KEY NOT NULL,
                group_name TEXT NOT NULL,
                group_author INTEGER NOT NULL,
                read_posts INT DEFAULT 1 NOT NULL,
                write_posts INT DEFAULT 1 NOT NULL,
                change_own_posts INT DEFAULT 1 NOT NULL,
                delete_own_posts INT DEFAULT 1 NOT NULL,
                change_self INT DEFAULT 1 NOT NULL,
                delete_self INT,
                upload_files INT DEFAULT 1 NOT NULL,
                use_files INT DEFAULT 1 NOT NULL,
                change_own_files INT DEFAULT 1 NOT NULL,
                delete_own_files INT DEFAULT 1 NOT NULL,
                change_files INT DEFAULT 0 NOT NULL,
                delete_files INT DEFAULT 0 NOT NULL,
                create_tags INT DEFAULT 0 NOT NULL,
                use_service_tags INT DEFAULT 0 NOT NULL,
                read_logs INT DEFAULT 0 NOT NULL,
                change_logs INT DEFAULT 0 NOT NULL,
                change_posts INT DEFAULT 0 NOT NULL,
                delete_posts INT DEFAULT 0 NOT NULL,
                ban_users INT DEFAULT 0 NOT NULL,
                permanent_ban_users INT DEFAULT 0 NOT NULL,
                change_users INT DEFAULT 0 NOT NULL,
                delete_users INT DEFAULT 0 NOT NULL,
                group_creation_date INT DEFAULT 0 NOT NULL,
                FOREIGN KEY (group_author) REFERENCES users (user_id)
            );
            CREATE UNIQUE INDEX user_groups_group_name_uindex ON groups (group_name);
            CREATE TABLE images
            (
                image_id INTEGER PRIMARY KEY NOT NULL,
                image_title TEXT NOT NULL,
                image_fname TEXT NOT NULL,
                image_author INTEGER NOT NULL,
                image_creation_date INT DEFAULT 0 NOT NULL,
                FOREIGN KEY (image_author) REFERENCES users (user_id)
            );
            CREATE UNIQUE INDEX images_image_fname_uindex ON images (image_fname);
            CREATE TABLE images_posts
            (
                image_id INT NOT NULL,
                post_id INT NOT NULL,
                CONSTRAINT images_posts_images_image_id_fk FOREIGN KEY (image_id) REFERENCES images (image_id),
                CONSTRAINT images_posts_posts_post_id_fk FOREIGN KEY (post_id) REFERENCES posts (post_id)
            );
            CREATE TABLE posts
            (
                post_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                post_name TEXT NOT NULL,
                post_author INTEGER NOT NULL,
                post_rating REAL DEFAULT 0 NOT NULL,
                post_text TEXT,
                post_creation_date INTEGER DEFAULT 0 NOT NULL,
                FOREIGN KEY (post_author) REFERENCES users (user_id)
            );
            CREATE TABLE sounds
            (
                sound_id INTEGER PRIMARY KEY NOT NULL,
                sound_name TEXT NOT NULL,
                sound_fname TEXT NOT NULL,
                sound_author INTEGER NOT NULL,
                sound_creation_date INT DEFAULT 0 NOT NULL,
                FOREIGN KEY (sound_author) REFERENCES users (user_id)
            );
            CREATE UNIQUE INDEX sounds_sound_fname_uindex ON sounds (sound_fname);
            CREATE TABLE sounds_posts
            (
                sound_id INT NOT NULL,
                post_id INT NOT NULL,
                CONSTRAINT sounds_posts_sounds_sound_id_fk FOREIGN KEY (sound_id) REFERENCES sounds (sound_id),
                CONSTRAINT sounds_posts_posts_post_id_fk FOREIGN KEY (post_id) REFERENCES posts (post_id)
            );
            CREATE TABLE tags
            (
                tag_id INTEGER PRIMARY KEY NOT NULL,
                tag_name TEXT NOT NULL,
                tag_author INTEGER NOT NULL,
                tag_rating REAL NOT NULL,
                tag_creation_date INT NOT NULL,
                FOREIGN KEY (tag_author) REFERENCES users (user_id)
            );
            CREATE UNIQUE INDEX tags_tag_name_uindex ON tags (tag_name);
            CREATE TABLE tags_posts
            (
                tag_id INT NOT NULL,
                post_id INT NOT NULL,
                CONSTRAINT tags_posts_tags_tag_id_fk FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
                CONSTRAINT tags_posts_posts_post_id_fk FOREIGN KEY (post_id) REFERENCES posts (post_id)
            );
            CREATE TABLE users
            (
                user_id INTEGER NOT NULL,
                user_name TEXT,
                user_rating REAL,
                user_creation_date INTEGER DEFAULT 0 NOT NULL
            );
            CREATE UNIQUE INDEX users_user_id_uindex ON users (user_id);
            CREATE TABLE users_groups
            (
                user_id INT NOT NULL,
                group_id INT NOT NULL,
                CONSTRAINT users_gropups_users_user_id_fk FOREIGN KEY (user_id) REFERENCES users (user_id),
                CONSTRAINT users_gropups_groups_group_id_fk FOREIGN KEY (group_id) REFERENCES groups (group_id)
            );'''
