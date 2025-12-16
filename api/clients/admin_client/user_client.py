from api.request_api import RequestApi
from urls.admin import AdminUrls


class UserClient:
    @staticmethod
    def login(payload):
        """
        Logowanie administratora.

        :param payload: (dict) – dane wymagane do zalogowania.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.User.login, payload=payload)

    @staticmethod
    def logout(context):
        """
        Wylogowanie administratora.

        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.User.logout, context=context)
