import asyncio
from src.processors.Embargos import EmbargoProcessor

async def main():
    print("🌍 Sistema de Download de Bases de Embargos Ambientais")
    print("=" * 60)
    
    try:
        processor = EmbargoProcessor()
        
        print("🚀 Iniciando processo completo...")
        results = await processor.run_full_process()
        
        print("✅ Processo finalizado com sucesso!")
        
        report = results.get('report', {})
        if report:
            summary = report.get('summary', {})
            print(f"\n📊 RESUMO FINAL:")
            print(f"   • Downloads realizados: {summary.get('total_downloads', 0)}")
            print(f"   • Shapefiles válidos: {summary.get('valid_shapefiles', 0)}")
            print(f"   • Arquivos alterados: {summary.get('changed_files', 0)}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")
        print("💡 Tente executar 'python examples.py' para mais opções.")


if __name__ == "__main__":
    asyncio.run(main())