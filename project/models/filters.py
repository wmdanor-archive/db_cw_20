from models.to_string import to_str


class EntityFilterRating:

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
        return 'toggle: ' + to_str(self.toggle) + '\nrating_date_from: ' + to_str(self.rating_date_from) + \
               ' | rating_date_to: ' + to_str(self.rating_date_to) + '\ntimes_rated_from: ' + \
               to_str(self.times_rated_from) + ' | times_rated_to: ' + to_str(self.times_rated_to) + \
               '\naverage_rating_from: ' + to_str(self.average_rating_from) + ' | average_rating_to: ' + \
               to_str(self.average_rating_to) + '\nusers_ids: ' + to_str(self.users_ids) + \
               '\nusers_ids_any: ' + to_str(self.users_ids_any)


# User filter ----------------------------------------------------------------------------------------------------------


class UserFilter:

    class UserFilterAttributes:

        def __init__(self, username=None, full_name=None, registration_from=None, registration_to=None,
                     birth_from=None, birth_to=None, genders=None, is_active=None, full_name_exclude_nulls=False,
                     birth_exclude_nulls=False, gender_exclude_nulls=False
                     ):
            self.username = username
            self.full_name = full_name
            self.registration_from = registration_from
            self.registration_to = registration_to
            self.birth_from = birth_from
            self.birth_to = birth_to
            self.genders = genders
            self.is_active = is_active
            self.full_name_exclude_nulls = full_name_exclude_nulls
            self.birth_exclude_nulls = birth_exclude_nulls
            self.gender_exclude_nulls = gender_exclude_nulls

        def __str__(self):
            return 'username: ' + to_str(self.username) + ' | full_name: ' + to_str(self.full_name) +\
                ' | full_name_exclude_nulls: ' + to_str(self.full_name_exclude_nulls) + '\nregistration_from: ' +\
                to_str(self.registration_from) + ' | registration_to: ' + to_str(self.registration_to) +\
                '\nbirth_from: ' + to_str(self.birth_from) + ' | birth_to: ' + to_str(self.birth_to) +\
                ' | birth_exclude_nulls: ' + to_str(self.birth_exclude_nulls) + '\ngenders: ' +\
                to_str(self.genders) + '\ngender_exclude_nulls: ' + to_str(self.gender_exclude_nulls) +\
                'is_active: ' + to_str(self.is_active)

    class UserFilterListeningHistory:

        def __init__(self, toggle=False, listened_date_from=None, listened_date_to=None,
                     times_listened_from=None, times_listened_to=None, compositions_ids=None,
                     compositions_ids_any=True):
            self.toggle = toggle
            self.listened_date_from = listened_date_from
            self.listened_date_to = listened_date_to
            self.times_listened_from = times_listened_from
            self.times_listened_to = times_listened_to
            self.compositions_ids = compositions_ids
            self.compositions_ids_any = compositions_ids_any

        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nlistened_date_from: ' + to_str(self.listened_date_from) +\
                ' | listened_date_to: ' + to_str(self.listened_date_to) + '\ntimes_listened_from: ' +\
                to_str(self.times_listened_from) + ' | times_listened_to: ' + to_str(self.times_listened_to) +\
                '\ncompositions_ids: ' + to_str(self.compositions_ids) + '\ncompositions_ids_any: ' +\
                to_str(self.compositions_ids_any)

    class UserFilterRatings:

        def __init__(self, toggle=False, rating_date_from=None, rating_date_to=None,
                     times_rated_from=None, times_rated_to=None,
                     average_rating_from=None, average_rating_to=None, rated_ids=None, rated_ids_any=True):
            self.toggle = toggle
            self.rating_date_from = rating_date_from
            self.rating_date_to = rating_date_to
            self.times_rated_from = times_rated_from
            self.times_rated_to = times_rated_to
            self.average_rating_from = average_rating_from
            self.average_rating_to = average_rating_to
            self.rated_ids = rated_ids
            self.rated_ids_any = rated_ids_any

        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nrating_date_from: ' + to_str(self.rating_date_from) +\
                ' | rating_date_to: ' + to_str(self.rating_date_to) + '\ntimes_rated_from: ' +\
                to_str(self.times_rated_from) + ' | times_rated_to: ' + to_str(self.times_rated_to) +\
                '\naverage_rating_from: ' + to_str(self.average_rating_from) + ' | average_rating_to: ' +\
                to_str(self.average_rating_to) + '\nrated_ids: ' + to_str(self.rated_ids) +\
                '\nrated_ids_any: ' + to_str(self.rated_ids_any)

    class UserFilterSavedCollections:

        def __init__(self, toggle=False, saved_number_from=None, saved_number_to=None,
                     saved_ids_list=None, saved_ids_any=True):
            self.toggle = toggle
            self.saved_number_from = saved_number_from
            self.saved_number_to = saved_number_to
            self.saved_ids_list = saved_ids_list
            self.saved_ids_any = saved_ids_any

        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nsaved_number_from: ' + to_str(self.saved_number_from) +\
                ' | saved_number_to: ' + to_str(self.saved_number_to) + '\nsaved_ids_list: ' +\
                to_str(self.saved_ids_list) + '\nsaved_ids_any: ' + to_str(self.saved_ids_any)

    def __init__(self, users_ids=None, attributes=UserFilterAttributes(), history=UserFilterListeningHistory(),
                 compositions_rating=UserFilterRatings(), playlists_rating=UserFilterRatings(),
                 albums_rating=UserFilterRatings(),
                 saved_playlists=UserFilterSavedCollections(), saved_albums=UserFilterSavedCollections()):
        self.users_ids = users_ids
        self.attributes = attributes
        self.history = history
        self.compositions_rating = compositions_rating
        self.playlists_rating = playlists_rating
        self.albums_rating = albums_rating
        self.saved_playlists = saved_playlists
        self.saved_albums = saved_albums

    def __str__(self):
        return 'user_ids:' + to_str(self.users_ids) + '\nattributes:\n' + to_str(self.attributes) + '\nhistory:\n' +\
            to_str(self.history) + '\ncompositions_rating:\n' + to_str(self.compositions_rating) +\
            '\nplaylists_rating:\n' + to_str(self.playlists_rating) + '\nalbums_rating:\n' +\
            to_str(self.albums_rating) + '\nsaved_playlists:\n' + to_str(self.saved_playlists) +\
            '\nsaved_albums:\n' + to_str(self.saved_albums)


