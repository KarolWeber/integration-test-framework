"""
Mappery stałych używane w systemie:
- GAME_TYPE_MAP: Mapowanie typów gier na nazwy i grupy raportowe.
- PROVIDER_ONE_STATUS_MAP: Mapowanie kodów statusów odpowiedzi dostawcy nr 1 na czytelne komunikaty.
- PROVIDER_TWO_STATUS_MAP: Mapowanie kodów statusów odpowiedzi dostawcy nr 2 na czytelne komunikaty.
- BONUS_TYPES_MAP: Mapowanie typu bonusu na parametry konfiguracyjne.
"""

# Mapowanie typów gier na nazwy i grupy raportowe
GAME_TYPE_MAP = {
    "CARD": {
        "name": "Cards game",
        "group": "group.card_games_no_poker"
    },
    "CYL": {
        "name": "Cylinder game",
        "group": "group.cylinder_games"
    },
    "DICE": {
        "name": "Dice game",
        "group": "group.dice_games"
    },
    "SLOTS": {
        "name": "Slots game",
        "group": "group.slot_games"
    }
}

# Mapowanie kodów statusów odpowiedzi dostawcy nr 1 na czytelne komunikaty
PROVIDER_ONE_STATUS_MAP = {
    0: "SUCCESS",
    1: "SESSION NOT FOUND",
    2: "SESSION EXPIRED",
    4: "LIMIT REACHED",
    5: "USER IS BLOCKED",
    8: "INSUFFICIENT FUNDS",
    500: "UNKNOWN ERROR",
    101: "GAME NOT VISIBLE"
}

# Mapowanie kodów statusów odpowiedzi dostawcy nr 2 na czytelne komunikaty
PROVIDER_TWO_STATUS_MAP = {
    1000: "Invalid request syntax or basic semantics",
    1001: "Invalid parameter",
    1002: "Invalid credentials",
    1003: "Invalid game",
    1004: "Invalid player",
    1005: "Invalid currency",
    1006: "Invalid session",
    1007: "Invalid token",
    1008: "Invalid round",
    1009: "Invalid bonus",
    1010: "IP not allowed",
    1100: "Could not start the game",
    1200: "Operator not available",
    1201: "Invalid operator configuration",
    1202: "Operator already exists",
    1203: "Provider not available",
    1204: "Invalid provider configuration",
    1205: "Provider already exist",
    2000: "Internal server error, please contact support",
    2001: "Invalid server configuration, please contact support",
    2002: "Connection error",
    2003: "Invalid operator response",
    2004: "Invalid provider:response",
    2005: "Invalid session state"
}

# Mapowanie typu bonusu na parametry konfiguracyjne
BONUS_TYPES_MAP = {
    "ReloadBonusAutoDeposit": {"bonusType": "RELOAD_BONUS",
                               "offeringMethod": "AUTO",
                               "claimContext": "DEPOSIT_CONTEXT"},
    "BonusMoneyAutoNoContext": {"bonusType": "BONUS_MONEY",
                                "offeringMethod": "AUTO",
                                "claimContext": "NO_CONTEXT"},
    "BonusMoneyAutoDeposit": {"bonusType": "BONUS_MONEY",
                              "offeringMethod": "AUTO",
                              "claimContext": "DEPOSIT_CONTEXT"},
    "BonusMoneyManualNoClaim": {"bonusType": "BONUS_MONEY",
                                "offeringMethod": "MANUAL",
                                "claimContext": "NO_CLAIM"},
    "BonusMoneyAutoNoClaim": {"bonusType": "BONUS_MONEY",
                              "offeringMethod": "AUTO",
                              "claimContext": "NO_CLAIM"},
    "FreeSpinAutosReloadProvider": {"bonusType": "FREE_SPINS",
                                    "offeringMethod": "AUTO",
                                    "claimContext": "DEPOSIT_CONTEXT",
                                    "freeSpinsMode": "PROVIDER_FREE_SPINS"},
    "FreeSpinsAutoReloadWallet": {"bonusType": "FREE_SPINS",
                                  "offeringMethod": "AUTO",
                                  "claimContext": "DEPOSIT_CONTEXT",
                                  "freeSpinsMode": "WALLET_FREE_SPINS"},
    "FreeSpinsManualNoClaimProvider": {"bonusType": "FREE_SPINS",
                                       "offeringMethod": "MANUAL",
                                       "claimContext": "NO_CLAIM",
                                       "freeSpinsMode": "PROVIDER_FREE_SPINS"},
    "FreeSpinsManualNoClaimWallet": {"bonusType": "FREE_SPINS",
                                     "offeringMethod": "MANUAL",
                                     "claimContext": "NO_CLAIM",
                                     "freeSpinsMode": "WALLET_FREE_SPINS"},
    "FreeSpinsAutoNoContextProvider": {"bonusType": "FREE_SPINS",
                                       "offeringMethod": "AUTO",
                                       "claimContext": "NO_CONTEXT",
                                       "freeSpinsMode": "PROVIDER_FREE_SPINS"},
    "FreeSpinsAutoNoContextWallet": {"bonusType": "FREE_SPINS",
                                     "offeringMethod": "AUTO",
                                     "claimContext": "NO_CONTEXT",
                                     "freeSpinsMode": "WALLET_FREE_SPINS"},
    "FreeSpinsAutoNoClaimProvider": {"bonusType": "FREE_SPINS",
                                     "offeringMethod": "AUTO",
                                     "claimContext": "NO_CLAIM",
                                     "freeSpinsMode": "PROVIDER_FREE_SPINS"},
    "FreeSpinsAutoNoClaimWallet": {"bonusType": "FREE_SPINS",
                                   "offeringMethod": "AUTO",
                                   "claimContext": "NO_CLAIM",
                                   "freeSpinsMode": "WALLET_FREE_SPINS"},
}
