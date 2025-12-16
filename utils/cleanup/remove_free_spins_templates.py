from api.services.admin_service.context import AdminService
from utils.logging.logger import StepLogger


def remove_free_spin_templates(context=None):
    """
    Usuwa szablony free spin utworzone prez testy automatyczne.
    :param context: Obiekt zalogowanego administratora.
    """
    admin = context if context is not None else AdminService()
    if not context:
        admin.user.login()
    templates = admin.marketing.free_spins_templates.list()
    removed_templates = 0
    for template in templates:

        if "AUTOMAT" in template.name:
            resp = admin.marketing.free_spins_templates.delete(template)
            StepLogger.log_step(f"REMOVE GAME:{template.name}: {resp if resp.status_code == 200 else resp.content}")
            removed_templates += 1

    StepLogger.log_step(f"CLEANUP COMPLETED REMOVE {removed_templates} TEMPLATES")
    return removed_templates


if __name__ == "__main__":
    remove_free_spin_templates()
