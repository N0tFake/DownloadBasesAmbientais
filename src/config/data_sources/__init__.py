"""
Módulo de definições de fontes de dados organizadas por categoria.
"""
from .alertas import DATA_SOURCES_ALERTAS
from .deter import DATA_SOURCES_DETER
from .embargos import DATA_SOURCES_EMBARGOS
from .terras_indigenas import DATA_SOURCES_TERRAS_INDIGENAS

__all__ = [
    'DATA_SOURCES_ALERTAS',
    'DATA_SOURCES_DETER', 
    'DATA_SOURCES_EMBARGOS',
    'DATA_SOURCES_TERRAS_INDIGENAS'
]
