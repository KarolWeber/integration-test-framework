from api.request_api import RequestApi
from faker import Faker
from urls.providers import ProviderOneUrls

fake = Faker("pl_PL")


class ProviderOneClient:
    @staticmethod
    def authenticate(context, payload):
        """
        Autentykuje sesję gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        :param payload: (dict) – dane wymagane do autentykacji.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderOneUrls.authenticate, context=context, payload=payload)

    @staticmethod
    def bet(context, payload):
        """
        Dokonuje zakładu.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do dokonania zakładu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderOneUrls.bet, context=context, payload=payload)

    @staticmethod
    def win(context, payload):
        """
        Zwraca wynik zakładu.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do zwrócenia wyniku zakładu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderOneUrls.win, context=context, payload=payload)

    @staticmethod
    def get_funds(context, payload):
        """
        Zwraca aktualne środki dostępne na grze.

        :param context: Obiekt zalogowanej sesji gry.
        :param payload: (dict) – dane wymagane do zwrócenia aktualnych środków.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=ProviderOneUrls.get_funds, context=context, payload=payload)
