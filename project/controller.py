from model import ModelPSQL, PaginationFilter
from models.filters import to_str
from copy import deepcopy


def bool_str(result):
    if result:
        return 'Success'
    else:
        return 'Failure'


def dict_str(dictionary, level=0):
    tabs = '\t' * level
    result = tabs
    length = len(dictionary)
    i = 1
    for key, value in dictionary.items():
        if type(value) is list:
            result += '\n' + list_str(value, key, '', level) + tabs
        else:
            result += to_str(key) + ': ' + to_str(value) + ('' if i == length else ' | ')
        i += 1
    return result


def list_str(container, entity, action='Found', level=0):
    tabs = '\t'*level
    action_formatted = '' if len(action) == 0 else action + ' '
    result = ''
    if container is None and action == 'Found':
        result += tabs + 'Not found\n'
    elif container is None:
        result += tabs + entity + 's is None\n'
    elif type(container) is not list:
        result += tabs + action_formatted + entity + ':\n' + dict_str(container, level+1) + '\n'
    elif len(container) == 1:
        result += tabs + action_formatted + entity + ':\n' + dict_str(container[0], level+1) + '\n'
    else:
        result += tabs + action_formatted + entity + 's:\n'
        for item in container:
            result += tabs + dict_str(item, level + 1) + '\n'

    return result


