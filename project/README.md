lab2 create table queries

CREATE TABLE areas	// in progress
(
    area_id integer GENERATED ALWAYS AS IDENTITY,
    name character varying(64),
    begin_date date, 
    end_date date,
    comment
);

CREATE TABLE artist_types
(
    type_id smallint GENERATED ALWAYS AS IDENTITY,
    name character varying(32) UNIQUE,
    PRIMARY KEY (type_id)
	INCLUDE (name)
);

INSERT INTO artist_types (name) 
VALUES ('person'), ('group'), ('orchestra'), ('choir'), ('character'), ('other');

CREATE TABLE genders
(
    gender_id smallint GENERATED ALWAYS AS IDENTITY,
    name character varying(32) UNIQUE,
    PRIMARY KEY (gender_id)
	INCLUDE (name)
);

INSERT INTO genders (name)
VALUES ('male'), ('female'), ('other');

CREATE TABLE artists
(
    artist_id integer GENERATED ALWAYS AS IDENTITY,
    name character varying(64) NOT NULL,
    type_id smallint NOT NULL,
    gender_id smallint,
    begin_date_year smallint,
    begin_date_month smallint,
    begin_date_day smallint,
    end_date_year smallint,
    end_date_month smallint,
    end_date_day smallint,
    begin_area integer,	// in progress
    end_area integer,	// in progress
    comment text,
    PRIMARY KEY (artist_id),
    FOREIGN KEY (type_id)
	REFERENCES artist_types (type_id)
	ON DELETE RESTRICT,
    FOREIGN KEY (gender_id)
	REFERENCES genders (gender_id)
	ON DELETE RESTRICT
);

CREATE TABLE compositions
(
    composition_id integer GENERATED ALWAYS AS IDENTITY,
    title character varying(64) NOT NULL,
    artist_id integer,
    duration smallint NOT NULL,
    release_year smallint,
    release_month smallint,
    release_day smallint,
    lyrics text,
    path_to_file text NOT NULL,
    times_listened bigint NOT NULL DEFAULT 0,	// may be deleted
    PRIMARY KEY (composition_id),
    FOREIGN KEY (artist_id)
	REFERENCES artists (artist_id)
	ON DELETE SET NULL
);

COMMENT ON COLUMN compositions.times_listened
    IS 'DO NOT SET WHILE CREATING
DO NOT UPDATE';

CREATE TABLE users
(
    user_id integer GENERATED ALWAYS AS IDENTITY,
    username character varying(16) NOT NULL UNIQUE,
    password_hash character varying(65) NOT NULL,
    registration_date date NOT NULL,
    is_active boolean NOT NULL DEFAULT TRUE,
    full_name character varying(65),
    birth_date date,
    gender_id smallint,
    PRIMARY KEY (user_id)
	INCLUDE(username)
    FOREIGN KEY (gender_id)
	REFERENCES genders (gender_id)
	ON DELETE RESTRICT
);

CREATE TABLE listening_history
(
    record_id bigint GENERATED ALWAYS AS IDENTITY,
    user_id integer NOT NULL,
    composition_id integer NOT NULL,
    listening_date date NOT NULL,
    PRIMARY KEY (record_id),
    FOREIGN KEY (user_id)
	REFERENCES users (user_id)
	ON DELETE CASCADE,
    FOREIGN KEY (composition_id)
	REFERENCES compositions (composition_id)
	ON DELETE CASCADE
);

CREATE TABLE playlists_privacy
(
    privacy_id integer GENERATED ALWAYS AS IDENTITY,
    privacy_type character varying(16) NOT NULL UNIQUE,
    PRIMARY KEY (privacy_id)
	INCLUDE(privacy_type)
);

INSERT INTO playlists_privacy (privacy_type)
VALUES ('public'), ('unlisted'), ('private');