# Composition filter ---------------------------------------------------------------------------------------------------


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
            return 'title: ' + to_str(self.title_lyrics) + ' | artists_ids: ' + to_str(self.artists_ids) + \
                   ' | artists_ids_exclude_nulls: ' + to_str(self.artists_ids_exclude_nulls) + \
                   '\nduration_from: ' + to_str(self.duration_from) + ' | duration_to: ' + to_str(self.duration_to) + \
                   '\nrelease_from: ' + to_str(self.release_from) + ' | release_to:' + to_str(self.release_to) + \
                   ' | release_date_exclude_nulls:' + to_str(self.release_date_exclude_nulls) + '\nsearch_lyrics: ' + \
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
            return 'toggle: ' + to_str(self.toggle) + '\nlistened_date_from: ' + to_str(self.listened_date_from) + \
                   ' | listened_date_to: ' + to_str(self.listened_date_to) + '\ntimes_listened_from: ' + \
                   to_str(self.times_listened_from) + ' | times_listened_to: ' + to_str(self.times_listened_to) + \
                   '\nusers_ids: ' + to_str(self.users_ids) + '\nusers_ids_any: ' + to_str(self.users_ids_any)

    class CompositionFilterCollections:

        def __init__(self, toggle=False, number_belongs_from=None, number_belongs_to=None,
                     collections_list=None, collections_any=None):
            self.toggle = toggle
            self.number_belongs_from = number_belongs_from
            self.number_belongs_to = number_belongs_to
            self.collections_list = collections_list
            self.collections_any = collections_any

        def __str__(self):
            return 'toggle: ' + to_str(self.toggle) + '\nnumber_belongs_from: ' + to_str(self.number_belongs_from) + \
                   ' | number_belongs_to: ' + to_str(self.number_belongs_to) + '\ncollections_list: ' + \
                   to_str(self.collections_list) + '\ncollections_any: ' + to_str(self.collections_any)

    def __init__(self, compositions_ids=None,
                 attributes=CompositionFilterAttributes(), history=CompositionFilterListeningHistory(),
                 rating=EntityFilterRating(), albums=CompositionFilterCollections(),
                 playlists=CompositionFilterCollections()):
        self.compositions_ids = compositions_ids
        self.attributes = attributes
        self.history = history
        self.rating = rating
        self.albums = albums
        self.playlists = playlists

    def __str__(self):
        return 'compositions_ids: ' + to_str(self.compositions_ids) + '\nattributes:\n' + to_str(self.attributes) +\
               '\nhistory:\n' + to_str(self.history) + \
               '\nrating:\n' + to_str(self.rating) + '\nalbums:\n' + to_str(self.albums) + \
               '\nplaylists:\n' + to_str(self.playlists)


