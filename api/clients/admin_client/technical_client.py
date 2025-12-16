from api.request_api import RequestApi
from urls.admin import AdminUrls


class TechnicalClient:
    class Game:
        @staticmethod
        def create_custom_game(context, payload):
            """
            Tworzy grę techniczną.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do utworzenia gry.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Technical.Game.create_custom_game, context=context,
                                      payload=payload)

        @staticmethod
        def delete_custom_game(context, payload):
            """
            Usuwa grę.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do usunięcia gry.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Technical.Game.delete_custom_game, context=context,
                                      payload=payload)

    class Bonus:
        @staticmethod
        def delete_bonus(context, payload):
            """
            Usuwa bonus.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do usunięcia bonusu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Technical.Bonus.delete, context=context,
                                      payload=payload)
