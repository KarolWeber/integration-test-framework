from enum import Enum


class FreeSpinsMode(Enum):
    """
    Enum zwracający dostępny typ free spinów
    """
    wallet_free_spin = "WALLET_FREE_SPINS"
    provider_free_spin = "PROVIDER_FREE_SPINS"
