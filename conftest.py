import os

import pytest
from api.services.admin_service.context import AdminService
from api.services.player_service.context import PlayerService
from dotenv import dotenv_values
from utils.assertions.assertions import CheckAssertions
from utils.logging.logger import dump_log, clear_log, StepLogger


@pytest.fixture(autouse=True)
def store_request(request):
    """
    Przypisauje obiekt request do klasy testowej.
    """
    if hasattr(request, "cls") and request.cls is not None:
        request.cls.request = request
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook pytesta wywoływany po każdym teście.
    Jeśli test nie powiedzie się, zrzuca logi testu (dump_log).
    Po każdym teście czyści logi (clear_log).
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        dump_log()
    clear_log()


@pytest.fixture(scope="session", autouse=True)
def generate_allure_environment():
    env_path = os.path.join(os.getcwd(), ".env")
    allure_results = os.path.join(os.getcwd(), "allure-results")
    os.makedirs(allure_results, exist_ok=True)

    env_vars = dotenv_values(env_path)
    env_file = os.path.join(allure_results, "environment.properties")
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")


@pytest.fixture(autouse=True, scope='function')
def init_step_loger():
    return StepLogger()


@pytest.fixture(scope="function")
def check_assertions(request):
    return CheckAssertions(request=request)


@pytest.fixture(scope="module")
def admin():
    admin = AdminService()
    admin.user.login()
    return admin


@pytest.fixture(scope="function")
def custom_game(admin):
    game = admin.technical.game.create_custom_game()
    yield game
    admin.technical.game.remove_game(game=game, step=False)


@pytest.fixture(scope="function")
def player():
    player = PlayerService()
    player.user.login()
    return player
