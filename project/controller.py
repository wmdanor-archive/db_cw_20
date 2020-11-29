from model import ModelPSQL, PaginationFilter
import view
import datetime
from distutils.util import strtobool
from copy import copy

from models.user import User
from models.composition import Composition
from models.performer import Artist
from models.album import Album
from models.playlist import Playlist
from models.rating import Rating
from models.history_record import HistoryRecord
from models.filters import *


def get_int():
    v = input()
    if v:
        return int(v)
    else:
        return None


def get_float():
    v = input()
    if v:
        return float(v)
    else:
        return None


def get_bool():
    v = input()
    if v:
        return bool(strtobool(v))
    else:
        return None


def get_str():
    v = input()
    if v:
        return v
    else:
        return None


def get_date():
    """
    Getting date string from YYYY-MM-DD format
    """
    v = input()
    if v:
        datetime.datetime.strptime(v, '%Y-%m-%d')
        return v
    else:
        return None


def get_partial_date():
    """
    Parsing date from YYYY-MM-DD format\n
    For None field input 0\n
    :return: tuple(year, month, day)
    """
    v = input()
    if v:
        splitted = v.split('-')
        if len(splitted) != 3:
            raise ValueError("time data '" + v + "' does not match format 'YYYY-MM-DD'")
        year = int(splitted[0])
        month = int(splitted[1])
        day = int(splitted[2])
        if year < 0 or month < 0 or day < 0:
            raise ValueError("time data '" + v + "' does not match format 'YYYY-MM-DD'")
        if year == 0 and month == 0 and day == 0:
            return None, None, None
        elif year != 0 and month == 0 and day == 0:
            return year, None, None
        elif year != 0 and month != 0 and day == 0:
            if not 1 <= month <= 12:
                raise ValueError("time data '" + v + "' does not match format 'YYYY-MM-DD'")
            return year, month, None
        elif year != 0 and month != 0 and day != 0:
            datetime.datetime.strptime(v, '%Y-%m-%d')
            return year, month, day
        else:
            raise ValueError("time data '" + v + "' does not match format 'YYYY-MM-DD'")
    else:
        return None


def edit_set(edited, element_type=str):
    """
    To add type: add a1 a2 a3 ...\n
    To remove type: rem a1 a2 a3 ...\n
    :return: edited set
    """
    command = input()
    if not command:
        raise ValueError("Invalid command input")
    arr = command.split()
    cmd = arr[0]
    arr.pop(0)
    vals = set()
    for item in arr:
        element = element_type(item)
        vals.add(element)
    set_copy = copy(edited)
    if cmd == 'add':
        if set_copy is None:
            set_copy = set()
        return set_copy.union(vals)
    elif cmd == 'rem':
        if set_copy is None:
            return None
        set_copy.difference_update(vals)
        print(set_copy)
        if not set_copy:
            return None
        return set_copy
    else:
        raise ValueError("Invalid input")


