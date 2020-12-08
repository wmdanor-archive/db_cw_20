import psycopg2

from model import PaginationFilter
from datetime import date
from controller import ControllerPSQL
from model import ModelPSQL
from view import ConsoleView

from models.album import Album
from models.rating import Rating
from models.history_record import HistoryRecord
from models.filters import *

import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


connection = psycopg2.connect(dbname='music_service_10', user='postgres',
                              password='1', host='localhost')

c = ControllerPSQL(connection)
m = ModelPSQL(connection)
v = ConsoleView(connection)
v.call_interface()
exit(0)

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
