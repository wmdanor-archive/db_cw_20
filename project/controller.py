from model import ModelPSQL, PaginationFilter
import view
import datetime

from models.user import User
from models.composition import Composition
from models.performer import Artist
from models.album import Album
from models.playlist import Playlist
from models.rating import Rating
from models.history_record import HistoryRecord
from models.filters import *


def to_int(number):
    try:
        return int(number)
    except Exception as err:
        return None


def to_float(number):
    try:
        return float(number)
    except Exception as err:
        return None


def is_valid_date(string):
    try:
        datetime.datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True


class ControllerPSQL:

    def __init__(self, connection):
        self.__model = ModelPSQL(connection)
        self.__view = view

    # interface

    def construct_album(self):
        self.__view.view_message('Enter title')
        title = input()
        if not title:
            self.__view.view_message('Title can not be None')
            return None
        self.__view.view_message('Enter release year')
        release_year = None
        release_year_in = input()
        if release_year_in:
            release_year = to_int(release_year_in)
            if release_year is None:
                self.__view.view_message('NaN')
                return None
        return Album(0, title, release_year)

    def construct_artist(self):
        self.__view.view_message('Enter name')
        name = input()
        if not name:
            self.__view.view_message('Name can not be None')
            return None
        self.__view.view_message('Choose type')
        types = ['person', 'group', 'orchestra', 'choir', 'character', 'other']
        i = 1
        for item in types:
            self.__view.view_message(i, '-', item)
            i += 1
        type_id = to_int(input())
        if type_id is None or not 1 <= type_id <= 6:
            self.__view.view_message('Invalid input')
            return None

        return Artist(0, name, type_id)

    def construct_composition(self):
        self.__view.view_message('Enter title')
        title = input()
        if not title:
            self.__view.view_message('Title can not be None')

        self.__view.view_message('Enter artist id')
        artist_id_in = input()
        artist_id = None
        if artist_id_in:
            artist_id = to_int(artist_id_in)
            if artist_id is None:
                self.__view.view_message('NaN')
                return None

        self.__view.view_message('Enter duration (seconds)')
        duration = to_int(input())
        if duration is None:
            self.__view.view_message('NaN')
            return None

        self.__view.view_message('Enter path to file')
        path_to_file = input()
        if not path_to_file:
            self.__view.view_message('Path can not be None')
            return None

        self.__view.view_message('Enter lyrics')
        lyrics = input()
        if not lyrics:
            lyrics = None

        release_year = None
        release_month = None
        release_day = None
        self.__view.view_message('Enter release year')
        year_in = input()
        if year_in:
            release_year = to_int(year_in)
            if release_year is None:
                self.__view.view_message('Nan')
                return None
            self.__view.view_message('Enter release month')
            month_in = input()
            if month_in:
                release_month = to_int(month_in)
                if release_month is None or not 1 <= release_month <= 12:
                    self.__view.view_message('Invalid month')
                    return None
                self.__view.view_message('Enter release day')
                day_in = input()
                if day_in:
                    release_day = to_int(day_in)
                    if release_day is None:
                        self.__view.view_message('NaN')
                    try:
                        datetime.datetime(release_year, release_month, release_day)
                    except ValueError:
                        self.__view.view_message('Invalid date')
                        return None

        return Composition(0, title, duration, path_to_file, 0, release_year, release_month, release_day, lyrics)

    def construct_playlist(self):
        self.__view.view_message('Enter title')
        title = input()
        if not title:
            self.__view.view_message('Title can not be None')
            return None

        self.__view.view_message('Enter creator_id')
        creator_id = None
        creator_in = input()
        if creator_in:
            creator_id = to_int(creator_in)
            if creator_id is None:
                self.__view.view_message('NaN')
                return None

        self.__view.view_message('Choose privacy')
        privacy_types = ['public', 'unlisted', 'private']
        i = 1
        for item in privacy_types:
            self.__view.view_message(i, '-', item)
            i += 1
        privacy_id = to_int(input())
        if privacy_id is None or not 1 <= privacy_id <= 3:
            self.__view.view_message('Invalid input')
            return None

        return Playlist(0, title, privacy_id, creator_id=creator_id)

    def construct_user(self):
        self.__view.view_message('Enter username')
        username = input()
        if not username:
            self.__view.view_message('Username can not be None')
            return None

        self.__view.view_message('Enter password hash')
        password_hash = input()
        if not password_hash:
            self.__view.view_message('Password hash can not be None')
            return None

        self.__view.view_message('Enter registration date (ISO8601)')
        registration_date = input()
        if not registration_date:
            self.__view.view_message('Can not be None')
            return None
        if not is_valid_date(registration_date):
            self.__view.view_message('Invalid date')
            return None

        self.__view.view_message('Is active? yes/no')
        is_active_in = input()
        is_active = None
        if not is_active_in:
            self.__view.view_message('Can not be None')
            return None
        if is_active_in == 'yes':
            is_active = True
        elif is_active_in == 'no':
            is_active = False
        else:
            self.__view.view_message('Invalid input')
            return None

        self.__view.view_message('Enter full name')
        full_name = input()
        if not full_name:
            full_name = None

        self.__view.view_message('Enter birth date (ISO8601)')
        birth_date = input()
        if not birth_date:
            birth_date = None
        else:
            if not is_valid_date(birth_date):
                self.__view.view_message('Invalid date')
                return None

        self.__view.view_message('Choose gender')
        genders = ['male', 'female', 'other']
        i = 1
        for item in genders:
            self.__view.view_message(i, '-', item)
            i += 1
        gender_id = to_int(input())
        if gender_id is None or not 1 <= gender_id <= 3:
            self.__view.view_message('Invalid input')
            return None

        return User(0, username, password_hash, registration_date, is_active, full_name, birth_date, gender_id)

    def construct_history_record(self):
        self.__view.view_message('Enter user_id')
        user_id = to_int(input())
        if user_id is None:
            self.__view.view_message('NaN')
            return None

        self.__view.view_message('Enter composition_id')
        composition_id = to_int(input())
        if composition_id is None:
            self.__view.view_message('NaN')
            return None

        self.__view.view_message('Enter date (ISO8601)')
        action_date = to_int(input())
        if not action_date:
            self.__view.view_message('Can not be None')
            return None
        if not is_valid_date(action_date):
            self.__view.view_message('Invalid date')
            return None

        return HistoryRecord(0,composition_id, user_id, action_date)

    def construct_rating_record(self):
        self.__view.view_message('Enter user_id')
        user_id = to_int(input())
        if user_id is None:
            self.__view.view_message('NaN')
            return None

        self.__view.view_message('Enter rated_id')
        rated_id = to_int(input())
        if rated_id is None:
            self.__view.view_message('NaN')
            return None

        self.__view.view_message('Enter date (ISO8601)')
        action_date = input()
        if not action_date:
            self.__view.view_message('Can not be None')
            return None
        if not is_valid_date(action_date):
            self.__view.view_message('Invalid date')
            return None

        self.__view.view_message('Is satisfied? yes/no')
        is_satisfied_in = input()
        is_satisfied = None
        if not is_satisfied_in:
            self.__view.view_message('Can not be None')
            return None
        if is_satisfied_in == 'yes':
            is_satisfied = True
        elif is_satisfied_in == 'no':
            is_satisfied = False
        else:
            self.__view.view_message('Invalid input')
            return None

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('Enter username')
                username = input()
                if not username:
                    username = None
                attributes.username = username
            elif res == 2:
                self.__view.view_message('Enter full_name')
                full_name = input()
                if not full_name:
                    full_name = None
                attributes.full_name = full_name
            elif res == 3:
                self.__view.view_message('Enter registration_from')
                registration_from = input()
                if not registration_from:
                    registration_from = None
                elif not is_valid_date(registration_from):
                    self.__view.view_message('Invalid date')
                    continue
                attributes.registration_from = registration_from
            elif res == 4:
                self.__view.view_message('Enter registration_to')
                registration_to = input()
                if not registration_to:
                    registration_to = None
                elif not is_valid_date(registration_to):
                    self.__view.view_message('Invalid date')
                    continue
                attributes.registration_to = registration_to
            elif res == 5:
                self.__view.view_message('Enter birth_from')
                birth_from = input()
                if not birth_from:
                    birth_from = None
                elif not is_valid_date(birth_from):
                    self.__view.view_message('Invalid date')
                    continue
                attributes.birth_from = birth_from
            elif res == 6:
                self.__view.view_message('Enter birth_to')
                birth_to = input()
                if not birth_to:
                    birth_to = None
                elif not is_valid_date(birth_to):
                    self.__view.view_message('Invalid date')
                    continue
                attributes.birth_to = birth_to
            elif res == 7:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set(arr)
                if cmd == 'ADD':
                    if attributes.genders is None:
                        attributes.genders = set()
                    attributes.genders = attributes.genders.union(vals)
                elif cmd == 'REM':
                    if attributes.genders is None:
                        continue
                    attributes.genders.difference_update(vals)
                    if not attributes.genders:
                        attributes.genders = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 8:
                self.__view.view_message('Is active? yes/no')
                ans = input()
                is_active = None
                if not ans:
                    is_active = None
                elif ans == 'yes':
                    is_active = True
                elif ans == 'no':
                    is_active = False
                else:
                    self.__view.view_message('Invalid input')
                    continue
                attributes.is_active = is_active
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
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
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
                listened_date_from = input()
                if not listened_date_from:
                    listened_date_from = None
                elif not is_valid_date(listened_date_from):
                    self.__view.view_message('Invalid date')
                    continue
                history.listened_date_from = listened_date_from
            elif res == 3:
                self.__view.view_message('Enter listened_date_to')
                listened_date_to = input()
                if not listened_date_to:
                    listened_date_to = None
                elif not is_valid_date(listened_date_to):
                    self.__view.view_message('Invalid date')
                    continue
                history.listened_date_to = listened_date_to
            elif res == 4:
                self.__view.view_message('Enter times_listened_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                history.times_listened_from = new_val
            elif res == 5:
                self.__view.view_message('Enter times_listened_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                history.times_listened_to = new_val
            elif res == 6:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if history.compositions_ids is None:
                        history.compositions_ids = set()
                    history.compositions_ids = history.compositions_ids.union(vals)
                elif cmd == 'REM':
                    if history.compositions_ids is None:
                        continue
                    history.compositions_ids.difference_update(vals)
                    if not history.compositions_ids:
                        history.compositions_ids = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 7:
                if history.compositions_ids_any is None:
                    history.compositions_ids_any = True
                else:
                    history.compositions_ids_any = not history.compositions_ids_any
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
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
                new_val = input()
                if not new_val:
                    new_val = None
                elif not is_valid_date(new_val):
                    self.__view.view_message('Invalid date')
                    continue
                rating.rating_date_from = new_val
            elif res == 3:
                self.__view.view_message('Enter rating_date_to')
                new_val = input()
                if not new_val:
                    new_val = None
                elif not is_valid_date(new_val):
                    self.__view.view_message('Invalid date')
                    continue
                rating.rating_date_to = new_val
            elif res == 4:
                self.__view.view_message('Enter times_rated_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.times_rated_from = new_val
            elif res == 5:
                self.__view.view_message('Enter times_rated_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.times_rated_to = new_val
            elif res == 6:
                self.__view.view_message('Enter average_rating_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_float(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.average_rating_from = new_val
            elif res == 7:
                self.__view.view_message('Enter average_rating_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_float(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.average_rating_to = new_val
            elif res == 8:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if rating.rated_ids is None:
                        rating.rated_ids = set()
                    rating.rated_ids = rating.rated_ids.union(vals)
                elif cmd == 'REM':
                    if rating.rated_ids is None:
                        continue
                    rating.rated_ids.difference_update(vals)
                    if not rating.rated_ids:
                        rating.rated_ids = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 9:
                if rating.rated_ids_any is None:
                    rating.rated_ids_any = True
                else:
                    rating.rated_ids_any = not rating.rated_ids_any
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
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
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                saved_collections.saved_number_from = new_val
            elif res == 3:
                self.__view.view_message('Enter saved_number_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                saved_collections.saved_number_to = new_val
            elif res == 4:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if saved_collections.saved_ids_list is None:
                        saved_collections.saved_ids_list = set()
                    saved_collections.saved_ids_list = saved_collections.saved_ids_list.union(vals)
                elif cmd == 'REM':
                    if saved_collections.saved_ids_list is None:
                        continue
                    saved_collections.saved_ids_list.difference_update(vals)
                    if not saved_collections.saved_ids_list:
                        saved_collections.saved_ids_list = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 5:
                if saved_collections.saved_ids_any is None:
                    saved_collections.saved_ids_any = True
                else:
                    saved_collections.saved_ids_any = not saved_collections.saved_ids_any
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if users_filter.users_ids is None:
                        users_filter.users_ids = set()
                    users_filter.users_ids = users_filter.users_ids.union(vals)
                elif cmd == 'REM':
                    if users_filter.users_ids is None:
                        continue
                    users_filter.users_ids.difference_update(vals)
                    if not users_filter.users_ids:
                        users_filter.users_ids = None
                else:
                    self.__view.view_message('Invalid input')
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
                self.__view.view_message('Invalid command')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('Enter title_lyrics')
                new_val = input()
                if not new_val:
                    new_val = None
                attributes.title_lyrics = new_val
            elif res == 2:
                if attributes.artists_ids_exclude_nulls is None:
                    attributes.artists_ids_exclude_nulls = True
                else:
                    attributes.artists_ids_exclude_nulls = not attributes.artists_ids_exclude_nulls
                self.__view.view_message('Changed')
            elif res == 3:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if attributes.artists_ids is None:
                        attributes.artists_ids = set()
                    attributes.artists_ids = attributes.artists_ids.union(vals)
                elif cmd == 'REM':
                    if attributes.artists_ids is None:
                        continue
                    attributes.artists_ids.difference_update(vals)
                    if not attributes.artists_ids:
                        attributes.artists_ids = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 4:
                self.__view.view_message('Enter duration_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                attributes.duration_from = new_val
            elif res == 5:
                self.__view.view_message('Enter duration_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                attributes.duration_to = new_val
            elif res == 6:
                if attributes.release_date_exclude_nulls is None:
                    attributes.release_date_exclude_nulls = True
                else:
                    attributes.release_date_exclude_nulls = not attributes.release_date_exclude_nulls
                self.__view.view_message('Changed')
            elif res == 7:
                self.__view.view_message('Enter release_from')
                new_val = input()
                if not new_val:
                    new_val = None
                elif not is_valid_date(new_val):
                    self.__view.view_message('Invalid date')
                    continue
                attributes.release_from = new_val
            elif res == 8:
                self.__view.view_message('Enter release_to')
                new_val = input()
                if not new_val:
                    new_val = None
                elif not is_valid_date(new_val):
                    self.__view.view_message('Invalid date')
                    continue
                attributes.release_to = new_val
            elif res == 9:
                if attributes.search_lyrics is None:
                    attributes.search_lyrics = True
                else:
                    attributes.search_lyrics = not attributes.search_lyrics
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
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
                listened_date_from = input()
                if not listened_date_from:
                    listened_date_from = None
                elif not is_valid_date(listened_date_from):
                    self.__view.view_message('Invalid date')
                    continue
                history.listened_date_from = listened_date_from
            elif res == 3:
                self.__view.view_message('Enter listened_date_to')
                listened_date_to = input()
                if not listened_date_to:
                    listened_date_to = None
                elif not is_valid_date(listened_date_to):
                    self.__view.view_message('Invalid date')
                    continue
                history.listened_date_to = listened_date_to
            elif res == 4:
                self.__view.view_message('Enter times_listened_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                history.times_listened_from = new_val
            elif res == 5:
                self.__view.view_message('Enter times_listened_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                history.times_listened_to = new_val
            elif res == 6:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if history.users_ids is None:
                        history.users_ids = set()
                    history.users_ids = history.users_ids.union(vals)
                elif cmd == 'REM':
                    if history.users_ids is None:
                        continue
                    history.users_ids.difference_update(vals)
                    if not history.users_ids:
                        history.users_ids = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 7:
                if history.users_ids_any is None:
                    history.users_ids_any = True
                else:
                    history.users_ids_any = not history.users_ids_any
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
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
                new_val = input()
                if not new_val:
                    new_val = None
                elif not is_valid_date(new_val):
                    self.__view.view_message('Invalid date')
                    continue
                rating.rating_date_from = new_val
            elif res == 3:
                self.__view.view_message('Enter rating_date_to')
                new_val = input()
                if not new_val:
                    new_val = None
                elif not is_valid_date(new_val):
                    self.__view.view_message('Invalid date')
                    continue
                rating.rating_date_to = new_val
            elif res == 4:
                self.__view.view_message('Enter times_rated_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.times_rated_from = new_val
            elif res == 5:
                self.__view.view_message('Enter times_rated_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.times_rated_to = new_val
            elif res == 6:
                self.__view.view_message('Enter average_rating_from')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_float(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.average_rating_from = new_val
            elif res == 7:
                self.__view.view_message('Enter average_rating_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_float(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                rating.average_rating_to = new_val
            elif res == 8:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if rating.users_ids is None:
                        rating.users_ids = set()
                    rating.users_ids = rating.users_ids.union(vals)
                elif cmd == 'REM':
                    if rating.users_ids is None:
                        continue
                    rating.users_ids.difference_update(vals)
                    if not rating.users_ids:
                        rating.users_ids = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 9:
                if rating.users_ids_any is None:
                    rating.users_ids_any = True
                else:
                    rating.users_ids_any = not rating.users_ids_any
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
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
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                collections.number_belongs_from = new_val
            elif res == 3:
                self.__view.view_message('Enter number_belongs_to')
                new_val = None
                ans = input()
                if ans:
                    new_val = to_int(ans)
                    if new_val is None:
                        self.__view.view_message('NaN')
                        continue
                collections.number_belongs_to = new_val
            elif res == 4:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if collections.collections_list is None:
                        collections.collections_list = set()
                    collections.collections_list = collections.collections_list.union(vals)
                elif cmd == 'REM':
                    if collections.collections_list is None:
                        continue
                    collections.collections_list.difference_update(vals)
                    if not collections.collections_list:
                        collections.collections_list = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 5:
                if collections.collections_any is None:
                    collections.collections_any = True
                else:
                    collections.collections_any = not collections.collections_any
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if compositions_filter.compositions_ids is None:
                        compositions_filter.compositions_ids = set()
                    compositions_filter.compositions_ids = compositions_filter.compositions_ids.union(vals)
                elif cmd == 'REM':
                    if compositions_filter.compositions_ids is None:
                        continue
                    compositions_filter.compositions_ids.difference_update(vals)
                    if not compositions_filter.compositions_ids:
                        compositions_filter.compositions_ids = None
                else:
                    self.__view.view_message('Invalid input')
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
                self.__view.view_message('Invalid command')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('Enter name_comment')
                new_val = input()
                if not new_val:
                    new_val = None
                attributes.name_comment = new_val
            elif res == 2:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set(arr)
                if cmd == 'ADD':
                    if attributes.types is None:
                        attributes.types = set()
                    attributes.types = attributes.types.union(vals)
                elif cmd == 'REM':
                    if attributes.types is None:
                        continue
                    attributes.types.difference_update(vals)
                    if not attributes.types:
                        attributes.types = None
                else:
                    self.__view.view_message('Invalid input')
            elif res == 3:
                if attributes.search_comments is None:
                    attributes.search_comments = True
                else:
                    attributes.search_comments = not attributes.search_comments
                self.__view.view_message('Changed')
            else:
                self.__view.view_message('Invalid input')

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
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('To add type: ADD a1 a2 a3 ...')
                self.__view.view_message('To remove type: REM a1 a2 a3 ...')
                command = input()
                if not command:
                    continue
                arr = command.split()
                cmd = arr[0]
                arr.pop(0)
                vals = set()
                for item in arr:
                    el = to_int(item)
                    if el is None:
                        self.__view.view_message(el, 'is not a number')
                        continue
                    vals.add(el)
                if cmd == 'ADD':
                    if artists_filter.artists_ids is None:
                        artists_filter.artists_ids = set()
                    artists_filter.artists_ids = artists_filter.artists_ids.union(vals)
                elif cmd == 'REM':
                    if artists_filter.artists_ids is None:
                        continue
                    artists_filter.artists_ids.difference_update(vals)
                    if not artists_filter.artists_ids:
                        artists_filter.artists_ids = None
                else:
                    self.__view.view_message('Invalid input')
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
                self.__view.view_message('Invalid command')

    def edit_pagination_filter(self, pagination_filter):
        while True:
            self.__view.view_message(pagination_filter)
            self.__view.view_message('What to edit')
            self.__view.view_message('0 - go back')
            self.__view.view_message('1 - page')
            self.__view.view_message('2 - page_size')
            res = to_int(input())
            if res is None:
                self.__view.view_message('NaN')
            elif res == 0:
                break
            elif res == 1:
                self.__view.view_message('Enter page')
                page = None
                page_in = input()
                if page_in:
                    page = to_int(page_in)
                    if page is None:
                        self.__view.view_message('NaN')
                pagination_filter.page = page
            elif res == 2:
                self.__view.view_message('Enter page_size')
                page_size = None
                page_size_in = input()
                if page_size_in:
                    page_size = to_int(page_size_in)
                    if page_size is None:
                        self.__view.view_message('NaN')
                pagination_filter.page_size = page_size
            else:
                self.__view.view_message('Invalid input')

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

            answer = input()
            method_id = to_int(answer)

            if method_id is None:
                self.__view.view_message('NaN')
            elif method_id == 0:
                break
            elif method_id == 1:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_artists(start_number, end_number)
            elif method_id == 2:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_compositions(start_number, end_number)
            elif method_id == 3:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_users(start_number, end_number)
            elif method_id == 4:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_history(start_number, end_number)
            elif method_id == 5:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_compositions_rating(start_number, end_number)
            elif method_id == 6:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_playlists(start_number, end_number)
            elif method_id == 7:
                self.__view.view_message('Enter start number')
                start_number = to_int(input())
                if start_number is None or start_number < 1:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Enter end number')
                end_number = to_int(input())
                if end_number is None or end_number <= start_number:
                    self.__view.view_message('Invalid input')
                    continue

                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.__model.fill_playlists_compositions(start_number, end_number)
            else:
                self.__view.view_message('Invalid input')

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
        while True:
            i = 1
            self.__view.view_message('Choose method')
            self.__view.view_message('-1 - exit')
            self.__view.view_message('0 - filling menu')
            for method in method_list:
                self.__view.view_message(i, '-', method)
                i += 1

            answer = input()
            method_id = to_int(answer)

            if method_id is None:
                self.__view.view_message('NaN')
            elif method_id == -1:
                self.__view.view_message('Closing')
                break
            elif method_id == 0:
                self.filling_menu()
            elif method_id == 1:
                self.__view.view_message('Enter album_id and composition_id:')
                album_id = to_int(input())
                composition_id = to_int(input())
                if album_id is None or composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.add_album_composition(album_id, composition_id)
            elif method_id == 2:
                self.__view.view_message('Enter playlist_id and composition_id:')
                playlist_id = to_int(input())
                composition_id = to_int(input())
                if playlist_id is None or composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.add_playlist_composition(playlist_id, composition_id)
            elif method_id == 3:
                self.__view.view_message('Enter album_id and user_id:')
                album_id = to_int(input())
                user_id = to_int(input())
                if album_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.add_user_album(album_id, user_id)
            elif method_id == 4:
                self.__view.view_message('Enter playlist_id and user_id:')
                playlist_id = to_int(input())
                user_id = to_int(input())
                if playlist_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.add_user_playlist(playlist_id, user_id)
            elif method_id == 5:
                album = self.construct_album()
                if album is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.create_album(album)
            elif method_id == 6:
                artist = self.construct_artist()
                if artist is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.create_artist(artist)
            elif method_id == 7:
                composition = self.construct_composition()
                if composition is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.create_composition(composition)
            elif method_id == 8:
                playlist = self.construct_playlist()
                if playlist is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.create_playlist(playlist)
            elif method_id == 9:
                user = self.construct_user()
                if user is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.create_user(user)
            elif method_id == 10:
                self.__view.view_message('Enter album id')
                album_id = to_int(input())
                if album_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.delete_album(album_id)
            elif method_id == 11:
                self.__view.view_message('Enter artist id')
                artist_id = to_int(input())
                if artist_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.delete_artist(artist_id)
            elif method_id == 12:
                self.__view.view_message('Enter composition id')
                composition_id = to_int(input())
                if composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.delete_composition(composition_id)
            elif method_id == 13:
                self.__view.view_message('Enter playlist id')
                playlist_id = to_int(input())
                if playlist_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.delete_artist(playlist_id)
            elif method_id == 14:
                self.__view.view_message('Enter user id')
                user_id = to_int(input())
                if user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.delete_user(user_id)
            elif method_id == 15:
                self.__view.view_message('Enter album id')
                album_id = to_int(input())
                if album_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_album(album_id)
            elif method_id == 16:
                self.__view.view_message('Enter album id')
                album_id = to_int(input())
                if album_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_album_rating(album_id)
            elif method_id == 17:
                self.__view.view_message('Enter artist id')
                artist_id = to_int(input())
                if artist_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_artist_rating(artist_id)
            elif method_id == 18:
                while True:
                    self.__view.view_message('Current filters')
                    self.__view.view_message(artists_filter)
                    self.__view.view_message(pagination_filter)
                    self.__view.view_message('Choose action')
                    self.__view.view_message('0 - go back')
                    self.__view.view_message('1 - execute')
                    self.__view.view_message('2 - edit filter')
                    self.__view.view_message('3 - change pagination')
                    res = to_int(input())
                    if res is None:
                        self.__view.view_message('NaN')
                        continue
                    if res == 0:
                        break
                    elif res == 1:
                        self.get_artists(artists_filter, pagination_filter)
                    elif res == 2:
                        self.edit_artists_filter(artists_filter)
                    elif res == 3:
                        self.edit_pagination_filter(pagination_filter)
                    else:
                        self.__view.view_message('Invalid input')
            elif method_id == 19:
                self.__view.view_message('Enter composition id')
                composition_id = to_int(input())
                if composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_composition_listening_history(composition_id)
            elif method_id == 20:
                self.__view.view_message('Enter composition id')
                composition_id = to_int(input())
                if composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_composition_rating(composition_id)
            elif method_id == 21:
                while True:
                    self.__view.view_message('Current filters')
                    self.__view.view_message(compositions_filter)
                    self.__view.view_message(pagination_filter)
                    self.__view.view_message('Choose action')
                    self.__view.view_message('0 - go back')
                    self.__view.view_message('1 - execute')
                    self.__view.view_message('2 - edit filter')
                    self.__view.view_message('3 - change pagination')
                    res = to_int(input())
                    if res is None:
                        self.__view.view_message('NaN')
                        continue
                    if res == 0:
                        break
                    elif res == 1:
                        self.get_compositions(compositions_filter, pagination_filter)
                    elif res == 2:
                        self.edit_compositions_filter(compositions_filter)
                    elif res == 3:
                        self.edit_pagination_filter(pagination_filter)
                    else:
                        self.__view.view_message('Invalid input')
            elif method_id == 22:
                self.__view.view_message('Enter playlist id')
                playlist_id = to_int(input())
                if playlist_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_playlist(playlist_id)
            elif method_id == 23:
                self.__view.view_message('Enter playlist id')
                playlist_id = to_int(input())
                if playlist_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_playlist_rating(playlist_id)
            elif method_id == 24:
                self.__view.view_message('Enter user id')
                user_id = to_int(input())
                if user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_user_albums(user_id)
            elif method_id == 25:
                self.__view.view_message('Enter user id')
                user_id = to_int(input())
                if user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_user_created_playlists(user_id)
            elif method_id == 26:
                self.__view.view_message('Enter user id')
                user_id = to_int(input())
                if user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_user_listening_history(user_id)
            elif method_id == 27:
                self.__view.view_message('Enter user id')
                user_id = to_int(input())
                if user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.get_user_playlists(user_id)
            elif method_id == 28:
                while True:
                    self.__view.view_message('Current filters')
                    self.__view.view_message(users_filter)
                    self.__view.view_message(pagination_filter)
                    self.__view.view_message('Choose action')
                    self.__view.view_message('0 - go back')
                    self.__view.view_message('1 - execute')
                    self.__view.view_message('2 - edit filter')
                    self.__view.view_message('3 - change pagination')
                    res = to_int(input())
                    if res is None:
                        self.__view.view_message('NaN')
                        continue
                    if res == 0:
                        break
                    elif res == 1:
                        self.get_users(users_filter, pagination_filter)
                    elif res == 2:
                        self.edit_users_filter(users_filter)
                    elif res == 3:
                        self.edit_pagination_filter(pagination_filter)
                    else:
                        self.__view.view_message('Invalid input')
            elif method_id == 29:
                record = self.construct_history_record()
                if record is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.listen_composition(record)
            elif method_id == 30:
                record = self.construct_rating_record()
                if record is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.rate_album(record)
            elif method_id == 31:
                record = self.construct_rating_record()
                if record is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.rate_composition(record)
            elif method_id == 32:
                record = self.construct_rating_record()
                if record is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.rate_playlist(record)
            elif method_id == 33:
                self.__view.view_message('Enter album_id and composition_id:')
                album_id = to_int(input())
                composition_id = to_int(input())
                if album_id is None or composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.remove_album_composition(album_id, composition_id)
            elif method_id == 34:
                self.__view.view_message('Enter playlist_id and composition_id:')
                playlist_id = to_int(input())
                composition_id = to_int(input())
                if playlist_id is None or composition_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.remove_playlist_composition(playlist_id, composition_id)
            elif method_id == 35:
                self.__view.view_message('Enter album_id and user_id:')
                album_id = to_int(input())
                user_id = to_int(input())
                if album_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.remove_user_album(album_id, user_id)
            elif method_id == 36:
                self.__view.view_message('Enter playlist_id and user_id:')
                playlist_id = to_int(input())
                user_id = to_int(input())
                if playlist_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.remove_user_playlist(playlist_id, user_id)
            elif method_id == 37:
                self.__view.view_message('Enter album_id and user_id:')
                album_id = to_int(input())
                user_id = to_int(input())
                if album_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.unrate_album(album_id, user_id)
            elif method_id == 38:
                self.__view.view_message('Enter composition_id and user_id:')
                composition_id = to_int(input())
                user_id = to_int(input())
                if composition_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.unrate_composition(composition_id, user_id)
            elif method_id == 39:
                self.__view.view_message('Enter playlist_id and user_id:')
                playlist_id = to_int(input())
                user_id = to_int(input())
                if playlist_id is None or user_id is None:
                    self.__view.view_message('NaN')
                else:
                    self.unrate_playlist(playlist_id, user_id)
            elif method_id == 40:
                    album = self.construct_album()
                    if album is None:
                        continue
                    self.__view.view_message('Are you sure? yes/no')
                    check = input()
                    if check == 'yes':
                        self.update_album(album)
            elif method_id == 41:
                artist = self.construct_artist()
                if artist is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.update_artist(artist)
            elif method_id == 42:
                composition = self.construct_composition()
                if composition is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.update_composition(composition)
            elif method_id == 43:
                playlist = self.construct_playlist()
                if playlist is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.update_playlist(playlist)
            elif method_id == 44:
                user = self.construct_user()
                if user is None:
                    continue
                self.__view.view_message('Are you sure? yes/no')
                check = input()
                if check == 'yes':
                    self.update_user(user)
            else:
                self.__view.view_message('Invalid input')

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
