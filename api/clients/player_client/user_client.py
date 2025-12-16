from api.request_api import RequestApi
from urls.player import PlayerUrls


class UserClient:
    @staticmethod
    def create(payload):
        """
        Techniczne stworzenie gracza.

        :param payload: (dict) – dane wymagane do stworzenia gracza.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=PlayerUrls.User.create, payload=payload)

    @staticmethod
    def login(payload):
        """
        Logowanie gracza.

        :param payload: (dict) – dane wymagane do zalogowania.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=PlayerUrls.User.login, payload=payload)

    @staticmethod
    def logout(context):
        """
        Wylogowanie gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=PlayerUrls.User.logout, context=context)
