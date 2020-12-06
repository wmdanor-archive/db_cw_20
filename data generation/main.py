from time import time, sleep
import psycopg2
import psycopg2.extensions
from psycopg2.extras import DictCursor
from datetime import datetime, timedelta, date
import random
import xlrd
import math
import csv
import sqlite3
import numpy

conn = sqlite3.connect(r"C:\Users\Igor\Desktop\billboard-200 — копия.db")
cur = conn.cursor()

connection = psycopg2.connect(dbname='music_service_10', user='postgres',
                              password='1', host='localhost')
cursor = connection.cursor(cursor_factory=DictCursor)

connection.autocommit = True


def execute(query):
    cursor.execute(query)
    for row in cursor:
        print(row)


# cur.execute('select * from acoustic_features limit 995')
#
# albums = set()
# comps = []
# arts = set()
#
# rows = cur.fetchall()
# for row in rows:
#     # print(type(row), row)
#     d = row[18].split('-')
#     comps.append((row[1], d[0], d[1], d[2], int(row[6]/1000), row[2], row[3]))
#     arts.add(row[3])
#     albums.add((row[2], d[0], d[1], d[2]))
#
# narts = {}
# cursor.execute('insert into artists(name, type_id) select unnest(%s), floor(random() * 2 + 1)::int returning *', (list(arts),))
# for i in cursor:
#     narts[i['name']] = i['artist_id']
#
#
# nalbs = {}
# for i in albums:
#     cursor.execute('insert into albums(title, release_year, release_month, release_day) values(%s, %s, %s, %s)'
#                    ' returning *',
#                    (i[0], i[1], i[2], i[3]))
#     r = cursor.fetchone()
#     nalbs[r['title']] = r['album_id']
#
# ncomps = {}
# for i in comps:
#     q = narts[i[6]]
#     cursor.execute("insert into compositions(title, release_year, release_month, release_day, artist_id, duration, path_to_file) "
#                    "values(%s, %s, %s, %s, %s, %s, %s) returning *",
#                    (i[0], i[1], i[2], i[3], q, i[4], 'fakepath'))
#     r = cursor.fetchone()
#     ncomps[r['title']] = r['composition_id']
#
# for i in nalbs:
#     print(i)
#
# for i in comps:
#     a = nalbs[i[5]]
#     c = ncomps[i[0]]
#     cursor.execute('insert into album_comp_links(album_id, composition_id) values(%s, %s) on conflict do nothing', (a, c))

# print((datetime.now() - datetime(2026, 12, 10)))
# exit(0)

# ----------------------------------------------------------------------------------------------------------------------

# region users generation

# def random_date(start, end):
#     """Generate a random datetime between `start` and `end`"""
#     return start + timedelta(
#         # Get a random amount of seconds between `start` and `end`
#         seconds=random.randint(0, int((end - start).total_seconds())),
#     )
#
#
# print('Users generation')
#
# usrs = []
# users = [[], [], [], []]  # username, full name, birth_date, gender
#
# f = open(r"C:\Users\Igor\Documents\GitHub\db_cw_20\docs\usernames.csv", 'r')
# reader = csv.reader(f)
# usr_set = set()
# for row in reader:
#     usr_set.add(row[14])
# f.close()
# usr_set = list(usr_set)
# usr_set = usr_set[0:3500]
# for i in usr_set:
#     usrs.append([i, None, None, None])
#
# f = open(r"C:\Users\Igor\Documents\GitHub\db_cw_20\docs\male names.TXT", 'r')
# c = 0
# for line in f:
#     usrs[c][1] = line[:-1]
#     if random.random() <= 0.9:
#         usrs[c][3] = 1 if random.random() <= 0.996 else 3
#         if random.random() <= 0.7:
#             usrs[c][2] = random_date(datetime(1980, 1, 1), datetime(2004, 1, 1)).date()
#     c += 1
# f.close()
#
# f = open(r"C:\Users\Igor\Documents\GitHub\db_cw_20\docs\female names.TXT", 'r')
# for line in f:
#     usrs[c][1] = line[:-1]
#     if random.random() <= 0.9:
#         usrs[c][3] = 2 if random.random() <= 0.996 else 3
#         if random.random() <= 0.7:
#             usrs[c][2] = random_date(datetime(1980, 1, 1), datetime(2004, 1, 1)).date()
#     c += 1
# f.close()
#
# random.shuffle(usrs)
#
# for item in usrs:
#     users[0].append(item[0])
#     users[1].append(item[1])
#     users[2].append(item[2])
#     users[3].append(item[3])
#
# cursor.execute(
#     "insert into users (username, password_hash, registration_date, is_active, full_name, birth_date, gender_id) "
#     "select unnest(%s), 'fakehash', "
#     "(date '2020-1-1' - '4 years'::interval + justify_interval('4 years'::interval/(3500 - 1 + 1) * generate_series(1, 3500)))::date, "
#     "toss_a_coin(0.95), unnest(%s), unnest(%s), unnest(%s)",
#     (users[0], users[1], users[2], users[3])
# )
#
# print('Users generation ended')

