"""
Configuração centralizada de fontes de dados ambientais.

Este módulo agrega todas as fontes de dados e fornece utilitários para acesso.

Estrutura:
- enums.py: Enumerações (Orgao, OrgaoCategoria)
- data_models.py: Dataclasses (DatasetsInfo, DataSourceInfo)
- factories.py: Factory functions (create_dataset, create_source)
- data_sources/: Definições por categoria
  - alertas.py
  - deter.py
  - embargos.py

Para adicionar uma nova fonte de dados:
1. Adicione o órgão em enums.Orgao
2. Adicione a definição no arquivo apropriado em data_sources/
3. Use create_source() e create_dataset() para criar a estrutura
"""

from typing import Dict, List, Optional
from .enums import Orgao, OrgaoCategoria
from .data_models import DataSourceInfo
from .data_sources import (
    DATA_SOURCES_ALERTAS,
    DATA_SOURCES_DETER,
    DATA_SOURCES_EMBARGOS
)


# ============================================================================
# AGREGADORES E REGISTROS
# ============================================================================

# Lista de todos os grupos
LIST_DATA_SOURCES = [
    DATA_SOURCES_ALERTAS,
    DATA_SOURCES_DETER,
    DATA_SOURCES_EMBARGOS
]

# Dicionário completo unificado
ALL_DATA_SOURCES: Dict[Orgao, DataSourceInfo] = {
    **DATA_SOURCES_ALERTAS,
    **DATA_SOURCES_DETER,
    **DATA_SOURCES_EMBARGOS
}


# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def get_source_by_orgao(orgao: Orgao) -> Optional[DataSourceInfo]:
    """
    Obtém informações de uma fonte de dados por órgão.
    
    Args:
        orgao: Enum do órgão desejado
        
    Returns:
        DataSourceInfo ou None se não encontrado
    """
    return ALL_DATA_SOURCES.get(orgao)


def get_sources_by_categoria(categoria: OrgaoCategoria) -> Dict[Orgao, DataSourceInfo]:
    """
    Obtém todas as fontes de uma categoria específica.
    
    Args:
        categoria: Categoria desejada (EMBARGOS, DESMATAMENTO, ALERTAS)
        
    Returns:
        Dicionário {Orgao: DataSourceInfo} filtrado
    """
    return {
        orgao: source 
        for orgao, source in ALL_DATA_SOURCES.items() 
        if source.categoria == categoria
    }


def list_all_orgaos() -> List[str]:
    """
    Lista todos os órgãos disponíveis.
    
    Returns:
        Lista com nomes dos órgãos
    """
    return [orgao.value for orgao in Orgao]


def get_dataset_count() -> Dict[str, int]:
    """
    Retorna estatísticas sobre os datasets.
    
    Returns:
        Dict com contagens totais e por categoria
    """
    stats = {
        "total_sources": len(ALL_DATA_SOURCES),
        "total_datasets": sum(len(source.datasets) for source in ALL_DATA_SOURCES.values()),
        "by_category": {}
    }
    
    for categoria in OrgaoCategoria:
        sources = get_sources_by_categoria(categoria)
        stats["by_category"][categoria.value] = {
            "sources": len(sources),
            "datasets": sum(len(s.datasets) for s in sources.values())
        }
    
    return stats


# ============================================================================
# EXPORTS PARA COMPATIBILIDADE
# ============================================================================

# Mantém compatibilidade com código antigo
DATA_SOURCE_ALERTAS = DATA_SOURCES_ALERTAS

__all__ = [
    # Dicionários de dados
    'DATA_SOURCES_ALERTAS',
    'DATA_SOURCES_DETER',
    'DATA_SOURCES_EMBARGOS',
    'DATA_SOURCE_ALERTAS',  # Compatibilidade
    'ALL_DATA_SOURCES',
    'LIST_DATA_SOURCES',
    
    # Funções utilitárias
    'get_source_by_orgao',
    'get_sources_by_categoria',
    'list_all_orgaos',
    'get_dataset_count'
]
