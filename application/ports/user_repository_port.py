from abc import ABC, abstractmethod
from typing import List
from domain.user_domain import User


class IUserRepository(ABC):
    """
    UserRepositoryが満たすべきインターフェース（契約）を定義するポート。
    Service層は具象クラスではなく、この抽象クラスに依存する。
    """

    @abstractmethod
    def get_users(self, limit: int = 100) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def add_user(self, user: User) -> User:
        raise NotImplementedError
