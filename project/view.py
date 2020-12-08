import datetime
from copy import copy
from distutils.util import strtobool

from controller import ControllerPSQL
from model import PaginationFilter
from models.album import Album
from models.composition import Composition
from models.filters import *
from models.history_record import HistoryRecord
from models.performer import Artist
from models.playlist import Playlist
from models.rating import Rating
from models.user import User

import matplotlib.pyplot as plt


def getters_interface(getter_func, filters, pagination_filter, possible_orders):
    orders = [1]
    while True:
        print('Current filters')
        print(filters)
        print('Order by:', orders)
        print(pagination_filter)
        print('Choose action')
        view_numerated_array(['go back', 'execute', 'edit filter', 'change order by', 'change pagination'])

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            if res == 0:
                break
            elif res == 1:
                print(getter_func(filters, orders, pagination_filter))
            elif res == 2:
                edit_entity_filters(filters)
            elif res == 3:
                print('Available orders:')
                view_numerated_array(possible_orders, 1)
                orders = get_unique_list(len(possible_orders), 'order')
                if orders is None:
                    orders = [1]
                    raise ValueError('Orders can not be empty')
            elif res == 4:
                edit_pagination_filter(pagination_filter)
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_entity_filters(filters):
    edit_functions = {
        AlbumFilter: edit_albums_filter,
        ArtistFilter: edit_artists_filter,
        CompositionFilter: edit_compositions_filter,
        PlaylistFilter: edit_playlists_filter,
        UserFilter: edit_users_filter,
        HistoryFilter: edit_history_filter,
        RatingFilter: edit_rating_filter
    }
    edit_functions[type(filters)](filters)


def edit_pagination_filter(pagination_filter):
    while True:
        print(pagination_filter)
        print('What to edit')
        view_numerated_array(['go back', 'page', 'page_size'])

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                pagination_filter.page = get_int('page')
            elif res == 2:
                pagination_filter.page_size = get_int('page_size')
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# region playlists filter


def edit_playlists_filter(playlists_filter: PlaylistFilter):
    filters = ['go back', 'playlists_ids', 'attributes', 'rating', 'compositions', 'users']
    while True:
        print(playlists_filter)
        print('What to edit')
        print('0 -')
        view_numerated_array(filters)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                playlists_filter.artists_ids = edit_set(playlists_filter.playlists_ids, int, 'playlist_id')
            elif res == 2:
                edit_playlists_filter_attributes(playlists_filter.attributes)
            elif res == 3:
                edit_entity_filter_rating(playlists_filter.rating)
            elif res == 4:
                edit_collections_filter_compositions(playlists_filter.compositions)
            elif res == 5:
                edit_collections_filter_users(playlists_filter.users)
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_playlists_filter_attributes(attributes: PlaylistFilter.PlaylistFilterAttributes):
    attrs = ['go back', 'title', 'creators_ids_exclude_nulls', 'creators_ids', 'privacies']
    while True:
        print(attributes)
        print('What to edit')
        print('0 - ')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                attributes.title = get_str('title')
            elif res == 2:
                if attributes.creators_ids_exclude_nulls is None:
                    attributes.creators_ids_exclude_nulls = True
                else:
                    attributes.creators_ids_exclude_nulls = not attributes.creators_ids_exclude_nulls
                print('Changed')
            elif res == 3:
                attributes.types = edit_set(attributes.creators_ids, int, 'creator_id')
            elif res == 4:
                attributes.types = edit_set(attributes.privacies, str, 'privacy')
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# endregion

# region history filter


def edit_history_filter(history_filter: HistoryFilter):
    attrs = ['go back', 'compositions_ids', 'users_ids', 'listened_from', 'listened_to',
             'user_listened_counter', 'composition_listened_counter']
    while True:
        print(history_filter)
        print('What to edit')
        print('0 - ')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                history_filter.compositions_ids = edit_set(history_filter.compositions_ids, int, 'compositions_id')
            elif res == 2:
                history_filter.users_ids = edit_set(history_filter.users_ids, int, 'users_id')
            elif res == 3:
                history_filter.listened_from = get_date('listened_from')
            elif res == 4:
                history_filter.listened_to = get_date('listened_to')
            elif res == 5:
                if history_filter.user_listened_counter is None:
                    history_filter.user_listened_counter = True
                else:
                    history_filter.user_listened_counter = not history_filter.user_listened_counter
            elif res == 6:
                if history_filter.composition_listened_counter is None:
                    history_filter.composition_listened_counter = True
                else:
                    history_filter.composition_listened_counter = not history_filter.composition_listened_counter
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# endregion

# region rating filter


