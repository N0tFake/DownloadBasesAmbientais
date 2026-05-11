"""
Exemplo de como usar o sistema de configuração de fontes de dados.

Execute: python -m src.config.example_usage
"""

from src.config.bases_infos import (
    get_source_by_orgao,
    get_sources_by_categoria,
    get_dataset_count,
    list_all_orgaos,
    ALL_DATA_SOURCES
)
from src.config.enums import Orgao, OrgaoCategoria


def example_1_listar_estatisticas():
    """Exemplo: Listar estatísticas dos datasets"""
    print("\n" + "="*70)
    print("📊 ESTATÍSTICAS DOS DATASETS")
    print("="*70)
    
    stats = get_dataset_count()
    print(f"\n✅ Total de fontes: {stats['total_sources']}")
    print(f"✅ Total de datasets: {stats['total_datasets']}")
    
    print("\n📋 Por Categoria:")
    for cat, info in stats['by_category'].items():
        print(f"   {cat}:")
        print(f"      • Fontes: {info['sources']}")
        print(f"      • Datasets: {info['datasets']}")


def example_2_acessar_orgao_especifico():
    """Exemplo: Acessar informações de um órgão específico"""
    print("\n" + "="*70)
    print("🗂️  ACESSAR ÓRGÃO ESPECÍFICO")
    print("="*70)
    
    ibama = get_source_by_orgao(Orgao.IBAMA)
    
    if ibama:
        print(f"\n✅ Órgão: {ibama.name}")
        print(f"✅ Categoria: {ibama.categoria.value if ibama.categoria else 'N/A'}")
        print(f"✅ Número de datasets: {len(ibama.datasets)}")
        print(f"✅ Metadados: {ibama.metadata}")
        
        print("\n📦 Datasets:")
        for ds in ibama.datasets:
            print(f"   • {ds.slug}")
            print(f"     Arquivo: {ds.file_name}")
            print(f"     URLs: {len(ds.urls)} disponível(eis)")
            if ds.description:
                print(f"     Descrição: {ds.description}")


def example_3_filtrar_por_categoria():
    """Exemplo: Filtrar fontes por categoria"""
    print("\n" + "="*70)
    print("🔍 FILTRAR POR CATEGORIA - EMBARGOS")
    print("="*70)
    
    embargos = get_sources_by_categoria(OrgaoCategoria.EMBARGOS)
    
    print(f"\n✅ Encontradas {len(embargos)} fontes de Embargos:\n")
    
    for orgao, info in embargos.items():
        nivel = info.metadata.get('nivel', 'N/A')
        estado = info.metadata.get('estado', '')
        
        print(f"   🗂️  {info.name}")
        print(f"      Nível: {nivel} {f'({estado})' if estado else ''}")
        print(f"      Datasets: {len(info.datasets)}")
        
        for ds in info.datasets:
            print(f"         • {ds.slug}")


def example_4_listar_todos_orgaos():
    """Exemplo: Listar todos os órgãos disponíveis"""
    print("\n" + "="*70)
    print("📋 TODOS OS ÓRGÃOS DISPONÍVEIS")
    print("="*70 + "\n")
    
    orgaos = list_all_orgaos()
    
    for i, orgao in enumerate(orgaos, 1):
        print(f"   {i:2d}. {orgao}")


def example_5_iterar_todas_fontes():
    """Exemplo: Iterar por todas as fontes"""
    print("\n" + "="*70)
    print("🔄 ITERANDO POR TODAS AS FONTES")
    print("="*70 + "\n")
    
    for orgao, info in ALL_DATA_SOURCES.items():
        total_urls = sum(len(ds.urls) for ds in info.datasets)
        
        print(f"   {info.name}:")
        print(f"      Categoria: {info.categoria.value if info.categoria else 'N/A'}")
        print(f"      Datasets: {len(info.datasets)}")
        print(f"      Total de URLs: {total_urls}")


def example_6_criar_subset_personalizado():
    """Exemplo: Criar subset personalizado de fontes"""
    print("\n" + "="*70)
    print("⚙️  CRIAR SUBSET PERSONALIZADO")
    print("="*70)
    
    # Criar um dicionário apenas com órgãos federais
    orgaos_federais = {
        orgao: info 
        for orgao, info in ALL_DATA_SOURCES.items()
        if info.metadata.get('nivel') == 'Federal'
    }
    
    print(f"\n✅ Encontrados {len(orgaos_federais)} órgãos federais:\n")
    
    for orgao, info in orgaos_federais.items():
        print(f"   • {info.name} - {len(info.datasets)} dataset(s)")


def example_7_validar_urls():
    """Exemplo: Validar estrutura de URLs"""
    print("\n" + "="*70)
    print("✅ VALIDAÇÃO DE URLs")
    print("="*70)
    
    print("\nÓrgãos com URLs de fallback:\n")
    
    for orgao, info in ALL_DATA_SOURCES.items():
        for ds in info.datasets:
            if len(ds.urls) > 1:
                print(f"   • {info.name} - {ds.slug}")
                print(f"     Principal: {ds.urls[0][:60]}...")
                print(f"     Fallbacks: {len(ds.urls) - 1}")


def main():
    """Executa todos os exemplos"""
    print("\n" + "="*70)
    print("🌿 EXEMPLOS DE USO - SISTEMA DE FONTES DE DADOS AMBIENTAIS")
    print("="*70)
    
    example_1_listar_estatisticas()
    example_2_acessar_orgao_especifico()
    example_3_filtrar_por_categoria()
    example_4_listar_todos_orgaos()
    example_5_iterar_todas_fontes()
    example_6_criar_subset_personalizado()
    example_7_validar_urls()
    
    print("\n" + "="*70)
    print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
