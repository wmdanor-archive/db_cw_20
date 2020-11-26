
class Rating:

    def __init__(self, rating_id, rated_id, user_id, satisfied, rating_date):
        self.rating_id = rating_id
        self.rated_id = rated_id
        self.user_id = user_id
        self.satisfied = satisfied
        self.rating_date = rating_date


class RatingFilter:

    def __init__(self, rated_ids=None, user_ids=None, satisfied=None, rated_from=None, rated_to=None):
        self.rated_ids = rated_ids
        self.user_ids = user_ids
        self.satisfied = satisfied
        self.rated_from = rated_from
        self.rated_to = rated_to