def edit_rating_filter(rating_filter: RatingFilter):
    attrs = ['go back', 'rated_type', 'rated_ids', 'users_ids', 'satisfied', 'rated_from', 'rated_to',
             'rated_rating_counter', 'user_rating_counter']
    while True:
        print(rating_filter)
        print('What to edit')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                types = ['compositions', 'albums', 'playlists']
                view_numerated_array(types, 1)
                new_type = get_int('rated_type')
                if new_type is None:
                    raise ValueError("Variable 'rated_type' can not be None")
                if not 1 <= new_type <= 3:
                    raise ValueError("Variable 'rated_type' invalid value")
                rating_filter.rated_type = new_type
            elif res == 2:
                rating_filter.rated_ids = edit_set(rating_filter.rated_ids, int, 'rated_id')
            elif res == 3:
                rating_filter.users_ids = edit_set(rating_filter.users_ids, int, 'users_id')
            elif res == 4:
                rating_filter.satisfied = get_bool('Is satisfied?')
            elif res == 5:
                rating_filter.rated_from = get_date('rated_from')
            elif res == 6:
                rating_filter.rated_to = get_date('rated_to')
            elif res == 7:
                if rating_filter.rated_rating_counter is None:
                    rating_filter.rated_rating_counter = True
                else:
                    rating_filter.rated_rating_counter = not rating_filter.rated_rating_counter
            elif res == 8:
                if rating_filter.user_rating_counter is None:
                    rating_filter.user_rating_counter = True
                else:
                    rating_filter.user_rating_counter = not rating_filter.user_rating_counter
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# endregion

# region users filter


def edit_users_filter(users_filter):
    filters = ['go back', 'users_ids', 'attributes', 'history', 'compositions_rating', 'playlists_rating',
               'albums_rating', 'saved_playlists', 'saved_albums']
    while True:
        print(users_filter)
        print('What to edit')
        view_numerated_array(filters)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                users_filter.users_ids = edit_set(users_filter.users_ids, int, 'users_id')
            elif res == 2:
                edit_users_filter_attributes(users_filter.attributes)
            elif res == 3:
                edit_users_filter_history(users_filter.history)
            elif res == 4:
                edit_users_filter_rating(users_filter.compositions_rating)
            elif res == 5:
                edit_users_filter_rating(users_filter.playlists_rating)
            elif res == 6:
                edit_users_filter_rating(users_filter.albums_rating)
            elif res == 7:
                edit_users_filter_collections(users_filter.saved_playlists)
            elif res == 8:
                edit_users_filter_collections(users_filter.saved_albums)
            else:
                raise ValueError('Invalid command')
        except Exception as err:
            print(err)


def edit_users_filter_collections(saved_collections):
    saved = ['go back', 'toggle', 'saved_number_from', 'saved_number_to', 'saved_ids_list', 'saved_ids_any']
    while True:
        print(saved_collections)
        print('What to edit')
        view_numerated_array(saved)

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
            elif res == 2:
                saved_collections.saved_number_from = get_int('saved_number_from')
            elif res == 3:
                saved_collections.saved_number_to = get_int('saved_number_to')
            elif res == 4:
                saved_collections.saved_ids_list = edit_set(saved_collections.saved_ids_list, int, 'saved_id')
            elif res == 5:
                if saved_collections.saved_ids_any is None:
                    saved_collections.saved_ids_any = True
                else:
                    saved_collections.saved_ids_any = not saved_collections.saved_ids_any
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_users_filter_rating(rating):
    rate = ['go back', 'toggle', 'rating_date_from', 'rating_date_to', 'times_rated_from', 'times_rated_to',
            'average_rating_from', 'average_rating_to', 'rated_ids', 'rated_ids_any']
    while True:
        print(rating)
        print('What to edit')
        view_numerated_array(rate)

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
            elif res == 2:
                rating.rating_date_from = get_date('rating_date_from')
            elif res == 3:
                rating.rating_date_to = get_date('rating_date_to')
            elif res == 4:
                rating.times_rated_from = get_int('times_rated_from')
            elif res == 5:
                rating.times_rated_to = get_int('times_rated_to')
            elif res == 6:
                rating.average_rating_from = get_float('average_rating_from')
            elif res == 7:
                rating.average_rating_to = get_float('average_rating_to')
            elif res == 8:
                rating.rated_ids = edit_set(rating.rated_ids, int, 'rated_id')
            elif res == 9:
                if rating.rated_ids_any is None:
                    rating.rated_ids_any = True
                else:
                    rating.rated_ids_any = not rating.rated_ids_any
            else:
                raise Exception('Invalid input')
        except Exception as err:
            print(err)


def edit_users_filter_history(history):
    hist = ['go back', 'toggle', 'listened_date_from', 'listened_date_to', 'times_listened_from', 'times_listened_to',
            'compositions_ids', 'compositions_ids_any']
    while True:
        print(history)
        print('What to edit')
        view_numerated_array(hist)

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
            elif res == 2:
                history.listened_date_from = get_date('listened_date_from')
            elif res == 3:
                history.listened_date_to = get_date('listened_date_to')
            elif res == 4:
                history.times_listened_from = get_int('times_listened_from')
            elif res == 5:
                history.times_listened_to = get_int('times_listened_to')
            elif res == 6:
                history.compositions_ids = edit_set(history.compositions_ids, int, 'compositions_id')
            elif res == 7:
                if history.compositions_ids_any is None:
                    history.compositions_ids_any = True
                else:
                    history.compositions_ids_any = not history.compositions_ids_any
            else:
                raise ValueError('Invalid action input')
        except Exception as err:
            print(err)


