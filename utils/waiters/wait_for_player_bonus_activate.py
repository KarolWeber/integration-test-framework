from time import sleep


def wait_for_bonus_activation(admin_context, player_context, bonus_object, status="ACTIVE", retries=10, interval=1):
    """
    Oczekuje na aktywację bonusu dla danego gracza.
    :param admin_context: Obiekt kontekstu zalogowanego administratora.
    :param player_context: Obiekt gracza.
    :param bonus_object: Obiekt bonusu, na który funkcja ma oczekiwać.
    :param status: (str) Oczekiwany status bonusu.
    :param retries: (int) Maksymalna liczba prób sprawdzenia statusu.
    :param interval: (float) Czas (w sekundach) oczekiwania pomiędzy kolejnymi próbami.
    """
    for _ in range(retries):
        player_bonus = admin_context.players.bonuses.current_bonuses(player=player_context, bonus=bonus_object, step=False)
        if player_bonus and player_bonus.bonus_definition_id == bonus_object.id and player_bonus.status == status:
            return player_bonus.status
        sleep(interval)
    return False
