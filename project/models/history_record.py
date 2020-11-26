
class HistoryRecord:

    def __init__(self, record_id, composition_id, user_id, listening_date):
        self.record_id = record_id
        self.composition_id = composition_id
        self.user_id = user_id
        self.listening_date = listening_date


class HistoryFilter:

    def __init__(self, compositions_ids=None, users_ids=None, listened_from=None, listened_to=None):
        self.compositions_ids = compositions_ids
        self.users_ids = users_ids
        self.listened_from = listened_from
        self.listened_to = listened_to
