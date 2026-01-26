import questionary
from questionary import Style
from src.config.bases_infos import DATA_SOURCES_EMBARGOS, DATA_SOURCES_DETER
from src.processors.Processor import Processor

# --- Estilo customizado para o questionary ---
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Marca de questão
    ('question', 'bold'),                # Texto da pergunta
    ('answer', 'fg:#f44336 bold'),       # Resposta selecionada
    ('pointer', 'fg:#673ab7 bold'),      # Ponteiro
    ('highlighted', 'fg:#673ab7 bold'),  # Item destacado
    ('selected', 'fg:#cc5454'),          # Item selecionado (checkbox)
    ('separator', 'fg:#cc5454'),         # Separador
    ('instruction', ''),                 # Instruções
    ('text', ''),                        # Texto normal
])

async def processar_base_especifica():
    """Menu para selecionar uma base específica do dicionário DATA_SOURCES_EMBARGOS"""
    print("\n" + "="*60)
    print("📊 SELECIONAR BASE ESPECÍFICA".center(60))
    print("="*60 + "\n")
    
    # Cria lista de choices com as keys do dicionário
    bases_disponiveis = []
    for orgao_key in DATA_SOURCES_EMBARGOS.keys():
        orgao_name = DATA_SOURCES_EMBARGOS[orgao_key].name
        bases_disponiveis.append(
            questionary.Choice(title=f"🗂️  {orgao_name}", value=orgao_key)
        )
    
    bases_disponiveis.append(questionary.Choice(title="⬅️  Voltar", value="voltar"))
    
    # Seleção da base
    base_selecionada = await questionary.select(
        "Escolha uma base específica:",
        choices=bases_disponiveis,
        style=custom_style
    ).ask_async()
    
    if base_selecionada == "voltar":
        return await main_menu()
    
    # Obtém o nome da base
    nome_base = DATA_SOURCES_EMBARGOS[base_selecionada].name
    
    print(f"\n{'='*60}")
    print(f"✅ Base selecionada: {nome_base}")
    print(f"{'='*60}\n")
    
    # Chama o EmbargoProcessor
    # EmbargoProcessor()

async def main_menu():
    """Menu principal do sistema"""
    print("\n" + "="*60)
    print("🌿 DOWNLOAD DE BASES AMBIENTAIS".center(60))
    print("="*60 + "\n")
    
    opcao = await questionary.select(
        "Selecione uma opção:",
        choices=[
            "Embargos",
            "Deters",
            "Alertas",
            "Selecionar Base Específica",
            "Sair"
        ],
        style=custom_style
    ).ask_async()
    
    if opcao == "Sair":
        print("\nEncerrando o sistema...\n")
        exit(0)
        
    elif opcao == "Embargos":
        print("\n" + "="*60)
        print("🚫 PROCESSANDO EMBARGOS".center(60))
        print("="*60 + "\n")
        processor = Processor(process_name='Embargos', data_sources=DATA_SOURCES_EMBARGOS, track_changes=True)
        return processor
        
    elif opcao == "Deters":
        print("\n" + "="*60)
        print("⚠️  PROCESSANDO DETERS".center(60))
        print("="*60 + "\n")
        # EmbargoProcessor()
    elif opcao == "Alertas":
        print("\n" + "="*60)
        print("🔔 PROCESSANDO ALERTAS".center(60))
        print("="*60 + "\n")
        # EmbargoProcessor()
    elif opcao == "Selecionar Base Específica":
        return await processar_base_especifica()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_menu())