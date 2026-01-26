from enum import Enum
from dataclasses import dataclass

class Orgao(Enum):
    IBAMA = "IBAMA"
    ICMBIO = "ICMbio"
    SEMA_MT = "SEMA_MT"
    SIGA_MT = "SIGA_MT"
    SIMGEO = "SIMGEO"
    LDI = "LDI"
    DETER_AMZ = 'DETER_AMZ'
    DETER_CRRD = 'DETER_CRRD'
    DETER_PANTANAL = 'DETER_PANTANAL'

@dataclass(frozen=True)
class DataSourceInfo:
    name: str
    datasets: list

@dataclass(frozen=True)
class DatasetsInfo:
    slug: str
    urls: list
    file_name: str

DATA_SOURCES_DETER = {
  Orgao.DETER_AMZ: DataSourceInfo(
    name="DETER_AMZ",
    datasets=[
      DatasetsInfo(
        slug="Deter Bioma Amazônia",
        urls=[
          "https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-amz/shape"
        ],
        file_name="SITE_Deter_AMZ.zip"
      )
    ]
  ),
  
  Orgao.DETER_CRRD: DataSourceInfo(
    name="DETER_CRRD",
    datasets=[
      DatasetsInfo(
        slug="Deter Bioma Cerrado",
        urls=[
          "https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-cerrado-nb/shape"
        ],
        file_name="SITE_Deter_CRRD.zip"
      )
    ]
  ),
  
  Orgao.DETER_PANTANAL: DataSourceInfo(
    name="DETER_PANTANAL",
    datasets=[
      DatasetsInfo(
        slug="Deter Bioma Pantanal",
        urls=[
          "https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-pantanal/shape"
        ],
        file_name="SITE_Deter_Pantanal.zip"
      )
    ]
  )
}  

DATA_SOURCES_EMBARGOS = {
  Orgao.IBAMA: DataSourceInfo(
    name="IBAMA",
    datasets=[
      DatasetsInfo(
        slug="Embargos IBAMA",
        urls=[
          "https://pamgia.ibama.gov.br/geoservicos/arquivos/adm_embargo_ibama_a.shp.zip"
        ],
        file_name="SITE_embargos_ibama.zip"
      )
    ]
  ),
  
  Orgao.ICMBIO: DataSourceInfo(
    name="ICMbio",
    datasets=[
      DatasetsInfo(
        slug="Embargos ICMbio",
        urls=[
          "https://www.gov.br/icmbio/pt-br/assuntos/dados_geoespaciais/mapa-tematico-e-dados-geoestatisticos-das-unidades-de-conservacao-federais/embargos_icmbio_shp.zip",
          "https://www.gov.br/icmbio/pt-br/assuntos/dados_geoespaciais/mapa-tematico-e-dados-geoestatisticos-das-unidades-de-conservacao-federais/embargos_icmbio.zip"
        ],
        file_name="SITE_embargos_icmbio.zip"
      )
    ]
  ),
  
  Orgao.SEMA_MT: DataSourceInfo(
    name="SEMA_MT",
    datasets=[
      DatasetsInfo(
        slug="Embargos SEMA MT",
        urls=[
          "https://geo.sema.mt.gov.br/geoserver/wfs?authkey=541085de-9a2e-454e-bdba-eb3d57a2f492&request=getfeature&service=wfs&version=1.0.0&typename=Geoportal:AREAS_EMBARGADAS_SEMA&outputformat=SHAPE-ZIP"
        ],
        file_name="SITE_embargos_sema_mt.zip"
      )
    ]
  ),
  
  Orgao.SIGA_MT: DataSourceInfo(
    name = "SIGA_MT",
    datasets = [
      DatasetsInfo(
        slug="Embargos SIGA MT Polígono",
        urls=[
          "https://geo.sema.mt.gov.br/geoserver/wfs?authkey=541085de-9a2e-454e-bdba-eb3d57a2f492&request=getfeature&service=wfs&version=1.0.0&typename=Geoportal:AREA_EMBARGADA_SIGA_POLIGONO&outputformat=SHAPE-ZIP"
        ],
        file_name="SITE_embargos_siga_poligono_mt.zip"
      ),
      DatasetsInfo(
        slug="Embargos SIGA MT Ponto",
        urls=[
          "https://geo.sema.mt.gov.br/geoserver/wfs?authkey=541085de-9a2e-454e-bdba-eb3d57a2f492&request=getfeature&service=wfs&version=1.0.0&typename=Geoportal:AREA_EMBARGADA_SIGA_PONTO&outputformat=SHAPE-ZIP"
        ],
        file_name="SITE_embargos_siga_ponto_mt.zip"
      )
    ],
  ),

  Orgao.SIMGEO: DataSourceInfo(
    name = "SIMGEO",
    datasets = [
      DatasetsInfo(
        slug="Embargos SIMGEO",
        urls=[
          "http://www.sema.mt.gov.br/transparencia/index.php/documentos/25/Dados-de-Desmatamento/2813/Base-de-Desmatamento-de-2018.zip"
        ],
        file_name="SITE_embargos_simgeo_mt.zip"
      )
    ],
  ),
  
  Orgao.LDI:  DataSourceInfo(
    name = "LDI",
    datasets = [  
      DatasetsInfo(
        slug="Embargos LDI manual",
        urls=[
          "https://monitoramento.semas.pa.gov.br/ldi/regioesdesmatamento/baixartodosshapefile?tipoShape=MANUAL"
        ],
        file_name="SITE_embargos_LDI_manual.zip"
      ),
      DatasetsInfo(
        slug="Embargos LDI automatizado",
        urls=[
          "https://monitoramento.semas.pa.gov.br/ldi/regioesdesmatamento/baixartodosshapefile?tipoShape=AUTOMATIZADO"
        ],
        file_name="SITE_embargos_LDI_automatico.zip"
      ),
      DatasetsInfo(
        slug="Embargos LDI sem sobreposição",
        urls=[
          "https://monitoramento.semas.pa.gov.br/ldi/regioesdesmatamento/baixartodosshapefile?tipoShape=SEMSOBREPOSICAO"
        ],
        file_name="SITE_embargos_LDI_sem_sobreposicao.zip"
      )
    ] 
  ),
}
