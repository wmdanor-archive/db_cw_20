from models.to_string import to_str

class User:

    def __init__(self, user_id, username, password_hash, registration_date, is_active,
                 full_name=None, birth_date=None, gender_id=None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.registration_date = registration_date
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender_id = gender_id
        self.is_active = is_active


class UserFilter:

    class OrderBy:
        user_id = 'user_id'
        username = 'username'
        registration_date = 'registration_date'
        full_name = 'full_name'
        birth_date = 'birth_date'
        sex = 'sex'
        is_active = 'is_active'

    class OrderType:
        ascending = 'ASC'
        descending = 'DESC'

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
                     times_listened_from=None, times_listened_to=None, compositions_ids=None, compositions_ids_any=True):
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

        def __init__(self, toggle=False, rating_date_from=None, rating_date_to=None, times_rated_from=None, times_rated_to=None,
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