CREATE TABLE playlists
(
    playlist_id integer GENERATED ALWAYS AS IDENTITY,
    creator_id integer,
    title character varying(32) NOT NULL,
    privacy_id integer NOT NULL,
    PRIMARY KEY (playlist_id),
    FOREIGN KEY (creator_id)
        REFERENCES users (user_id)
	ON DELETE SET NULL,
    FOREIGN KEY (privacy_id)
	REFERENCES playlists_privacy (privacy_id)
	ON DELETE RESTRICT
);

CREATE TABLE albums
(
    album_id integer GENERATED ALWAYS AS IDENTITY,
    title character varying(32) NOT NULL,
    release_year smallint,
    release_month smallint,
    release_day smallint,
    PRIMARY KEY (album_id)
);

CREATE TABLE plist_comp_links
(
    link_id integer GENERATED ALWAYS AS IDENTITY,
    playlist_id integer NOT NULL,
    composition_id integer NOT NULL,
    PRIMARY KEY (link_id),
    UNIQUE (playlist_id, composition_id),
    FOREIGN KEY (composition_id)
        REFERENCES compositions (composition_id)
	ON DELETE CASCADE,
    FOREIGN KEY (playlist_id)
        REFERENCES playlists (playlist_id)
	ON DELETE CASCADE
);

CREATE TABLE album_comp_links
(
    link_id integer GENERATED ALWAYS AS IDENTITY,
    album_id integer NOT NULL,
    composition_id integer NOT NULL,
    PRIMARY KEY (link_id),
    UNIQUE (album_id, composition_id),
    FOREIGN KEY (album_id)
        REFERENCES albums (album_id)
	ON DELETE CASCADE,
    FOREIGN KEY (composition_id)
        REFERENCES compositions (composition_id)
	ON DELETE CASCADE
);

CREATE TABLE user_saved_plists
(
    link_id integer GENERATED ALWAYS AS IDENTITY,
    playlist_id integer NOT NULL,
    user_id integer NOT NULL,
    PRIMARY KEY (link_id),
    UNIQUE (playlist_id, user_id),
    FOREIGN KEY (playlist_id)
        REFERENCES playlists (playlist_id)
	ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
	ON DELETE CASCADE
);

CREATE TABLE user_saved_albums
(
    link_id integer GENERATED ALWAYS AS IDENTITY,
    album_id integer NOT NULL,
    user_id integer NOT NULL,
    PRIMARY KEY (link_id),
    UNIQUE (album_id, user_id),
    FOREIGN KEY (album_id)
        REFERENCES albums (album_id)
	ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
	ON DELETE CASCADE
);

CREATE TABLE compositions_rating
(
    rating_id bigint GENERATED ALWAYS AS IDENTITY,
    composition_id integer NOT NULL,
    user_id integer NOT NULL,
    satisfied bool NOT NULL,
    rating_date date NOT NULL,
    PRIMARY KEY (rating_id),
    UNIQUE (user_id, composition_id),
    FOREIGN KEY (composition_id)
        REFERENCES compositions (composition_id)
	ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
	ON DELETE CASCADE
);

CREATE TABLE playlists_rating
(
    rating_id bigint GENERATED ALWAYS AS IDENTITY,
    playlist_id integer NOT NULL,
    user_id integer NOT NULL,
    satisfied bool NOT NULL,
    rating_date date NOT NULL,
    PRIMARY KEY (rating_id),
    UNIQUE (user_id, playlist_id),
    FOREIGN KEY (playlist_id)
        REFERENCES playlists (playlist_id)
	ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
	ON DELETE CASCADE
);

CREATE TABLE albums_rating
(
    rating_id bigint GENERATED ALWAYS AS IDENTITY,
    album_id integer NOT NULL,
    user_id integer NOT NULL,
    satisfied bool NOT NULL,
    rating_date date NOT NULL,
    PRIMARY KEY (rating_id),
    UNIQUE (user_id, album_id),
    FOREIGN KEY (album_id)
        REFERENCES albums (album_id)
	ON DELETE CASCADE,
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
	ON DELETE CASCADE
);