import asyncio
import os
from dotenv import load_dotenv
from cli import main_menu

# Carrega variáveis de ambiente
load_dotenv()


async def main():
    # Verifica se está em modo teste
    modo_teste = os.getenv('TESTE', '').lower() == 'true'
    print(modo_teste)
    
    if modo_teste:
        print("\n" + "="*70)
        print("⚠️  ATENÇÃO: MODO DE TESTE ATIVADO".center(70))
        print("="*70)
        print("\n🔧 Os downloads serão salvos em:")
        print("   C:\\...\\Atualizações de Bases\\TESTE\\\n")
        print("📝 Para desativar, edite o arquivo .env e defina: TESTE=false\n")
        
        confirmacao = input("Digite 'SIM' para continuar em modo teste: ").strip().upper()
        
        if confirmacao != 'SIM':
            print("\n❌ Operação cancelada pelo usuário.")
            return
        
        print("\n✅ Prosseguindo em MODO TESTE...\n")
    
    try:
        processor = await main_menu()
        results = await processor.run()
        
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