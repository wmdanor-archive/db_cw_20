
class Playlist:

    def __init__(self, playlist_id, title, privacy_id, creator_id=None):
        self.playlist_id = playlist_id
        self.title = title
        self.privacy_id = privacy_id
        self.creator_id = creator_id
