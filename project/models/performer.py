from models.to_string import to_str


class Artist:

    def __init__(self, artist_id, name, type_id, gender_id=None, comment=None,
                 begin_date_year=None, begin_date_month=None, begin_date_day=None,
                 end_date_year=None, end_date_month=None, end_date_day=None):
        self.artist_id = artist_id
        self.name = name
        self.type_id = type_id
        self.gender_id = gender_id
        self.begin_date_year = begin_date_year
        self.begin_date_month = begin_date_month
        self.begin_date_day = begin_date_day
        self.end_date_year = end_date_year
        self.end_date_month = end_date_month
        self.end_date_day = end_date_day
        self.comment = comment
