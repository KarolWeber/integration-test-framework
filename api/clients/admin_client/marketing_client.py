from api.request_api import RequestApi
from urls.admin import AdminUrls


class MarketingClient:
    class FreeSpinTemplates:
        @staticmethod
        def set_enabled(context, payload):
            """
            Włącza lub wyłącza szablon free spin.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do zmiany stanu szablonu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.FreeSpinTemplates.enable, context=context,
                                      payload=payload)

        @staticmethod
        def edit_games(context, payload):
            """
            Edytuje gry szablonu free spin.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do edycji gier.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.FreeSpinTemplates.edit_games, context=context,
                                      payload=payload)

        @staticmethod
        def get(context, template_id):
            """
            Zwraca szablon free spin po uuid.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param template_id: (uuid) Identyfikator szablonu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET,
                                      url=AdminUrls.Marketing.FreeSpinTemplates.get.format(template_id=template_id),
                                      context=context)

        @staticmethod
        def create(context, payload):
            """
            Tworzy szablon free spin.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do stworzenia szablonu.
            :return: uuid utworzonego szablonu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.FreeSpinTemplates.create, context=context,
                                      payload=payload)

        @staticmethod
        def list(context):
            """
            Zwraca listę szablonów free spin.

            :param context: Obiekt kontekstu zalogowanego administratora.
            """
            payload = {'queryParams': {}}
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.FreeSpinTemplates.list, context=context,
                                      payload=payload)

        @staticmethod
        def delete(context, payload):
            """
            Usuwa szablon free spin.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do usunięcia szablonu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.FreeSpinTemplates.delete, context=context,
                                      payload=payload)

    class Bonuses:
        @staticmethod
        def create(context, payload, file):
            """
            Tworzy bonus.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do usunięcia szablonu.
            :param file: plik graficzny w formacie bytes.
            :return: uuid utworzonego bonusu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.Bonuses.create, context=context,
                                      payload=payload, files=file)

        @staticmethod
        def get(context, bonus_definition_id):
            """
            Zwraca bonus po podanym uuid.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param bonus_definition_id: (uuid) Identyfikator bonusu.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET,
                                      url=AdminUrls.Marketing.Bonuses.get.format(bonus_definition_id=bonus_definition_id),
                                      context=context)

        @staticmethod
        def list(context):
            """
            Zwraca listę bonusów.

            :param context: Obiekt kontekstu zalogowanego administratora.
            """
            payload = {'queryParams': {"limit": 500}}
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Marketing.Bonuses.get_list, context=context,
                                      payload=payload)
