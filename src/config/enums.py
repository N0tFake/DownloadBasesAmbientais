"""
Enumerações para classificação de fontes de dados ambientais.
"""
from enum import Enum


class Orgao(Enum):
    """Enumeração de todos os órgãos/fontes de dados disponíveis."""
    # Embargos
    IBAMA = "IBAMA"
    ICMBIO = "ICMbio"
    SEMA_MT = "SEMA_MT"
    SIGA_MT = "SIGA_MT"
    SIMGEO = "SIMGEO"
    LDI = "LDI"
    
    # Desmatamento
    DETER_AMZ = "DETER_AMZ"
    DETER_CRRD = "DETER_CRRD"
    DETER_PANTANAL = "DETER_PANTANAL"
    
    # Alertas
    ALERTAS = "Alertas"

    #TI
    TERRAS_INDIGENAS = "Terras Indigenas"

class OrgaoCategoria(Enum):
    """Categorias de dados ambientais."""
    EMBARGOS = "Embargos"
    DESMATAMENTO = "Deter"
    ALERTAS = "Alertas"
    TERRAS_INDIGENAS = "Terras Indígenas"