class ControllerPSQL:

    def __init__(self, connection):
        self.__model = ModelPSQL(connection)
        self.__view = view

    # interface

    def construct_album(self):
        self.__view.view_message('Enter title')
        title = get_str()
        if not title:
            raise ValueError("Variable 'title' can not be None")
        self.__view.view_message('Enter release year')
        release_year = get_int()
        return Album(0, title, release_year)

    def construct_artist(self):
        self.__view.view_message('Enter name')
        name = get_str()
        if name is None:
            raise ValueError("Variable 'name' can not be None")
        self.__view.view_message('Choose type')
        types = ['person', 'group', 'orchestra', 'choir', 'character', 'other']
        i = 1
        for item in types:
            self.__view.view_message(i, '-', item)
            i += 1
        type_id = get_int()
        if type_id is None or not 1 <= type_id <= 6:
            raise ValueError("Variable 'type_id' invalid input")

        return Artist(0, name, type_id)

    def construct_composition(self):
        self.__view.view_message('Enter title')
        title = get_str()
        if title is None:
            raise ValueError("Variable 'title' can not be None")

        self.__view.view_message('Enter duration (seconds)')
        duration = get_int()
        if duration is None:
            raise ValueError("Variable 'duration' can not be None")

        self.__view.view_message('Enter path to file')
        path_to_file = get_str()
        if path_to_file is None:
            raise ValueError("Variable 'path_to_file' can not be None")

        self.__view.view_message('Enter lyrics')
        lyrics = get_str()

        date_tuple = get_partial_date()
        self.__view.view_message('Enter release date in format YYYY-MM-DD, for None field input 0')

        return Composition(0, title, duration, path_to_file, 0, date_tuple[0], date_tuple[1], date_tuple[2], lyrics)

    def construct_playlist(self):
        self.__view.view_message('Enter title')
        title = get_str()
        if title is None:
            raise ValueError("Variable 'title' can not be None")

        self.__view.view_message('Enter creator_id')
        creator_id = get_int()

        self.__view.view_message('Choose privacy')
        privacy_types = ['public', 'unlisted', 'private']
        i = 1
        for item in privacy_types:
            self.__view.view_message(i, '-', item)
            i += 1
        privacy_id = get_int()
        if privacy_id is None or not 1 <= privacy_id <= 3:
            raise ValueError("Variable 'privacy_id' invalid input")

        return Playlist(0, title, privacy_id, creator_id)

    def construct_user(self):
        self.__view.view_message('Enter username')
        username = get_str()
        if username is None:
            raise ValueError("Variable 'username' can not be None")

        self.__view.view_message('Enter password hash')
        password_hash = get_str()
        if password_hash is None:
            raise ValueError("Variable 'password_hash' can not be None")

        self.__view.view_message('Enter registration date (ISO8601)')
        registration_date = get_date()
        if registration_date is None:
            raise ValueError("Variable 'registration_date' can not be None")

        self.__view.view_message('Is active?')
        is_active = get_bool()
        if is_active is None:
            raise ValueError("Variable 'registration_date' can not be None")

        self.__view.view_message('Enter full name')
        full_name = get_str()

        self.__view.view_message('Enter birth date (ISO8601)')
        birth_date = get_date()

        self.__view.view_message('Choose gender')
        genders = ['male', 'female', 'other']
        i = 1
        for item in genders:
            self.__view.view_message(i, '-', item)
            i += 1
        gender_id = get_int()
        if not 1 <= gender_id <= 3:
            raise ValueError("Variable 'gender_id' invalid input")

        return User(0, username, password_hash, registration_date, is_active, full_name, birth_date, gender_id)

    def construct_history_record(self):
        self.__view.view_message('Enter user_id')
        user_id = get_int()
        if user_id is None:
            raise ValueError("Variable 'user_id' can not be None")

        self.__view.view_message('Enter composition_id')
        composition_id = get_int()
        if composition_id is None:
            raise ValueError("Variable 'composition_id' can not be None")

        self.__view.view_message('Enter date (ISO8601)')
        action_date = get_date()
        if action_date is None:
            raise ValueError("Variable 'listening_date' can not be None")

        return HistoryRecord(0, composition_id, user_id, action_date)

    def construct_rating_record(self):
        self.__view.view_message('Enter user_id')
        user_id = get_int()
        if user_id is None:
            raise ValueError("Variable 'user_id' can not be None")

        self.__view.view_message('Enter rated_id')
        rated_id = get_int()
        if rated_id is None:
            raise ValueError("Variable 'rated_id' can not be None")

        self.__view.view_message('Enter date (ISO8601)')
        action_date = get_date()
        if action_date is None:
            raise ValueError("Variable 'rating_date' can not be None")

        self.__view.view_message('Is satisfied?')
        is_satisfied = get_bool()
        if is_satisfied is None:
            raise ValueError("Variable 'registration_date' can not be None")

        return Rating(0, rated_id, user_id, is_satisfied, action_date)

    def edit_users_filter_attributes(self, attributes):
        while True:
            self.__view.view_message(attributes)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            attrs = ['username', 'full_name', 'registration_from', 'registration_to', 'birth_from', 'birth_to',
                     'genders', 'is_active', 'full_name_exclude_nulls', 'birth_exclude_nulls', 'gender_exclude_nulls']
            i = 1
            for item in attrs:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('Enter username')
                    attributes.username = get_str()
                elif res == 2:
                    self.__view.view_message('Enter full_name')
                    attributes.full_name = get_str()
                elif res == 3:
                    self.__view.view_message('Enter registration_from')
                    attributes.registration_from = get_date()
                elif res == 4:
                    self.__view.view_message('Enter registration_to')
                    attributes.registration_to = get_date()
                elif res == 5:
                    self.__view.view_message('Enter birth_from')
                    attributes.birth_from = get_date()
                elif res == 6:
                    self.__view.view_message('Enter birth_to')
                    attributes.birth_to = get_date()
                elif res == 7:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...\nTo remove type: REM a1 a2 a3 ...')
                    attributes.genders = edit_set(attributes.genders)
                elif res == 8:
                    self.__view.view_message('Is active?')
                    attributes.is_active = get_bool()
                elif res == 9:
                    if attributes.full_name_exclude_nulls is None:
                        attributes.full_name_exclude_nulls = True
                    else:
                        attributes.full_name_exclude_nulls = not attributes.full_name_exclude_nulls
                    self.__view.view_message('Changed')
                elif res == 10:
                    if attributes.birth_exclude_nulls is None:
                        attributes.birth_exclude_nulls = True
                    else:
                        attributes.birth_exclude_nulls = not attributes.birth_exclude_nulls
                    self.__view.view_message('Changed')
                elif res == 11:
                    if attributes.gender_exclude_nulls is None:
                        attributes.gender_exclude_nulls = True
                    else:
                        attributes.gender_exclude_nulls = not attributes.gender_exclude_nulls
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid action input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_users_filter_history(self, history):
        while True:
            self.__view.view_message(history)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            hist = ['toggle', 'listened_date_from', 'listened_date_to', 'times_listened_from', 'times_listened_to',
                    'compositions_ids', 'compositions_ids_any']
            i = 1
            for item in hist:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    if history.toggle is None:
                        history.toggle = True
                    else:
                        history.toggle = not history.toggle
                    self.__view.view_message('Changed')
                elif res == 2:
                    self.__view.view_message('Enter listened_date_from')
                    history.listened_date_from = get_date()
                elif res == 3:
                    self.__view.view_message('Enter listened_date_to')
                    history.listened_date_to = get_date()
                elif res == 4:
                    self.__view.view_message('Enter times_listened_from')
                    history.times_listened_from = get_int()
                elif res == 5:
                    self.__view.view_message('Enter times_listened_to')
                    history.times_listened_to = get_int()
                elif res == 6:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    history.compositions_ids = edit_set(history.compositions_ids, int)
                elif res == 7:
                    if history.compositions_ids_any is None:
                        history.compositions_ids_any = True
                    else:
                        history.compositions_ids_any = not history.compositions_ids_any
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid action input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_users_filter_rating(self, rating):
        while True:
            self.__view.view_message(rating)
            self.__view.view_message('What to edit')
            rate = ['toggle', 'rating_date_from', 'rating_date_to', 'times_rated_from', 'times_rated_to',
                    'average_rating_from', 'average_rating_to', 'rated_ids', 'rated_ids_any']
            self.__view.view_message('0 - go back')
            i = 1
            for item in rate:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    if rating.toggle is None:
                        rating.toggle = True
                    else:
                        rating.toggle = not rating.toggle
                    self.__view.view_message('Changed')
                elif res == 2:
                    self.__view.view_message('Enter rating_date_from')
                    rating.rating_date_from = get_date()
                elif res == 3:
                    self.__view.view_message('Enter rating_date_to')
                    rating.rating_date_to = get_date()
                elif res == 4:
                    self.__view.view_message('Enter times_rated_from')
                    rating.times_rated_from = get_int()
                elif res == 5:
                    self.__view.view_message('Enter times_rated_to')
                    rating.times_rated_to = get_int()
                elif res == 6:
                    self.__view.view_message('Enter average_rating_from')
                    rating.average_rating_from = get_float()
                elif res == 7:
                    self.__view.view_message('Enter average_rating_to')
                    rating.average_rating_to = get_float()
                elif res == 8:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    rating.rated_ids = edit_set(rating.rated_ids, int)
                elif res == 9:
                    if rating.rated_ids_any is None:
                        rating.rated_ids_any = True
                    else:
                        rating.rated_ids_any = not rating.rated_ids_any
                    self.__view.view_message('Changed')
                else:
                    raise Exception('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_users_filter_collections(self, saved_collections):
        while True:
            self.__view.view_message(saved_collections)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            saved = ['toggle', 'saved_number_from', 'saved_number_to', 'saved_ids_list', 'saved_ids_any']
            i = 1
            for item in saved:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    if saved_collections.toggle is None:
                        saved_collections.toggle = True
                    else:
                        saved_collections.toggle = not saved_collections.toggle
                    self.__view.view_message('Changed')
                elif res == 2:
                    self.__view.view_message('Enter saved_number_from')
                    saved_collections.saved_number_from = get_int()
                elif res == 3:
                    self.__view.view_message('Enter saved_number_to')
                    saved_collections.saved_number_to = get_int()
                elif res == 4:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    saved_collections.saved_ids_list = edit_set(saved_collections.saved_ids_list, int)
                elif res == 5:
                    if saved_collections.saved_ids_any is None:
                        saved_collections.saved_ids_any = True
                    else:
                        saved_collections.saved_ids_any = not saved_collections.saved_ids_any
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_users_filter(self, users_filter):
        while True:
            self.__view.view_message(users_filter)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            filters = ['users_ids', 'attributes', 'history', 'compositions_rating', 'playlists_rating', 'albums_rating',
                       'saved_playlists', 'saved_albums']
            i = 1
            for item in filters:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    users_filter.users_ids = edit_set(users_filter.users_ids, int)
                elif res == 2:
                    self.edit_users_filter_attributes(users_filter.attributes)
                elif res == 3:
                    self.edit_users_filter_history(users_filter.history)
                elif res == 4:
                    self.edit_users_filter_rating(users_filter.compositions_rating)
                elif res == 5:
                    self.edit_users_filter_rating(users_filter.playlists_rating)
                elif res == 6:
                    self.edit_users_filter_rating(users_filter.albums_rating)
                elif res == 7:
                    self.edit_users_filter_collections(users_filter.saved_playlists)
                elif res == 8:
                    self.edit_users_filter_collections(users_filter.saved_albums)
                else:
                    raise ValueError('Invalid command')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_compositions_filter_attributes(self, attributes):
        while True:
            self.__view.view_message(attributes)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            attrs = ['title_lyrics', 'artists_ids_exclude_nulls', 'artists_ids', 'duration_from', 'duration_to',
                     'release_date_exclude_nulls', 'release_from', 'release_to', 'search_lyrics']
            i = 1
            for item in attrs:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('Enter title_lyrics')
                    attributes.title_lyrics = get_str()
                elif res == 2:
                    if attributes.artists_ids_exclude_nulls is None:
                        attributes.artists_ids_exclude_nulls = True
                    else:
                        attributes.artists_ids_exclude_nulls = not attributes.artists_ids_exclude_nulls
                    self.__view.view_message('Changed')
                elif res == 3:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    attributes.artists_ids = edit_set(attributes.artists_ids, int)
                elif res == 4:
                    self.__view.view_message('Enter duration_from')
                    attributes.duration_from = get_int()
                elif res == 5:
                    self.__view.view_message('Enter duration_to')
                    attributes.duration_to = get_int()
                elif res == 6:
                    if attributes.release_date_exclude_nulls is None:
                        attributes.release_date_exclude_nulls = True
                    else:
                        attributes.release_date_exclude_nulls = not attributes.release_date_exclude_nulls
                    self.__view.view_message('Changed')
                elif res == 7:
                    self.__view.view_message('Enter release_from')
                    attributes.release_from = get_date()
                elif res == 8:
                    self.__view.view_message('Enter release_to')
                    attributes.release_to = get_date()
                elif res == 9:
                    if attributes.search_lyrics is None:
                        attributes.search_lyrics = True
                    else:
                        attributes.search_lyrics = not attributes.search_lyrics
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_compositions_filter_history(self, history):
        while True:
            self.__view.view_message(history)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            hist = ['toggle', 'listened_date_from', 'listened_date_to', 'times_listened_from', 'times_listened_to',
                    'users_ids', 'users_ids_any']
            i = 1
            for item in hist:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    if history.toggle is None:
                        history.toggle = True
                    else:
                        history.toggle = not history.toggle
                    self.__view.view_message('Changed')
                elif res == 2:
                    self.__view.view_message('Enter listened_date_from')
                    history.listened_date_from = get_date()
                elif res == 3:
                    self.__view.view_message('Enter listened_date_to')
                    history.listened_date_to = get_date()
                elif res == 4:
                    self.__view.view_message('Enter times_listened_from')
                    history.times_listened_from = get_int()
                elif res == 5:
                    self.__view.view_message('Enter times_listened_to')
                    history.times_listened_to = get_int()
                elif res == 6:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    history.users_ids = edit_set(history.users_ids, int)
                elif res == 7:
                    if history.users_ids_any is None:
                        history.users_ids_any = True
                    else:
                        history.users_ids_any = not history.users_ids_any
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_compositions_filter_rating(self, rating):
        while True:
            self.__view.view_message(rating)
            self.__view.view_message('What to edit')
            rate = ['toggle', 'rating_date_from', 'rating_date_to', 'times_rated_from', 'times_rated_to',
                    'average_rating_from', 'average_rating_to', 'users_ids', 'users_ids_any']
            self.__view.view_message('0 - go back')
            i = 1
            for item in rate:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    if rating.toggle is None:
                        rating.toggle = True
                    else:
                        rating.toggle = not rating.toggle
                    self.__view.view_message('Changed')
                elif res == 2:
                    self.__view.view_message('Enter rating_date_from')
                    rating.rating_date_from = get_date()
                elif res == 3:
                    self.__view.view_message('Enter rating_date_to')
                    rating.rating_date_to = get_date()
                elif res == 4:
                    self.__view.view_message('Enter times_rated_from')
                    rating.times_rated_from = get_int()
                elif res == 5:
                    self.__view.view_message('Enter times_rated_to')
                    rating.times_rated_to = get_int()
                elif res == 6:
                    self.__view.view_message('Enter average_rating_from')
                    rating.average_rating_from = get_float()
                elif res == 7:
                    self.__view.view_message('Enter average_rating_to')
                    rating.average_rating_to = get_float()
                elif res == 8:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    rating.users_ids = edit_set(rating.users_ids, int)
                elif res == 9:
                    if rating.users_ids_any is None:
                        rating.users_ids_any = True
                    else:
                        rating.users_ids_any = not rating.users_ids_any
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_compositions_filter_collections(self, collections):
        while True:
            self.__view.view_message(collections)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            saved = ['toggle', 'number_belongs_from', 'number_belongs_to', 'collections_ids', 'collections_any']
            i = 1
            for item in saved:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    if collections.toggle is None:
                        collections.toggle = True
                    else:
                        collections.toggle = not collections.toggle
                    self.__view.view_message('Changed')
                elif res == 2:
                    self.__view.view_message('Enter number_belongs_from')
                    collections.number_belongs_from = get_int()
                elif res == 3:
                    self.__view.view_message('Enter number_belongs_to')
                    collections.number_belongs_to = get_int()
                elif res == 4:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    collections.collections_list = edit_set(collections.collections_list, int)
                elif res == 5:
                    if collections.collections_any is None:
                        collections.collections_any = True
                    else:
                        collections.collections_any = not collections.collections_any
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_compositions_filter(self, compositions_filter):
        while True:
            self.__view.view_message(compositions_filter)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            filters = ['compositions_ids', 'attributes', 'history', 'rating', 'playlists', 'albums']
            i = 1
            for item in filters:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    compositions_filter.compositions_ids = edit_set(compositions_filter.compositions_ids, int)
                elif res == 2:
                    self.edit_compositions_filter_attributes(compositions_filter.attributes)
                elif res == 3:
                    self.edit_compositions_filter_history(compositions_filter.history)
                elif res == 4:
                    self.edit_compositions_filter_rating(compositions_filter.rating)
                elif res == 5:
                    self.edit_compositions_filter_collections(compositions_filter.playlists)
                elif res == 6:
                    self.edit_compositions_filter_collections(compositions_filter.albums)
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_artists_filter_attributes(self, attributes):
        while True:
            self.__view.view_message(attributes)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            attrs = ['name_comment', 'types', 'search_comments']
            i = 1
            for item in attrs:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('Enter name_comment')
                    attributes.name_comment = get_str()
                elif res == 2:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    attributes.types = edit_set(attributes.types)
                elif res == 3:
                    if attributes.search_comments is None:
                        attributes.search_comments = True
                    else:
                        attributes.search_comments = not attributes.search_comments
                    self.__view.view_message('Changed')
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_artists_filter(self, artists_filter):
        while True:
            self.__view.view_message(artists_filter)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            filters = ['artists_ids', 'attributes', 'history', 'rating', 'playlists', 'albums']
            i = 1
            for item in filters:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                    self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                    artists_filter.artists_ids = edit_set(artists_filter.artists_ids, int)
                elif res == 2:
                    self.edit_artists_filter_attributes(artists_filter.attributes)
                elif res == 3:
                    self.edit_compositions_filter_history(artists_filter.history)
                elif res == 4:
                    self.edit_compositions_filter_rating(artists_filter.rating)
                elif res == 5:
                    self.edit_compositions_filter_collections(artists_filter.playlists)
                elif res == 6:
                    self.edit_compositions_filter_collections(artists_filter.albums)
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def edit_pagination_filter(self, pagination_filter):
        while True:
            self.__view.view_message(pagination_filter)
            self.__view.view_message('What to edit')
            actions = ['go back', 'page', 'page_size']
            i = 0
            for item in actions:
                self.__view.view_message(i, '-', item)
                i += 1

            try:
                res = get_int()
                if res is None:
                    raise ValueError('You need to enter action')
                elif res == 0:
                    break
                elif res == 1:
                    self.__view.view_message('Enter page')
                    pagination_filter.page = get_int()
                elif res == 2:
                    self.__view.view_message('Enter page_size')
                    pagination_filter.page_size = get_int()
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def filling_menu(self):
        while True:
            self.__view.view_message('Choose action')
            self.__view.view_message('0 - go back')
            tables = ['artists', 'compositions', 'users', 'history', 'compositions_rating',
                      'playlists', 'playlists_compositions']
            i = 1
            for item in tables:
                self.__view.view_message(i, '- fill', item)
                i += 1

            try:
                method_id = get_int()
                if method_id is None:
                    raise ValueError('You need to enter action')
                elif method_id == 0:
                    break
                elif method_id == 1:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_artists(start_number, end_number)
                elif method_id == 2:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_compositions(start_number, end_number)
                elif method_id == 3:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_users(start_number, end_number)
                elif method_id == 4:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_history(start_number, end_number)
                elif method_id == 5:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_compositions_rating(start_number, end_number)
                elif method_id == 6:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_playlists(start_number, end_number)
                elif method_id == 7:
                    self.__view.view_message('Enter start number')
                    start_number = get_int()
                    if start_number is None or start_number < 1:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Enter end number')
                    end_number = get_int()
                    if end_number is None or end_number <= start_number:
                        raise ValueError('Invalid input')

                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.__model.fill_playlists_compositions(start_number, end_number)
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def call_interface(self):
        users_filter = UserFilter()
        compositions_filter = CompositionFilter()
        artists_filter = ArtistFilter()
        pagination_filter = PaginationFilter()

        # method_list = [func for func in dir(ControllerPSQL) if callable(getattr(ControllerPSQL, func)) and
        #                not func.startswith('__') and func != 'call_interface']
        method_list = ['add_album_composition', 'add_playlist_composition', 'add_user_album', 'add_user_playlist',
                       'create_album', 'create_artist', 'create_composition', 'create_playlist', 'create_user',
                       'delete_album', 'delete_artist', 'delete_composition', 'delete_playlist', 'delete_user',
                       'get_album', 'get_album_rating', 'get_artist_rating', 'get_artists',
                       'get_composition_listening_history', 'get_composition_rating', 'get_compositions',
                       'get_playlist', 'get_playlist_rating', 'get_user_albums', 'get_user_created_playlists',
                       'get_user_listening_history', 'get_user_playlists', 'get_users', 'listen_composition',
                       'rate_album', 'rate_composition', 'rate_playlist', 'remove_album_composition',
                       'remove_playlist_composition', 'remove_user_album', 'remove_user_playlist', 'unrate_album',
                       'unrate_composition', 'unrate_playlist', 'update_album', 'update_artist', 'update_composition',
                       'update_playlist', 'update_user']
        method_list = ['add_album_composition', 'add_playlist_composition', 'add_user_album', 'add_user_playlist',
                       'create_album', 'create_artist', 'create_composition', 'create_playlist', 'create_user',
                       'delete_album', 'delete_artist', 'delete_composition', 'delete_playlist', 'delete_user',
                       'get_album', 'get_albums', 'get_artists', 'get_compositions', 'get_listening_history',
                       'get_playlist', 'get_playlists', 'get_rating', 'get_users', 'listen_composition', 'rate_album',
                       'rate_composition', 'rate_playlist', 'remove_album_composition', 'remove_playlist_composition',
                       'remove_user_album', 'remove_user_playlist', 'unrate_album', 'unrate_composition',
                       'unrate_playlist', 'update_album', 'update_artist', 'update_composition', 'update_playlist',
                       'update_user']
        while True:
            i = 1
            self.__view.view_message('Choose method')
            self.__view.view_message('-1 - exit')
            self.__view.view_message('0 - filling menu')
            for method in method_list:
                self.__view.view_message(i, '-', method)
                i += 1

            try:
                method_id = get_int()
                if method_id is None:
                    raise ValueError('You need to enter action')
                elif method_id == -1:
                    self.__view.view_message('Closing')
                    break
                elif method_id == 0:
                    self.filling_menu()
                elif method_id == 1:
                    self.__view.view_message('Enter album_id and composition_id:')
                    album_id = get_int()
                    composition_id = get_int()
                    self.add_album_composition(album_id, composition_id)
                elif method_id == 2:
                    self.__view.view_message('Enter playlist_id and composition_id:')
                    playlist_id = get_int()
                    composition_id = get_int()
                    self.add_playlist_composition(playlist_id, composition_id)
                elif method_id == 3:
                    self.__view.view_message('Enter album_id and user_id:')
                    album_id = get_int()
                    user_id = get_int()
                    self.add_user_album(album_id, user_id)
                elif method_id == 4:
                    self.__view.view_message('Enter playlist_id and user_id:')
                    playlist_id = get_int()
                    user_id = get_int()
                    self.add_user_playlist(playlist_id, user_id)
                elif method_id == 5:
                    album = self.construct_album()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.create_album(album)
                elif method_id == 6:
                    artist = self.construct_artist()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.create_artist(artist)
                elif method_id == 7:
                    composition = self.construct_composition()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.create_composition(composition)
                elif method_id == 8:
                    playlist = self.construct_playlist()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.create_playlist(playlist)
                elif method_id == 9:
                    user = self.construct_user()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.create_user(user)
                elif method_id == 10:
                    self.__view.view_message('Enter album id')
                    album_id = get_int()
                    self.delete_album(album_id)
                elif method_id == 11:
                    self.__view.view_message('Enter artist id')
                    artist_id = get_int()
                    self.delete_artist(artist_id)
                elif method_id == 12:
                    self.__view.view_message('Enter composition id')
                    composition_id = get_int()
                    self.delete_composition(composition_id)
                elif method_id == 13:
                    self.__view.view_message('Enter playlist id')
                    playlist_id = get_int()
                    self.delete_artist(playlist_id)
                elif method_id == 14:
                    self.__view.view_message('Enter user id')
                    user_id = get_int()
                    self.delete_user(user_id)
                elif method_id == 15:
                    self.__view.view_message('Enter album id')
                    album_id = get_int()
                    self.get_album(album_id)
                elif method_id == 16:  # get albums
                    pass
                elif method_id == 17:  # get artists
                    try:
                        while True:
                            self.__view.view_message('Current filters')
                            self.__view.view_message(artists_filter)
                            self.__view.view_message(pagination_filter)
                            self.__view.view_message('Choose action')
                            self.__view.view_message('0 - go back')
                            self.__view.view_message('1 - execute')
                            self.__view.view_message('2 - edit filter')
                            self.__view.view_message('3 - change pagination')
                            res = get_int()
                            if res is None:
                                raise ValueError('You need to enter action')
                            if res == 0:
                                break
                            elif res == 1:
                                self.get_artists(artists_filter, pagination_filter)
                            elif res == 2:
                                self.edit_artists_filter(artists_filter)
                            elif res == 3:
                                self.edit_pagination_filter(pagination_filter)
                            else:
                                raise ValueError('Invalid input')
                    except Exception as err:
                        self.__view.view_exception(err)
                elif method_id == 18:  # get compositions
                    try:
                        while True:
                            self.__view.view_message('Current filters')
                            self.__view.view_message(compositions_filter)
                            self.__view.view_message(pagination_filter)
                            self.__view.view_message('Choose action')
                            self.__view.view_message('0 - go back')
                            self.__view.view_message('1 - execute')
                            self.__view.view_message('2 - edit filter')
                            self.__view.view_message('3 - change pagination')
                            res = get_int()
                            if res is None:
                                raise ValueError('You need to enter action')
                            if res == 0:
                                break
                            elif res == 1:
                                self.get_compositions(compositions_filter, pagination_filter)
                            elif res == 2:
                                self.edit_compositions_filter(compositions_filter)
                            elif res == 3:
                                self.edit_pagination_filter(pagination_filter)
                            else:
                                raise ValueError('Invalid input')
                    except Exception as err:
                        self.__view.view_exception(err)
                elif method_id == 19:  # get listening history
                    pass
                elif method_id == 20:
                    self.__view.view_message('Enter playlist id')
                    playlist_id = get_int()
                    self.get_playlist(playlist_id)
                elif method_id == 21:  # get playlists
                    pass
                elif method_id == 22:  # get rating
                    pass
                elif method_id == 23:  # get users
                    try:
                        while True:
                            self.__view.view_message('Current filters')
                            self.__view.view_message(users_filter)
                            self.__view.view_message(pagination_filter)
                            self.__view.view_message('Choose action')
                            self.__view.view_message('0 - go back')
                            self.__view.view_message('1 - execute')
                            self.__view.view_message('2 - edit filter')
                            self.__view.view_message('3 - change pagination')
                            res = get_int()
                            if res is None:
                                raise ValueError('You need to enter action')
                            if res == 0:
                                break
                            elif res == 1:
                                self.get_users(users_filter, pagination_filter)
                            elif res == 2:
                                self.edit_users_filter(users_filter)
                            elif res == 3:
                                self.edit_pagination_filter(pagination_filter)
                            else:
                                raise ValueError('Invalid input')
                    except Exception as err:
                        self.__view.view_exception(err)
                elif method_id == 24:
                    record = self.construct_history_record()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.listen_composition(record)
                elif method_id == 25:
                    record = self.construct_rating_record()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.rate_album(record)
                elif method_id == 26:
                    record = self.construct_rating_record()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.rate_composition(record)
                elif method_id == 27:
                    record = self.construct_rating_record()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.rate_playlist(record)
                elif method_id == 28:
                    self.__view.view_message('Enter album_id and composition_id:')
                    album_id = get_int()
                    composition_id = get_int()
                    self.remove_album_composition(album_id, composition_id)
                elif method_id == 29:
                    self.__view.view_message('Enter playlist_id and composition_id:')
                    playlist_id = get_int()
                    composition_id = get_int()
                    self.remove_playlist_composition(playlist_id, composition_id)
                elif method_id == 30:
                    self.__view.view_message('Enter album_id and user_id:')
                    album_id = get_int()
                    user_id = get_int()
                    self.remove_user_album(album_id, user_id)
                elif method_id == 31:
                    self.__view.view_message('Enter playlist_id and user_id:')
                    playlist_id = get_int()
                    user_id = get_int()
                    self.remove_user_playlist(playlist_id, user_id)
                elif method_id == 32:
                    self.__view.view_message('Enter record id')
                    record_id = get_int()
                    self.unlisten_composition(record_id)
                elif method_id == 33:
                    self.__view.view_message('Enter album_id and user_id:')
                    album_id = get_int()
                    user_id = get_int()
                    self.unrate_album(album_id, user_id)
                elif method_id == 34:
                    self.__view.view_message('Enter composition_id and user_id:')
                    composition_id = get_int()
                    user_id = get_int()
                    self.unrate_composition(composition_id, user_id)
                elif method_id == 35:
                    self.__view.view_message('Enter playlist_id and user_id:')
                    playlist_id = get_int()
                    user_id = get_int()
                    self.unrate_playlist(playlist_id, user_id)
                elif method_id == 36:
                    album = self.construct_album()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.update_album(album)
                elif method_id == 37:
                    artist = self.construct_artist()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.update_artist(artist)
                elif method_id == 38:
                    composition = self.construct_composition()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.update_composition(composition)
                elif method_id == 39:
                    playlist = self.construct_playlist()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.update_playlist(playlist)
                elif method_id == 40:
                    user = self.construct_user()
                    self.__view.view_message('Are you sure?')
                    check = get_bool()
                    if check:
                        self.update_user(user)
                else:
                    raise ValueError('Invalid input')
            except Exception as err:
                self.__view.view_exception(err)

    def get_users(self, users_filter, pagination_filter):
        try:
            result = self.__model.get_users(users_filter, pagination_filter)
            self.__view.view_entity_list(result, 'User')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_compositions(self, compositions_filter, pagination_filter):
        try:
            result = self.__model.get_compositions(compositions_filter, pagination_filter)
            self.__view.view_entity_list(result, 'Composition')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_artists(self, artists_filter, pagination_filter):
        try:
            result = self.__model.get_artists(artists_filter, pagination_filter)
            self.__view.view_entity_list(result, 'Artist')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # standard user operations

    def create_user(self, user_model):
        try:
            result = self.__model.create_user(user_model)
            self.__view.view_entity_list(result, 'User', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def update_user(self, user_model):
        try:
            result = self.__model.update_user(user_model)
            self.__view.view_entity_list(result, 'User', 'Updated')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def delete_user(self, user_id):
        try:
            result = self.__model.delete_user(user_id)
            self.__view.view_entity_list(result, 'User', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # advanced composition operations

    def add_user_playlist(self, playlist_id, user_id):
        try:
            result = self.__model.add_user_playlist(playlist_id, user_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def remove_user_playlist(self, playlist_id, user_id):
        try:
            result = self.__model.remove_user_playlist(playlist_id, user_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_user_playlists(self, user_id):
        try:
            result = self.__model.get_user_playlists(user_id)
            self.__view.view_entity_list(result, 'Playlist')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_user_created_playlists(self, user_id):
        try:
            result = self.__model.get_user_created_playlists(user_id)
            self.__view.view_entity_list(result, 'Playlist')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def add_user_album(self, album_id, user_id):
        try:
            result = self.__model.add_user_album(album_id, user_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def remove_user_album(self, album_id, user_id):
        try:
            result = self.__model.remove_user_album(album_id, user_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_user_albums(self, user_id):
        try:
            result = self.__model.get_user_albums(user_id)
            self.__view.view_entity_list(result, 'Album')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_user_listening_history(self, user_id):
        try:
            result = self.__model.get_user_listening_history(user_id)
            self.__view.view_entity_list(result, 'History record')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # standard composition operations

    def create_composition(self, composition_model):
        try:
            result = self.__model.create_composition(composition_model)
            self.__view.view_entity_list(result, 'Composition', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def update_composition(self, composition_model):
        try:
            result = self.__model.update_composition(composition_model)
            self.__view.view_entity_list(result, 'Composition', 'Updated')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def delete_composition(self, composition_id):
        try:
            result = self.__model.delete_composition(composition_id)
            self.__view.view_entity_list(result, 'Composition', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # advanced composition operations

    def listen_composition(self, history_record):
        try:
            result = self.__model.listen_composition(history_record)
            self.__view.view_entity_list(result, 'History record', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def unlisten_composition(self, history_record):
        try:
            result = self.__model.unlisten_composition(history_record)
            self.__view.view_entity_list(result, 'History record', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_composition_listening_history(self, composition_id):
        try:
            result = self.__model.get_composition_listening_history(composition_id)
            self.__view.view_entity_list(result, 'History record')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def rate_composition(self, rating_model):
        try:
            result = self.__model.rate_composition(rating_model)
            self.__view.view_entity_list(result, 'Composition rating record', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def unrate_composition(self, composition_id, user_id):
        try:
            result = self.__model.unrate_composition(composition_id, user_id)
            self.__view.view_entity_list(result, 'Composition rating record', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_composition_rating(self, composition_id):
        try:
            result = self.__model.get_composition_rating(composition_id)
            self.__view.view_entity_list(result, 'Composition rating record')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # standard artist operations

    def create_artist(self, artist_model):
        try:
            result = self.__model.create_artist(artist_model)
            self.__view.view_entity_list(result, 'Artist', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def update_artist(self, artist_model):
        try:
            result = self.__model.update_artist(artist_model)
            self.__view.view_entity_list(result, 'Artist', 'Updated')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def delete_artist(self, artist_id):
        try:
            result = self.__model.delete_artist(artist_id)
            self.__view.view_entity_list(result, 'Artist', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # advanced artist operations

    def get_artist_rating(self, artist_id):
        try:
            result = self.__model.get_artist_rating(artist_id)
            self.__view.view_entity_list(result, 'Artist rating record')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # standard playlist operations

    def create_playlist(self, playlist_model):
        try:
            result = self.__model.create_playlist(playlist_model)
            self.__view.view_entity_list(result, 'Playlist', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def update_playlist(self, playlist_model):
        try:
            result = self.__model.update_playlist(playlist_model)
            self.__view.view_entity_list(result, 'Playlist', 'Updated')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def delete_playlist(self, playlist_id):
        try:
            result = self.__model.delete_playlist(playlist_id)
            self.__view.view_entity_list(result, 'Playlist', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_playlist(self, playlist_id):
        try:
            result = self.__model.get_playlist(playlist_id)
            self.__view.view_entity_list(result, 'Playlist')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # advanced playlist operations

    def add_playlist_composition(self, playlist_id, composition_id):
        try:
            result = self.__model.add_playlist_composition(playlist_id, composition_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def remove_playlist_composition(self, playlist_id, composition_id):
        try:
            result = self.__model.remove_playlist_composition(playlist_id, composition_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def rate_playlist(self, rating_model):
        try:
            result = self.__model.rate_playlist(rating_model)
            self.__view.view_entity_list(result, 'Playlist rating record', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def unrate_playlist(self, playlist_id, user_id):
        try:
            result = self.__model.unrate_playlist(playlist_id, user_id)
            self.__view.view_entity_list(result, 'Playlist rating record', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_playlist_rating(self, playlist_id):
        try:
            result = self.__model.get_playlist_rating(playlist_id)
            self.__view.view_entity_list(result, 'Playlist rating record')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # standard album operations

    def create_album(self, album_model):
        try:
            result = self.__model.create_album(album_model)
            self.__view.view_entity_list(result, 'Album', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def update_album(self, album_model):
        try:
            result = self.__model.update_album(album_model)
            self.__view.view_entity_list(result, 'Album', 'Updated')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def delete_album(self, album_id):
        try:
            result = self.__model.delete_album(album_id)
            self.__view.view_entity_list(result, 'Album', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_album(self, album_id):
        try:
            result = self.__model.get_album(album_id)
            self.__view.view_entity_list(result, 'Album')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    # advanced album operations

    def add_album_composition(self, album_id, composition_id):
        try:
            result = self.__model.add_album_composition(album_id, composition_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def remove_album_composition(self, album_id, composition_id):
        try:
            result = self.__model.remove_album_composition(album_id, composition_id)
            self.__view.view_boolean_result(result)
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def rate_album(self, rating_model):
        try:
            result = self.__model.rate_album(rating_model)
            self.__view.view_entity_list(result, 'Album rating record', 'Created')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def unrate_album(self, album_id, user_id):
        try:
            result = self.__model.unrate_album(album_id, user_id)
            self.__view.view_entity_list(result, 'Album rating record', 'Deleted')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)

    def get_album_rating(self, album_id):
        try:
            result = self.__model.get_album_rating(album_id)
            self.__view.view_entity_list(result, 'Album rating record')
            self.__view.view_query_runtime(self.__model.last_query_runtime)
        except Exception as err:
            self.__view.view_exception(err)
