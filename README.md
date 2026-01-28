# 🌍 Sistema de Download de Bases de Dados Ambientais

## 📖 Descrição

Sistema modular e extensível para automatizar o download, validação e processamento de bases de dados ambientais de diferentes órgãos brasileiros. Suporta múltiplas categorias: **Embargos**, **Desmatamento (DETER)** e **Alertas**.

## ✨ Funcionalidades

### Core
- 🔗 **Validação de Links**: Verifica disponibilidade com fallback automático
- 📥 **Download Inteligente**: Barra de progresso e retry automático
- 📁 **Verificação de Shapefile**: Confirma arquivos geoespaciais válidos
- 🔒 **Comparação de Hash**: Detecta mudanças entre versões
- 📊 **Relatórios Detalhados**: Estatísticas completas de processamento
- 🗄️ **Banco de Dados SQLite**: Histórico completo (opcional)
- 📝 **Logging Rico**: Saída colorida com Rich Handler

### Arquitetura
- 🏗️ **Modular**: Estrutura organizada seguindo Clean Code
- 🔧 **Extensível**: Fácil adição de novas fontes
- ✅ **Validação Automática**: Type hints e validação de dados
- 🎨 **Factory Pattern**: Criação simplificada de configurações
- 📦 **Separação de Responsabilidades**: Cada módulo com função específica

## 🗂️ Categorias de Dados

### 🚫 Embargos Ambientais
- **IBAMA** - Instituto Brasileiro do Meio Ambiente
- **ICMBio** - Instituto Chico Mendes de Conservação da Biodiversidade
- **SEMA-MT** - Secretaria de Estado de Meio Ambiente de Mato Grosso
- **SIGA-MT** - Sistema Integrado de Gestão Ambiental de MT
- **SIMGEO** - Sistema de Informações Geográficas
- **LDI** - Lista de Desflorestamento e Infratores (PA)

### ⚠️ Desmatamento (DETER)
- **DETER Amazônia** - Detecção de Desmatamento em Tempo Real
- **DETER Cerrado** - Monitoramento do bioma Cerrado
- **DETER Pantanal** - Monitoramento do bioma Pantanal

### 🔔 Alertas
- **Sistema de Alertas** - Dashboard de alertas de desmatamento

## 🚀 Como Usar

### Instalação

```bash
# Clone o repositório
cd DownloadBasesEmbagosAmbientais

# Instalar dependências
pip install -r requirements.txt
```

### Interface CLI (Recomendado)

```bash
# Menu interativo com questionary
python main.py
```

#### Opções do Menu:
- **Embargos** - Processa todas as fontes de embargos
- **Deters** - Processa dados de desmatamento DETER
- **Alertas** - Processa sistema de alertas
- **Selecionar Base Específica** - Escolhe categoria e órgão individual
- **Sair** - Encerra o sistema

### Uso Programático

#### Processamento Completo
```python
import asyncio
from src.processors.Processor import Processor
from src.config.bases_infos import DATA_SOURCES_EMBARGOS

async def main():
    # Processar todos os embargos com tracking
    processor = Processor(
        process_name='Embargos',
        data_sources=DATA_SOURCES_EMBARGOS,
        track_changes=True
    )
    results = await processor.run()
    
asyncio.run(main())
```

#### Processar Órgão Específico
```python
from src.config.bases_infos import get_source_by_orgao
from src.config.enums import Orgao

# Obter apenas IBAMA
ibama_source = get_source_by_orgao(Orgao.IBAMA)
single_source = {Orgao.IBAMA: ibama_source}

processor = Processor(
    process_name='Embargos',
    data_sources=single_source,
    track_changes=True
)
results = await processor.run()
```

#### Filtrar por Categoria
```python
from src.config.bases_infos import get_sources_by_categoria
from src.config.enums import OrgaoCategoria

# Obter apenas fontes de Desmatamento
deter_sources = get_sources_by_categoria(OrgaoCategoria.DESMATAMENTO)

processor = Processor(
    process_name='Deter',
    data_sources=deter_sources,
    track_changes=False
)
```

#### Validação de Links
```python
# Validar sem fazer download
processor = Processor('Embargos', DATA_SOURCES_EMBARGOS)
valid_links = await processor.validate_links()
```

## 📁 Estrutura do Projeto

```
DownloadBasesEmbagosAmbientais/
├── main.py                       # Entrada principal do sistema
├── cli.py                        # Interface CLI com questionary
├── examples.py                   # Exemplos de uso
├── project_routes.py             # Gerenciamento de caminhos
├── requirements.txt              # Dependências
├── src/
│   ├── config/
│   │   ├── enums.py             # 🆕 Enumerações (Orgao, Categoria)
│   │   ├── data_models.py       # 🆕 Dataclasses (estruturas)
│   │   ├── factories.py         # 🆕 Factory functions
│   │   ├── bases_infos.py       # 🔄 Agregador + utilitários
│   │   ├── logger_config.py     # Configuração de logs
│   │   ├── example_usage.py     # 🆕 Exemplos de uso
│   │   └── data_sources/        # 🆕 Fontes por categoria
│   │       ├── README.md        # Documentação
│   │       ├── alertas.py       # Definições de alertas
│   │       ├── deter.py         # Definições DETER
│   │       └── embargos.py      # Definições embargos
│   ├── core/
│   │   ├── downloader.py        # Download com progress bar
│   │   └── Validations.py       # Validações e hash
│   ├── processors/
│   │   ├── Processor.py         # 🔄 Processor genérico
│   │   └── Embargos.py          # Processor especializado
│   └── utils/
│       ├── check_link.py        # Verificação de links
│       ├── compression_detector.py
│       └── templates.py
├── logs/                        # Arquivos de log
└── *_database.db               # Bancos SQLite (se track_changes=True)
```

