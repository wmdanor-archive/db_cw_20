from model import ModelPSQL
from models.filters import to_str


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
            result += key + ': ' + value + ' | ' if i != length else ''
        i += 1
    return result


def list_str(container, entity, action='Found', level=0):
    tabs = '\t'*level
    action_formatted = '' if len(action) == 0 else action + ' '
    result = ""
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
        self.__model = ModelPSQL(connection)

    def get_users(self, users_filter, orders_list, pagination_filter):
        return self.__model.get_users(users_filter, orders_list, pagination_filter)

    def get_compositions(self, compositions_filter, orders_list, pagination_filter):
        return self.__model.get_compositions(compositions_filter, orders_list, pagination_filter)

    def get_artists(self, artists_filter, orders_list, pagination_filter):
        return self.__model.get_artists(artists_filter, orders_list, pagination_filter)

    def get_albums(self, albums_filter, orders_list, pagination_filter):
        return self.__model.get_albums(albums_filter, orders_list, pagination_filter)

    def get_playlists(self, playlists_filter, orders_list, pagination_filter):
        return self.__model.get_playlists(playlists_filter, orders_list, pagination_filter)

    def get_history(self, history_filter, orders_list, pagination_filter):
        return self.__model.get_listening_history(history_filter, orders_list, pagination_filter)

    def get_rating(self, rating_filter, orders_list, pagination_filter):
        return self.__model.get_rating(rating_filter, orders_list, pagination_filter)

    # standard user operations

    def create_user(self, user_model):
        return self.__model.create_user(user_model)

    def update_user(self, user_model):
        return self.__model.update_user(user_model)

    def delete_user(self, user_id):
        return self.__model.delete_user(user_id)

    # advanced composition operations

    def add_user_playlist(self, playlist_id, user_id):
        return self.__model.add_user_playlist(playlist_id, user_id)

    def remove_user_playlist(self, playlist_id, user_id):
        return self.__model.remove_user_playlist(playlist_id, user_id)

    def add_user_album(self, album_id, user_id):
        return self.__model.add_user_album(album_id, user_id)

    def remove_user_album(self, album_id, user_id):
        return self.__model.remove_user_album(album_id, user_id)

    # standard composition operations

    def create_composition(self, composition_model):
        return self.__model.create_composition(composition_model)

    def update_composition(self, composition_model):
        return self.__model.update_composition(composition_model)

    def delete_composition(self, composition_id):
        return self.__model.delete_composition(composition_id)

    # advanced composition operations

    def listen_composition(self, history_record):
        return self.__model.listen_composition(history_record)

    def unlisten_composition(self, history_record):
        return self.__model.unlisten_composition(history_record)

    def rate_composition(self, rating_model):
        return self.__model.rate_composition(rating_model)

    def unrate_composition(self, composition_id, user_id):
        return self.__model.unrate_composition(composition_id, user_id)

    # standard artist operations

    def create_artist(self, artist_model):
        return self.__model.create_artist(artist_model)

    def update_artist(self, artist_model):
        return self.__model.update_artist(artist_model)

    def delete_artist(self, artist_id):
        return self.__model.delete_artist(artist_id)

    # advanced artist operations

    # None?

    # standard playlist operations

    def create_playlist(self, playlist_model):
        return self.__model.create_playlist(playlist_model)

    def update_playlist(self, playlist_model):
        return self.__model.update_playlist(playlist_model)

    def delete_playlist(self, playlist_id):
        return self.__model.delete_playlist(playlist_id)

    def get_playlist(self, playlist_id):
        return self.__model.get_playlist(playlist_id)

    # advanced playlist operations

    def add_playlist_composition(self, playlist_id, composition_id):
        return self.__model.add_playlist_composition(playlist_id, composition_id)

    def remove_playlist_composition(self, playlist_id, composition_id):
        return self.__model.remove_playlist_composition(playlist_id, composition_id)

    def rate_playlist(self, rating_model):
        return self.__model.rate_playlist(rating_model)

    def unrate_playlist(self, playlist_id, user_id):
        return self.__model.unrate_playlist(playlist_id, user_id)

    # standard album operations

    def create_album(self, album_model):
        return self.__model.create_album(album_model)

    def update_album(self, album_model):
        return self.__model.update_album(album_model)

    def delete_album(self, album_id):
        return self.__model.delete_album(album_id)

    def get_album(self, album_id):
        return self.__model.get_album(album_id)

    # advanced album operations

    def add_album_composition(self, album_id, composition_id):
        return self.__model.add_album_composition(album_id, composition_id)

    def remove_album_composition(self, album_id, composition_id):
        return self.__model.remove_album_composition(album_id, composition_id)

    def rate_album(self, rating_model):
        return self.__model.rate_album(rating_model)

    def unrate_album(self, album_id, user_id):
        return self.__model.unrate_album(album_id, user_id)

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


