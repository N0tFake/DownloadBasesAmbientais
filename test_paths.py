"""
Script para testar o novo caminho de download.
"""

import asyncio
from pathlib import Path
from src.processors.embargo_processor import EmbargoProcessor
from src.config.bases_infos import DATA_SOURCES_EMBARGOS, Orgao
import project_routes


def test_paths():
    print("🗂️ Testando caminhos de download...")
    print("=" * 60)
    
    routes = project_routes.Routes()
    
    base_path = project_routes.DOWNLOADS_ROOT
    print(f"📁 Caminho base: {base_path}")
    print(f"   Existe: {'✅' if base_path.exists() else '❌ (será criado)'}")
    
    print(f"\n📋 Caminhos para cada órgão:")
    
    for orgao, source in DATA_SOURCES_EMBARGOS.items():
        output_path = routes.get_output_path(source.name)
        
        print(f"   {source.name:<12} | {output_path}")
        
        if output_path.exists():
            print(f"                  | ✅ Diretório criado")
        else:
            print(f"                  | ❌ Erro ao criar diretório")
    
    print(f"\n🔍 Verificando estrutura de pastas:")
    if base_path.exists():
        for orgao_folder in base_path.iterdir():
            if orgao_folder.is_dir():
                print(f"   📂 {orgao_folder.name}")
                for year_folder in orgao_folder.iterdir():
                    if year_folder.is_dir():
                        print(f"      📅 {year_folder.name}")
                        months = list(year_folder.iterdir())[:3]
                        for month_folder in months:
                            if month_folder.is_dir():
                                print(f"         📆 {month_folder.name}")
                        if len(list(year_folder.iterdir())) > 3:
                            print(f"         ... (+{len(list(year_folder.iterdir())) - 3} meses)")


async def test_single_download():
    print(f"\n🚀 Testando download único...")
    
    try:
        processor = EmbargoProcessor()
        
        ibama_source = DATA_SOURCES_EMBARGOS[Orgao.IBAMA]
        
        print(f"📥 Testando download do {ibama_source.name}...")
        
        output_path = processor.routes.get_output_path(ibama_source.name)
        print(f"📁 Arquivo será salvo em: {output_path}")
        
        original_sources = DATA_SOURCES_EMBARGOS.copy()
        DATA_SOURCES_EMBARGOS.clear()
        DATA_SOURCES_EMBARGOS[Orgao.IBAMA] = original_sources[Orgao.IBAMA]
        
        try:
            results = await processor.download_all_embargos()
            
            ibama_results = results.get('IBAMA', [])
            if ibama_results and ibama_results[0]['success']:
                download_info = ibama_results[0]['downloads'][0]
                print(f"✅ Download realizado com sucesso!")
                print(f"📄 Arquivo salvo em: {download_info['path']}")
                print(f"📊 Tamanho: {download_info['file_size'] / (1024*1024):.1f} MB")
                print(f"🔒 Hash: {download_info['hash'][:16]}...")
                print(f"📁 É shapefile: {'✅' if download_info['is_shapefile'] else '❌'}")
            else:
                print("❌ Falha no download de teste")
                
        finally:
            DATA_SOURCES_EMBARGOS.clear()
            DATA_SOURCES_EMBARGOS.update(original_sources)
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")


def main():
    print("🧪 Teste do Sistema de Caminhos")
    print("=" * 40)
    print("1. Testar caminhos configurados")
    print("2. Testar download único (IBAMA)")
    print("3. Ambos")
    print("0. Sair")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        test_paths()
    elif choice == "2":
        asyncio.run(test_single_download())
    elif choice == "3":
        test_paths()
        asyncio.run(test_single_download())
    elif choice == "0":
        print("👋 Saindo...")
    else:
        print("❌ Opção inválida!")


if __name__ == "__main__":
    main()