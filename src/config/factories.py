"""
Factory functions para criação simplificada de fontes de dados.
"""
from typing import List, Dict
from .data_models import DatasetsInfo, DataSourceInfo
from .enums import Orgao, OrgaoCategoria


def create_dataset(
    slug: str, 
    urls: List[str], 
    file_name: str, 
    description: str = None
) -> DatasetsInfo:
    """
    Factory para criar um dataset de forma mais limpa.
    
    Args:
        slug: Identificador do dataset
        urls: Lista de URLs para download (fallback)
        file_name: Nome do arquivo de saída
        description: Descrição opcional do dataset
        
    Returns:
        DatasetsInfo instanciado
    """
    return DatasetsInfo(
        slug=slug,
        urls=urls,
        file_name=file_name,
        description=description
    )


def create_source(
    orgao: Orgao, 
    datasets: List[DatasetsInfo], 
    categoria: OrgaoCategoria = None, 
    **metadata
) -> Dict[Orgao, DataSourceInfo]:
    """
    Factory para criar uma fonte de dados completa.
    
    Args:
        orgao: Enum do órgão
        datasets: Lista de datasets do órgão
        categoria: Categoria da fonte (Embargos, Desmatamento, etc)
        **metadata: Metadados adicionais (nível, estado, bioma, etc)
        
    Returns:
        Dicionário {Orgao: DataSourceInfo}
    """
    return {
        orgao: DataSourceInfo(
            name=orgao.value,
            datasets=datasets,
            categoria=categoria,
            metadata=metadata
        )
    }
