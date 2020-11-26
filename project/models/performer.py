from models.to_string import to_str


class Artist:

    def __init__(self, artist_id, name, type_id, comment=None):
        self.artist_id = artist_id
        self.name = name
        self.type_id = type_id
        self.comment = comment
