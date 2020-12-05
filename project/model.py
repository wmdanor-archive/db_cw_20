from psycopg2.extras import DictCursor
from models.to_string import to_str

from models.filters import *

import time


def to_setlike_list(container):
    if container is None:
        return None
    elif type(container) in [set, frozenset, range]:
        return list(container)
    elif type(container) in [list, tuple]:
        res = []
        for value in container:
            if value not in res:
                res.append(value)
        return res
    elif type(container) in [int, str]:
        return [container]
    else:
        raise Exception('Supported types: list, tuple, set, frozenset, range, int, str')


class PaginationFilter:

    def __init__(self, page_size=None, page=None):
        self.__page_size = page_size
        self.__page = page
        self.__offset = (page - 1) * page_size if (page_size is not None and page is not None) else None

    def __str__(self):
        return 'page: ' + to_str(self.__page) + ' | page_size : ' + to_str(self.__page_size)

    @property
    def page_size(self):
        return self.__page_size

    @page_size.setter
    def page_size(self, value):
        self.__page_size = value
        self.__offset = (self.__page - 1) * self.__page_size \
            if (self.__page_size is not None and self.__page is not None) else None

    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, value):
        self.__page = value
        self.__offset = (self.__page - 1) * self.__page_size \
            if (self.__page_size is not None and self.__page is not None) else None

    @property
    def offset(self):
        return self.__offset


