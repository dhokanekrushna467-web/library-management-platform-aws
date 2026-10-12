class User:
    def __init__(self, user_id, name, email, role="Student"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.active = True

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "active": self.active
        }
