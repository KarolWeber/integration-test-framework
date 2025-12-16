from api.request_api import RequestApi
from urls.player import PlayerUrls


class BonusClient:
    @staticmethod
    def available_bonuses(context):
        """
        Zwraca listę dostępnych bonusów.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=PlayerUrls.Bonus.available_bonuses, context=context)

    @staticmethod
    def current_bonuses(context):
        """
        Zwraca listę aktywnych bonusów.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=PlayerUrls.Bonus.current_bonuses, context=context)

    @staticmethod
    def accept(context, payload):
        """
        Akceptacja warunków wybranego bonusu.

        :param context: Obiekt kontekstu zalogowanego gracza.
        :param payload: (dict) – dane wymagane do zaakceptowania bonusu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=PlayerUrls.Bonus.accept, context=context, payload=payload)

    @staticmethod
    def claim(context, payload):
        """
        Przyjęcie wybranego bonusu.

        :param context: Obiekt kontekstu zalogowanego gracza.
        :param payload: (dict) – dane wymagane do przyjęcia bonusu.
        """
        return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=PlayerUrls.Bonus.claim, context=context, payload=payload)
