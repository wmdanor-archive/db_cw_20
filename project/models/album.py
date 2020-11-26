
class Album:

    def __init__(self, album_id, title, release_year, compositions=None):
        self.album_id = album_id
        self.title = title
        self.release_year = release_year
        self.compositions = compositions


class AlbumFilter:

    def __init__(self, title=None, release_from=None, release_to=None, compositions_ids=None):
        self.title = title
        self.release_from = release_from
        self.release_to = release_to
        self.compositions_ids = compositions_ids