def edit_users_filter_attributes(attributes):
    attrs = ['go back', 'username', 'full_name', 'registration_from', 'registration_to', 'birth_from', 'birth_to',
             'genders', 'is_active', 'full_name_exclude_nulls', 'birth_exclude_nulls', 'gender_exclude_nulls']
    while True:
        print(attributes)
        print('What to edit')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                attributes.username = get_str('username')
            elif res == 2:
                attributes.full_name = get_str('full_name')
            elif res == 3:
                attributes.registration_from = get_date('registration_from')
            elif res == 4:
                attributes.registration_to = get_date('registration_to')
            elif res == 5:
                attributes.birth_from = get_date('birth_from')
            elif res == 6:
                attributes.birth_to = get_date('birth_to')
            elif res == 7:
                attributes.genders = edit_set(attributes.genders, str, 'gender')
            elif res == 8:
                attributes.is_active = get_bool('Is active?')
            elif res == 9:
                if attributes.full_name_exclude_nulls is None:
                    attributes.full_name_exclude_nulls = True
                else:
                    attributes.full_name_exclude_nulls = not attributes.full_name_exclude_nulls
            elif res == 10:
                if attributes.birth_exclude_nulls is None:
                    attributes.birth_exclude_nulls = True
                else:
                    attributes.birth_exclude_nulls = not attributes.birth_exclude_nulls
            elif res == 11:
                if attributes.gender_exclude_nulls is None:
                    attributes.gender_exclude_nulls = True
                else:
                    attributes.gender_exclude_nulls = not attributes.gender_exclude_nulls
            else:
                raise ValueError('Invalid action input')
        except Exception as err:
            print(err)


# endregion

# region compositions filter


def edit_compositions_filter(compositions_filter):
    filters = ['go back', 'compositions_ids', 'attributes', 'history', 'rating', 'playlists', 'albums']
    while True:
        print(compositions_filter)
        print('What to edit')
        view_numerated_array(filters)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                compositions_filter.compositions_ids = edit_set(
                    compositions_filter.compositions_ids, int, 'composition_id'
                )
            elif res == 2:
                edit_compositions_filter_attributes(compositions_filter.attributes)
            elif res == 3:
                edit_compositions_filter_history(compositions_filter.history)
            elif res == 4:
                edit_entity_filter_rating(compositions_filter.rating)
            elif res == 5:
                edit_compositions_filter_collections(compositions_filter.playlists)
            elif res == 6:
                edit_compositions_filter_collections(compositions_filter.albums)
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_compositions_filter_collections(collections):
    saved = ['go back', 'toggle', 'number_belongs_from', 'number_belongs_to', 'collections_ids', 'collections_any']
    while True:
        print(collections)
        print('What to edit')
        view_numerated_array(saved)

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
            elif res == 2:
                collections.number_belongs_from = get_int('number_belongs_from')
            elif res == 3:
                collections.number_belongs_to = get_int('number_belongs_to')
            elif res == 4:
                collections.collections_list = edit_set(collections.collections_list, int, 'collection_id')
            elif res == 5:
                if collections.collections_any is None:
                    collections.collections_any = True
                else:
                    collections.collections_any = not collections.collections_any
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_entity_filter_rating(rating):
    rate = ['go back', 'toggle', 'rating_date_from', 'rating_date_to', 'times_rated_from', 'times_rated_to',
            'average_rating_from', 'average_rating_to', 'users_ids', 'users_ids_any']
    while True:
        print(rating)
        print('What to edit')
        view_numerated_array(rate)

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
            elif res == 2:
                rating.rating_date_from = get_date('rating_date_from')
            elif res == 3:
                rating.rating_date_to = get_date('rating_date_to')
            elif res == 4:
                rating.times_rated_from = get_int('times_rated_from')
            elif res == 5:
                rating.times_rated_to = get_int('times_rated_to')
            elif res == 6:
                rating.average_rating_from = get_float('average_rating_from')
            elif res == 7:
                rating.average_rating_to = get_float('average_rating_to')
            elif res == 8:
                rating.users_ids = edit_set(rating.users_ids, int, 'users_id')
            elif res == 9:
                if rating.users_ids_any is None:
                    rating.users_ids_any = True
                else:
                    rating.users_ids_any = not rating.users_ids_any
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_compositions_filter_history(history):
    hist = ['go back', 'toggle', 'listened_date_from', 'listened_date_to', 'times_listened_from', 'times_listened_to',
            'users_ids', 'users_ids_any']
    while True:
        print(history)
        print('What to edit')
        view_numerated_array(hist)

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
            elif res == 2:
                history.listened_date_from = get_date('listened_date_from')
            elif res == 3:
                history.listened_date_to = get_date('listened_date_to')
            elif res == 4:
                history.times_listened_from = get_int('times_listened_from')
            elif res == 5:
                history.times_listened_to = get_int('times_listened_to')
            elif res == 6:
                history.users_ids = edit_set(history.users_ids, int, 'users_id')
            elif res == 7:
                if history.users_ids_any is None:
                    history.users_ids_any = True
                else:
                    history.users_ids_any = not history.users_ids_any
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_compositions_filter_attributes(attributes):
    attrs = ['go back', 'title_lyrics', 'artists_ids_exclude_nulls', 'artists_ids', 'duration_from', 'duration_to',
             'release_date_exclude_nulls', 'release_from', 'release_to', 'search_lyrics']
    while True:
        print(attributes)
        print('What to edit')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                attributes.title_lyrics = get_str('title_lyrics')
            elif res == 2:
                if attributes.artists_ids_exclude_nulls is None:
                    attributes.artists_ids_exclude_nulls = True
                else:
                    attributes.artists_ids_exclude_nulls = not attributes.artists_ids_exclude_nulls
            elif res == 3:
                attributes.artists_ids = edit_set(attributes.artists_ids, int, 'artists_id')
            elif res == 4:
                attributes.duration_from = get_int('duration_from')
            elif res == 5:
                attributes.duration_to = get_int('duration_to')
            elif res == 6:
                if attributes.release_date_exclude_nulls is None:
                    attributes.release_date_exclude_nulls = True
                else:
                    attributes.release_date_exclude_nulls = not attributes.release_date_exclude_nulls
            elif res == 7:
                attributes.release_from = get_date('release_from')
            elif res == 8:
                attributes.release_to = get_date('release_to')
            elif res == 9:
                if attributes.search_lyrics is None:
                    attributes.search_lyrics = True
                else:
                    attributes.search_lyrics = not attributes.search_lyrics
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# endregion

