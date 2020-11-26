from enum import Enum


class PlaylistPrivacy(Enum):
    public = 1
    unlisted = 2
    private = 3


class Playlist:

    def __init__(self, playlist_id, title, privacy_id, compositions=None, creator_id=None):
        self.playlist_id = playlist_id
        self.title = title
        self.privacy_id = privacy_id
        self.compositions = compositions
        self.creator_id = creator_id


class PlaylistFilter:

    class PlaylistFilterAttributes:

        pass

    def __init__(self, title=None, creators_ids=None, privacies_ids=None, compositions_ids=None):
        self.title = title
        self.creators_ids = creators_ids
        self.privacies_ids = privacies_ids
        self.compositions_ids = compositions_ids
