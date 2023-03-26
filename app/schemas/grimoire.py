"""
Grimoire schema
"""
from enum import Enum


class Grimoire(str, Enum):
    """
    Grimoire class that inherits from built-in Enum
    """
    SINCERITY: str = 'Sinceridad'
    HOPE: str = 'Esperanza'
    LOVE: str = 'Amor'
    GOOD_FORTUNE: str = 'Buena Fortuna'
    DESPERATION: str = 'Desesperación'
