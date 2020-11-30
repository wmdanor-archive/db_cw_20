import psycopg2

from model import PaginationFilter
from datetime import date
from controller import ControllerPSQL
from model import ModelPSQL

from models.album import Album
from models.rating import Rating
from models.history_record import HistoryRecord
from models.filters import *

import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


connection = psycopg2.connect(dbname='music_service_10', user='postgres',
                              password='postgres', host='localhost')

c = ControllerPSQL(connection)
m = ModelPSQL(connection)

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

# c.call_interface()
# method_list = [func for func in dir(ModelPSQL) if callable(getattr(ModelPSQL, func)) and
#                not func.startswith('__') and not func.startswith('fill_')]
# print(method_list)
# i = 1
# for item in method_list:
#     print(i, item)
#     i += 1
# c.create_user(User(0, 'test 1', 'ph', '2020-11-8', True, gender_id=1))
# user_model = User(0, 'test 1', 'ph', '2020-11-8', True, gender_id=1)
# cursor = connection.cursor()
# print(c.construct_artist())
# c.delete_playlist(10)

# print(users_filter)

# playlist = m.get_playlist(1)
#
# v.view_playlist(playlist)

hf = HistoryFilter()
hf.compositions_ids = 1
hf.composition_listened_counter = True

hist = m.get_listening_history(hf, [4], PaginationFilter())

# d1 = date(2016, 11, 3)
# d2 = date(2020, 10, 30)
# ts = (d2 - d1)/4
# arr = []
# i = 0
# while i < 5:
#     arr.append(d1 + ts*i)
#     i += 1
#
# t1 = 0
# t2 = 810
#
# ax = plt.gca()
# formatter = mdates.DateFormatter("%Y-%m-%d")
# ax.xaxis.set_major_formatter(formatter)
#
# locator = mdates.DayLocator()
# ax.xaxis.set_major_locator(locator)

x_arr = []
y_arr = []

s = len(hist)
dt = int(s/99)
for i in range(0, 100):
    x_arr.append(hist[i*dt]['listening_date'])
    y_arr.append(hist[i * dt]['times_composition_listened'])

fig = plt.figure()
plt.plot(x_arr, y_arr)
plt.show()

# ----------------------------------------------------------------

cf = CompositionFilter()
cf.rating.toggle = True
pf = PaginationFilter()
pf.page_size = 20
pf.page = 1
comps = m.get_compositions(cf, [7], pf)

x_arr = []
y_arr = []

s = len(comps)
dt = int(s/99)
for i in range(0, 100):
    x_arr.append(hist[i*dt]['listening_date'])
    y_arr.append(hist[i * dt]['times_composition_listened'])
