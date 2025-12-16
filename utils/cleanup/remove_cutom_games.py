from api.services.admin_service.context import AdminService
from utils.logging.logger import StepLogger


def remove_custom_games(context=None):
    """
    Usuwa gry utworzone prez testy automatyczne.
    :param context: Obiekt zalogowanego administratora.
    """
    admin = context if context is not None else AdminService()
    if not context:
        admin.user.login()
    games = admin.casino.games.list()
    removed_games = 0

    for game in games:
        if "AUTOMAT" in game.name:
            resp = admin.technical.game.remove_game(game, step=False)
            StepLogger.log_step(f"REMOVE GAME:{game.name}: {resp if resp.status_code == 200 else resp.content}")
            removed_games += 1

    StepLogger.log_step(f"CLEANUP COMPLETED REMOVE {removed_games} GAMES")
    return removed_games


if __name__ == "__main__":
    remove_custom_games()
