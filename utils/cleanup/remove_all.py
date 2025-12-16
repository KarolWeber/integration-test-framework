from api.services.admin_service.context import AdminService
from utils.cleanup.remove_bonuses import remove_bonuses
from utils.cleanup.remove_cutom_games import remove_custom_games
from utils.cleanup.remove_free_spins_templates import \
    remove_free_spin_templates


def remove_all():
    """
    Usuwa elementy utworzone przez testy automatyczne:
    Bonusy, Gry, Szablony free spin.
    """
    admin = AdminService()
    admin.user.login()
    remove_bonuses(admin)
    remove_custom_games(admin)
    remove_free_spin_templates(admin)
    print('CLEANUP COMPLETED')


remove_all()
