"""
MagicAffinity schema
"""
from enum import Enum


class MagicAffinity(str, Enum):
    """
    MagicAffinity class that inherits from built-in Enum
    """
    DARKNESS: str = 'Oscuridad'
    LIGHT: str = 'Luz'
    FIRE: str = 'Fuego'
    WATER: str = 'Agua'
    WIND: str = 'Viento'
    EARTH: str = 'Tierra'
