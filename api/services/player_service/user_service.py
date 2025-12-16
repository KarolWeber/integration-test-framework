from time import sleep

import allure
from api.clients.player_client.user_client import UserClient
from utils.data_generators.player_generators import player_full_data
from utils.logging.logger import StepLogger


class UserService:
    """
    Serwis do obsługi konta gracza przez gracza.
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        self._context = context

    @allure.step("Create player")
    def create(self, username, password, identity_verified, iban_verified, max_retries):
        """
        Tworzy konto gracza (uwaga, nie jest to rejestracja za pośrednictwem formularza).

        :param username: (str, opcjonalny) Nazwa konta gracza.
        :param password: (str, opcjonalny) Hasło do konta gracza.
        :param identity_verified: (bool) Flaga określająca czy tożsamość gracza została potwierdzona.
        :param iban_verified:(bool) (bool) Flaga określająca czy numer konta bonkowego został potwierdzony.
        :param max_retries: (int) Ilość ponowień rejestracji z nowymi danymi w przypadku kiedy wygenerowane dane już są w systemie.
        :return: Aktualizuje obiekt gracza po udanym utworzeniu.
        """
        attempt = 0
        final_resp = None
        player_data = None
        while attempt < max_retries:
            attempt += 1
            player_data = player_full_data(username=username,
                                           password=password,
                                           identity_verified=identity_verified,
                                           iban_verified=iban_verified)
            self._context.email = player_data['account']['email']
            self._context.password = player_data['account']['password']

            resp = UserClient.create(player_data)
            final_resp = resp
            if resp.status_code == 200:
                self._context.id = resp.json()['playerId']
                self._context.iban_id = resp.json()['ibanId']
                self._context.wallet_id = resp.json()['walletId']
                break
        StepLogger.log_step(f"PLAYER CREATE: {self._context.email}", payload=player_data, response=final_resp)
        if final_resp.status_code != 200:
            raise RuntimeError(f"Failed to create player after {max_retries} attempts")
        return final_resp

    @allure.step("Player login")
    def login(self, retries=3):
        """
        Logowanie gracza.

        :param retries: (int) Ilość prób logowania w przypadku nieprawidłwych danych
            (jeśli skryp spróbuje zalogować gracza szybciej niż zaktualizuje się baza danych).
        :return: Zwraca i aktualizuje token autoryzacyjny obiektu gracza.
        """
        for attempt in range(1, retries + 1):
            resp = UserClient.login(self._context.credentials)
            if resp.status_code != 200:
                print(f"Login failed after {attempt} attempt(s): {resp.status_code}\n{self._context.credentials} {resp.content}")
                sleep(1)
                continue
            StepLogger.log_step(f"PLAYER LOGIN: {self._context.email}", payload=self._context.credentials, response=resp)
            token = resp.json()['authToken'] if resp.status_code == 200 else resp
            self._context.token = token
            return token

    def logout(self):
        """
        Wylogowuje gracza.

        :return: Przy sukcesie usuwa token autoryzacyjny z obiektu gracza.
        """
        resp = UserClient.logout(self._context)
        StepLogger.log_step(f"PLAYER LOGOUT: {self._context.email}", response=resp)
        if resp.status_code == 200:
            self._context.token = None
        return resp
