"""
Definições de fontes de dados de DETER (Desmatamento).
"""
from typing import Dict
from ..enums import Orgao, OrgaoCategoria
from ..data_models import DataSourceInfo
from ..factories import create_dataset, create_source


_DETER_AMZ_SOURCE = create_source(
    orgao=Orgao.DETER_AMZ,
    categoria=OrgaoCategoria.DESMATAMENTO,
    datasets=[
        create_dataset(
            slug="Deter Bioma Amazônia",
            urls=["https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-amz/shape"],
            file_name="SITE_Deter_AMZ.zip",
            description="Sistema de Detecção de Desmatamento em Tempo Real - Amazônia"
        )
    ],
    bioma="Amazônia"
)

_DETER_CERRADO_SOURCE = create_source(
    orgao=Orgao.DETER_CRRD,
    categoria=OrgaoCategoria.DESMATAMENTO,
    datasets=[
        create_dataset(
            slug="Deter Bioma Cerrado",
            urls=["https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-cerrado-nb/shape"],
            file_name="SITE_Deter_CRRD.zip",
            description="Sistema de Detecção de Desmatamento em Tempo Real - Cerrado"
        )
    ],
    bioma="Cerrado"
)

_DETER_PANTANAL_SOURCE = create_source(
    orgao=Orgao.DETER_PANTANAL,
    categoria=OrgaoCategoria.DESMATAMENTO,
    datasets=[
        create_dataset(
            slug="Deter Bioma Pantanal",
            urls=["https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-pantanal/shape"],
            file_name="SITE_Deter_Pantanal.zip",
            description="Sistema de Detecção de Desmatamento em Tempo Real - Pantanal"
        )
    ],
    bioma="Pantanal"
)


DATA_SOURCES_DETER: Dict[Orgao, DataSourceInfo] = {
    **_DETER_AMZ_SOURCE,
    **_DETER_CERRADO_SOURCE,
    **_DETER_PANTANAL_SOURCE
}