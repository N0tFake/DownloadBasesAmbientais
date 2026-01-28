"""
Definições de fontes de dados de EMBARGOS.
"""
from typing import Dict
from ..enums import Orgao, OrgaoCategoria
from ..data_models import DataSourceInfo
from ..factories import create_dataset, create_source


_IBAMA_SOURCE = create_source(
    orgao=Orgao.IBAMA,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Embargos IBAMA",
            urls=["https://pamgia.ibama.gov.br/geoservicos/arquivos/adm_embargo_ibama_a.shp.zip"],
            file_name="SITE_embargos_ibama.zip",
            description="Áreas embargadas pelo IBAMA"
        )
    ],
    nivel="Federal"
)

_ICMBIO_SOURCE = create_source(
    orgao=Orgao.ICMBIO,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Embargos ICMbio",
            urls=[
                "https://www.gov.br/icmbio/pt-br/assuntos/dados_geoespaciais/mapa-tematico-e-dados-geoestatisticos-das-unidades-de-conservacao-federais/embargos_icmbio_shp.zip",
                "https://www.gov.br/icmbio/pt-br/assuntos/dados_geoespaciais/mapa-tematico-e-dados-geoestatisticos-das-unidades-de-conservacao-federais/embargos_icmbio.zip"
            ],
            file_name="SITE_embargos_icmbio.zip",
            description="Áreas embargadas pelo ICMbio em Unidades de Conservação"
        )
    ],
    nivel="Federal"
)

_SEMA_MT_SOURCE = create_source(
    orgao=Orgao.SEMA_MT,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Embargos SEMA MT",
            urls=["https://geo.sema.mt.gov.br/geoserver/wfs?authkey=541085de-9a2e-454e-bdba-eb3d57a2f492&request=getfeature&service=wfs&version=1.0.0&typename=Geoportal:AREAS_EMBARGADAS_SEMA&outputformat=SHAPE-ZIP"],
            file_name="SITE_embargos_sema_mt.zip",
            description="Áreas embargadas pela SEMA Mato Grosso"
        )
    ],
    nivel="Estadual",
    estado="MT"
)

_SIGA_MT_SOURCE = create_source(
    orgao=Orgao.SIGA_MT,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Embargos SIGA MT Polígono",
            urls=["https://geo.sema.mt.gov.br/geoserver/wfs?authkey=541085de-9a2e-454e-bdba-eb3d57a2f492&request=getfeature&service=wfs&version=1.0.0&typename=Geoportal:AREA_EMBARGADA_SIGA_POLIGONO&outputformat=SHAPE-ZIP"],
            file_name="SITE_embargos_siga_poligono_mt.zip",
            description="Embargos SIGA MT - geometria de polígono"
        ),
        create_dataset(
            slug="Embargos SIGA MT Ponto",
            urls=["https://geo.sema.mt.gov.br/geoserver/wfs?authkey=541085de-9a2e-454e-bdba-eb3d57a2f492&request=getfeature&service=wfs&version=1.0.0&typename=Geoportal:AREA_EMBARGADA_SIGA_PONTO&outputformat=SHAPE-ZIP"],
            file_name="SITE_embargos_siga_ponto_mt.zip",
            description="Embargos SIGA MT - geometria de ponto"
        )
    ],
    nivel="Estadual",
    estado="MT"
)

_SIMGEO_SOURCE = create_source(
    orgao=Orgao.SIMGEO,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Embargos SIMGEO",
            urls=["http://www.sema.mt.gov.br/transparencia/index.php/documentos/25/Dados-de-Desmatamento/2813/Base-de-Desmatamento-de-2018.zip"],
            file_name="SITE_embargos_simgeo_mt.zip",
            description="Dados de desmatamento SIMGEO 2018"
        )
    ],
    nivel="Estadual",
    estado="MT",
    warning="URL pode estar desatualizada"
)

_LDI_SOURCE = create_source(
    orgao=Orgao.LDI,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Embargos LDI manual",
            urls=["https://monitoramento.semas.pa.gov.br/ldi/regioesdesmatamento/baixartodosshapefile?tipoShape=MANUAL"],
            file_name="SITE_embargos_LDI_manual.zip",
            description="Lista de Imóveis Embargados - validação manual"
        ),
        create_dataset(
            slug="Embargos LDI automatizado",
            urls=["https://monitoramento.semas.pa.gov.br/ldi/regioesdesmatamento/baixartodosshapefile?tipoShape=AUTOMATIZADO"],
            file_name="SITE_embargos_LDI_automatico.zip",
            description="Lista de Imóveis Embargados - processo automatizado"
        ),
        create_dataset(
            slug="Embargos LDI sem sobreposição",
            urls=["https://monitoramento.semas.pa.gov.br/ldi/regioesdesmatamento/baixartodosshapefile?tipoShape=SEMSOBREPOSICAO"],
            file_name="SITE_embargos_LDI_sem_sobreposicao.zip",
            description="Lista de Imóveis Embargados - sem sobreposição"
        )
    ],
    nivel="Estadual",
    estado="PA"
)


DATA_SOURCES_EMBARGOS: Dict[Orgao, DataSourceInfo] = {
    **_IBAMA_SOURCE,
    **_ICMBIO_SOURCE,
    **_SEMA_MT_SOURCE,
    **_SIGA_MT_SOURCE,
    **_SIMGEO_SOURCE,
    **_LDI_SOURCE
}