# endregion

# ----------------------------------------------------------------------------------------------------------------------

# region comp, album pre generation

n = 100
m = 100000

ruser = 0

# users_d = dict()
users_d = []
users = []
comps = []
comps_r = {}
comps_a = {}
comps_distr = []
h_records = [[], [], []]
r_records = [[], [], [], []]
ar_records = [[], [], [], []]
c = 0
yrs4 = timedelta(days=4 * 365)
dt = yrs4 / (n * m)
st_date = date(2016, 1, 1)
ed_date = date(2020, 1, 1)
# print(dt)

cursor.execute('select user_id, registration_date from users')
for row in cursor:
    # users_d[row['user_id']] = row['registration_date']
    users_d.append((row['user_id'], row['registration_date']))
    users.append(row['user_id'])

cursor.execute('select compositions.composition_id, album_id from compositions '
               'inner join album_comp_links on '
               'album_comp_links.composition_id = compositions.composition_id')
for row in cursor:
    comps.append(row['composition_id'])
    while True:
        temp = numpy.random.normal(7, 0.5**0.5) / 10
        if 0 <= temp <= 10:
            comps_r[row['composition_id']] = temp
            break
    comps_a[row['composition_id']] = row['album_id']

print(len(users))
print(len(comps))
ulen = len(users) - 1
clen = len(comps) - 1


part = 1 / len(comps)
for counter in range(0, len(comps)):
    while True:
        temp = numpy.random.normal(1, 0.22**0.5) / len(comps)
        if temp > 0:
            comps_distr.append(temp)
            break
# comps[len(comps)-1] = 1 - sum(comps_distr[0:len(comps_distr)-2])
print(sum(comps_distr))
temp = (1 - sum(comps_distr)) / len(comps_distr)
print(temp)
for counter in range(0, len(comps_distr)):
    comps_distr[counter] += temp
print(sum(comps_distr))
print(comps_distr)
# comps[len(comps) - 1] = 1 - temp
# print(sum(comps))
for counter in range(1, len(comps_distr)):
    comps_distr[counter] += comps_distr[counter - 1]
comps_distr[len(comps_distr) - 1] = 1
print(comps_distr)
# exit(0)

# endregion

# region comps and albums rating gen start

ts = time()

