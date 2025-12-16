from api.services.admin_service.context import AdminService
from utils.logging.logger import StepLogger


def remove_bonuses(context=None):
    """
    Usuwa bonusy utworzone prez testy automatyczne.
    :param context: Obiekt zalogowanego administratora.
    """
    admin = context if context is not None else AdminService()
    if not context:
        admin.user.login()
    bonuses = admin.marketing.bonuses.list()
    removed_bonuses = 0
    for bonus in bonuses:

        if "AUTOMAT" in bonus.name:
            resp = admin.technical.bonus.delete(bonus)
            StepLogger.log_step(f"REMOVE GAME:{bonus.name}: {resp if resp.status_code == 200 else resp.content}")
            removed_bonuses += 1

    StepLogger.log_step(f"CLEANUP COMPLETED REMOVE {removed_bonuses} BONUSES")
    return removed_bonuses


if __name__ == "__main__":
    remove_bonuses()
