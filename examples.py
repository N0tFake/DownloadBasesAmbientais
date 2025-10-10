"""
Exemplos de uso do sistema de processamento de embargos.

Este arquivo mostra diferentes formas de usar o EmbargoProcessor.
"""

import asyncio
from embargo_processor import EmbargoProcessor


async def example_validate_links_only():
    """Exemplo: apenas validar links."""
    print("🔍 Validando apenas os links...")
    
    processor = EmbargoProcessor()
    results = await processor.validate_links()
    
    print(f"\n📊 Resultados da validação:")
    for link, is_valid in results.items():
        status = "✅ Válido" if is_valid else "❌ Inválido"
        print(f"  {link}: {status}")


async def example_download_specific_orgao():
    from src.config.bases_infos import EMBARGOS_DATA_SOURCES, Orgao
    
    print("📥 Fazendo download apenas do IBAMA...")
    
    processor = EmbargoProcessor()
    
    original_sources = EMBARGOS_DATA_SOURCES.copy()
    EMBARGOS_DATA_SOURCES.clear()
    EMBARGOS_DATA_SOURCES[Orgao.IBAMA] = original_sources[Orgao.IBAMA]
    
    try:
        results = await processor.download_all_embargos()
        report = processor.generate_report()
        processor.print_report(report)
    finally:
        EMBARGOS_DATA_SOURCES.clear()
        EMBARGOS_DATA_SOURCES.update(original_sources)


async def example_check_database():
    import sqlite3
    from pathlib import Path
    
    print("🗄️ Verificando dados no banco...")
    
    processor = EmbargoProcessor()
    
    conn = sqlite3.connect(processor.database_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM downloads')
    total = cursor.fetchone()[0]
    print(f"Total de downloads registrados: {total}")
    
    cursor.execute('''
        SELECT orgao, dataset_slug, download_date, hash_changed 
        FROM downloads 
        ORDER BY created_at DESC 
        LIMIT 5
    ''')
    
    recent = cursor.fetchall()
    print(f"\nÚltimos downloads:")
    for record in recent:
        changed = "🔄 Alterado" if record[3] else "➖ Inalterado"
        print(f"  {record[0]} | {record[1]} | {record[2]} | {changed}")
    
    conn.close()


def example_report_only():
    print("📊 Gerando relatório dos downloads de hoje...")
    
    processor = EmbargoProcessor()
    report = processor.generate_report()
    
    if report['summary']['total_downloads'] == 0:
        print("Nenhum download foi realizado hoje.")
    else:
        processor.print_report(report)


async def example_custom_workflow():
    print("⚙️ Executando workflow personalizado...")
    
    processor = EmbargoProcessor()
    
    print("1️⃣ Validando links...")
    links = await processor.validate_links()
    valid_count = sum(1 for v in links.values() if v)
    
    if valid_count == 0:
        print("❌ Nenhum link válido encontrado. Abortando.")
        return
    
    print(f"✅ {valid_count} links válidos encontrados.")
    
    print("2️⃣ Realizando downloads...")
    downloads = await processor.download_all_embargos()
    
    print("3️⃣ Analisando resultados...")

    total_success = 0
    shapefiles_valid = 0
    files_changed = 0
    
    for orgao, datasets in downloads.items():
        for dataset in datasets:
            if dataset['success']:
                total_success += 1
                for download in dataset['downloads']:
                    if download.get('is_shapefile'):
                        shapefiles_valid += 1
                    if download.get('hash_changed'):
                        files_changed += 1
    
    print(f"📈 Análise:")
    print(f"  • Downloads bem-sucedidos: {total_success}")
    print(f"  • Shapefiles válidos: {shapefiles_valid}")
    print(f"  • Arquivos com mudança: {files_changed}")
    
    # 4. Relatório final
    print("4️⃣ Relatório final...")
    report = processor.generate_report()
    processor.print_report(report)


async def main():
    print("🎯 Sistema de Processamento de Embargos - Exemplos")
    print("=" * 60)
    print("1. Processo completo (recomendado)")
    print("2. Apenas validar links")
    print("3. Download específico (IBAMA)")
    print("4. Verificar banco de dados")
    print("5. Apenas relatório")
    print("6. Workflow personalizado")
    print("0. Sair")
    
    try:
        choice = input("\nEscolha uma opção (0-6): ").strip()
        
        if choice == "1":
            processor = EmbargoProcessor()
            await processor.run_full_process()
        elif choice == "2":
            await example_validate_links_only()
        elif choice == "3":
            await example_download_specific_orgao()
        elif choice == "4":
            await example_check_database()
        elif choice == "5":
            example_report_only()
        elif choice == "6":
            await example_custom_workflow()
        elif choice == "0":
            print("👋 Saindo...")
            return
        else:
            print("❌ Opção inválida!")
            
    except KeyboardInterrupt:
        print("\n👋 Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())