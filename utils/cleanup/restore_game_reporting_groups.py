from api.services.admin_service.context import AdminService


def restore_game_reporting_groups():
    """
    Ustawia wszystkim grom grupy raportowe w zależności od typu gry w danych dostawcy
    """
    admin = AdminService()
    admin.user.login()
    games = admin.casino.games.list()
    game_types = {"SLOTS": "group.slot_games",
                  "OTHER": "group.slot_games",
                  "ROULETTE": "group.cylinder_games",
                  "BLACKJACK": "group.card_games_no_poker",
                  "VIDEO_POKER": "group.card_games_no_poker",
                  "POKER": "group.card_games_no_poker",
                  }
    for game in games:
        game_type = game.provider_game_data.game_type
        if game.reporting_game_group != game_types.get(game_type):
            admin.casino.games.change_reporting_group(game, group_name=game_types.get(game_type))
