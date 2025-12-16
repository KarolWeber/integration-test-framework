from urllib.parse import urlencode, urljoin

from api.request_api import RequestApi
from urls.admin import AdminUrls
from utils.logging.logger import StepLogger


class CasinoClient:
    class Providers:
        @staticmethod
        def sync_games(context, payload, provider_name):
            """
            Synchronizuje gry wybranego dostawcy.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) Dane wymagane do żądania synchronizacji.
            :param provider_name: (str) Nazwa dostawcy - używana w logach kroków testowych.
            """
            try:
                RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Casino.GameProvider.sync_games, context=context,
                                   payload=payload, timeout=1)
            except Exception:
                StepLogger.log_step(
                    f"ADMIN SYNC GAMES ON PROVIDER {provider_name}")
            return True

        @staticmethod
        def get(context):
            """
            Zwraca listę dostawców gier.

            :param context: Obiekt kontekstu zalogowanego administratora.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=AdminUrls.Casino.GameProvider.get, context=context)

    class Game:
        @staticmethod
        def list(context, provider, limit, visible, name, game_id, free_spins):
            """
            Zwraca listę gier.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param provider: Opcjonalny Obiekt dostawcy gry.
            :param limit: (int) Maksymalna ilość pobiranych pozycji.
            :param visible: (bool, opcjonalny) Filtr po widoczności gry.
            :param name: (str, opcjonalny) Filtr po nazwie gry.
            :param game_id: (uudi, opcjonalny) Filtr po identyfikatorze gry.
            :param free_spins: (bool, opcjonalny) Filtr po dostępnej rozgrywce free spin.
            """
            params = {
                "limit": limit,
            }
            if provider:
                params.update({
                    "filters[providerId][0][value]": provider.id,
                    "filters[providerId][0][operator]": "eq"
                })
            if visible:
                params.update({
                    "filters[visible][0][value]": visible,
                    "filters[visible][0][operator]": 'eq',
                })
            if name:
                params.update({
                    "filters[name][0][value]": name,
                    "filters[name][0][operator]": 'eq',
                })
            if game_id:
                params.update({
                    "filters[id][0][value]": game_id,
                    "filters[id][0][operator]": 'eq',
                })
            if free_spins:
                params.update({
                    "filters[enabledFreeSpins][0][value]": free_spins,
                    "filters[enabledFreeSpins][0][operator]": 'eq',
                })
            query = urlencode(params)
            url = urljoin(f'{AdminUrls.Casino.Game.list}', f'?{query}')
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=url, context=context)

        @staticmethod
        def change_reporting_group(context, payload):
            """
            Zmienia grupę raportową gry.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do zmiany grupy raportowej.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Casino.Game.change_reporting_group, context=context,
                                      payload=payload)

        @staticmethod
        def change_visibility(context, payload):
            """
            Zmienia widoczność gry.

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param payload: (dict) – dane wymagane do zmiany widoczności gry.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.POST, url=AdminUrls.Casino.Game.change_visibility, context=context,
                                      payload=payload)

    class ReportingGroups:
        @staticmethod
        def get(context):
            """
            Zwraca listę grup raportowych.

            :param context: Obiekt kontekstu zalogowanego administratora.
            """
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=AdminUrls.Casino.ReportingGroup.get, context=context)
