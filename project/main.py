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

# region listening history chart

hf = HistoryFilter()
hf.compositions_ids = 1
hf.composition_listened_counter = True

hist = m.get_listening_history(hf, [4], PaginationFilter())

x_arr = []
y_arr = []

s = len(hist)
dt = max(1, int(s/99))
for i in range(0, min(s, 100)):
    x_arr.append(hist[i*dt]['listening_date'])
    y_arr.append(hist[i * dt]['times_composition_listened'])

fig = plt.figure()
plt.plot(x_arr, y_arr)
plt.xticks(rotation='vertical')
plt.title('INSERT TITLE' + ' listening chart')
plt.savefig('./matplotlib_files/composition_'+str(1)+'_listening_chart.png', bbox_inches='tight')
# plt.show()

# endregion

# region rating chart

rf = RatingFilter()
rf.rated_ids = 1
rf.rated_rating_counter = True

rate = m.get_rating(rf, [5], PaginationFilter())

rate = rate[50:]  # temp

x_arr = []
y_arr = []

s = len(rate)
print(s)
dt = max(1, int(s/99))
for i in range(0, min(s, 100)):
    x_arr.append(rate[i*dt]['rating_date'])
    y_arr.append(rate[i * dt]['avg_rated_rating'])
    print(i, '(', i*dt, ') -', rate[i * dt]['avg_rated_rating'])

# for item in y_arr:
#     print(item)

fig = plt.figure()
plt.plot(x_arr, y_arr)
plt.xticks(rotation='vertical')
plt.title('INSERT TITLE' + ' rating chart')
plt.savefig('./matplotlib_files/composition_'+str(1)+'_rating_chart.png', bbox_inches='tight')
# plt.show()

# endregion

# region compositions times listened bar char

cf = CompositionFilter()
cf.history.toggle = True
pf = PaginationFilter()
pf.page_size = 20
pf.page = 1
comps = m.get_compositions(cf, -6, pf)

# for item in comps:
#     print(item)

x = list(range(1, 21))
listened = []
label = []

for item in comps:
    label.append(item['title'])
    listened.append(item['times_listened'])

fig, ax = plt.subplots()

bar_plot = plt.bar(x, listened)
plt.xticks(x, label, rotation='vertical')

plt.title('Top 20 listened compositions')
plt.savefig('./matplotlib_files/compositions_listening_bar_char.png', bbox_inches='tight')
# plt.show()

# endregion

# region entities rating bar char

cf = CompositionFilter()
cf.rating.toggle = True
pf = PaginationFilter()
pf.page_size = 20
pf.page = 1
comps = m.get_compositions(cf, -7, pf)

# for item in comps:
#     print(item)

x = list(range(1, 21))
rating = []
label = []
count = []

for item in comps:
    label.append(item['title'])
    rating.append(item['average_rating'])
    count.append(item['times_rated'])

fig, ax = plt.subplots()

bar_plot = plt.bar(x, rating)
plt.xticks(x, label, rotation='vertical')

for idx, rect in enumerate(bar_plot):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., 0.5*height,
            count[idx],
            ha='center', va='bottom', rotation=90)

plt.ylim(0, 10)
plt.title('Top 20 rated compositions')
plt.savefig('./matplotlib_files/compositions_rating_bar_char.png', bbox_inches='tight')
# plt.show()

# endregion
