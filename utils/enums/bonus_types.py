from enum import Enum

from utils.mappers.mappers import BONUS_TYPES_MAP


class BonusType(Enum):
    """
    Enum zwracający dostępne konfiguracje bonusów.
    Zawiera wymagane parametry używane przy tworzeniu bonusu:
        - bonusType,
        - offeringMethod,
        - claimContext,
        - freeSpinsMode.
    """
    reload_bonus_auto_deposit = BONUS_TYPES_MAP.get("ReloadBonusAutoDeposit")
    bonus_money_auto_no_context = BONUS_TYPES_MAP.get("BonusMoneyAutoNoContext")
    bonus_money_auto_deposit = BONUS_TYPES_MAP.get("BonusMoneyAutoDeposit")
    bonus_money_manual_no_claim = BONUS_TYPES_MAP.get("BonusMoneyManualNoClaim")
    bonus_money_auto_no_claim = BONUS_TYPES_MAP.get("BonusMoneyAutoNoClaim")
    free_spins_auto_reload_provider = BONUS_TYPES_MAP.get("FreeSpinAutosReloadProvider")
    free_spins_auto_reload_wallet = BONUS_TYPES_MAP.get("FreeSpinsAutoReloadWallet")
    free_spins_manualNoClaimProvider = BONUS_TYPES_MAP.get("FreeSpinsManualNoClaimProvider")
    free_spins_manualNoClaimWallet = BONUS_TYPES_MAP.get("FreeSpinsManualNoClaimWallet")
    free_spins_auto_no_context_provider = BONUS_TYPES_MAP.get("FreeSpinsAutoNoContextProvider")
    free_spins_auto_no_context_wallet = BONUS_TYPES_MAP.get("FreeSpinsAutoNoContextWallet")
    free_spins_auto_no_claim_provider = BONUS_TYPES_MAP.get("FreeSpinsAutoNoClaimProvider")
    free_spins_auto_no_claim_wallet = BONUS_TYPES_MAP.get("FreeSpinsAutoNoClaimWallet")
