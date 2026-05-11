"""
Definições de fontes de dados de ALERTAS.
"""
from typing import Dict
from ..enums import Orgao, OrgaoCategoria
from ..data_models import DataSourceInfo
from ..factories import create_dataset, create_source


_ALERTAS_SOURCE = create_source(
    orgao=Orgao.ALERTAS,
    categoria=OrgaoCategoria.ALERTAS,
    datasets=[
        create_dataset(
            slug="Alertas",
            urls=["https://storage.googleapis.com/alerta-public/dashboard/downloads/dashboard_alerts-shapefile.zip"],
            file_name="SITE_Alertas.zip",
            description="Dashboard de alertas de desmatamento"
        )
    ]
)


DATA_SOURCES_ALERTAS: Dict[Orgao, DataSourceInfo] = {
    **_ALERTAS_SOURCE
}
