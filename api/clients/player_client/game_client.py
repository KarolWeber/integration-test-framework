from api.request_api import RequestApi
from urls.player import PlayerUrls


class GameClient:
    @staticmethod
    def init_token(player, game, player_bonus=None):
        """
        Inicjalizuje sesję rozgrywki gracza.

        :param player: Obiekt kontekstu zalogowanego gracza.
        :param game: Obiekt gry.
        :param player_bonus: Opcjonalny Obiekt bonusu gracza.
        :return: Zwraca uuid token rozgrywki.
        """
        url = PlayerUrls.Games.init_token.format(
            platform="WEB",
            currency="PLN",
            username=player.email,
            slug=game.slug
        )
        if player_bonus:
            url += f'&bonusToPlay={player_bonus.claim_id}'
        return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=url, context=player)

    @staticmethod
    def demo(player, game):
        """
        Uruchomienie dema gry zalogowanego bądź niezalogowanego gracza.

        :param player: Obiekt kontekstu gracza.
        :param game: Obiekt gry.
        :return: Zwraca url rozgrywki.
        """
        url = (
            PlayerUrls.Games.demo_for_logged_player.format(slug=game.slug, lang="pl", platform="web") if player.token is not None
            else PlayerUrls.Games.demo_for_not_logged_player.format(
                slug=game.slug, lang="pl", platform="web"))
        return RequestApi.execute(method=RequestApi.HTTPMethod.GET, url=url, context=player if player else None)
