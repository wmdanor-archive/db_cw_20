from models.to_string import to_str


class Composition:

    def __init__(self, composition_id, title, duration, path_to_file, times_listened, release_year=None,
                 release_month=None, release_day=None, lyrics=None):
        self.composition_id = composition_id
        self.title = title
        self.duration = duration
        self.path_to_file = path_to_file
        self.times_listened = times_listened
        self.release_year = release_year
        self.release_month = release_month
        self.release_day = release_day
        self.lyrics = lyrics

    def __str__(self):
        return 'composition_id: ' + to_str(self.composition_id) + ' | title: ' + self.title + ' | duration: ' + \
               to_str(self.duration) + ' | release_year: ' + to_str(self.release_year) + ' | release_month: ' + \
               to_str(self.release_month) + ' | release_day: ' + to_str(self.release_day) + ' | times listened: ' + \
               to_str(self.times_listened) + ' | path: ' + self.path_to_file + ' |\nlyrics: ' + to_str(self.lyrics)


class CompositionFilter:

    class CompositionFilterAttributes:

        def __init__(self, title_lyrics=None, artists_ids_exclude_nulls=False, artists_ids=None,
                     duration_from=None, duration_to=None, release_date_exclude_nulls=False,
                     release_from=None, release_to=None, search_lyrics=False):
            self.title_lyrics = title_lyrics
            self.artists_ids_exclude_nulls = artists_ids_exclude_nulls
            self.artists_ids = artists_ids
            self.duration_from = duration_from
            self.duration_to = duration_to
            self.release_date_exclude_nulls = release_date_exclude_nulls
            self.release_from = release_from
            self.release_to = release_to
            self.search_lyrics = search_lyrics

        def __str__(self):
            return 'title: ' + to_str(self.title_lyrics) + ' | artists_ids: ' + to_str(self.artists_ids) +\
                ' | artists_ids_exclude_nulls: ' + to_str(self.artists_ids_exclude_nulls) +\
                '\nduration_from: ' + to_str(self.duration_from) + ' | duration_to: ' + to_str(self.duration_to) +\
                '\nrelease_from: ' + to_str(self.release_from) + ' | release_to:' + to_str(self.release_to) +\
                ' | release_date_exclude_nulls:' + to_str(self.release_date_exclude_nulls) + '\nsearch_lyrics: ' +\
                to_str(self.search_lyrics)

    class CompositionFilterListeningHistory:

        def __init__(self, toggle=False, times_listened_from=None, times_listened_to=None,
                     listened_date_from=None, listened_date_to=None, users_ids=None, users_ids_any=None):
            self.toggle = toggle
            self.times_listened_from = times_listened_from
            self.times_listened_to = times_listened_to
            self.listened_date_from = listened_date_from
            self.listened_date_to = listened_date_to
            self.users_ids = users_ids
            self.users_ids_any = users_ids_any
            
        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nlistened_date_from: ' + to_str(self.listened_date_from) +\
                ' | listened_date_to: ' + to_str(self.listened_date_to) + '\ntimes_listened_from: ' +\
                to_str(self.times_listened_from) + ' | times_listened_to: ' + to_str(self.times_listened_to) +\
                '\nusers_ids: ' + to_str(self.users_ids) + '\nusers_ids_any: ' +\
                to_str(self.users_ids_any)

    class CompositionFilterRating:

        def __init__(self, toggle=False, rating_date_from=None, rating_date_to=None, times_rated_from=None,
                     times_rated_to=None, average_rating_from=None, average_rating_to=None, users_ids=None,
                     users_ids_any=None):
            self.toggle = toggle
            self.rating_date_from = rating_date_from
            self.rating_date_to = rating_date_to
            self.times_rated_from = times_rated_from
            self.times_rated_to = times_rated_to
            self.average_rating_from = average_rating_from
            self.average_rating_to = average_rating_to
            self.users_ids = users_ids
            self.users_ids_any = users_ids_any

        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nrating_date_from: ' + to_str(self.rating_date_from) +\
                ' | rating_date_to: ' + to_str(self.rating_date_to) + '\ntimes_rated_from: ' +\
                to_str(self.times_rated_from) + ' | times_rated_to: ' + to_str(self.times_rated_to) +\
                '\naverage_rating_from: ' + to_str(self.average_rating_from) + ' | average_rating_to: ' +\
                to_str(self.average_rating_to) + '\nusers_ids: ' + to_str(self.users_ids) +\
                '\nusers_ids_any: ' + to_str(self.users_ids_any)

    class CompositionFilterCollections:

        def __init__(self, toggle=False,  number_belongs_from=None, number_belongs_to=None,
                     collections_list=None, collections_any=None):
            self.toggle = toggle
            self.number_belongs_from = number_belongs_from
            self.number_belongs_to = number_belongs_to
            self.collections_list = collections_list
            self.collections_any = collections_any

        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nnumber_belongs_from: ' + to_str(self.number_belongs_from) +\
                ' | number_belongs_to: ' + to_str(self.number_belongs_to) + '\ncollections_list: ' +\
                to_str(self.collections_list) + '\ncollections_any: ' + to_str(self.collections_any)

    def __init__(self, compositions_ids=None,
                 attributes=CompositionFilterAttributes(), history=CompositionFilterListeningHistory(),
                 rating=CompositionFilterRating(), albums=CompositionFilterCollections(),
                 playlists=CompositionFilterCollections()):
        self.compositions_ids = compositions_ids
        self.attributes = attributes
        self.history = history
        self.rating = rating
        self.albums = albums
        self.playlists = playlists

    def __str__(self):
        return 'compositions_ids: ' + to_str(self.compositions_ids) + '\nhistory:\n' + to_str(self.history) +\
            '\nrating:\n' + to_str(self.rating) + '\nalbums:\n' + to_str(self.albums) +\
            '\nplaylists:\n' + to_str(self.playlists)
