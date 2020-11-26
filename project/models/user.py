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