### 🆕 Novidades na Estrutura

- **Modularização**: Configurações separadas por responsabilidade
- **data_sources/**: Cada categoria em arquivo próprio
- **Factories**: Criação simplificada de configurações
- **Enums**: Tipagem forte para órgãos e categorias
- **Utilitários**: Funções helpers para acesso aos dados

## 🔧 Configuração e Extensão

### Como Adicionar Nova Fonte de Dados

#### 1. Adicionar Órgão no Enum
```python
# Em src/config/enums.py
class Orgao(Enum):
    # ... órgãos existentes
    NOVO_ORGAO = "NOVO_ORGAO"
```

#### 2. Criar Definição
```python
# Em src/config/data_sources/embargos.py (ou arquivo apropriado)
from ..enums import Orgao, OrgaoCategoria
from ..factories import create_dataset, create_source

_NOVO_ORGAO_SOURCE = create_source(
    orgao=Orgao.NOVO_ORGAO,
    categoria=OrgaoCategoria.EMBARGOS,
    datasets=[
        create_dataset(
            slug="Nome do Dataset",
            urls=[
                "https://url-principal.com/dados.zip",
                "https://url-backup.com/dados.zip"  # fallback opcional
            ],
            file_name="SITE_dados.zip",
            description="Descrição do dataset"
        )
    ],
    # Metadados opcionais
    nivel="Federal",      # ou "Estadual"
    estado="SP",          # se estadual
    bioma="Amazônia",     # se aplicável
    observacao="Nota adicional"
)
```

#### 3. Registrar no Agregador
```python
# No mesmo arquivo
DATA_SOURCES_EMBARGOS: Dict[Orgao, DataSourceInfo] = {
    **_IBAMA_SOURCE,
    **_ICMBIO_SOURCE,
    **_NOVO_ORGAO_SOURCE,  # ← Adicionar aqui
    # ...
}
```

### Exemplo ComAvançados

### Executar Exemplos Integrados
```bash
# Ver todos os exemplos de uso da configuração
python -m src.config.example_usage
```

### Criar Subset Personalizado
```python
from src.config.bases_infos import ALL_DATA_SOURCES

# Filtrar apenas órgãos federais
orgaos_federais = {
    orgao: info 
    for orgao, info in ALL_DATA_SOURCES.items()
    if info.metadata.get('nivel') == 'Federal'
}

processor = Processor('Embargos', orgaos_federais, track_changes=True)
await processor.run()
```

### Processar por Estado
```python
# Filtrar apenas Mato Grosso
orgaos_mt = {
    orgao: info
    for orgao, info in ALL_DATA_SOURCES.items()
    if info.metadata.get('estado') == 'MT'
}
```

### Validar Configurações
```python
from src.config.bases_infos import get_dataset_count

# Ver estatísticas
stats = get_dataset_count()
for categoria, info in stats['by_category'].items():
    print(f"{categoria}: {info['sources']} fontes, {info['datasets']} datasets")
```

### Modo Debug/Desenvolvimento
```python
# Processar sem tracking (mais rápido)
processor = Processor(
    process_name='Embargos',
    data_sources=DATA_SOURCES_EMBARGOS,
    track_changes=False  # ← Sem banco de dados
mbargos_sema_sp_historico.zip",
            description="Histórico completo"
        )
    ],
    nivel="Estadual",
    estado="SP",
    frequencia_atualizacao="Mensal",
    contato="contato@ambiente.sp.gov.br"
)
```

### Funções Utilitárias Disponíveis

```python
from src.config.bases_infos import (
    get_source_by_orgao,
    get_sources_by_categoria,
    list_all_orgaos,
    get_dataset_count
)

# Buscar órgão específico
ibama = get_source_by_orgao(Orgao.IBAMA)

# Filtrar por categoria
embargos = get_sources_by_categoria(OrgaoCategoria.EMBARGOS)

# Listar todos
orgaos = list_all_orgaos()

# Estatísticas
stats = get_dataset_count()
print(f"Total: {stats['total_sources']} fontes, {stats['total_datasets']} datasets")
```

## 📊 Relatórios

O sistema gera relatórios detalhados mostrando:

- ✅ Downloads bem-sucedidos
- 📁 Validação de shapefiles
- 🔄 Arquivos que foram alterados
- 📈 Estatísticas gerais
- 🗄️ Histórico no banco de dados

### Estrutura de Commits
```bash
# Adicionar nova fonte
git commit -m "feat: adiciona fonte SEMA-SP em embargos"

# Corrigir bug
git commit -m "fix: corrige validação de URLs em DETER"

# Atualizar documentação
git commit -m "docs: atualiza README com novos exemplos"
```

### Testes
```bash
# Validar configurações
python -m src.config.example_usage

# Testar CLI
python main.py

# Executar processamento
python examples.py
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feat/nova-fonte`)
3. Siga os padrões de código existentes
4. Documente mudanças no README se necessário
5. Commit suas mudanças seguindo Conventional Commits
6. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno para automatização de processos ambientais.

---

## 🛠️ Desenvolvimento

Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno para automatização de processos ambientais.
