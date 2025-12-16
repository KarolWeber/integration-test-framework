import allure
from api.clients.admin_client.user_client import UserClient
from utils.logging.logger import StepLogger


class UserService:
    def __init__(self, context):
        self._context = context

    @allure.step("Admin login")
    def login(self, step=True):
        """
        Logowanie administratora.

        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca i aktualizuje token autoryzacyjny obiektu administratora.
        """
        resp = UserClient.login(self._context.credentials)
        if step:
            StepLogger.log_step(f"ADMIN LOGIN: {self._context.credentials['login']}", response=resp)
        token = resp.json()['authToken'] if resp.status_code == 200 else resp
        self._context.token = token
        return token

    @allure.step("Admin logout")
    def logout(self, step=True):
        """
        Wylogowuje administratora.

        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Przy sukcesie usuwa token autoryzacyjny z obiektu administratora.
        """
        resp = UserClient.logout(self._context)
        if step:
            StepLogger.log_step("ADMIN LOGOUT", response=resp)
        if resp.status_code == 200:
            self._context.token = None
        return resp