# Artist filter --------------------------------------------------------------------------------------------------------


class ArtistFilter:

    class ArtistFilterAttributes:

        def __init__(self, name_comment=None, types=None, gender_exclude_nulls=None, genders=None,
                     begin_date_exclude_nulls=None, begin_date_from=None, begin_date_to=None,
                     end_date_exclude_nulls=None, end_date_from=None, end_date_to=None, search_comments=None, ):
            self.name_comment = name_comment
            self.types = types
            self.gender_exclude_nulls = gender_exclude_nulls
            self.genders = genders
            self.begin_date_exclude_nulls = begin_date_exclude_nulls
            self.begin_date_from = begin_date_from
            self.begin_date_to = begin_date_to
            self.end_date_exclude_nulls = end_date_exclude_nulls
            self.end_date_from = end_date_from
            self.end_date_to = end_date_to
            self.search_comments = search_comments

        def __str__(self):
            return 'name_comment: ' + to_str(self.name_comment) + '\ntypes: ' + to_str(self.types) +\
                '\ngenders: ' + to_str(self.genders) + '\nbegin_date_from: ' + to_str(self.begin_date_from) +\
                ' | begin_date_to: ' + to_str(self.begin_date_to) + '\nend_date_from: ' + to_str(self.end_date_from) +\
                ' | end_date_to: ' + to_str(self.end_date_to) +\
                '\nsearch_comments:' + to_str(self.search_comments)

    def __init__(self, artists_ids=None,
                 attributes=ArtistFilterAttributes(),
                 history=CompositionFilter.CompositionFilterListeningHistory(),
                 rating=EntityFilterRating(),
                 albums=CompositionFilter.CompositionFilterCollections(),
                 playlists=CompositionFilter.CompositionFilterCollections()):
        self.artists_ids = artists_ids
        self.attributes = attributes
        self.history = history
        self.rating = rating
        self.albums = albums
        self.playlists = playlists

    def __str__(self):
        return 'artists_ids: ' + to_str(self.artists_ids) + '\nattributes:\n' + to_str(self.attributes) +\
            '\nhistory:\n' + to_str(self.history) +\
            '\nrating:\n' + to_str(self.rating) + '\nalbums:\n' + to_str(self.albums) +\
            '\nplaylists:\n' + to_str(self.playlists)


# Collection filter ----------------------------------------------------------------------------------------------------


class CollectionFilterCompositions:

    def __init__(self, toggle=False, compositions_number_from=None, compositions_number_to=None,
                 compositions_list=None, compositions_any=None):
        self.toggle = toggle
        self.compositions_number_from = compositions_number_from
        self.compositions_number_to = compositions_number_to
        self.compositions_list = compositions_list
        self.compositions_any = compositions_any

    def __str__(self):
        return 'compositions_number_from: ' + to_str(self.compositions_number_from) + ' | compositions_number_to: ' +\
            to_str(self.compositions_number_to) + '\ncompositions_list: ' + to_str(self.compositions_list) +\
            '\ncompositions_any: ' + to_str(self.compositions_any)


class CollectionFilterUsers:

    def __init__(self, toggle=False, users_number_from=None, users_number_to=None, users_list=None, users_any=None):
        self.toggle = toggle
        self.users_number_from = users_number_from
        self.users_number_to = users_number_to
        self.users_list = users_list
        self.users_any = users_any

    def __str__(self):
        return 'users_number_from: ' + to_str(self.users_number_from) + ' | users_number_to: ' + \
               to_str(self.users_number_to) + '\nusers_list: ' + to_str(self.users_list) + \
               '\nusers_any: ' + to_str(self.users_any)


# Playlist filter ------------------------------------------------------------------------------------------------------


