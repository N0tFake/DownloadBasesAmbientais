"""
Definições de fontes de dados de ALERTAS.
"""
from typing import Dict
from ..enums import Orgao, OrgaoCategoria
from ..data_models import DataSourceInfo
from ..factories import create_dataset, create_source


_TERRAS_INDIGENAS_SOURCE = create_source(
    orgao=Orgao.TERRAS_INDIGENAS,
    categoria=OrgaoCategoria.TERRAS_INDIGENAS,
    datasets=[
        create_dataset(
            slug="Terras Indígenas",
            urls=["https://geoserver.funai.gov.br/geoserver/Funai/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Funai%3Atis_poligonais&maxFeatures=10000&outputFormat=SHAPE-ZIP"],
            file_name="SITE_TI.zip",
            description="Terras Indígenas: Dados Geoespaciais e Mapas"
        )
    ]
)


DATA_SOURCES_TERRAS_INDIGENAS: Dict[Orgao, DataSourceInfo] = {
    **_TERRAS_INDIGENAS_SOURCE
}
