from domain.user_domain import User


def test_user_creation():
    user = User(id=1, name="John Doe", age=30)
    assert user.id == 1
    assert user.name == "John Doe"
    assert user.age == 30
    assert user.nickname is None


def test_user_creation_with_nickname():
    user = User(id=2, name="Jane Smith", age=25, nickname="Janey")
    assert user.id == 2
    assert user.name == "Jane Smith"
    assert user.age == 25
    assert user.nickname == "Janey"
