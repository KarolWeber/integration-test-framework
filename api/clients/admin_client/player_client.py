from urllib.parse import urlencode, urljoin
from api.request_api import RequestApi
from urls.admin import AdminUrls


class PlayersClient:
    class Bonuses:
        @staticmethod
        def bonuses(context, player):
            """
            Pobiera aktualne bonusy gracza

            :param context: Obiekt kontekstu zalogowanego administratora.
            :param player: Obiekt kontekstu gracza.
            """
            params = {
                'filters[playerId][0][value]': player.id,
                'filters[playerId][0][operator]': 'eq',
                'filters[walletId][1][value]': player.wallet_id,
                'filters[walletId][1][operator]': 'eq',
            }
            url = AdminUrls.Players.Bonuses.player_bonuses
            query_string = urlencode(params)
            url_with_params = f"{url}?{query_string}"
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=url_with_params, context=context)

    class Wallet:
        @staticmethod
        def activity(context, player, limit):
            """
            Pobiera logi aktywności portfela gracza
            :param context: Obiekt kontekstu zalogowanego administratora.
            :param player: Obiekt kontekstu gracza.
            :param limit: (int) Maksymalna ilość pobiranych pozycji.
            """
            params = {
                "limit": limit,
                "filters[playerId][0][value]": player.id,
                "filters[playerId][0][operator]": "in"
            }
            query = urlencode(params)
            url = urljoin(f'{AdminUrls.Players.Wallet.activity}', f'?{query}')
            return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=url, context=context)
