import psycopg2

from model import PaginationFilter
import view
from controller import ControllerPSQL
from model import ModelPSQL

from models.user import User, UserFilter
from models.composition import Composition, CompositionFilter
from models.performer import ArtistFilter
from models.playlist import Playlist
from models.playlist import PlaylistPrivacy
from models.album import Album
from models.rating import Rating
from models.history_record import HistoryRecord


connection = psycopg2.connect(dbname='music_service_10', user='postgres',
                              password='postgres', host='localhost')

c = ControllerPSQL(connection)

# c.get_playlist(9)

# playlist = Playlist(None, 'test pl1', PlaylistPrivacy.public, None, 1)

# users_filter = UserFilter()
# compositions_filter = CompositionFilter()
# artists_filter = ArtistFilter()
#
# pagination_filter = PaginationFilter()
# users_filter.history.toggle = True
# compositions_filter.history.toggle = True
# compositions_filter.rating.toggle = True
# compositions_filter.playlists.toggle = True
# compositions_filter.albums.toggle = True
# artists_filter.history.toggle = True
# artists_filter.rating.toggle = True
# artists_filter.playlists.toggle = True
# artists_filter.albums.toggle = True

# c.get_users(users_filter, pagination_filter)
# c.get_compositions(compositions_filter, pagination_filter)
# c.get_artists(artists_filter, pagination_filter)
# c.create_playlist(playlist)

c.call_interface()
# c.create_user(User(0, 'test 1', 'ph', '2020-11-8', True, gender_id=1))
# user_model = User(0, 'test 1', 'ph', '2020-11-8', True, gender_id=1)
# cursor = connection.cursor()
# print(c.construct_artist())
# c.delete_playlist(10)

# print(users_filter)

# playlist = m.get_playlist(1)
#
# v.view_playlist(playlist)