class ControllerPSQL:

    def __init__(self, connection):
        self.model = ModelPSQL(connection)

    def get_users(self, users_filter, orders_list, pagination_filter):
        return list_str(self.model.get_users(users_filter, orders_list, pagination_filter), 'User')

    def get_compositions(self, compositions_filter, orders_list, pagination_filter):
        return list_str(self.model.get_compositions(compositions_filter, orders_list, pagination_filter), 'Composition')

    def get_artists(self, artists_filter, orders_list, pagination_filter):
        return list_str(self.model.get_artists(artists_filter, orders_list, pagination_filter), 'Artist')

    def get_albums(self, albums_filter, orders_list, pagination_filter):
        return list_str(self.model.get_albums(albums_filter, orders_list, pagination_filter), 'Album')

    def get_playlists(self, playlists_filter, orders_list, pagination_filter):
        return list_str(self.model.get_playlists(playlists_filter, orders_list, pagination_filter), 'Playlist')

    def get_history(self, history_filter, orders_list, pagination_filter):
        return list_str(
            self.model.get_listening_history(history_filter, orders_list, pagination_filter), 'History record'
        )

    def get_rating(self, rating_filter, orders_list, pagination_filter):
        return list_str(self.model.get_rating(rating_filter, orders_list, pagination_filter), 'Rating record')

    # standard user operations

    def create_user(self, user_model):
        return list_str(self.model.create_user(user_model), 'User')

    def update_user(self, user_model):
        return list_str(self.model.update_user(user_model), 'User')

    def delete_user(self, user_id):
        return list_str(self.model.delete_user(user_id), 'User')

    # advanced composition operations

    def add_user_playlist(self, playlist_id, user_id):
        return bool_str(self.model.add_user_playlist(playlist_id, user_id))

    def remove_user_playlist(self, playlist_id, user_id):
        return bool_str(self.model.remove_user_playlist(playlist_id, user_id))

    def add_user_album(self, album_id, user_id):
        return bool_str(self.model.add_user_album(album_id, user_id))

    def remove_user_album(self, album_id, user_id):
        return bool_str(self.model.remove_user_album(album_id, user_id))

    # standard composition operations

    def create_composition(self, composition_model):
        return list_str(self.model.create_composition(composition_model), 'Composition')

    def update_composition(self, composition_model):
        return list_str(self.model.update_composition(composition_model), 'Composition')

    def delete_composition(self, composition_id):
        return list_str(self.model.delete_composition(composition_id), 'Composition')

    # advanced composition operations

    def listen_composition(self, history_record):
        return list_str(self.model.listen_composition(history_record), 'History record')

    def unlisten_composition(self, history_record):
        return list_str(self.model.unlisten_composition(history_record), 'History record')

    def rate_composition(self, rating_model):
        return list_str(self.model.rate_composition(rating_model), 'Rating record')

    def unrate_composition(self, composition_id, user_id):
        return list_str(self.model.unrate_composition(composition_id, user_id), 'Rating record')

    # standard artist operations

    def create_artist(self, artist_model):
        return list_str(self.model.create_artist(artist_model), 'Artist')

    def update_artist(self, artist_model):
        return list_str(self.model.update_artist(artist_model), 'Artist')

    def delete_artist(self, artist_id):
        return list_str(self.model.delete_artist(artist_id), 'Artist')

    # advanced artist operations

    # None?

    # standard playlist operations

    def create_playlist(self, playlist_model):
        return list_str(self.model.create_playlist(playlist_model), 'Playlist')

    def update_playlist(self, playlist_model):
        return list_str(self.model.update_playlist(playlist_model), 'Playlist')

    def delete_playlist(self, playlist_id):
        return list_str(self.model.delete_playlist(playlist_id), 'Playlist')

    def get_playlist(self, playlist_id):
        return list_str(self.model.get_playlist(playlist_id), 'Playlist')

    # advanced playlist operations

    def add_playlist_composition(self, playlist_id, composition_id):
        return bool_str(self.model.add_playlist_composition(playlist_id, composition_id))

    def remove_playlist_composition(self, playlist_id, composition_id):
        return bool_str(self.model.remove_playlist_composition(playlist_id, composition_id))

    def rate_playlist(self, rating_model):
        return list_str(self.model.rate_playlist(rating_model), 'Rating record')

    def unrate_playlist(self, playlist_id, user_id):
        return list_str(self.model.unrate_playlist(playlist_id, user_id), 'Rating record')

    # standard album operations

    def create_album(self, album_model):
        return list_str(self.model.create_album(album_model), 'Album')

    def update_album(self, album_model):
        return list_str(self.model.update_album(album_model), 'Album')

    def delete_album(self, album_id):
        return list_str(self.model.delete_album(album_id), 'Album')

    def get_album(self, album_id):
        return list_str(self.model.get_album(album_id), 'Album')

    # advanced album operations

    def add_album_composition(self, album_id, composition_id):
        return bool_str(self.model.add_album_composition(album_id, composition_id))

    def remove_album_composition(self, album_id, composition_id):
        return bool_str(self.model.remove_album_composition(album_id, composition_id))

    def rate_album(self, rating_model):
        return list_str(self.model.rate_album(rating_model), 'Rating record')

    def unrate_album(self, album_id, user_id):
        return list_str(self.model.unrate_album(album_id, user_id), 'Rating record')

    # fillers

    def fill_artists(self, start_number, end_number):
        self.fill_artists(start_number, end_number)

    def fill_compositions(self, start_number, end_number):
        self.fill_compositions(start_number, end_number)

    def fill_users(self, start_number, end_number):
        self.fill_users(start_number, end_number)

    def fill_history(self, start_number, end_number):
        self.fill_history(start_number, end_number)

    def fill_compositions_rating(self, start_number, end_number):
        self.fill_compositions_rating(start_number, end_number)

    def fill_playlists(self, start_number, end_number):
        self.fill_playlists(start_number, end_number)

    def fill_playlists_compositions(self, start_number, end_number):
        self.fill_playlists_compositions(start_number, end_number)

    # for analysis

    def get_albums_rating_analysis_data(self, albums_filter, pagination_filter):
        filter_copy = deepcopy(albums_filter)
        filter_copy.users.toggle = False
        filter_copy.compositions.toggle = False
        filter_copy.rating.toggle = True
        objects = self.model.get_albums(filter_copy, -8, pagination_filter)
        data = []
        for item in objects:
            data.append({
                'name': item['title'],
                'times_rated': item['times_rated'],
                'avg_rating': item['average_rating']
            })
        return data

    def get_artists_rating_analysis_data(self, artists_filter, pagination_filter):
        filter_copy = deepcopy(artists_filter)
        filter_copy.rating.toggle = True
        filter_copy.history.toggle = False
        filter_copy.albums.toggle = False
        filter_copy.playlists.toggle = False
        objects = self.model.get_artists(filter_copy, -12, pagination_filter)
        data = []
        for item in objects:
            data.append({
                'name': item['name'],
                'times_rated': item['times_rated'],
                'avg_rating': item['average_rating']
            })
        return data

    def get_compositions_rating_analysis_data(self, compositions_filter, pagination_filter):
        filter_copy = deepcopy(compositions_filter)
        filter_copy.rating.toggle = True
        filter_copy.history.toggle = False
        filter_copy.albums.toggle = False
        filter_copy.playlists.toggle = False
        objects = self.model.get_compositions(filter_copy, -11, pagination_filter)
        data = []
        for item in objects:
            data.append({
                'name': item['title'],
                'times_rated': item['times_rated'],
                'avg_rating': item['average_rating']
            })
        return data

    def get_playlists_rating_analysis_data(self, playlists_filter, pagination_filter):
        filter_copy = deepcopy(playlists_filter)
        filter_copy.rating.toggle = True
        filter_copy.users.toggle = False
        filter_copy.compositions.toggle = False
        objects = self.model.get_playlists(filter_copy, -9, pagination_filter)
        data = []
        for item in objects:
            data.append({
                'name': item['title'],
                'times_rated': item['times_rated'],
                'avg_rating': item['average_rating']
            })
        return data

    def get_artists_listening_analysis_data(self, artists_filter, pagination_filter):
        filter_copy = deepcopy(artists_filter)
        filter_copy.rating.toggle = False
        filter_copy.history.toggle = True
        filter_copy.albums.toggle = False
        filter_copy.playlists.toggle = False
        objects = self.model.get_artists(filter_copy, -7, pagination_filter)
        data = []
        for item in objects:
            data.append({
                'name': item['name'],
                'times_listened': item['times_listened']
            })
        return data

    def get_compositions_listening_analysis_data(self, compositions_filter, pagination_filter):
        filter_copy = deepcopy(compositions_filter)
        filter_copy.rating.toggle = False
        filter_copy.history.toggle = True
        filter_copy.albums.toggle = False
        filter_copy.playlists.toggle = False
        objects = self.model.get_compositions(filter_copy, -6, pagination_filter)
        data = []
        for item in objects:
            data.append({
                'name': item['title'],
                'times_listened': item['times_listened']
            })
        return data

    def get_listening_history_analysis_data(self, history_filter):
        if history_filter.compositions_ids is None or len(history_filter.compositions_ids) != 1:
            raise ValueError('Can analyse only one composition in this mode')
        filter_copy = deepcopy(history_filter)
        filter_copy.composition_listened_counter = True
        filter_copy.user_rating_counter = False
        objects = self.model.get_listening_history(filter_copy, 4, PaginationFilter())
        data = []
        for item in objects:
            data.append({
                'listening_date': item['listening_date'],
                'times_listened': item['times_composition_listened']
            })
        return data

    def get_rating_analysis_data(self, rating_filter):
        if rating_filter.rated_ids is None or len(rating_filter.rated_ids) != 1:
            raise ValueError('Can analyse only one entity in this mode')
        filter_copy = deepcopy(rating_filter)
        filter_copy.rated_rating_counter = True
        filter_copy.user_rating_counter = False
        objects = self.model.get_rating(filter_copy, 5, PaginationFilter())
        data = []
        for item in objects:
            data.append({
                'rating_date': item['rating_date'],
                'avg_rating': item['avg_rated_rating']
            })
        return data
