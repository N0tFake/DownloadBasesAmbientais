import asyncio
from embargo_processor import EmbargoProcessor


async def test_system():
    print("🧪 Teste do Sistema de Embargos")
    print("-" * 40)
    
    try:
        processor = EmbargoProcessor()
        print("✅ Processador criado com sucesso")
        
        # Teste 1: Validar alguns links (apenas os primeiros)
        print("\n🔗 Testando validação de links...")
        links = await processor.validate_links()
        valid_count = sum(1 for v in links.values() if v)
        print(f"   Links válidos: {valid_count}/{len(links)}")
        
        # Teste 2: Verificar banco de dados
        print("\n🗄️ Testando banco de dados...")
        report = processor.generate_report()
        total_downloads = report['summary']['total_downloads']
        print(f"   Downloads registrados hoje: {total_downloads}")
        
        print("\n✅ Todos os testes passaram!")
        print("💡 Execute 'python main.py' para processo completo")
        print("💡 Execute 'python examples.py' para mais opções")
        
    except Exception as e:
        print(f"\n❌ Erro no teste: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_system())
    exit(0 if success else 1)