class ModelPSQL:

    def __init__(self, connection):
        self.__connection = connection
        self.__connection.autocommit = True
        self.__cursor = connection.cursor(cursor_factory=DictCursor)
        self.last_query_runtime = 0.0

    # random fillers

    def fill_artists(self, start_number, end_number):
        self.__cursor.execute('insert into artists (name, type_id) '
                              'select \'artist\'||s.a,  floor(random()* (6) + 1)::smallint '
                              'from generate_series(%s, %s) as s(a)',
                              (start_number, end_number))

    def fill_compositions(self, start_number, end_number):
        self.__cursor.execute('insert into compositions '
                              '(title, artist_id, duration, release_year, release_month, release_day, '
                              'lyrics, path_to_file) '
                              'select * from select_random_compositions(%s, %s)',
                              (start_number, end_number))

    def fill_users(self, start_number, end_number):
        self.__cursor.execute('insert into users (username, password_hash, registration_date, is_active, full_name, '
                              'birth_date, gender_id) '
                              'select \'username \'||s.a, \'password hash \'||s.a, '
                              '(date \'2020-1-1\' - \'4 years\'::interval + justify_interval(\'4 years\'::interval/'
                              '(%(end)s - %(start)s + 1) * s.a))::date, '
                              'toss_a_coin(0.95), case when toss_a_coin(0.6) then \'full name \'||s.a else null::text '
                              'end, '
                              'case when toss_a_coin(0.4) then (timestamp \'1970-1-1\' + random()*(timestamp '
                              '\'2004-1-1\' - timestamp \'1970-1-1\'))::date '
                              'else null::date end, case when toss_a_coin(0.5) then floor(random()* '
                              '(3) + 1)::smallint else null::smallint end '
                              'from generate_series(%(start)s, %(end)s) as s(a)',
                              {'start': start_number, 'end': end_number})

    def fill_history(self, start_number, end_number):
        self.__cursor.execute('insert into listening_history (user_id, composition_id, listening_date) '
                              'select * from select_random_history(%s, %s)',
                              (start_number, end_number))

    def fill_compositions_rating(self, start_number, end_number):
        self.__cursor.execute('insert into compositions_rating '
                              '(user_id, composition_id, rating_date, satisfied) '
                              'select * from select_random_comp_rating(%s, %s) '
                              'on conflict do nothing',
                              (start_number, end_number))

    def fill_playlists(self, start_number, end_number):
        self.__cursor.execute('insert into playlists (title, creator_id, privacy_id) '
                              'select * from select_random_playlists(%s, %s)',
                              (start_number, end_number))

    def fill_playlists_compositions(self, start_number, end_number):
        self.__cursor.execute('insert into plist_comp_links (playlist_id, composition_id) '
                              'select * from select_random_playlists_filling(%s, %s) '
                              'on conflict do nothing',
                              (start_number, end_number))

    # basic getters

    def get_users(self, users_filter, orders_list, pagination_filter):
        timestamp = time.time()
        self.__cursor.execute(
            'SELECT * FROM get_users(%s, '
            'row(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s), '
            'row(%s, %s), %s)',
            (to_setlike_list(users_filter.users_ids),
             users_filter.attributes.username,
             users_filter.attributes.full_name_exclude_nulls, users_filter.attributes.full_name,
             users_filter.attributes.registration_from, users_filter.attributes.registration_to,
             users_filter.attributes.birth_exclude_nulls,
             users_filter.attributes.birth_from, users_filter.attributes.birth_to,
             users_filter.attributes.gender_exclude_nulls,
             to_setlike_list(users_filter.attributes.genders), users_filter.attributes.is_active,
             users_filter.history.toggle,
             users_filter.history.listened_date_from, users_filter.history.listened_date_to,
             users_filter.history.times_listened_from, users_filter.history.times_listened_to,
             to_setlike_list(users_filter.history.compositions_ids), users_filter.history.compositions_ids_any,
             users_filter.compositions_rating.toggle,
             users_filter.compositions_rating.rating_date_from, users_filter.compositions_rating.rating_date_to,
             users_filter.compositions_rating.times_rated_from, users_filter.compositions_rating.times_rated_to,
             users_filter.compositions_rating.average_rating_from, users_filter.compositions_rating.average_rating_to,
             to_setlike_list(users_filter.compositions_rating.rated_ids),
             users_filter.compositions_rating.rated_ids_any,
             users_filter.playlists_rating.toggle,
             users_filter.playlists_rating.rating_date_from, users_filter.playlists_rating.rating_date_to,
             users_filter.playlists_rating.times_rated_from, users_filter.playlists_rating.times_rated_to,
             users_filter.playlists_rating.average_rating_from, users_filter.playlists_rating.average_rating_to,
             to_setlike_list(users_filter.playlists_rating.rated_ids), users_filter.playlists_rating.rated_ids_any,
             users_filter.albums_rating.toggle,
             users_filter.albums_rating.rating_date_from, users_filter.albums_rating.rating_date_to,
             users_filter.albums_rating.times_rated_from, users_filter.albums_rating.times_rated_to,
             users_filter.albums_rating.average_rating_from, users_filter.albums_rating.average_rating_to,
             to_setlike_list(users_filter.albums_rating.rated_ids), users_filter.albums_rating.rated_ids_any,
             users_filter.saved_playlists.toggle,
             users_filter.saved_playlists.saved_number_from, users_filter.saved_playlists.saved_number_to,
             to_setlike_list(users_filter.saved_playlists.saved_ids_list), users_filter.saved_playlists.saved_ids_any,
             users_filter.saved_albums.toggle,
             users_filter.saved_albums.saved_number_from, users_filter.saved_albums.saved_number_to,
             to_setlike_list(users_filter.saved_albums.saved_ids_list), users_filter.saved_albums.saved_ids_any,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        self.last_query_runtime = time.time() - timestamp
        users = []
        for row in self.__cursor:
            # print(row)
            user = dict()
            user['user_id'] = row['user_id']
            user['username'] = row['username']
            user['password_hash'] = row['password_hash']
            user['registration_date'] = row['registration_date']
            user['is_active'] = row['is_active']
            user['full_name'] = row['full_name']
            user['birth_date'] = row['birth_date']
            user['gender'] = row['gender']
            if users_filter.history.toggle:
                user['times_listened'] = row['times_listened']
            if users_filter.compositions_rating.toggle:
                user['times_compositions_rated'] = row['times_compositions_rated']
                user['compositions_average_rating'] = row['compositions_average_rating']
            if users_filter.playlists_rating.toggle:
                user['times_playlists_rated'] = row['times_playlists_rated']
                user['playlists_average_rating'] = row['playlists_average_rating']
            if users_filter.albums_rating.toggle:
                user['times_albums_rated'] = row['times_albums_rated']
                user['albums_average_rating'] = row['albums_average_rating']
            if users_filter.saved_playlists.toggle:
                user['playlists_saved_number'] = row['playlists_saved_number']
            if users_filter.saved_albums.toggle:
                user['albums_saved_number'] = row['albums_saved_number']
            users.append(user)
        return users

    def get_compositions(self, compositions_filter, orders_list, pagination_filter):
        timestamp = time.time()
        self.__cursor.execute(
            'SELECT * FROM get_compositions(%s,'
            'row(%s, %s, %s, %s, %s, %s, %s, %s, %s),'
            '%s, row(%s, %s, %s, %s, %s, %s),'
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s),'
            '%s, row(%s, %s, %s, %s), '
            'row(%s, %s), %s)',
            (to_setlike_list(compositions_filter.compositions_ids),
             compositions_filter.attributes.title_lyrics,
             compositions_filter.attributes.artists_ids_exclude_nulls,
             to_setlike_list(compositions_filter.attributes.artists_ids),
             compositions_filter.attributes.duration_from, compositions_filter.attributes.duration_to,
             compositions_filter.attributes.release_date_exclude_nulls,
             compositions_filter.attributes.release_from, compositions_filter.attributes.release_to,
             compositions_filter.attributes.search_lyrics,
             compositions_filter.history.toggle,
             compositions_filter.history.listened_date_from, compositions_filter.history.listened_date_to,
             compositions_filter.history.times_listened_from, compositions_filter.history.times_listened_to,
             to_setlike_list(compositions_filter.history.users_ids), compositions_filter.history.users_ids_any,
             compositions_filter.rating.toggle,
             compositions_filter.rating.rating_date_from, compositions_filter.rating.rating_date_to,
             compositions_filter.rating.times_rated_from, compositions_filter.rating.times_rated_to,
             compositions_filter.rating.average_rating_from, compositions_filter.rating.average_rating_to,
             to_setlike_list(compositions_filter.rating.users_ids_any), compositions_filter.rating.users_ids,
             compositions_filter.playlists.toggle,
             compositions_filter.playlists.number_belongs_from, compositions_filter.playlists.number_belongs_to,
             to_setlike_list(compositions_filter.playlists.collections_list),
             compositions_filter.playlists.collections_any,
             compositions_filter.albums.toggle,
             compositions_filter.albums.number_belongs_from, compositions_filter.albums.number_belongs_to,
             to_setlike_list(compositions_filter.albums.collections_list),
             compositions_filter.albums.collections_any,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        self.last_query_runtime = time.time() - timestamp
        compositions = []
        for row in self.__cursor:
            composition = dict()
            composition['composition_id'] = row['composition_id']
            composition['title'] = row['title']
            composition['artist_id'] = row['artist_id']
            composition['duration'] = row['duration']
            composition['release_year'] = row['release_year']
            composition['release_month'] = row['release_month']
            composition['release_day'] = row['release_day']
            composition['lyrics'] = row['lyrics']
            composition['path_to_file'] = row['path_to_file']
            if compositions_filter.history.toggle:
                composition['times_listened'] = row['times_listened']
            if compositions_filter.rating.toggle:
                composition['times_rated'] = row['times_rated']
                composition['average_rating'] = row['average_rating']
            if compositions_filter.playlists.toggle:
                composition['playlists_belong_number'] = row['playlists_belong_number']
            if compositions_filter.albums.toggle:
                composition['albums_belong_number'] = row['albums_belong_number']
            compositions.append(composition)
        return compositions

    def get_artists(self, artists_filter, orders_list, pagination_filter):
        timestamp = time.time()
        self.__cursor.execute(
            'SELECT * FROM get_artists(%s,'
            'row(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),'
            '%s, row(%s, %s, %s, %s, %s, %s),'
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s),'
            '%s, row(%s, %s, %s, %s), '
            'row(%s, %s), %s)',
            (to_setlike_list(artists_filter.artists_ids),
             artists_filter.attributes.name_comment,
             to_setlike_list(artists_filter.attributes.types),
             artists_filter.attributes.gender_exclude_nulls, to_setlike_list(artists_filter.attributes.genders),
             artists_filter.attributes.begin_date_exclude_nulls,
             artists_filter.attributes.begin_date_from, artists_filter.attributes.begin_date_to,
             artists_filter.attributes.end_date_exclude_nulls,
             artists_filter.attributes.end_date_from, artists_filter.attributes.end_date_to,
             artists_filter.attributes.search_comments,
             artists_filter.history.toggle,
             artists_filter.history.listened_date_from, artists_filter.history.listened_date_to,
             artists_filter.history.times_listened_from, artists_filter.history.times_listened_to,
             to_setlike_list(artists_filter.history.users_ids), artists_filter.history.users_ids_any,
             artists_filter.rating.toggle,
             artists_filter.rating.rating_date_from, artists_filter.rating.rating_date_to,
             artists_filter.rating.times_rated_from, artists_filter.rating.times_rated_to,
             artists_filter.rating.average_rating_from, artists_filter.rating.average_rating_to,
             to_setlike_list(artists_filter.rating.users_ids_any), artists_filter.rating.users_ids,
             artists_filter.playlists.toggle,
             artists_filter.playlists.number_belongs_from, artists_filter.playlists.number_belongs_to,
             to_setlike_list(artists_filter.playlists.collections_list), artists_filter.playlists.collections_any,
             artists_filter.albums.toggle,
             artists_filter.albums.number_belongs_from, artists_filter.albums.number_belongs_to,
             to_setlike_list(artists_filter.albums.collections_list), artists_filter.albums.collections_any,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        self.last_query_runtime = time.time() - timestamp
        artists = []
        for row in self.__cursor:
            artist = dict()
            artist['artist_id'] = row['artist_id']
            artist['name'] = row['name']
            artist['type'] = row['type']
            artist['gender'] = row['gender']
            artist['begin_date_year'] = row['begin_date_year']
            artist['begin_date_month'] = row['begin_date_month']
            artist['begin_date_day'] = row['begin_date_day']
            artist['end_date_year'] = row['end_date_year']
            artist['end_date_month'] = row['end_date_month']
            artist['end_date_day'] = row['end_date_day']
            artist['comment'] = row['comment']
            if artists_filter.history.toggle:
                artist['times_listened'] = row['times_listened']
            if artists_filter.rating.toggle:
                artist['times_rated'] = row['times_rated']
                artist['average_rating'] = row['average_rating']
            if artists_filter.playlists.toggle:
                artist['playlists_belong_number'] = row['playlists_belong_number']
            if artists_filter.albums.toggle:
                artist['albums_belong_number'] = row['albums_belong_number']
            artists.append(artist)
        return artists

    def get_playlists(self, playlists_filter, orders_list, pagination_filter):
        self.__cursor.execute(
            'SELECT * FROM get_playlists(%s, '
            'row(%s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s), '
            'row(%s, %s), %s)',
            (to_setlike_list(playlists_filter.playlists_ids),
             playlists_filter.attributes.title, playlists_filter.attributes.creators_ids_exclude_nulls,
             to_setlike_list(playlists_filter.attributes.creators_ids),
             to_setlike_list(playlists_filter.attributes.privacies),
             playlists_filter.compositions.toggle,
             playlists_filter.compositions.compositions_number_from,
             playlists_filter.compositions.compositions_number_to,
             to_setlike_list(playlists_filter.compositions.compositions_list),
             playlists_filter.compositions.compositions_any,
             playlists_filter.rating.toggle,
             playlists_filter.rating.rating_date_from, playlists_filter.rating.rating_date_to,
             playlists_filter.rating.times_rated_from, playlists_filter.rating.times_rated_to,
             playlists_filter.rating.average_rating_from, playlists_filter.rating.average_rating_to,
             to_setlike_list(playlists_filter.rating.users_ids_any), playlists_filter.rating.users_ids,
             playlists_filter.users.toggle,
             playlists_filter.users.users_number_from, playlists_filter.users.users_number_to,
             to_setlike_list(playlists_filter.users.users_list), playlists_filter.users.users_any,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        playlists = []
        for row in self.__cursor:
            playlist = dict(row)
            playlist['playlist_id'] = row['playlist_id']
            playlist['title'] = row['title']
            playlist['creator_id'] = row['creator_id']
            playlist['privacy'] = row['privacy']
            if playlists_filter.compositions.toggle:
                playlist['compositions_number'] = row['compositions_number']
            if playlists_filter.rating.toggle:
                playlist['times_rated'] = row['times_rated']
                playlist['average_rating'] = row['average_rating']
            if playlists_filter.users.toggle:
                playlist['users_saved_number'] = row['users_saved_number']
            playlists.append(playlist)
        return playlists

    def get_albums(self, albums_filter, orders_list, pagination_filter):
        self.__cursor.execute(
            'SELECT * FROM get_albums(%s, '
            'row(%s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s, %s, %s, %s, %s), '
            '%s, row(%s, %s, %s, %s), '
            'row(%s, %s), %s)',
            (to_setlike_list(albums_filter.albums_ids),
             albums_filter.attributes.title, albums_filter.attributes.release_date_exclude_nulls,
             albums_filter.attributes.release_date_from, albums_filter.attributes.release_date_from,
             albums_filter.compositions.toggle,
             albums_filter.compositions.compositions_number_from,
             albums_filter.compositions.compositions_number_to,
             to_setlike_list(albums_filter.compositions.compositions_list),
             albums_filter.compositions.compositions_any,
             albums_filter.rating.toggle,
             albums_filter.rating.rating_date_from, albums_filter.rating.rating_date_to,
             albums_filter.rating.times_rated_from, albums_filter.rating.times_rated_to,
             albums_filter.rating.average_rating_from, albums_filter.rating.average_rating_to,
             to_setlike_list(albums_filter.rating.users_ids_any), albums_filter.rating.users_ids,
             albums_filter.users.toggle,
             albums_filter.users.users_number_from, albums_filter.users.users_number_to,
             to_setlike_list(albums_filter.users.users_list), albums_filter.users.users_any,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        albums = []
        for row in self.__cursor:
            album = dict()
            album['albums_id'] = row['albums_id']
            album['title'] = row['title']
            album['release_year'] = row['release_year']
            album['release_month'] = row['release_month']
            album['release_day'] = row['release_day']
            if albums_filter.compositions.toggle:
                album['compositions_number'] = row['compositions_number']
            if albums_filter.rating.toggle:
                album['times_rated'] = row['times_rated']
                album['average_rating'] = row['average_rating']
            if albums_filter.users.toggle:
                album['users_saved_number'] = row['users_saved_number']
            albums.append(album)
        return albums

    def get_listening_history(self, history_filter, orders_list, pagination_filter):  # work in progress
        self.__cursor.execute(
            'SELECT * FROM get_history('
            'row(%s, %s, %s, %s), %s, %s, '
            'row(%s, %s), %s)',
            (to_setlike_list(history_filter.users_ids), to_setlike_list(history_filter.compositions_ids),
             history_filter.listened_from, history_filter.listened_to,
             history_filter.user_listened_counter, history_filter.composition_listened_counter,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        listening_history = []
        for row in self.__cursor:
            record = dict()
            record['record_id'] = row['record_id']
            record['user_id'] = row['user_id']
            record['composition_id'] = row['composition_id']
            record['listening_date'] = row['listening_date']
            if history_filter.user_listened_counter:
                record['times_user_listened'] = row['times_user_listened']
            if history_filter.composition_listened_counter:
                record['times_composition_listened'] = row['times_composition_listened']
            listening_history.append(record)
        return listening_history

    def get_rating(self, rating_filter, orders_list, pagination_filter):
        self.__cursor.execute(
            'SELECT * FROM get_rating(%s, '
            'row(%s, %s, %s, %s, %s), %s, %s, '
            'row(%s, %s), %s)',
            (rating_filter.rated_type,
             to_setlike_list(rating_filter.users_ids), to_setlike_list(rating_filter.rated_ids),
             rating_filter.satisfied,
             rating_filter.rated_from, rating_filter.rated_to,
             rating_filter.rated_rating_counter, rating_filter.user_rating_counter,
             pagination_filter.page_size, pagination_filter.offset, to_setlike_list(orders_list)))
        rating = []
        for row in self.__cursor:
            record = dict()
            record['record_id'] = row['record_id']
            record['rated_id'] = row['rated_id']
            record['user_id'] = row['user_id']
            record['satisfied'] = row['satisfied']
            record['rating_date'] = row['rating_date']
            if rating_filter.rated_rating_counter:
                record['times_rated_rated'] = row['times_rated_rated']
                record['avg_rated_rating'] = row['avg_rated_rating']
            if rating_filter.user_rating_counter:
                record['times_user_rated'] = row['times_user_rated']
                record['avg_user_rating'] = row['avg_user_rating']
            rating.append(record)
        return rating

    # standard user operations

    def create_user(self, user_model):
        self.__cursor.execute('INSERT INTO users '
                              '(username, password_hash, registration_date, is_active, '
                              'full_name, birth_date, gender_id) '
                              'VALUES (%s, %s, %s, %s, %s, %s, %s) '
                              'RETURNING *',
                              (user_model.username, user_model.password_hash, user_model.registration_date,
                               user_model.is_active, user_model.full_name, user_model.birth_date, user_model.gender_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_user(self, user_model):
        self.__cursor.execute('UPDATE users '
                              'SET username = %s, password_hash = %s, registration_date = %s, '
                              'is_active = %s, full_name = %s, birth_date = %s, gender_id = %s '
                              'WHERE user_id = %s '
                              'RETURNING *',
                              (user_model.username, user_model.password_hash, user_model.registration_date,
                               user_model.is_active, user_model.full_name, user_model.birth_date, user_model.gender_id,
                               user_model.user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_user(self, user_id):
        self.__cursor.execute('DELETE users '
                              'WHERE user_id = %s '
                              'RETURNING *',
                              (user_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # advanced composition operations

    def add_user_playlist(self, playlist_id, user_id):
        self.__cursor.execute('INSERT INTO user_saved_plists '
                              '(playlist_id, user_id) '
                              'VALUES (%s, %s)'
                              'ON CONFLICT ON CONSTRAINT '
                              'user_saved_plists_playlist_id_user_id_key '
                              'DO NOTHING '
                              'RETURNING *',
                              (playlist_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def remove_user_playlist(self, playlist_id, user_id):
        self.__cursor.execute('DELETE FROM user_saved_plists '
                              'WHERE playlist_id = %s AND user_id = %s '
                              'RETURNING *',
                              (playlist_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def add_user_album(self, album_id, user_id):
        self.__cursor.execute('INSERT INTO user_saved_albums '
                              '(album_id, user_id) '
                              'VALUES (%s, %s)'
                              'ON CONFLICT ON CONSTRAINT '
                              'user_saved_albums_album_id_user_id_key '
                              'DO NOTHING '
                              'RETURNING *',
                              (album_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def remove_user_album(self, album_id, user_id):
        self.__cursor.execute('DELETE FROM user_saved_albums'
                              'WHERE album_id = %s AND user_id = %s '
                              'RETURNING *',
                              (album_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    # standard composition operations

    def create_composition(self, composition_model):  # add file
        self.__cursor.execute('INSERT INTO compositions '
                              '(title, duration, release_year, release_month, release_day, lyrics, path_to_file) '
                              'VALUES (%s, %s, %s, %s, %s, %s, %s) '
                              'RETURNING *',
                              (composition_model.title, composition_model.duration, composition_model.release_year,
                               composition_model.release_month, composition_model.release_day,
                               composition_model.lyrics, composition_model.path_to_file))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_composition(self, composition_model):  # add file
        self.__cursor.execute('UPDATE users '
                              'SET title = %s, duration = %s, release_year = %s, release_month = %s, release_day = %s '
                              'lyrics = %s, path_to_file = %s '
                              'WHERE composition_id = %s '
                              'RETURNING *',
                              (composition_model.title, composition_model.duration, composition_model.release_year,
                               composition_model.release_month, composition_model.release_day,
                               composition_model.lyrics, composition_model.path_to_file))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_composition(self, composition_id):
        self.__cursor.execute('DELETE FROM compositions '
                              'WHERE composition_id = %s '
                              'RETURNING *',
                              (composition_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # advanced composition operations

    def listen_composition(self, history_record):
        self.__cursor.execute('INSERT INTO listening_history '
                              '(user_id, composition_id, listening_date) '
                              'VALUES (%s, %s, %s) '
                              'RETURNING *',
                              (history_record.user_id, history_record.composition_id,
                               history_record.listening_date))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def unlisten_composition(self, record_id):
        self.__cursor.execute('DELETE FROM listening_history '
                              'WHERE record_id = %s '
                              'RETURNING *',
                              (record_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def rate_composition(self, rating_model):
        self.__cursor.execute('INSERT INTO compositions_rating '
                              '(composition_id, user_id, satisfied, rating_date) '
                              'VALUES (%s, %s, %s, %s) '
                              'ON CONFLICT ON CONSTRAINT '
                              'compositions_rating_user_id_composition_id_key '
                              'DO UPDATE '
                              'SET satisfied = EXCLUDED.satisfied, '
                              'rating_date = EXCLUDED.rating_date '
                              'RETURNING *',
                              (rating_model.rated_id, rating_model.user_id,
                               rating_model.satisfied, rating_model.rating_date))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def unrate_composition(self, composition_id, user_id):
        self.__cursor.execute('DELETE FROM compositions_rating '
                              'WHERE composition_id = %s AND user_id = %s '
                              'RETURNING *',
                              (composition_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # standard artist operations

    def create_artist(self, artist_model):
        self.__cursor.execute('INSERT INTO artists '
                              '(name, type_id) '
                              'VALUES (%s, %s, %s) '
                              'RETURNING *',
                              (artist_model.name, artist_model.type_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_artist(self, artist_model):
        self.__cursor.execute('UPDATE artists '
                              'SET name = %s, type_id = %s '
                              'RETURNING *',
                              (artist_model.name, artist_model.type_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_artist(self, artist_id):
        self.__cursor.execute('DELETE FROM artists '
                              'WHERE artist_id = %s '
                              'RETURNING *',
                              (artist_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # advanced artist operations

    # nothing ?

    # standard playlist operations

    def create_playlist(self, playlist_model):
        self.__cursor.execute('INSERT INTO playlists '
                              '(title, privacy_id, creator_id) '
                              'VALUES (%s, %s, %s) '
                              'RETURNING *',
                              (playlist_model.title, playlist_model.privacy_id,
                               playlist_model.creator_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_playlist(self, playlist_model):
        self.__cursor.execute('UPDATE playlists '
                              'SET title = %s, privacy_id = %s, creator_id = %s '
                              'RETURNING *',
                              (playlist_model.title, playlist_model.privacy_id,
                               playlist_model.creator_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_playlist(self, playlist_id):
        self.__cursor.execute('DELETE FROM playlists '
                              'WHERE playlist_id = %s '
                              'RETURNING *',
                              (playlist_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def get_playlist(self, playlist_id):
        timestamp = time.time()
        self.__cursor.execute('SELECT * FROM playlists '
                              'WHERE playlist_id = %s',
                              (playlist_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            playlist_compositions = []
            self.__cursor.execute('SELECT * FROM compositions '
                                  'WHERE EXISTS '
                                  '(SELECT composition_id FROM plist_comp_links '
                                  'WHERE plist_comp_links.playlist_id = %s AND '
                                  'plist_comp_links.composition_id = compositions.composition_id)',
                                  (playlist_id,))
            self.last_query_runtime = time.time() - timestamp
            for comp in self.__cursor:
                playlist_compositions.append(dict(comp))
            res = dict(row)
            res['compositions'] = playlist_compositions
            return res

    # advanced playlist operations

    def add_playlist_composition(self, playlist_id, composition_id):
        self.__cursor.execute('INSERT INTO plist_comp_links '
                              '(playlist_id, composition_id) '
                              'VALUES (%s, %s) '
                              'ON CONFLICT ON CONSTRAINT '
                              'plist_comp_links_playlist_id_composition_id_key '
                              'DO NOTHING '
                              'RETURNING *',
                              (playlist_id, composition_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def remove_playlist_composition(self, playlist_id, composition_id):
        self.__cursor.execute('DELETE FROM plist_comp_links '
                              'WHERE playlist_id = %s AND composition_id = %s '
                              'RETURNING *',
                              (playlist_id, composition_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def rate_playlist(self, rating_model):
        self.__cursor.execute('INSERT INTO playlists_rating '
                              '(playlist_id, user_id, satisfied, rating_date) '
                              'VALUES (%s, %s, %s, %s) '
                              'ON CONFLICT ON CONSTRAINT '
                              'playlists_rating_user_id_playlist_id_key '
                              'DO UPDATE '
                              'SET satisfied = EXCLUDED.satisfied, '
                              'rating_date = EXCLUDED.rating_date '
                              'RETURNING *',
                              (rating_model.rated_id, rating_model.user_id,
                               rating_model.satisfied, rating_model.rating_date))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def unrate_playlist(self, playlist_id, user_id):
        self.__cursor.execute('DELETE FROM playlists_rating '
                              'WHERE playlist_id = %s AND user_id = %s '
                              'RETURNING *',
                              (playlist_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    # standard album operations

    def create_album(self, album_model):
        self.__cursor.execute('INSERT INTO albums '
                              '(title, release_year) '
                              'VALUES (%s, %s) '
                              'RETURNING *',
                              (album_model.title, album_model.release_year))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def update_album(self, album_model):
        self.__cursor.execute('UPDATE albums '
                              'SET title = %s, release_year = %s '
                              'RETURNING *',
                              (album_model.title, album_model.release_year))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def delete_album(self, album_id):
        self.__cursor.execute('DELETE FROM albums '
                              'WHERE album_id = %s '
                              'RETURNING *',
                              (album_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def get_album(self, album_id):
        self.__cursor.execute('SELECT * FROM albums '
                              'WHERE album_id = %s',
                              (album_id,))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            album_compositions = []
            self.__cursor.execute('SELECT * FROM compositions '
                                  'WHERE EXISTS '
                                  '(SELECT composition_id FROM album_comp_links '
                                  'WHERE album_comp_links.album_id = %s AND '
                                  'album_comp_links.composition_id = compositions.composition_id)',
                                  (album_id,))
            for comp in self.__cursor:
                album_compositions.append(dict(comp))
            res = dict(row)
            res['compositions'] = album_compositions
            return res

    # advanced album operations

    def add_album_composition(self, album_id, composition_id):
        self.__cursor.execute('INSERT INTO album_comp_links '
                              '(album_id, composition_id) '
                              'VALUES (%s, %s) '
                              'ON CONFLICT ON CONSTRAINT '
                              'album_comp_links_album_id_composition_id_key '
                              'DO NOTHING '
                              'RETURNING *',
                              (album_id, composition_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def remove_album_composition(self, album_id, composition_id):
        self.__cursor.execute('DELETE FROM album_comp_links '
                              'WHERE album_id = %s AND composition_id = %s '
                              'RETURNING *',
                              (album_id, composition_id))
        row = self.__cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def rate_album(self, rating_model):
        self.__cursor.execute('INSERT INTO albums_rating '
                              '(album_id, user_id, satisfied, rating_date) '
                              'VALUES (%s, %s, %s, %s) '
                              'ON CONFLICT ON CONSTRAINT '
                              'albums_rating_user_id_album_id_key '
                              'DO UPDATE '
                              'SET satisfied = EXCLUDED.satisfied, '
                              'rating_date = EXCLUDED.rating_date '
                              'RETURNING *',
                              (rating_model.rated_id, rating_model.user_id,
                               rating_model.satisfied, rating_model.rating_date))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)

    def unrate_album(self, album_id, user_id):
        self.__cursor.execute('DELETE FROM albums_rating '
                              'WHERE album_id = %s AND user_id = %s '
                              'RETURNING *',
                              (album_id, user_id))
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return dict(row)