print('Generating start, ', n, ' times with ', m, ' times each', sep='')
for i in range(0, n):
    h_records = [[], [], []]
    r_records = [[], [], [], []]
    ar_records = [[], [], [], []]
    albums_saved = [[], []]  # user_id, album_id
    ts1 = time()
    for j in range(0, m):
        random_val = random.random()
        comp_index = len(comps_distr) - 1
        # for w in range(0, len(comps_distr)):
        #     if random_val < comps_distr[w]:
        #         comp_index = w
        # rcomp = comp_index

        low = 0
        high = len(comps_distr) - 1
        middle = -1
        while low <= high:
            middle = int((low + high) / 2)
            # print(comps_distr[middle-1] if middle != 0 else 0, random_val, comps_distr[middle])
            # sleep(0.5)
            if random_val > comps_distr[middle]:
                low = middle + 1
            elif (comps_distr[middle - 1] if middle != 0 else 0) <= random_val <= comps_distr[middle]:
                comp_index = middle
                break
            else:
                high = middle - 1
        # print(' |', comp_index)
        rcomp = comps[comp_index]

        # rcomp = comps[random.randint(0, clen)]
        rdate = (st_date + dt * c)
        k = 1
        while True:
            print('\r', j + 1, '/', m, sep='', end='')
            # cp = users_d[0:max(1, int(3500 * (1 - (ed_date - rdate)/yrs4)))]
            # ruser = cp[random.randint(0, len(cp)-1)]
            ruser = users_d[random.randint(0, max(1, int(3500 * (1 - (ed_date - rdate) / yrs4))))]
            if ruser[1] <= rdate:
                break
            k += 1

            # ruser = users[random.randint(0, ulen)]
            # if users_d[ruser] <= rdate:
            #     break
        # h_records.append((ruser[0], rcomp, rdate))
        h_records[0].append(ruser[0])
        h_records[1].append(rcomp)
        h_records[2].append(rdate)
        if random.random() <= 0.055:
            r_records[0].append(ruser[0])
            r_records[1].append(rcomp)
            r_records[2].append(rdate)
            # sat = random.random() <= random.uniform(0.55, 1)
            sat = random.random() <= comps_r[rcomp]
            r_records[3].append(sat)
            if random.random() <= 0.02:
                ar_records[0].append(ruser[0])
                ar_records[1].append(comps_a[rcomp])
                ar_records[2].append(rdate)
                ar_records[3].append(sat)

                if sat and random.random() <= 0.2:
                    albums_saved[0].append(ruser[0])
                    albums_saved[1].append(comps_a[rcomp])

        c += 1
    # print()
    print(' | ', i + 1, '/', n, ' | gen time: ', round(time() - ts1, 2), sep='', end='')
    ts1 = time()
    # print(len(r_records[0]))
    # cursor.execute('select pg_typeof(unnest(%s)), unnest(%s)', (h_records, h_records))
    # row = cursor.fetchone()
    # print(row)
    cursor.execute('insert into listening_history(user_id, composition_id, listening_date) '
                   'select unnest(%s), unnest(%s), unnest(%s)', (h_records[0], h_records[1], h_records[2]))
    cursor.execute('insert into compositions_rating(user_id, composition_id, rating_date, satisfied) '
                   'select unnest(%s), unnest(%s), unnest(%s), unnest(%s) on conflict do nothing',
                   (r_records[0], r_records[1], r_records[2], r_records[3]))
    if len(ar_records[0]) != 0:
        cursor.execute('insert into albums_rating(user_id, album_id, rating_date, satisfied) '
                       'select unnest(%s), unnest(%s), unnest(%s), unnest(%s) on conflict do nothing',
                       (ar_records[0], ar_records[1], ar_records[2], ar_records[3]))
    if len(albums_saved[0]) != 0:
        cursor.execute('insert into user_saved_albums(user_id, album_id) '
                       'select unnest(%s), unnest(%s) on conflict do nothing', (albums_saved[0], albums_saved[1]))
    print(', query time: ', round(time() - ts1, 2), sep='', end='\n')
    # print(len(h_records))
print()

print('Execution time', round(time() - ts, 2))

# exit(0)
# endregion

# ----------------------------------------------------------------------------------------------------------------------

# region playlists gen

print('Playlists generation')

users_pl = {}
plist_size = {}
plists = [[], [], [], []]  # user_id, size, privacy_id, title
plists_auto = [[], []]  # size, title

for i in users:
    users_pl[i] = random.randint(1, 6)

print(users_pl)
for k, v in users_pl.items():
    for i in range(0, v):
        plists[0].append(k)
        plists[1].append(random.randint(1, 250))
        rval = random.random()
        if rval <= 0.5:
            plists[2].append(3)
        elif rval <= 0.8:
            plists[2].append(2)
        else:
            plists[2].append(1)
        plists[3].append('User ' + str(k) + ' playlist #' + str(i+1))

for i in range(0, 1000):
    plists_auto[0].append(random.randint(25, 100))
    plists_auto[1].append('Auto-generated playlist ' + str(i+1))

auto_pl_ids = {}

cursor.execute('insert into playlists(title, privacy_id) '
               'select unnest(%s), 1 returning *', (plists_auto[1],))
for i in cursor:
    auto_pl_ids[i['title']] = i['playlist_id']
print('Auto playlists OK')

user_pl_ids = {}
user_cr_pl = [[], []]