# region albums filter


def edit_albums_filter(albums_filter: AlbumFilter):
    filters = ['go back', 'albums_ids', 'attributes', 'rating', 'compositions', 'users']
    while True:
        print(albums_filter)
        print('What to edit')
        view_numerated_array(filters)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                albums_filter.artists_ids = edit_set(albums_filter.albums_ids, int, 'album_id')
            elif res == 2:
                edit_albums_filter_attributes(albums_filter.attributes)
            elif res == 3:
                edit_entity_filter_rating(albums_filter.rating)
            elif res == 4:
                edit_collections_filter_compositions(albums_filter.compositions)
            elif res == 5:
                edit_collections_filter_users(albums_filter.users)
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_albums_filter_attributes(attributes: AlbumFilter.AlbumFilterAttributes):
    attrs = ['go back', 'title', 'release_date_exclude_nulls', 'release_date_from', 'release_date_to']
    while True:
        print(attributes)
        print('What to edit')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                attributes.title = get_str('title')
            elif res == 2:
                if attributes.release_date_exclude_nulls is None:
                    attributes.release_date_exclude_nulls = True
                else:
                    attributes.release_date_exclude_nulls = not attributes.release_date_exclude_nulls
            elif res == 3:
                attributes.release_date_from = get_date('release_date_from')
            elif res == 4:
                attributes.release_date_to = get_date('release_date_to')
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_collections_filter_users(users: CollectionFilterUsers):
    saved = ['go back', 'toggle', 'users_number_from', 'users_number_to',
             'users_list', 'users_any']
    while True:
        print(users)
        print('What to edit')
        view_numerated_array(saved)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                if users.toggle is None:
                    users.toggle = True
                else:
                    users.toggle = not users.toggle
            elif res == 2:
                users.users_number_from = get_int('users_number_from')
            elif res == 3:
                users.users_number_to = get_int('users_number_to')
            elif res == 4:
                users.users_list = edit_set(users.users_list, int, 'user_id')
            elif res == 5:
                if users.users_any is None:
                    users.users_any = True
                else:
                    users.users_any = not users.users_any
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_collections_filter_compositions(compositions: CollectionFilterCompositions):
    saved = ['go back', 'toggle', 'compositions_number_from', 'compositions_number_to',
             'compositions_list', 'compositions_any']
    while True:
        print(compositions)
        print('What to edit')
        view_numerated_array(saved)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                if compositions.toggle is None:
                    compositions.toggle = True
                else:
                    compositions.toggle = not compositions.toggle
                print('Changed')
            elif res == 2:
                compositions.compositions_number_from = get_int('compositions_number_from')
            elif res == 3:
                compositions.compositions_number_to = get_int('compositions_number_to')
            elif res == 4:
                compositions.compositions_list = edit_set(compositions.compositions_list, int, 'composition_id')
            elif res == 5:
                if compositions.compositions_any is None:
                    compositions.compositions_any = True
                else:
                    compositions.compositions_any = not compositions.compositions_any
                print('Changed')
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# endregion

# region artists filter


