# 🌍 Sistema de Download de Bases de Embargos Ambientais

## Descrição

Este projeto automatiza o download, validação e processamento de bases de dados de embargos ambientais de diferentes órgãos brasileiros.

## ✨ Funcionalidades

- 🔗 **Validação de Links**: Verifica se os links das bases estão funcionando
- 📥 **Download Automático**: Baixa as bases com barra de progresso
- 📁 **Verificação de Shapefile**: Confirma se os arquivos são shapefiles válidos
- 🔒 **Comparação de Hash**: Compara com downloads anteriores para detectar mudanças
- 📊 **Relatórios Detalhados**: Gera relatórios completos dos downloads
- 🗄️ **Banco de Dados**: Armazena histórico de downloads no SQLite
- 📝 **Logging Completo**: Registra todas as operações

## 🏢 Órgãos Suportados

- **IBAMA** - Embargos do Instituto Brasileiro do Meio Ambiente
- **ICMBio** - Embargos do Instituto Chico Mendes
- **SEMA-MT** - Secretaria de Estado de Meio Ambiente de MT
- **SIGA-MT** - Sistema Integrado de Gestão Ambiental de MT
- **SIMGEO** - Sistema de Informações Geográficas
- **LDI** - Lista de Desflorestamento e Infratores

## 🚀 Como Usar

### Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Uso Básico

```bash
# Processo completo (recomendado)
python main.py

# Exemplos e opções avançadas
python examples.py
```

### Uso Programático

```python
from embargo_processor import EmbargoProcessor

# Processo completo
processor = EmbargoProcessor()
results = await processor.run_full_process()

# Apenas validar links
links = await processor.validate_links()

# Apenas downloads
downloads = await processor.download_all_embargos()

# Gerar relatório
report = processor.generate_report()
processor.print_report(report)
```

## 📁 Estrutura do Projeto

```
DownloadBasesEmbagosAmbientais/
├── main.py                    # Entrada principal do sistema
├── embargo_processor.py       # Classe principal integrada
├── examples.py               # Exemplos de uso
├── requirements.txt          # Dependências
├── src/
│   ├── config/
│   │   ├── bases_infos.py    # Configuração das bases
│   │   └── logger_config.py  # Configuração de logs
│   ├── core/
│   │   ├── downloader.py     # Download com barra de progresso
│   │   └── Validations.py    # Validações e hash
│   └── utils/
│       ├── check_link.py     # Verificação de links
│       └── ...               # Outras utilitários
├── C:\Users\silvio.chaves\Desktop\MAIN\Atualizações de Bases\Embargos\  # Arquivos baixados
├── logs/                     # Arquivos de log
└── embargo_database.db       # Banco de dados SQLite
```

## 🔧 Configuração

As configurações das bases estão em `src/config/bases_infos.py`. Para adicionar novas bases:

```python
# Adicionar novo órgão
class Orgao(Enum):
    NOVO_ORGAO = "NOVO_ORGAO"

# Adicionar configuração
DATA_SOURCES_EMBARGOS[Orgao.NOVO_ORGAO] = DataSourceInfo(
    name="NOVO_ORGAO",
    datasets=[
        DatasetsInfo(
            slug="Nome do Dataset",
            urls=["http://exemplo.com/data.zip"],
            file_name="arquivo_destino.zip"
        )
    ]
)
```

## 📊 Relatórios

O sistema gera relatórios detalhados mostrando:

- ✅ Downloads bem-sucedidos
- 📁 Validação de shapefiles
- 🔄 Arquivos que foram alterados
- 📈 Estatísticas gerais
- 🗄️ Histórico no banco de dados

## 🗄️ Banco de Dados

O sistema usa SQLite para armazenar:

- Histórico de downloads
- Hashes dos arquivos
- Informações de validação
- Comparações entre versões

## 📝 Logs

Todos os logs são salvos em `logs/` com timestamps detalhados:

- Validação de links
- Processo de download
- Verificações de shapefile
- Comparações de hash
- Erros e exceções

## 🔍 Exemplos de Uso

### Validar apenas links
```python
processor = EmbargoProcessor()
results = await processor.validate_links()
```

### Download de órgão específico
```python
# Ver examples.py para exemplos completos
```

### Verificar banco de dados
```python
report = processor.generate_report()
processor.print_report(report)
```

## 🛠️ Desenvolvimento

Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno para automatização de processos ambientais.
