from infra.repository.user_repository import UserRepository


class UserService():
    def __init__(self):
        self.user_repository = UserRepository()

    def get_users(self):
        return self.user_repository.get_users()
        