def edit_artists_filter(artists_filter):
    filters = ['go back', 'artists_ids', 'attributes', 'history', 'rating', 'playlists', 'albums']
    while True:
        print(artists_filter)
        print('What to edit')
        view_numerated_array(filters)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                artists_filter.artists_ids = edit_set(artists_filter.artists_ids, int, 'artists_id')
            elif res == 2:
                edit_artists_filter_attributes(artists_filter.attributes)
            elif res == 3:
                edit_compositions_filter_history(artists_filter.history)
            elif res == 4:
                edit_entity_filter_rating(artists_filter.rating)
            elif res == 5:
                edit_compositions_filter_collections(artists_filter.playlists)
            elif res == 6:
                edit_compositions_filter_collections(artists_filter.albums)
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


def edit_artists_filter_attributes(attributes):
    attrs = ['go back', 'name_comment', 'types', 'gender_exclude_nulls', 'genders', 'begin_date_exclude_nulls',
             'begin_date_from', 'begin_date_to', 'end_date_exclude_nulls', 'end_date_from', 'end_date_to',
             'search_comments']
    while True:
        print(attributes)
        print('What to edit')
        view_numerated_array(attrs)

        try:
            res = get_int()
            if res is None:
                raise ValueError('You need to enter action')
            elif res == 0:
                break
            elif res == 1:
                attributes.name_comment = get_str('attributes')
            elif res == 2:
                attributes.types = edit_set(attributes.types, str, 'type')
            elif res == 3:
                if attributes.gender_exclude_nulls is None:
                    attributes.gender_exclude_nulls = True
                else:
                    attributes.gender_exclude_nulls = not attributes.gender_exclude_nulls
            elif res == 4:
                attributes.genders = edit_set(attributes.genders, str, 'gender')
            elif res == 5:
                if attributes.begin_date_exclude_nulls is None:
                    attributes.begin_date_exclude_nulls = True
                else:
                    attributes.begin_date_exclude_nulls = not attributes.begin_date_exclude_nulls
            elif res == 6:
                attributes.begin_date_from = get_date('begin_date_from')
            elif res == 7:
                attributes.begin_date_to = get_date('begin_date_to')
            elif res == 8:
                if attributes.end_date_exclude_nulls is None:
                    attributes.end_date_exclude_nulls = True
                else:
                    attributes.end_date_exclude_nulls = not attributes.end_date_exclude_nulls
            elif res == 9:
                attributes.end_date_from = get_date('end_date_from')
            elif res == 10:
                attributes.end_date_to = get_date('end_date_to')
            elif res == 11:
                if attributes.search_comments is None:
                    attributes.search_comments = True
                else:
                    attributes.search_comments = not attributes.search_comments
            else:
                raise ValueError('Invalid input')
        except Exception as err:
            print(err)


# endregion

# region entity construction


def construct_album():
    title = get_str('title')
    if not title:
        raise ValueError("Variable 'title' can not be None")

    date_tuple = get_partial_date('release_year')
    return Album(0, title, date_tuple[0], date_tuple[1], date_tuple[2])


def construct_artist():
    name = get_str('name')
    if name is None:
        raise ValueError("Variable 'name' can not be None")

    types = ['person', 'group', 'orchestra', 'choir', 'character', 'other']
    view_numerated_array(types, 1)
    type_id = get_int('type_id')
    if type_id is None or not 1 <= type_id <= 6:
        raise ValueError("Variable 'type_id' invalid input")

    genders = ['male', 'female', 'other']
    view_numerated_array(genders, 1)
    gender_id = get_int('gender_id')
    if gender_id is not None and not 1 <= gender_id <= 3:
        raise ValueError("Variable 'gender_id' invalid input")

    begin_date = get_partial_date('begin_date')

    end_date = get_partial_date('end_date')

    comment = get_str('comment')

    return Artist(0, name, type_id, gender_id, comment, begin_date[0], begin_date[1], begin_date[2],
                  end_date[0], end_date[1], end_date[2])


def construct_composition():
    title = get_str('title')
    if title is None:
        raise ValueError("Variable 'title' can not be None")

    duration = get_int('duration')
    if duration is None:
        raise ValueError("Variable 'duration' can not be None")

    path_to_file = get_str('path_to_file')
    if path_to_file is None:
        raise ValueError("Variable 'path_to_file' can not be None")

    lyrics = get_str('lyrics')

    date_tuple = get_partial_date('release_year')

    return Composition(0, title, duration, path_to_file, 0, date_tuple[0], date_tuple[1], date_tuple[2], lyrics)


def construct_playlist():
    title = get_str('title')
    if title is None:
        raise ValueError("Variable 'title' can not be None")

    creator_id = get_int('creator_id')

    privacy_types = ['public', 'unlisted', 'private']
    view_numerated_array(privacy_types, 1)
    privacy_id = get_int('privacy_id')
    if privacy_id is None or not 1 <= privacy_id <= 3:
        raise ValueError("Variable 'privacy_id' invalid input")

    return Playlist(0, title, privacy_id, creator_id)


