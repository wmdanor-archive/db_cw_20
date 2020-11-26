from models.to_string import to_str
from models.composition import CompositionFilter


class Artist:

    def __init__(self, artist_id, name, type_id, comment=None):
        self.artist_id = artist_id
        self.name = name
        self.type_id = type_id
        self.comment = comment


class ArtistFilter:

    class ArtistFilterAttributes:

        def __init__(self, name_comment=None, types=None, genders=None, begin_date_from=None, begin_date_to=None,
                     end_date_from=None, end_date_to=None, search_comments=None, ):
            self.name_comment = name_comment
            self.types = types
            self.genders = genders
            self.begin_date_from = begin_date_from
            self.begin_date_to = begin_date_to
            self.end_date_from = end_date_from
            self.end_date_to = end_date_to
            self.search_comments = search_comments

        def __str__(self):
            return 'name_comment: ' + to_str(self.name_comment) + '\ntypes: ' + to_str(self.types) +\
                '\nsearch_comments:' + to_str(self.search_comments)

    def __init__(self, artists_ids=None,
                 attributes=ArtistFilterAttributes(),
                 history=CompositionFilter.CompositionFilterListeningHistory(),
                 rating=CompositionFilter.CompositionFilterRating(),
                 albums=CompositionFilter.CompositionFilterCollections(),
                 playlists=CompositionFilter.CompositionFilterCollections()):
        self.artists_ids = artists_ids
        self.attributes = attributes
        self.history = history
        self.rating = rating
        self.albums = albums
        self.playlists = playlists

    def __str__(self):
        return 'artists_ids: ' + to_str(self.artists_ids) + '\nhistory:\n' + to_str(self.history) +\
            '\nrating:\n' + to_str(self.rating) + '\nalbums:\n' + to_str(self.albums) +\
            '\nplaylists:\n' + to_str(self.playlists)