class PlaylistFilter:

    class PlaylistFilterAttributes:

        def __init__(self, title=None, creators_ids_exclude_nulls=False, creators_ids=None, privacies=None):
            self.title = title
            self.creators_ids = creators_ids
            self.creators_ids_exclude_nulls = creators_ids_exclude_nulls
            self.privacies = privacies

        def __str__(self):
            return 'title: ' + to_str(self.title) + '\ncreators_ids: ' + to_str(self.creators_ids) +\
                ' | creators_ids_exclude_nulls: ' + to_str(self.creators_ids_exclude_nulls) + '\nprivacies: ' +\
                to_str(self.privacies)

    def __init__(self, playlists_ids=None,
                 attributes=PlaylistFilterAttributes(), compositions=CollectionFilterCompositions(),
                 rating=EntityFilterRating(), users=CollectionFilterUsers()):
        self.playlists_ids = playlists_ids
        self.attributes = attributes
        self.compositions = compositions
        self.rating = rating
        self.users = users

    def __str__(self):
        return 'playlists_ids: ' + to_str(self.playlists_ids) + '\nattributes:\n' + to_str(self.attributes) + \
               '\ncompositions:\n' + to_str(self.compositions) + \
               '\nrating:\n' + to_str(self.rating) +\
               '\nusers:\n' + to_str(self.users)


# Album filter ---------------------------------------------------------------------------------------------------------


class AlbumFilter:

    class AlbumFilterAttributes:

        def __init__(self, title=None, release_date_exclude_nulls=None,
                     release_date_from=None, release_date_to=None):
            self.title = title
            self.release_date_exclude_nulls = release_date_exclude_nulls
            self.release_date_from = release_date_from
            self.release_date_to = release_date_to

        def __str__(self):
            return 'title: ' + to_str(self.title) + '\nrelease_date_exclude_nulls: ' +\
                   to_str(self.release_date_exclude_nulls) + \
                   '\nrelease_date_from' + to_str(self.release_date_from) + ' | release_date_to: ' + \
                   to_str(self.release_date_to)

    def __init__(self, albums_ids=None,
                 attributes=AlbumFilterAttributes(),
                 compositions=CollectionFilterCompositions(),
                 rating=EntityFilterRating(),
                 users=CollectionFilterUsers()):
        self.albums_ids = albums_ids
        self.attributes = attributes
        self.compositions = compositions
        self.rating = rating
        self.users = users

    def __str__(self):
        return 'albums_ids: ' + to_str(self.albums_ids) + '\nattributes:\n' + to_str(self.attributes) + \
               '\ncompositions:\n' + to_str(self.compositions) + \
               '\nrating:\n' + to_str(self.rating) + \
               '\nusers:\n' + to_str(self.users)


# History filter


class HistoryFilter:

    def __init__(self, compositions_ids=None, users_ids=None, listened_from=None, listened_to=None,
                 user_listened_counter=None, composition_listened_counter=None):
        self.compositions_ids = compositions_ids
        self.users_ids = users_ids
        self.listened_from = listened_from
        self.listened_to = listened_to
        self.user_listened_counter = user_listened_counter
        self.composition_listened_counter = composition_listened_counter

    def __str__(self):
        return 'compositions_ids: ' + to_str(self.compositions_ids) + '\nusers_ids: ' +\
                to_str(self.users_ids) + '\nlistened_from: ' + to_str(self.listened_from) +\
                ' | listened_to: ' + to_str(self.listened_to) + '\nuser_listened_counter: '+\
                to_str(self.user_listened_counter) + '\ncomposition_listened_counter: ' +\
                to_str(self.composition_listened_counter)


# Rating filter


class RatingFilter:

    def __init__(self, rated_type=1,
                 rated_ids=None, users_ids=None, satisfied=None, rated_from=None, rated_to=None,
                 rated_rating_counter=None, user_rating_counter=None):
        self.rated_type = rated_type
        self.rated_ids = rated_ids
        self.users_ids = users_ids
        self.satisfied = satisfied
        self.rated_from = rated_from
        self.rated_to = rated_to
        self.rated_rating_counter = rated_rating_counter
        self.user_rating_counter = user_rating_counter

    def __str__(self):
        return 'rated_ids: ' + to_str(self.rated_ids) + '\nusers_ids: ' + \
               to_str(self.users_ids) + '\nrated_from: ' + to_str(self.rated_from) + \
               ' | rated_to: ' + to_str(self.rated_to) + ' | satisfied: ' + to_str(self.satisfied) +\
               '\nrated_rating_counter: ' + to_str(self.rated_rating_counter) +\
               '\nuser_rating_counter: ' + to_str(self.user_rating_counter)