def construct_user():
    username = get_str('username')
    if username is None:
        raise ValueError("Variable 'username' can not be None")

    password_hash = get_str('password_hash')
    if password_hash is None:
        raise ValueError("Variable 'password_hash' can not be None")

    registration_date = get_date('registration_date')
    if registration_date is None:
        raise ValueError("Variable 'registration_date' can not be None")

    is_active = get_bool('is_active')
    if is_active is None:
        raise ValueError("Variable 'registration_date' can not be None")

    full_name = get_str('full_name')

    birth_date = get_date('birth_date')

    genders = ['male', 'female', 'other']
    view_numerated_array(genders, 1)
    gender_id = get_int('gender_id')
    if not 1 <= gender_id <= 3:
        raise ValueError("Variable 'gender_id' invalid input")

    return User(0, username, password_hash, registration_date, is_active, full_name, birth_date, gender_id)


def construct_history_record():
    user_id = get_int('user_id')
    if user_id is None:
        raise ValueError("Variable 'user_id' can not be None")

    composition_id = get_int('composition_id')
    if composition_id is None:
        raise ValueError("Variable 'composition_id' can not be None")

    action_date = get_date('date')
    if action_date is None:
        raise ValueError("Variable 'listening_date' can not be None")

    return HistoryRecord(0, composition_id, user_id, action_date)


def construct_rating_record():
    user_id = get_int('user_id')
    if user_id is None:
        raise ValueError("Variable 'user_id' can not be None")

    rated_id = get_int('rated_id')
    if rated_id is None:
        raise ValueError("Variable 'rated_id' can not be None")

    action_date = get_date('date')
    if action_date is None:
        raise ValueError("Variable 'rating_date' can not be None")

    is_satisfied = get_bool('Satisfied?')
    if is_satisfied is None:
        raise ValueError("Variable 'is_satisfied' can not be None")

    return Rating(0, rated_id, user_id, is_satisfied, action_date)


# endregion

# region helper functions


def get_int(target=None):
    if target:
        print('Enter', target)
    v = input()
    if v:
        return int(v)
    else:
        return None


def get_float(target=None):
    if target:
        print('Enter', target)
    v = input()
    if v:
        return float(v)
    else:
        return None


def get_bool(message=None):
    if message:
        print(message)
    v = input()
    if v:
        return bool(strtobool(v))
    else:
        return None


def get_str(target=None):
    if target:
        print('Enter', target)
    v = input()
    if v:
        return v
    else:
        return None


def get_date(target=None):
    """
    Getting date string from YYYY-MM-DD format
    """
    if target:
        print('Enter', target, '(ISO-8601)')
    v = input()
    if v:
        datetime.datetime.strptime(v, '%Y-%m-%d')
        return v
    else:
        return None


def get_partial_date(target=None):
    """
    Parsing date from YYYY-MM-DD format\n
    For None field input 0\n
    :return: tuple(year, month, day)
    """
    if target:
        print('Enter ', target, ', for None field input 0 (ISO-8601)', sep='')
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


def edit_set(edited: set, element_type: type, target=None):
    """
    To add type: add a1 a2 a3 ...\n
    To remove type: rem a1 a2 a3 ...\n
    :return: set
    """
    if target:
        print("To add '", target, "' type: add a1 a2 a3 ...", sep='')
        print("To remove '", target, "' type: rem a1 a2 a3 ...", sep='')
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


def get_unique_list(maximum: int, target=None):
    """
    Input format: a1 a2 a3 ...\n
    :return: list
    """
    if target:
        print('Enter', target, 'in format: a1 a2 a3 ...')
    orders = get_str()
    if orders is None:
        return None
    orders_arr = orders.split()
    new_arr = []
    for item in orders_arr:
        temp = int(item)
        if abs(temp) > maximum or temp == 0:
            raise ValueError("Can not be 0 or abs bigger than " + str(maximum))
        if abs(temp) in new_arr:
            raise ValueError("List values must be unique")
        new_arr.append(temp)
    return new_arr


# endregion

# region views


def view_numerated_array(array: list, start_from=0):
    for item in array:
        print(start_from, '-', item)
        start_from += 1


# endregion


def visualize_entities_rating(data, filename):
    x = list(range(1, len(data) + 1))
    rating = []
    label = []
    count = []

    for item in data:
        label.append(item['name'])
        rating.append(item['avg_rating'])
        count.append(item['times_rated'])

    fig, ax = plt.subplots()

    bar_plot = plt.bar(x, rating)
    plt.xticks(x, label, rotation='vertical')

    for idx, rect in enumerate(bar_plot):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 0.5 * height,
                count[idx],
                ha='center', va='bottom', rotation=90)

    plt.ylim(0, 10)
    plt.title('Most rated')
    plt.savefig('./matplotlib_files/' + filename + '.png', bbox_inches='tight')


def visualize_entities_listening(data, filename):
    x = list(range(1, len(data) + 1))
    listened = []
    label = []

    for item in data:
        label.append(item['name'])
        listened.append(item['times_listened'])

    fig, ax = plt.subplots()

    bar_plot = plt.bar(x, listened)
    plt.xticks(x, label, rotation='vertical')

    plt.title('Most listened')
    plt.savefig('./matplotlib_files/' + filename + '.png', bbox_inches='tight')


