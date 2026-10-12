import threading


class Database:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                instance.lock = threading.RLock()
                instance._seed_initial_data()
                cls._instance = instance
            return cls._instance

    def _seed_initial_data(self):
        self.users = {
            "U101": {
                "user_id": "U101",
                "name": "Alice Johnson",
                "email": "alice@university.edu",
                "role": "Student",
                "active": True,
                "active_loans": 0,
            },
            "U102": {
                "user_id": "U102",
                "name": "Dr. Robert Smith",
                "email": "robert.smith@university.edu",
                "role": "Faculty",
                "active": True,
                "active_loans": 0,
            },
        }

        self.books = {
            "B001": {
                "book_id": "B001",
                "title": "Cloud Native DevOps Architecture",
                "author": "Linus Torvalds",
                "isbn": "978-0134685991",
                "total_copies": 5,
                "available_copies": 5,
            },
            "B002": {
                "book_id": "B002",
                "title": "Continuous Delivery Principles",
                "author": "Jez Humble & David Farley",
                "isbn": "978-0321601919",
                "total_copies": 3,
                "available_copies": 3,
            },
        }

        self.loans = []
        self.loan_counter = 0

    def reset(self):
        with self.lock:
            self._seed_initial_data()


db = Database()
