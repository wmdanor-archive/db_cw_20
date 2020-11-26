from models.to_string import to_str


class Composition:

    def __init__(self, composition_id, title, duration, path_to_file, times_listened, release_year=None,
                 release_month=None, release_day=None, lyrics=None):
        self.composition_id = composition_id
        self.title = title
        self.duration = duration
        self.path_to_file = path_to_file
        self.times_listened = times_listened
        self.release_year = release_year
        self.release_month = release_month
        self.release_day = release_day
        self.lyrics = lyrics

    def __str__(self):
        return 'composition_id: ' + to_str(self.composition_id) + ' | title: ' + self.title + ' | duration: ' + \
               to_str(self.duration) + ' | release_year: ' + to_str(self.release_year) + ' | release_month: ' + \
               to_str(self.release_month) + ' | release_day: ' + to_str(self.release_day) + ' | times listened: ' + \
               to_str(self.times_listened) + ' | path: ' + self.path_to_file + ' |\nlyrics: ' + to_str(self.lyrics)
