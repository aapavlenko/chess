import pytest
from Server import UserManager
from ServerLogic import Game

@pytest.fixture
def user_manager():
    return UserManager(
        users_passwords={"a": 123, "b": 123},
        active_users={"a": 1},
        current_games=[Game(player1=1)]
    )

def test_login_success(user_manager):
    result = user_manager.login("b", 123)

    assert result == 2
    assert user_manager.active_users == {"a": 1, "b": 2}
    assert user_manager.users_passwords == {"a": 123, "b": 123}
    assert len(user_manager.current_games) == 1
    assert user_manager.current_games[0].players[0] == 1  # изменено с player1

def test_login_wrong_password(user_manager):
    result = user_manager.login("b", 111)

    assert result == "Incorrect password"
    assert user_manager.active_users == {"a": 1}
    assert user_manager.users_passwords == {"a": 123, "b": 123}
    assert len(user_manager.current_games) == 1
    assert user_manager.current_games[0].players[0] == 1

def test_login_wrong_username(user_manager):
    result = user_manager.login("ddd", 123)

    assert result == "No such user found"
    assert user_manager.active_users == {"a": 1}
    assert user_manager.users_passwords == {"a": 123, "b": 123}
    assert len(user_manager.current_games) == 1
    assert user_manager.current_games[0].players[0] == 1

def test_register_success(user_manager):
    result = user_manager.register("c", 123)

    assert result == 2
    assert user_manager.active_users == {"a": 1, "c" : 2}
    assert user_manager.users_passwords == {"a": 123, "b": 123, "c" : 123}
    assert len(user_manager.current_games) == 1
    assert user_manager.current_games[0].players[0] == 1

def test_register_user_already_exists(user_manager):
    result = user_manager.register("a", 456)

    assert result == "This user already exists"
    assert user_manager.active_users == {"a": 1}
    assert user_manager.users_passwords == {"a": 123, "b": 123}
    assert len(user_manager.current_games) == 1
    assert user_manager.current_games[0].players[0] == 1

def test_add_active_user(user_manager):
    result = user_manager.add_active_user("c")

    assert result == 2
    assert user_manager.active_users == {"a": 1,"c":2}
    assert user_manager.users_passwords == {"a": 123, "b": 123}
    assert len(user_manager.current_games) == 1
    assert user_manager.current_games[0].players[0] == 1