cursor.execute('insert into playlists(title, privacy_id, creator_id) '
               'select unnest(%s), unnest(%s), unnest(%s) returning *', (plists[3], plists[2], plists[0]))
for i in cursor:
    user_pl_ids[i['title']] = i['playlist_id']
    user_cr_pl[0].append(i['creator_id'])
    user_cr_pl[1].append(i['playlist_id'])

cursor.execute('insert into user_saved_plists(user_id, playlist_id) '
               'select unnest(%s), unnest(%s)', (user_cr_pl[0], user_cr_pl[1]))
print('User playlists OK')

for i in range(0, len(auto_pl_ids)):
    pl_comps = []
    for j in range(0, plists_auto[0][i]):
        pl_comps.append(comps[random.randint(0, len(comps) - 1)])
    cursor.execute('insert into plist_comp_links(composition_id, playlist_id) '
                   'select unnest(%s), %s on conflict do nothing', (pl_comps, auto_pl_ids[plists_auto[1][i]]))
print('Auto playlists compositions OK')

for i in range(0, len(user_pl_ids)):
    pl_comps = []
    for j in range(0, plists[1][i]):
        pl_comps.append(comps[random.randint(0, len(comps) - 1)])
    cursor.execute('insert into plist_comp_links(composition_id, playlist_id) '
                   'select unnest(%s), %s on conflict do nothing', (pl_comps, user_pl_ids[plists[3][i]]))
print('User playlists compositions OK')

print('Playlists generation ended')

# endregion

# ----------------------------------------------------------------------------------------------------------------------

print('Playlists rating generation')

r_records = [[], [], [], []]

c = 0
dt = yrs4 / 175000

plists = []
plists_distr = []
plists_r = {}
cursor.execute('select playlist_id from playlists where privacy_id = 1')
for row in cursor:
    plists.append(row['playlist_id'])
    while True:
        temp = numpy.random.normal(7, 0.5**0.5) / 10
        if 0 <= temp <= 10:
            plists_r[row['playlist_id']] = temp
            break


part = 1 / len(plists)
for counter in range(0, len(plists)):
    while True:
        temp = numpy.random.normal(1, 0.22**0.5) / len(plists)
        if temp > 0:
            plists_distr.append(temp)
            break

temp = (1 - sum(plists_distr)) / len(plists_distr)
for counter in range(0, len(plists_distr)):
    plists_distr[counter] += temp

for counter in range(1, len(plists_distr)):
    plists_distr[counter] += plists_distr[counter - 1]
plists_distr[len(plists_distr) - 1] = 1
print(plists_distr)

plists_saved = [[], []]  # user_id, playlist_id

for i in range(0, 175000):
    random_val = random.random()
    index = len(plists_distr) - 1

    low = 0
    high = len(plists_distr) - 1
    middle = -1
    while low <= high:
        middle = int((low + high) / 2)
        if random_val > plists_distr[middle]:
            low = middle + 1
        elif (plists_distr[middle - 1] if middle != 0 else 0) <= random_val <= plists_distr[middle]:
            index = middle
            break
        else:
            high = middle - 1
    rplist = plists[index]
    rdate = (st_date + dt * c)

    k = 1
    while True:
        ruser = users_d[random.randint(0, max(1, int(3500 * (1 - (ed_date - rdate) / yrs4))))]
        if ruser[1] <= rdate:
            break
        k += 1

    r_records[0].append(ruser[0])
    r_records[1].append(rplist)
    r_records[2].append(rdate)
    sat = random.random() <= plists_r[rplist]
    r_records[3].append(sat)

    if sat and random.random() <= 0.033:
        plists_saved[0].append(ruser[0])
        plists_saved[1].append(rplist)

    c += 1

cursor.execute('insert into playlists_rating(user_id, playlist_id, rating_date, satisfied) '
                   'select unnest(%s), unnest(%s), unnest(%s), unnest(%s) on conflict do nothing returning *',
                   (r_records[0], r_records[1], r_records[2], r_records[3]))
cursor.execute('insert into user_saved_plists(user_id, playlist_id) '
                   'select unnest(%s), unnest(%s) on conflict do nothing', (plists_saved[0], plists_saved[1]))

print('Playlists rating generation ended')
