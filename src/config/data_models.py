"""
Modelos de dados para representação de fontes e datasets.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .enums import OrgaoCategoria


@dataclass(frozen=True)
class DatasetsInfo:
    """Informações sobre um dataset específico."""
    slug: str
    urls: List[str]
    file_name: str
    description: Optional[str] = None
    
    def __post_init__(self):
        """Valida os dados após inicialização."""
        if not self.urls:
            raise ValueError(f"Dataset '{self.slug}' deve ter pelo menos uma URL")
        if not self.file_name:
            raise ValueError(f"Dataset '{self.slug}' deve ter um nome de arquivo")


@dataclass(frozen=True)
class DataSourceInfo:
    """Informações sobre uma fonte de dados (órgão)."""
    name: str
    datasets: List[DatasetsInfo]
    categoria: Optional[OrgaoCategoria] = None
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Valida os dados após inicialização."""
        if not self.datasets:
            raise ValueError(f"Fonte '{self.name}' deve ter pelo menos um dataset")