def visualize_listening_history(data, filename):
    x_arr = []
    y_arr = []

    s = len(data)
    dt = max(1, int(s / 99))
    for i in range(0, min(s, 100)):
        x_arr.append(data[i * dt]['listening_date'])
        y_arr.append(data[i * dt]['times_listened'])

    fig = plt.figure()
    plt.plot(x_arr, y_arr)
    plt.xticks(rotation='vertical')
    plt.title('Listening chart')
    plt.savefig('./matplotlib_files/' + filename + '.png', bbox_inches='tight')


def visualize_rating_history(data, filename):
    x_arr = []
    y_arr = []

    s = len(data)
    dt = max(1, int(s / 99))
    for i in range(0, min(s, 100)):
        x_arr.append(data[i * dt]['rating_date'])
        y_arr.append(data[i * dt]['avg_rating'])

    fig = plt.figure()
    plt.plot(x_arr, y_arr)
    plt.xticks(rotation='vertical')
    plt.title('Rating chart')
    plt.savefig('./matplotlib_files/' + filename + '.png', bbox_inches='tight')


class ConsoleView:

    def __init__(self, connection):
        self.controller = ControllerPSQL(connection)

    def graph_menu(self, albums_filter, artists_filter, compositions_filter, playlists_filter,
                   history_filter, rating_filter, pagination):
        actions_list = ['go back', 'get_albums_rating_analysis_data', 'get_artists_rating_analysis_data',
                        'get_compositions_rating_analysis_data', 'get_playlists_rating_analysis_data',
                        'get_artists_listening_analysis_data', 'get_compositions_listening_analysis_data',
                        'get_composition_listening_analysis_data', 'get_rating_analysis_data']

        pagination_addition = '_page-' + to_str(pagination.page) + '_page_size-' + to_str(pagination.page_size)
        rated_types = {1: 'composition', 2: 'album', 3: 'playlist'}
        rated_type = rated_types[rating_filter.rated_type]

        actions = {
            1: lambda: visualize_entities_rating(self.controller.get_albums_rating_analysis_data(albums_filter, pagination), 'top_rated_albums'+pagination_addition),
            2: lambda: visualize_entities_rating(self.controller.get_artists_rating_analysis_data(artists_filter, pagination), 'top_rated_artists'+pagination_addition),
            3: lambda: visualize_entities_rating(self.controller.get_compositions_rating_analysis_data(compositions_filter, pagination), 'top_rated_compositions'+pagination_addition),
            4: lambda: visualize_entities_rating(self.controller.get_playlists_rating_analysis_data(playlists_filter, pagination), 'top_rated_playlists'+pagination_addition),
            5: lambda: visualize_entities_listening(self.controller.get_artists_listening_analysis_data(artists_filter, pagination), 'top_listened_artists'+pagination_addition),
            6: lambda: visualize_entities_listening(self.controller.get_compositions_listening_analysis_data(compositions_filter, pagination), 'top_listened_compositios'+pagination_addition),
            7: lambda: visualize_listening_history(self.controller.get_listening_history_analysis_data(history_filter), 'listening_chart_for_'+to_str(history_filter.compositions_ids)),
            8: lambda: visualize_rating_history(self.controller.get_rating_analysis_data(rating_filter), 'rating_chart_for_'+rated_type+'_'+to_str(history_filter.compositions_ids)),
        }

        while True:
            print('Choose analysis target')
            view_numerated_array(actions_list)

            try:
                action = get_int()
                if action is None:
                    raise ValueError('You need to enter action')
                elif action == 0:
                    break

                actions[action]()
            except Exception as err:
                print(err)

    def call_interface(self):
        users_filter = UserFilter()
        compositions_filter = CompositionFilter()
        artists_filter = ArtistFilter()
        albums_filter = AlbumFilter()
        playlists_filter = PlaylistFilter()
        history_filter = HistoryFilter()
        rating_filter = RatingFilter()
        pagination = PaginationFilter()

        albums_orders = ['album_id', 'title', 'release_date', 'compositions_number', 'times_rated',
                         'average_rating', 'users_saved_number', 'rating_weight']
        artists_orders = ['artist_id', 'name', 'type', 'gender', 'begin_date', 'times_listened',
                          'times_rated', 'average_rating', 'playlists_belong_number',
                          'albums_belong_number', 'rating_weight']
        compositions_orders = ['composition_id', 'title', 'artist_id', 'duration', 'release_date',
                               'times_listened', 'times_rated', 'average_rating',
                               'playlists_belong_number', 'albums_belong_number', 'rating_weight']
        history_orders = ['record_id', 'user_id', 'composition_id', 'listening_date']
        playlists_orders = ['playlist_id', 'title', 'creator_id', 'privacy_id',
                            'compositions_number', 'times_rated', 'average_rating',
                            'users_saved_number', 'rating_weight']
        rating_orders = ['rating_id', 'rated_id', 'user_id', 'satisfied', 'rating_date']
        users_orders = ['user_id', 'username', 'registration_date', 'is_active', 'full_name',
                        'birth_date', 'gender', 'times_listened', 'times_compositions_rated',
                        'compositions_average_rating', 'times_albums_rated',
                        'albums_average_rating', 'times_playlists_rate',
                        'playlists_average_rating',
                        'albums_saved_number', 'playlists_saved_number']

        # method_list = [func for func in dir(ModelPSQL) if callable(getattr(ModelPSQL, func)) and
        #                not func.startswith('__') and not func.startswith('fill_')]
        method_list = ['exit', 'graph analysis menu',
                       'add_album_composition', 'add_playlist_composition', 'add_user_album', 'add_user_playlist',
                       'create_album', 'create_artist', 'create_composition', 'create_playlist', 'create_user',
                       'delete_album', 'delete_artist', 'delete_composition', 'delete_playlist', 'delete_user',
                       'get_album', 'get_albums', 'get_artists', 'get_compositions', 'get_listening_history',
                       'get_playlist', 'get_playlists', 'get_rating', 'get_users', 'listen_composition', 'rate_album',
                       'rate_composition', 'rate_playlist', 'remove_album_composition', 'remove_playlist_composition',
                       'remove_user_album', 'remove_user_playlist', 'unlisten_composition', 'unrate_album',
                       'unrate_composition', 'unrate_playlist', 'update_album', 'update_artist', 'update_composition',
                       'update_playlist', 'update_user']

        methods = {
            1: lambda: self.controller.add_album_composition(get_int('album_id'), get_int('composition_id')),
            2: lambda: self.controller.add_playlist_composition(get_int('playlist_id'), get_int('composition_id')),
            3: lambda: self.controller.add_user_album(get_int('album_id'), get_int('user_id')),
            4: lambda: self.controller.add_user_playlist(get_int('playlist_id'), get_int('user_id')),
            5: lambda: self.controller.create_album(construct_album()),
            6: lambda: self.controller.create_artist(construct_artist()),
            7: lambda: self.controller.create_composition(construct_composition()),
            8: lambda: self.controller.create_playlist(construct_playlist()),
            9: lambda: self.controller.create_user(construct_user()),
            10: lambda: self.controller.delete_album(get_int('id')),
            11: lambda: self.controller.delete_artist(get_int('id')),
            12: lambda: self.controller.delete_composition(get_int('id')),
            13: lambda: self.controller.delete_playlist(get_int('id')),
            14: lambda: self.controller.delete_user(get_int('id')),
            15: lambda: self.controller.get_album(get_int('id')),
            16: lambda: getters_interface(self.controller.get_albums, albums_filter, pagination, albums_orders),
            17: lambda: getters_interface(self.controller.get_artists, artists_filter, pagination, artists_orders),
            18: lambda: getters_interface(self.controller.get_compositions, compositions_filter, pagination, compositions_orders),
            19: lambda: getters_interface(self.controller.get_history, history_filter, pagination, history_orders),
            20: lambda: self.controller.get_playlist(get_int('id')),
            21: lambda: getters_interface(self.controller.get_playlists, playlists_filter, pagination, playlists_orders),
            22: lambda: getters_interface(self.controller.get_rating, rating_filter, pagination, rating_orders),
            23: lambda: getters_interface(self.controller.get_users, users_filter, pagination, users_orders),
            24: lambda: self.controller.listen_composition(construct_history_record()),
            25: lambda: self.controller.rate_album(construct_rating_record()),
            26: lambda: self.controller.rate_composition(construct_rating_record()),
            27: lambda: self.controller.rate_playlist(construct_rating_record()),
            28: lambda: self.controller.remove_album_composition(get_int('album_id'), get_int('composition_id')),
            29: lambda: self.controller.remove_playlist_composition(get_int('playlist_id'), get_int('composition_id')),
            30: lambda: self.controller.remove_user_album(get_int('album_id'), get_int('user_id')),
            31: lambda: self.controller.remove_playlist_composition(get_int('playlist_id'), get_int('user_id')),
            32: lambda: self.controller.unlisten_composition(get_int('id')),
            33: lambda: self.controller.unrate_album(get_int('album_id'), get_int('user_id')),
            34: lambda: self.controller.unrate_composition(get_int('composition_id'), get_int('user_id')),
            35: lambda: self.controller.unrate_playlist(get_int('playlist_id'), get_int('user_id')),
            36: lambda: self.controller.update_album(construct_album()),
            37: lambda: self.controller.update_artist(construct_artist()),
            38: lambda: self.controller.update_composition(construct_composition()),
            39: lambda: self.controller.update_playlist(construct_playlist()),
            40: lambda: self.controller.update_user(construct_user()),
        }

        while True:
            print('Choose method')
            view_numerated_array(method_list, -1)

            try:
                method_id = get_int()
                if method_id is None:
                    raise ValueError('You need to enter action')
                elif method_id == -1:
                    print('Closing')
                    break
                elif method_id == 0:
                    self.graph_menu(albums_filter, artists_filter, compositions_filter, playlists_filter,
                                    history_filter, rating_filter, pagination)
                print(methods[method_id]())
            except Exception as err:
                print(err)
